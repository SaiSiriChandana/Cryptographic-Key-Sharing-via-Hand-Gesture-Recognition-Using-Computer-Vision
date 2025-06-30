from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64

def get_aes_key_from_binary(binary_string):
    # Convert binary to string, hash it, and use first 16 bytes as AES key
    key_bytes = hashlib.sha256(binary_string.encode()).digest()[:16]  # AES-128
    return key_bytes

def encrypt_message(message, binary_key):
    key = get_aes_key_from_binary(binary_key)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = cipher.iv
    ciphertext = base64.b64encode(iv + ct_bytes).decode()
    return ciphertext

def decrypt_message(ciphertext, binary_key):
    key = get_aes_key_from_binary(binary_key)
    raw = base64.b64decode(ciphertext)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode()
    return decrypted
