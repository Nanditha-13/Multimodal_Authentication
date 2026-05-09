from gesture_auth import register_gesture, authenticate_gesture
from signature_verification import verify_signature, get_latest_signature
import os

def test_gesture_auth():
    print("\n=== Testing Gesture Authentication ===")
    print("First, let's register a gesture...")
    if register_gesture("testuser"):
        print("Gesture registered successfully!")
        print("\nNow, let's authenticate...")
        if authenticate_gesture("testuser"):
            print("Gesture authentication successful!")
        else:
            print("Gesture authentication failed!")
    else:
        print("Failed to register gesture!")

def test_signature_verification():
    print("\n=== Testing Signature Verification ===")
    registered_signature = get_latest_signature("testuser")
    
    if registered_signature:
        result = verify_signature("testuser", registered_signature)
        print(f"Signature verification {'successful' if result else 'failed'}!")
    else:
        print("No signature found! Please register a signature first through the web interface.")

if __name__ == "__main__":
    print("Starting authentication tests...")
    test_gesture_auth()
    test_signature_verification()
    print("\nTests completed!") 