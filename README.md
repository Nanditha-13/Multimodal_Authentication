# Multimodal Authentication

A Flask-based authentication demo that combines:
- Hand gesture verification (webcam + OpenCV)
- Signature verification (browser canvas + image comparison)

## Requirements

- Windows 10/11
- Python 3.10+ (3.11 recommended)
- Webcam access

## Setup (PowerShell)

Run these commands from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Project

```powershell
python app.py
```

Open in browser:
- https://multimodal-authentication.onrender.com

## How to Use

### Register
1. Open `/register`
2. Enter a username
3. Webcam window opens
   - Press `s` to capture gesture
   - Press `q` to cancel
4. Draw and submit signature on the signature page

### Login
1. Open `/login`
2. Enter the same username
3. Webcam window opens
   - Press `s` to capture login gesture
   - Press `q` to cancel
4. Draw and submit signature for verification

## Data Storage

Captured files are stored in:
- `user_data/`

This includes gesture images and signature PNG files for registration/login attempts.

## Troubleshooting

- **`ModuleNotFoundError` for cv2/skimage/flask**
  - Make sure virtual environment is activated.
  - Reinstall dependencies:
    ```powershell
    pip install -r requirements.txt
    ```

- **PowerShell blocks venv activation**
  - Use:
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
  - Then activate again:
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

- **Webcam not opening**
  - Close apps using camera (Zoom/Teams/Camera app).
  - Check Windows camera permissions.

- **Signature/Gesture keeps failing**
  - Use similar lighting/background.
  - Keep hand position and signature style consistent.

## Optional Test Script

You can run:

```powershell
python test_auth.py
```

Note: this still requires webcam and properly registered user data.

## Deployment (Render)

This project is configured for deployment on [Render](https://render.com/). 
The following configurations are included to support cloud deployment:
- **`Procfile`**: Configures Gunicorn to serve the Flask app (`web: gunicorn app:app`).
- **`requirements.txt`**: Uses `opencv-python-headless` instead of `opencv-python` to prevent errors relating to missing GUI system libraries in Render's container, and includes `gunicorn`.
- **`.python-version`**: Enforces Python 3.11.6 on the server.
- **Environment Variables**: The app requires a `SECRET_KEY` environment variable configured in Render's dashboard for Flask sessions.

### Deployment Steps
1. Push this repository to GitHub.
2. In the Render Dashboard, create a new **Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect the build command (`pip install -r requirements.txt`) and start command (`gunicorn app:app`).
5. Under Advanced, add an Environment Variable:
   - **Key**: `SECRET_KEY`
   - **Value**: Provide a strong, random string.
6. Deploy!

> **Note:** Render's free tier uses an ephemeral file system. User data (gestures and signatures) stored in the `user_data/` folder will be lost whenever the server restarts or re-deploys unless connected to persistent storage.
