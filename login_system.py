from gesture_auth import register_gesture, authenticate_gesture
from signature_verification import verify_signature, get_latest_signature
import os

class LoginSystem:
    def __init__(self):
        self.user_data_dir = "user_data"
        os.makedirs(self.user_data_dir, exist_ok=True)

    def register_user(self, username):
        print(f"\n=== Registering User: {username} ===")
        
        # Step 1: Register Gesture
        print("\nStep 1: Register your hand gesture")
        print("Please face the camera and press 's' when ready to capture your gesture")
        if not register_gesture(username):
            print("❌ Gesture registration failed!")
            return False

        # Step 2: Register Signature (this happens through the web interface)
        print("\nStep 2: Register your signature")
        print(f"Please go to http://127.0.0.1:8080?username={username}&mode=register to register your signature")
        print("After registering your signature there, press Enter to continue...")
        input()

        # Verify signature was registered
        if not get_latest_signature(username):
            print("❌ No signature found! Please register your signature first.")
            return False

        print("✅ Registration successful!")
        return True

    def authenticate_user(self, username):
        print(f"\n=== Authenticating User: {username} ===")
        
        # Step 1: Verify Gesture
        print("\nStep 1: Verify your hand gesture")
        print("Please face the camera and press 's' when ready")
        if not authenticate_gesture(username):
            print("❌ Gesture authentication failed!")
            return False

        # Step 2: Verify Signature
        print("\nStep 2: Verify your signature")
        print(f"Please go to http://127.0.0.1:8080?username={username}&mode=login to provide your signature")
        print("After providing your signature there, press Enter to continue...")
        input()

        # Get the latest signature (which should be the login attempt)
        latest_sig = get_latest_signature(username)
        if not latest_sig:
            print("❌ No signature found!")
            return False

        # Verify the signature
        if not verify_signature(username, latest_sig):
            print("❌ Signature verification failed!")
            return False

        print("✅ Authentication successful!")
        return True

if __name__ == "__main__":
    login_system = LoginSystem()
    username = input("Enter username: ")

    # Ask if registering or logging in
    action = input("Do you want to (r)egister or (l)ogin? ").lower()

    if action.startswith('r'):
        if login_system.register_user(username):
            print(f"\n🎉 Successfully registered user {username}!")
        else:
            print(f"\n❌ Failed to register user {username}")
    elif action.startswith('l'):
        if login_system.authenticate_user(username):
            print(f"\n🎉 Successfully logged in as {username}!")
        else:
            print(f"\n❌ Login failed for user {username}")
    else:
        print("Invalid action. Please choose 'r' for register or 'l' for login.") 