import json
import os

from ..crypto import encrypt_data, decrypt_data, SALT_FILE

AUTH_CONFIG_FILE = os.path.expanduser("~/.osintool_auth.enc")
AUTH_PASSWORD_ENV = "OSINTOOL_AUTH_PW"


class AuthConfig:
    def __init__(self):
        self._data = {}
        self._password = os.environ.get(AUTH_PASSWORD_ENV, "osintool_default_change_me")
        self._load()

    def _load(self):
        if os.path.exists(AUTH_CONFIG_FILE):
            with open(AUTH_CONFIG_FILE, "rb") as f:
                raw = f.read()
            try:
                self._data = decrypt_data(raw, self._password)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def get(self, platform):
        return self._data.get(platform)

    def set(self, platform, credentials):
        self._data[platform] = credentials

    def list_platforms(self):
        return list(self._data.keys())

    def exists(self):
        return os.path.exists(AUTH_CONFIG_FILE)

    def save(self):
        encrypted = encrypt_data(self._data, self._password)
        with open(AUTH_CONFIG_FILE, "wb") as f:
            f.write(encrypted)
