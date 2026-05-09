# signature_verification.py
import cv2
from skimage.metrics import structural_similarity as ssim
import os
import glob
import numpy as np

def get_registered_signature(username):
    pattern = f"user_data/{username}register*.png"
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def verify_signature(username, captured_signature_path, threshold=0.98):
    registered_signature = get_registered_signature(username)
    
    if not registered_signature:
        print("❌ No registered signature found")
        return False

    try:
        # Read images in grayscale
        captured = cv2.imread(captured_signature_path, cv2.IMREAD_GRAYSCALE)
        registered = cv2.imread(registered_signature, cv2.IMREAD_GRAYSCALE)

        if captured is None or registered is None:
            print("❌ Error reading signature images")
            return False

        # Resize both images to same size
        captured = cv2.resize(captured, (500, 300))
        registered = cv2.resize(registered, (500, 300))

        # Apply thresholding to make signatures binary
        _, captured_binary = cv2.threshold(captured, 127, 255, cv2.THRESH_BINARY)
        _, registered_binary = cv2.threshold(registered, 127, 255, cv2.THRESH_BINARY)

        # Calculate structural similarity index
        score = ssim(captured_binary, registered_binary)
        print(f"Signature Similarity Score: {score:.2f}")

        # Calculate contours
        contours_captured, _ = cv2.findContours(captured_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_registered, _ = cv2.findContours(registered_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Compare number of strokes (contours)
        def count_significant_contours(contours, min_area=25):
            return sum(1 for c in contours if cv2.contourArea(c) > min_area)

        # Get shape features
        def get_shape_features(contours):
            features = []
            for c in contours:
                if cv2.contourArea(c) > 25:
                    # Calculate contour features
                    area = cv2.contourArea(c)
                    perimeter = cv2.arcLength(c, True)
                    x, y, w, h = cv2.boundingRect(c)
                    aspect_ratio = float(w)/h if h > 0 else 0
                    extent = float(area)/(w*h) if w*h > 0 else 0
                    
                    # Calculate shape complexity
                    hull = cv2.convexHull(c)
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area)/hull_area if hull_area > 0 else 0
                    
                    features.append((area, perimeter, aspect_ratio, extent, solidity))
            return sorted(features, key=lambda x: x[0], reverse=True)

        reg_features = get_shape_features(contours_registered)
        cap_features = get_shape_features(contours_captured)

        # Compare shape features
        def compare_features(f1, f2):
            if not f1 or not f2:
                print("❌ No valid signature components found")
                return 0
            
            if len(f1) != len(f2):
                print(f"❌ Different number of signature components (Registered: {len(f1)}, Captured: {len(f2)})")
                return 0
            
            matches = 0
            total = len(f1)
            
            for r, c in zip(f1, f2):
                area_ratio = min(r[0], c[0]) / max(r[0], c[0])
                perimeter_ratio = min(r[1], c[1]) / max(r[1], c[1])
                aspect_diff = abs(r[2] - c[2])
                extent_diff = abs(r[3] - c[3])
                solidity_diff = abs(r[4] - c[4])
                
                print(f"Component comparison:")
                print(f"Area ratio: {area_ratio:.2f}")
                print(f"Perimeter ratio: {perimeter_ratio:.2f}")
                print(f"Aspect ratio difference: {aspect_diff:.2f}")
                print(f"Extent difference: {extent_diff:.2f}")
                print(f"Solidity difference: {solidity_diff:.2f}")
                
                # Count how many features match within thresholds
                feature_matches = 0
                if area_ratio > 0.95: feature_matches += 1
                if perimeter_ratio > 0.95: feature_matches += 1
                if aspect_diff < 0.10: feature_matches += 1
                if extent_diff < 0.10: feature_matches += 1
                if solidity_diff < 0.10: feature_matches += 1
                
                # Component matches if at least 4 out of 5 features match
                if feature_matches >= 4:
                    matches += 1
                else:
                    print("❌ Component features don't match closely enough")
                    
            match_ratio = matches / total if total > 0 else 0
            print(f"Component match ratio: {match_ratio:.2f}")
            return 1 if match_ratio >= 0.95 else 0

        shape_match = compare_features(reg_features, cap_features)

        captured_strokes = count_significant_contours(contours_captured)
        registered_strokes = count_significant_contours(contours_registered)
        stroke_diff = abs(captured_strokes - registered_strokes)
        
        print(f"Registered strokes: {registered_strokes}")
        print(f"Captured strokes: {captured_strokes}")
        print(f"Stroke difference: {stroke_diff}")

        # Calculate density of signature
        def calculate_density(binary_img):
            return np.sum(binary_img == 0) / binary_img.size

        registered_density = calculate_density(registered_binary)
        captured_density = calculate_density(captured_binary)
        density_diff = abs(registered_density - captured_density)
        print(f"Density difference: {density_diff:.2f}")

        # Strict verification checks
        if score < threshold:
            print(f"❌ Signatures don't match closely enough (score: {score:.2f}, required: {threshold:.2f})")
            return False
        
        if stroke_diff != 0:  # Must have exact same number of strokes
            print(f"❌ Different number of signature strokes ({stroke_diff} difference)")
            return False
            
        if density_diff > 0.02:  # Reduced from 0.03 to 0.02 (2% density difference maximum)
            print(f"❌ Signature density differs significantly ({density_diff:.2f})")
            return False

        if not shape_match:
            print("❌ Signature shapes don't match")
            return False

        print("✅ Signature verification passed")
        return True

    except Exception as e:
        print(f"❌ Error during signature verification: {str(e)}")
        return False