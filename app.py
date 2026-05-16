from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import base64
from datetime import datetime
from signature_verification import verify_signature, get_registered_signature
from gesture_auth import register_gesture, authenticate_gesture

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Required for flash messages

# Ensure the user_data directory exists
USER_DATA_DIR = "user_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    if not username:
        flash("Username is required!")
        return redirect(url_for("register"))
    
    # Create user directory
    user_dir = os.path.join(USER_DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    
    # Register gesture first
    print(f"[INFO] Starting gesture registration for user: {username}")
    if not register_gesture(username):
        flash("Gesture registration failed! Please try again.")
        return redirect(url_for("register"))
    
    print(f"[INFO] Gesture registration successful for user: {username}")
    # Proceed to signature registration
    return redirect(url_for("capture_signature", username=username, mode="register"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    if not username:
        flash("Username is required!")
        return redirect(url_for("login"))
    
    # Verify gesture first
    print(f"\n[INFO] Attempting gesture verification for {username}")
    if not authenticate_gesture(username):
        flash("Gesture authentication failed! Please try again.")
        return redirect(url_for("login"))
    
    print(f"[INFO] Gesture verification successful for {username}")
    return redirect(url_for("capture_signature", username=username, mode="login"))

@app.route("/capture-signature")
def capture_signature():
    username = request.args.get("username")
    mode = request.args.get("mode", "register")
    if not username:
        flash("Username is required!")
        return redirect(url_for("home"))
    
    return render_template("signature_auth.html", 
                         user=username, 
                         register=(mode == "register"))

@app.route("/submit-signature", methods=["POST"])
def submit_signature():
    print("[INFO] Received signature submission")
    data = request.get_json()

    username = data.get("user")
    signature_data = data.get("signature")
    is_register = data.get("register", False)

    print(f"[INFO] Processing signature for user: {username}")

    if not signature_data:
        return "No signature data received", 400

    try:
        header, encoded = signature_data.split(",", 1)
        decoded_bytes = base64.b64decode(encoded)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = 'register' if is_register else 'login'
        filename = f"{username}{suffix}{timestamp}.png"
        filepath = os.path.join(USER_DATA_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(decoded_bytes)

        print(f"[INFO] Signature saved to: {filepath}")

        if not is_register:
            print("[INFO] Verifying signature...")
            if verify_signature(username, filepath):
                return "Login successful! Welcome back!", 200
            else:
                return "Login failed: Signature verification failed", 401

        print("✅ Registration complete")
        return "Registration complete! You can now login.", 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return str(e), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)