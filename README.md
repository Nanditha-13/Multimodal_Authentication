# 🔐 Multimodal Authentication System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![Deployment](https://img.shields.io/badge/Deployment-Render-purple?style=for-the-badge)

A robust, dual-layer authentication system combining **Computer Vision-based Hand Gesture Recognition** and **Digital Signature Verification**. This project explores alternative, password-less biometric authentication mechanisms for web applications.

---

## 📖 Project Overview

Traditional passwords are fundamentally flawed and prone to social engineering. This project introduces a **two-step biometric authentication pipeline**:
1. **Physical Token (Hand Gesture)**: Users register a unique hand gesture captured via webcam.
2. **Behavioral Token (Signature)**: Users draw their unique signature on an HTML5 Canvas.

During login, the system strictly compares the captured gesture and signature against the registered baseline using advanced image processing algorithms, ensuring high security and preventing unauthorized access.

---

## ✨ Features

- **Gesture Authentication**: Real-time webcam capture and evaluation of hand shapes.
- **Signature Verification**: Smooth, browser-based drawing canvas to capture digital signatures.
- **Structural Similarity (SSIM)**: Pixel-perfect structural comparison of images.
- **Contour & Shape Analysis**: Compares stroke count, contour area, aspect ratios, and density for strict validation.
- **Cloud-Ready**: Pre-configured for deployment on Render.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Gunicorn
- **Computer Vision**: OpenCV, MediaPipe (conceptually for advanced tracking), Scikit-Image (SSIM)
- **Frontend**: HTML5 Canvas, CSS, JavaScript (Vanilla)
- **Data Storage**: Local File System (`user_data/`)

---

## 🧠 System Architecture & Workflow

### 1. Registration Flow
1. User enters a unique username.
2. **Webcam Initialization**: User presses `s` to snapshot a secret hand gesture.
3. **Canvas Initialization**: User draws their signature on the screen and submits.
4. Images are thresholded, processed, and stored securely as baselines.

### 2. Login Flow
1. User enters their username to initiate login.
2. System prompts for the **Gesture**: User mimics the exact registered gesture.
3. System prompts for the **Signature**: User signs the canvas.
4. **Validation Engine**:
   - Compares gesture similarity and contour differences.
   - Computes Structural Similarity Index (SSIM) for the signature.
   - Matches stroke counts, area density, and bounding boxes.
5. Access is Granted or Denied based on threshold adherence.

---

## 📂 Folder Structure

```text
📦 Multimodal_Authentication
 ┣ 📂 static/                # CSS and client-side JavaScript
 ┣ 📂 templates/             # HTML templates (Jinja2)
 ┣ 📂 user_data/             # Stored registration baselines (ephemeral in cloud)
 ┣ 📜 app.py                 # Main Flask application & routes
 ┣ 📜 gesture_auth.py        # OpenCV gesture processing logic
 ┣ 📜 signature_verification.py # SSIM & Contour analysis logic
 ┣ 📜 requirements.txt       # Python dependencies
 ┣ 📜 Procfile               # Gunicorn deployment config
 ┣ 📜 .python-version        # Server Python runtime version
 ┗ 📜 README.md              # Project documentation
```

---

## 🚀 Installation Steps

### Prerequisites
- Windows 10/11
- Python 3.10+ (3.11 recommended)
- Working Webcam

### Local Setup (PowerShell)

1. **Clone the repository** (if you haven't):
   ```powershell
   git clone https://github.com/Nanditha-13/Multimodal_Authentication.git
   cd Multimodal_Authentication
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   *(Note: If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*

3. **Install Dependencies**:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```powershell
   python app.py
   ```
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## ☁️ Deployment Guide (Render)

This application is configured for seamless deployment on [Render](https://render.com/).

1. Push your code to a GitHub repository.
2. Go to the Render Dashboard and create a new **Web Service**.
3. Connect your GitHub repository.
4. Render will auto-detect:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (via `Procfile`)
5. Under **Advanced**, add an Environment Variable:
   - **Key**: `SECRET_KEY`
   - **Value**: *(A strong random string for Flask sessions)*
6. Click **Deploy!**

> ⚠️ **Security & Storage Note**: Render's free tier uses an *ephemeral file system*. User data stored in `user_data/` will be wiped during server restarts. For production, integrate AWS S3 or a persistent Render Disk.

---

## 🔮 Future Enhancements

- **Deep Learning Integration**: Upgrade from OpenCV SSIM to a CNN-based Siamese Network for more robust signature verification.
- **MediaPipe Hand Tracking**: Integrate MediaPipe to track exact finger joints instead of relying purely on image contours.
- **Cloud Storage**: Migrate from local file system (`user_data/`) to cloud blob storage (AWS S3/GCS) for persistence.

---
*Built with ❤️ for a password-less future.*
