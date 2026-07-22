#!/usr/bin/env python3
import base64
import json
import os
import sys
import tkinter as tk
from tkinter import scrolledtext

ROOT = os.path.expanduser("~/.founds.dat")
SALT = os.path.expanduser("~/.founds.salt")

class DecryptApp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("founds decrypt")
        self.win.geometry("640x520")
        self.win.configure(bg="#1e1e2e")

        frame = tk.Frame(self.win, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        pw_frame = tk.Frame(frame, bg="#1e1e2e")
        pw_frame.pack(fill="x", pady=(0, 10))
        tk.Label(pw_frame, text="Password:", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 10)).pack(side="left")
        self.pw_entry = tk.Entry(pw_frame, bg="#2d2d44", fg="#cdd6f4",
                                 insertbackground="#cdd6f4", font=("Consolas", 11),
                                 borderwidth=0, highlightthickness=1,
                                 highlightbackground="#45475a", highlightcolor="#89b4fa")
        self.pw_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.pw_entry.bind("<Return>", lambda e: self.on_decrypt())

        self.txt = scrolledtext.ScrolledText(
            frame, wrap="word", bg="#2d2d44", fg="#cdd6f4",
            insertbackground="#cdd6f4", font=("Consolas", 10),
            borderwidth=0, highlightthickness=0,
        )
        self.txt.pack(fill="both", expand=True)
        self.txt.insert("1.0", "Enter password and click Decrypt.")
        self.txt.config(state="disabled")

        btn_frame = tk.Frame(frame, bg="#1e1e2e")
        btn_frame.pack(pady=(12, 0))

        self.btn = tk.Button(
            btn_frame, text="Decrypt", command=self.on_decrypt,
            bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
            padx=24, pady=6, borderwidth=0, cursor="hand2",
            activebackground="#74c7ec", activeforeground="#1e1e2e",
        )
        self.btn.pack()

        self.status = tk.Label(frame, text="", bg="#1e1e2e", fg="#a6adc8", font=("Segoe UI", 9))
        self.status.pack(pady=(6, 0))

    def on_decrypt(self):
        pw = self.pw_entry.get()
        if not pw:
            self.status.config(text="Enter a password", fg="#f38ba8")
            return
        if not os.path.exists(ROOT):
            self._show("No encrypted data found at ~/.founds.dat")
            return
        try:
            from cryptography.fernet import InvalidToken
            salt = self._salt()
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
            key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
            from cryptography.fernet import Fernet
            f = Fernet(key)
            with open(ROOT, "rb") as fp:
                raw = f.decrypt(fp.read())
            data = json.loads(raw.decode("utf-8"))
            self._show(self._fmt(data))
            self.status.config(text="Decrypted successfully", fg="#a6e3a1")
        except InvalidToken:
            self._show("ERROR: Wrong password or corrupted file.")
            self.status.config(text="Decryption failed", fg="#f38ba8")
        except Exception as e:
            self._show(f"ERROR: {e}")
            self.status.config(text="Decryption failed", fg="#f38ba8")

    def _salt(self):
        if os.path.exists(SALT):
            with open(SALT, "rb") as f:
                return f.read()
        return b""

    def _fmt(self, data):
        meta = data.pop("_meta", {})
        lines = []
        for qtype in ("username", "name", "phone"):
            entry = data.get(qtype)
            if entry:
                lines.append(f">> {qtype.upper()} search: {entry['query']}")
                for s in entry.get("sites", []):
                    lines.append(f"   [+] {s['site']}: {s['url']}")
                lines.append("")
        if not lines:
            lines.append("No results found.")
        return "\n".join(lines)

    def _show(self, text):
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", text)
        self.txt.config(state="disabled")

    def run(self):
        self.win.mainloop()

def headless_decrypt(password):
    pw = password.strip()
    if not pw:
        return "[founds] sifre gerekli"
    if not os.path.exists(ROOT):
        return "[founds] ~/.founds.dat bulunamadi"
    try:
        from cryptography.fernet import InvalidToken
        salt = b""
        if os.path.exists(SALT):
            with open(SALT, "rb") as f:
                salt = f.read()
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
        key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
        from cryptography.fernet import Fernet
        f = Fernet(key)
        with open(ROOT, "rb") as fp:
            raw = f.decrypt(fp.read())
        data = json.loads(raw.decode("utf-8"))
        lines = []
        for qtype in ("username", "name", "phone"):
            entry = data.get(qtype)
            if entry:
                lines.append(f">> {qtype.upper()} search: {entry['query']}")
                for s in entry.get("sites", []):
                    lines.append(f"   [+] {s['site']}: {s['url']}")
                lines.append("")
        if not lines:
            lines.append("No results found.")
        return "\n".join(lines)
    except InvalidToken:
        return "[founds] Yanlis sifre veya bozuk dosya"
    except Exception as e:
        return f"[founds] Hata: {e}"

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--headless":
        print(headless_decrypt(sys.argv[2]))
    else:
        DecryptApp().run()
