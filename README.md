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
- http://127.0.0.1:5000

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
