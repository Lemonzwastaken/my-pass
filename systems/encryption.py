import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT_FILE = "salt.key"

def get_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def get_fernet(master_password):
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return Fernet(key)

def encrypt_password(master_password, password):
    f = get_fernet(master_password)
    return f.encrypt(password.encode()).decode()

def decrypt_password(master_password, encrypted_password):
    f = get_fernet(master_password)
    return f.decrypt(encrypted_password.encode()).decode()