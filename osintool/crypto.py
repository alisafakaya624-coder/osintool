import base64
import hashlib
import json
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_FILE = os.path.expanduser("~/.founds.salt")
STORAGE_FILE = os.path.expanduser("~/.founds.dat")

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def _load_or_create_salt() -> bytes:
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def encrypt_data(data: dict, password: str) -> bytes:
    salt = _load_or_create_salt()
    key = _derive_key(password, salt)
    f = Fernet(key)
    raw = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
    return f.encrypt(raw)

def decrypt_data(encrypted: bytes, password: str) -> dict:
    salt = _load_or_create_salt()
    key = _derive_key(password, salt)
    f = Fernet(key)
    raw = f.decrypt(encrypted)
    return json.loads(raw.decode("utf-8"))

def save_encrypted(data: dict, password: str):
    encrypted = encrypt_data(data, password)
    with open(STORAGE_FILE, "wb") as f:
        f.write(encrypted)

def load_encrypted(password: str) -> dict:
    if not os.path.exists(STORAGE_FILE):
        return None
    with open(STORAGE_FILE, "rb") as f:
        encrypted = f.read()
    return decrypt_data(encrypted, password)
