# MyPass 🔐

A simple, lightweight password manager built with Python and Tkinter. Passwords are saved locally to both an Excel file and a plain text file.

---

## Features

- Generate strong random passwords instantly
- Save passwords with website and email/username
- Saves to both `passwords.xlsx` and `passwords.txt`
- Duplicate entry detection
- Auto-copies generated password to clipboard
- Clean, minimal UI

---

## Requirements

Install dependencies before running:

```bash
pip install pandas openpyxl pyperclip
```

---

## Running the App

Make sure `logo.png` is in the same folder as `main.py`, then run:

```bash
python main.py
```

---

## File Structure

```
password-manager/
│
├── dist/
│   ├── main.exe           # Compiled executable
│   ├── passwords.txt      # Saved passwords (plain text)
│   └── passwords.xlsx     # Saved passwords (Excel)
│
├── build/                 # PyInstaller build files (can be ignored)
├── main.py                # Main application
├── mypass_logo.png        # App logo
└── README.md              # This file
```

---

## How to Use

1. Enter the **website**, **email/username**, and **password**
2. Click **Generate** to auto-generate a strong password (also copies it to the clipboard)
3. Click **Add** to save the entry
4. A confirmation dialog will appear before saving
5. Passwords are saved to both `passwords.xlsx` and `passwords.txt.`

---

## Notes

- Passwords are stored **locally and unencrypted** — keep your `passwords.xlsx` and `passwords.txt` files safe
- Do not share these files with anyone
- The app does not require an internet connection
