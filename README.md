# 🔐 Cryptographic Key Sharing via Hand Gesture Recognition

A secure communication system that uses real-time hand gestures as dynamic cryptographic keys — combining computer vision, gesture recognition, and cryptography for secure message exchange.

## 📌 Features

- ✋ Real-time hand gesture recognition using webcam
- 🔑 Unique encryption key generated from 3 sequential gestures
- 🔐 AES-based message encryption and decryption
- 🔄 Randomized gesture-to-binary mapping for added security
- 🧑‍💻 Streamlit-based web interface for:
  - User Registration / Login / Logout
  - Secure message sending and receiving
- 📤 Optional QR code-based key sharing

---

## 🎯 Project Workflow

1. 🎥 User performs 3 hand gestures (e.g., Thumbs Up, Peace, OK)
2. 🧠 Gestures are mapped to binary → combined to form a secret key
3. 🔒 Key is hashed + used to encrypt the message using AES
4. 🔐 Receiver performs same gestures to regenerate key and decrypt

---

## 🔧 Technologies Used

| Component           | Technology                     |
|--------------------|---------------------------------|
| Hand Tracking       | OpenCV, cvzone, MediaPipe       |
| Gesture Mapping     | Python logic + dynamic mapping  |
| Cryptography        | AES (Crypto.Cipher) + SHA-256   |
| Frontend            | Streamlit                       |
| Key Sharing Option  | qrcode (optional)               |
| User Auth & Storage | JSON-based login system         |

---

## 🗂️ Folder Structure

```bash
cryptogesture-keyshare/
├── src/
│   ├── crypto_engine.py        # AES encryption & decryption
│   ├── gesture_detector.py     # Hand gesture recognition & key logic
│   └── streamlit_app.py        # Streamlit UI for user interaction
│
├── data/
│   ├── users.json              # User login & credentials
│   ├── gesture_map.json        # Randomized gesture-to-bits mapping
│   └── encrypted_messages.json # (Optional) Encrypted message records
│
├── outputs/
│   ├── key.txt                 # Generated binary key
│   └── key_qr.png              # QR code for key (optional)
│
├── requirements.txt            # Project dependencies
├── .gitignore
├── README.md
└── __pycache__/                # Python cache (ignored in Git)


```
---
## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SaiSiriChandana/Cryptographic-Key-Sharing-via-Hand-Gesture-Recognition-Using-Computer-Vision.git
mv Cryptographic-Key-Sharing-via-Hand-Gesture-Recognition-Using-Computer-Vision cryptogesture-keyshare
cd cryptogesture-keyshare

```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Application
```bash
cd src
streamlit run streamlit_app.py
```

---
## 🛡️ Use Case Ideas
- 🔐 Secure IoT device pairing
- 🧠 Human-friendly encryption for field agents
- 👥 Peer-to-peer encrypted file transfers

---

## 🛠️ Future Enhancements

- Multi-user gesture support
- Gesture-based OTP generation
- Integration with secure messaging platforms
---




