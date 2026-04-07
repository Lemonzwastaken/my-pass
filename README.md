# MyPass 🔐
<img width="1360" height="686" alt="mypass_logo" src="https://github.com/user-attachments/assets/171314c4-6c53-4104-a171-b70088e3fedf" />

A modern, lightweight password manager built with Python and Tkinter.
Your passwords are securely encrypted and stored locally on your device.

---

## ✨ Features

* 🔐 **Secure encryption** using Fernet (AES-based)
* 🔑 **Master password protection**
* 🎲 Generate strong random passwords instantly
* 📋 Auto-copy generated passwords to the clipboard
* 📁 View all saved passwords in a clean table UI
* 🗑️ Delete saved passwords

---

##  Requirements (for running from code)

Install dependencies:

```bash
pip install cryptography pystray pillow pyperclip
```

---

##  Running the App

### EXE (Recommended)

1. Download the ZIP
2. Extract it anywhere
3. Run `main.exe`

---

### From Source Code

Make sure the following file exists in the same folder:

* `mypass_logo.png`

Then run:

```bash
python main.py
```

---

##  How to Use

1. On first launch, **set a master password**
2. Enter:

   * Website
   * Email/Username
   * Password (or generate one)
3. Click **Generate Password** to create a strong one (auto-copied)
4. Click **Add** to save
5. Use:

   * **Find Password** → search by website
   * **View All Passwords** → see everything
   * **Change Master Password** → update security
6. Toggle 🌙 **Dark Mode** anytime (it will be remembered)

---


## 🔒 Security Notes

* All passwords are **encrypted using strong cryptography (Fernet)**
* Master password is **hashed (SHA-256)** and never stored in plain text
* Data is stored **locally only**
* No internet connection is used

⚠️ If you forget your master password, your saved passwords **cannot be recovered**

---

---

## Dependencies

* Python 🐍
* Tkinter (GUI)
* Cryptography (Fernet encryption)
* PyStray (system tray integration)

---

---

## 📜 License

This project is for educational and personal use.
