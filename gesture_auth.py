import cv2
import os
import numpy as np
from datetime import datetime
import glob

USER_DATA_DIR = "user_data"

def get_registered_gesture(username):
    # Find the most recent registered gesture for the user
    pattern = os.path.join(USER_DATA_DIR, f"{username}_register_gesture_*.jpg")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def compare_gestures(registered_path, login_path, threshold=0.40):
    # Read images in grayscale
    registered = cv2.imread(registered_path, cv2.IMREAD_GRAYSCALE)
    login = cv2.imread(login_path, cv2.IMREAD_GRAYSCALE)
    
    if registered is None or login is None:
        print("❌ Error reading gesture images")
        return False
    
    # Resize both images to same size
    registered = cv2.resize(registered, (200, 200))
    login = cv2.resize(login, (200, 200))
    
    # Apply binary thresholding with Gaussian blur to reduce noise
    registered = cv2.GaussianBlur(registered, (5, 5), 0)
    login = cv2.GaussianBlur(login, (5, 5), 0)
    
    _, registered_binary = cv2.threshold(registered, 127, 255, cv2.THRESH_BINARY)
    _, login_binary = cv2.threshold(login, 127, 255, cv2.THRESH_BINARY)
    
    # Calculate structural similarity
    try:
        from skimage.metrics import structural_similarity as ssim
        similarity = ssim(registered_binary, login_binary)
    except:
        # Fallback to template matching if skimage is not available
        result = cv2.matchTemplate(registered_binary, login_binary, cv2.TM_CCOEFF_NORMED)
        similarity = np.max(result)
    
    print(f"Gesture Similarity Score: {similarity:.2f}")
    
    # Compare contours
    contours_registered, _ = cv2.findContours(registered_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_login, _ = cv2.findContours(login_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Compare number of major contours (filter out small noise)
    def count_major_contours(contours, min_area=50):
        return sum(1 for c in contours if cv2.contourArea(c) > min_area)
    
    reg_contours = count_major_contours(contours_registered)
    login_contours = count_major_contours(contours_login)
    
    contour_diff = abs(reg_contours - login_contours)
    print(f"Number of major shapes - Registered: {reg_contours}, Login: {login_contours}")
    print(f"Shape count difference: {contour_diff}")
    
    # Calculate average contour areas and perimeters
    def get_shape_features(contours):
        features = []
        for c in contours:
            if cv2.contourArea(c) > 50:  # Only consider major shapes
                area = cv2.contourArea(c)
                perimeter = cv2.arcLength(c, True)
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = float(w)/h if h > 0 else 0
                features.append((area, perimeter, aspect_ratio))
        return sorted(features, key=lambda x: x[0], reverse=True)  # Sort by area
    
    reg_features = get_shape_features(contours_registered)
    login_features = get_shape_features(contours_login)
    
    # Compare shape features
    def compare_features(f1, f2):
        if not f1 or not f2:
            return 0, 0, 0
        
        # Compare only the number of shapes that exist in both gestures
        min_shapes = min(len(f1), len(f2))
        if min_shapes == 0:
            return 0, 0, 0
            
        area_ratios = []
        perimeter_ratios = []
        aspect_ratios = []
        
        for r, l in zip(f1[:min_shapes], f2[:min_shapes]):
            # Compare areas
            area_ratio = min(r[0], l[0]) / max(r[0], l[0])
            area_ratios.append(area_ratio)
            
            # Compare perimeters
            perim_ratio = min(r[1], l[1]) / max(r[1], l[1])
            perimeter_ratios.append(perim_ratio)
            
            # Compare aspect ratios
            aspect_diff = abs(r[2] - l[2])
            aspect_ratios.append(1 - min(aspect_diff, 1))
        
        return (sum(area_ratios) / min_shapes,
                sum(perimeter_ratios) / min_shapes,
                sum(aspect_ratios) / min_shapes)
    
    area_match, perim_match, aspect_match = compare_features(reg_features, login_features)
    print(f"Area match ratio: {area_match:.2f}")
    print(f"Perimeter match ratio: {perim_match:.2f}")
    print(f"Aspect ratio match: {aspect_match:.2f}")
    
    # Calculate density of gesture
    def calculate_density(binary_img):
        return np.sum(binary_img == 0) / binary_img.size
    
    reg_density = calculate_density(registered_binary)
    login_density = calculate_density(login_binary)
    density_ratio = min(reg_density, login_density) / max(reg_density, login_density)
    print(f"Density ratio: {density_ratio:.2f}")
    
    # Verification checks with balanced thresholds
    if similarity < threshold:
        print(f"❌ Gesture shapes don't match closely enough (score: {similarity:.2f}, required: {threshold:.2f})")
        return False
        
    if contour_diff > 2:  # Allow up to 2 shape difference
        print(f"❌ Gesture structure is too different (shape count difference: {contour_diff})")
        return False
        
    if area_match < 0.45:  # Reduced from 0.60 to 0.45
        print(f"❌ Gesture shapes have different sizes (match: {area_match:.2f})")
        return False
        
    if perim_match < 0.45:  # Reduced from 0.60 to 0.45
        print(f"❌ Gesture shapes have different perimeters (match: {perim_match:.2f})")
        return False
        
    if aspect_match < 0.45:  # Reduced from 0.50 to 0.45
        print(f"❌ Gesture shapes have different proportions (match: {aspect_match:.2f})")
        return False
        
    if density_ratio < 0.60:  # Keep density check at 0.60 as it's already good
        print(f"❌ Gesture density is too different (ratio: {density_ratio:.2f})")
        return False
        
    print("✅ Gesture verification passed")
    return True

def save_gesture(username, frame, is_register=True):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = 'register' if is_register else 'login'
    filename = f"{username}_{suffix}_gesture_{timestamp}.jpg"
    filepath = os.path.join(USER_DATA_DIR, filename)
    
    # Ensure directory exists
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    # Save the image
    cv2.imwrite(filepath, frame)
    return filepath

def register_gesture(username):
    print("\n[INFO] Starting gesture registration...")
    print("[INFO] Opening webcam...")
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return False

        print("\n👋 Please show your gesture to the camera")
        print("Press 's' to capture or 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read from webcam")
                break
                
            # Display the frame
            cv2.imshow("Register Gesture (Press 's' to capture)", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                # Save the gesture
                filepath = save_gesture(username, frame, True)
                print(f"✅ Gesture saved: {filepath}")
                break
            elif key == ord('q'):
                print("❌ Registration cancelled by user")
                break

        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        return True

    except Exception as e:
        print(f"❌ Error during gesture registration: {str(e)}")
        return False
    finally:
        try:
            cap.release()
            cv2.destroyAllWindows()
        except:
            pass

def authenticate_gesture(username):
    print("\n[INFO] Starting gesture authentication...")
    
    # First, check if there's a registered gesture
    registered_gesture = get_registered_gesture(username)
    if not registered_gesture:
        print("❌ No registered gesture found for this user")
        return False
    
    print("[INFO] Opening webcam...")
    cap = None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return False

        print("\n👋 Please show your gesture to the camera")
        print("Press 's' to capture or 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read from webcam")
                break
                
            # Display the frame
            cv2.imshow("Verify Gesture (Press 's' to capture)", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                # Save the login gesture
                login_gesture = save_gesture(username, frame, False)
                print(f"✅ Gesture captured for verification")
                
                # Clean up before verification
                cap.release()
                cv2.destroyAllWindows()
                
                # Compare gestures with strict verification
                if compare_gestures(registered_gesture, login_gesture):
                    return True
                return False
                    
            elif key == ord('q'):
                print("❌ Authentication cancelled by user")
                return False

        return False

    except Exception as e:
        print(f"❌ Error during gesture authentication: {str(e)}")
        return False
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
