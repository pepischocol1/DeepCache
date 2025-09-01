import os
import random
import string
from cryptography.fernet import Fernet

# ===== CONFIG =====
LOG_FILE = os.path.join("data", "file_map.enc")
KEY_FILE = os.path.join("data", "log_key.key")

# ===== RANDOM NAME GENERATOR =====
def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ===== ENCRYPTION HELPERS =====
def load_or_create_key():
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as keyfile:
            return keyfile.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as keyfile:
            keyfile.write(key)
        print(f"[INFO] Encryption key created at {KEY_FILE}")
        return key

def encrypt_log_entry(entry, key):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    f = Fernet(key)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "rb") as lf:
            data = lf.read()
        decrypted = f.decrypt(data).decode()
        decrypted += entry + "\n"
        encrypted = f.encrypt(decrypted.encode())
    else:
        encrypted = f.encrypt((entry + "\n").encode())
    with open(LOG_FILE, "wb") as lf:
        lf.write(encrypted)

def decrypt_log(key):
    if not os.path.exists(LOG_FILE):
        print("❌ ERROR: Encrypted log file not found.")
        return None
    f = Fernet(key)
    with open(LOG_FILE, "rb") as lf:
        data = lf.read()
    return f.decrypt(data).decode().strip().split("\n")
