import streamlit as st
import json
import os
from PIL import Image
import qrcode
from crypto_engine import encrypt_message, decrypt_message

st.set_page_config(page_title="Gesture-Based Encryption", layout="centered")

# === Helper Functions ===

def load_users():
    if os.path.exists("users.json"):
        with open("users.json") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def save_message(msg):
    if os.path.exists("encrypted_messages.json"):
        with open("encrypted_messages.json", "r") as f:
            messages = json.load(f)
    else:
        messages = []
    messages.append(msg)
    with open("encrypted_messages.json", "w") as f:
        json.dump(messages, f, indent=2)

def load_messages_for_user(user):
    if os.path.exists("encrypted_messages.json"):
        with open("encrypted_messages.json", "r") as f:
            all_messages = json.load(f)
        return [m for m in all_messages if m["to"] == user]
    return []

# === Sidebar Login/Register ===

st.sidebar.title("🧑‍💻 Welcome")
action = st.sidebar.radio("Choose an action", ["Login", "Register"])
users = load_users()

if "user" not in st.session_state:

    if action == "Login":
        st.sidebar.subheader("🔐 Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_btn = st.sidebar.button("Login")

        if login_btn:
            if username in users and users[username] == password:
                st.session_state["user"] = username
                st.success(f"✅ Logged in as {username}")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid username or password.")

    elif action == "Register":
        st.sidebar.subheader("🧾 Register New User")
        new_user = st.sidebar.text_input("New Username")
        new_pass = st.sidebar.text_input("New Password", type="password")
        reg_btn = st.sidebar.button("Register")

        if reg_btn:
            if new_user in users:
                st.sidebar.warning("⚠️ Username already exists.")
            elif not new_user or not new_pass:
                st.sidebar.warning("❗ Please enter both username and password.")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.sidebar.success("✅ Registered successfully! You can now log in.")

    st.stop()

# === Main App (After Login) ===

current_user = st.session_state["user"]
st.sidebar.success(f"Logged in as: {current_user}")
if st.sidebar.button("Logout"):
    del st.session_state["user"]
    st.rerun()

st.title("🔐 Gesture-Based Secure Messaging")

# Load gesture key
if os.path.exists("key.txt"):
    with open("key.txt", "r") as f:
        binary_key = f.read().strip()
    st.success(f"🔑 Gesture Key Loaded: {binary_key}")
else:
    st.warning("⚠️ key.txt not found. Run gesture_detector.py first.")
    st.stop()

# === Encrypt and Send ===

st.header("✉️ Send Encrypted Message")
message = st.text_input("Enter your message")
receiver = st.selectbox("Select receiver", [u for u in users if u != current_user])

if st.button("Encrypt and Send"):
    if message and receiver:
        cipher = encrypt_message(message, binary_key)
        msg = {"from": current_user, "to": receiver, "cipher": cipher}
        save_message(msg)
        st.success(f"✅ Message encrypted and sent to {receiver}")
        st.code(cipher, language="text")
    else:
        st.warning("Please enter a message and select a receiver.")

# === Inbox ===

st.header("📥 Your Messages")
inbox = load_messages_for_user(current_user)
if inbox:
    for i, msg in enumerate(inbox, 1):
        st.markdown(f"**#{i} From:** {msg['from']}")
        st.code(msg['cipher'])
        if st.button(f"Decrypt #{i}", key=f"dec{i}"):
            try:
                plain = decrypt_message(msg['cipher'], binary_key)
                st.success(f"Decrypted: {plain}")
            except Exception:
                st.error("❌ Decryption failed. Key mismatch or message altered.")
else:
    st.info("📭 No messages received yet.")

# === QR Code for Key Sharing ===

st.header("📷 QR Code for Gesture Key")
if st.button("Generate QR Code"):
    qr = qrcode.make(binary_key)
    qr.save("key_qr.png")
    st.image(Image.open("key_qr.png"), caption="QR Code for Binary Key")
