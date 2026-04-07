from tkinter import *
import os
import sys

# ---------------- SINGLE INSTANCE LOCK ---------------- #
LOCK_FILE = "app.lock"

def create_lock():
    if os.path.exists(LOCK_FILE):
        from tkinter import messagebox
        messagebox.showerror("MyPass", "Application is already running!")
        sys.exit()
    with open(LOCK_FILE, "w") as f:
        f.write("locked")

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

create_lock()


# ---------------- IMPORTS ---------------- #
from systems.password_generator import generate_password
from systems.auth import setup_master_password, check_master_password, change_master_password, MASTER_PASSWORD_FILE
from systems.passwords import find_password, save_password, view_all_passwords
from systems.tray import setup_tray
from systems.themes import *

import pyperclip

# ---------------- RESOURCE PATH (FOR EXE) ---------------- #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------- LOAD THEME ---------------- #
load_theme()
theme = get_theme()

BG   = theme["bg"]
TEXT = theme["text"]
RED  = theme["red"]
BLUE = theme["blue"]
MUTED = theme["muted"]

FONT = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")


# ---------------- WINDOW ---------------- #
window = Tk()
window.title("MyPass")
window.config(padx=50, pady=20, bg=BG)
window.withdraw()


# ---------------- MASTER PASSWORD ---------------- #
if os.path.exists(MASTER_PASSWORD_FILE):
    check_master_password()
else:
    setup_master_password(window)

window.deiconify()


# ---------------- UI HELPERS ---------------- #
def styled_entry(parent, **kwargs):
    return Entry(
        parent,
        font=FONT,
        relief="flat",
        bg=theme["entry_bg"],
        fg=TEXT,
        insertbackground=TEXT,
        highlightthickness=1,
        highlightbackground=theme["border"],
        highlightcolor=BLUE,
        **kwargs
    )


# ---------------- CANVAS ---------------- #
LOGO_W, LOGO_H = 280, 320
canvas = Canvas(window, width=LOGO_W, height=LOGO_H, bg=BG, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 5))

logo_img = PhotoImage(file=resource_path("mypass_logo.png"))
logo_img = logo_img.subsample(2, 2)

canvas.create_image(LOGO_W // 2, 115, image=logo_img)
title_text = canvas.create_text(LOGO_W // 2, 240, text="MyPass", font=("Helvetica", 22, "bold"), fill=RED)
sub_text = canvas.create_text(LOGO_W // 2, 262, text="your passwords, locked tight", font=("Helvetica", 8), fill=MUTED)


# ---------------- DIVIDER ---------------- #
Frame(window, height=1, bg=theme["border"]).grid(row=1, column=0, columnspan=3, sticky="EW", pady=(5, 20))


# ---------------- LABELS ---------------- #
Label(window, text="Website:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=2, column=0, sticky="E", pady=10, padx=(0, 14))
Label(window, text="Email/Username:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=3, column=0, sticky="E", pady=10, padx=(0, 14))
Label(window, text="Password:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=4, column=0, sticky="E", pady=10, padx=(0, 14))


# ---------------- ENTRIES ---------------- #
website_entry = styled_entry(window, width=21)
website_entry.grid(row=2, column=1, sticky="EW", pady=10, ipady=7)
website_entry.focus()

email_entry = styled_entry(window, width=35)
email_entry.grid(row=3, column=1, columnspan=2, sticky="EW", pady=10, ipady=7)
email_entry.insert(0, "yourname@mail.com")

password_entry = styled_entry(window, width=21)
password_entry.grid(row=4, column=1, sticky="EW", pady=10, ipady=7)


# ---------------- FUNCTIONS ---------------- #
def apply_theme():
    theme = get_theme()

    window.config(bg=theme["bg"])
    canvas.config(bg=theme["bg"])

    for widget in window.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg=theme["bg"], fg=theme["text"])
        elif isinstance(widget, Frame):
            widget.config(bg=theme["bg"])

    for entry in [website_entry, email_entry, password_entry]:
        entry.config(
            bg=theme["entry_bg"],
            fg=theme["text"],
            highlightbackground=theme["border"],
            insertbackground=theme["text"]
        )

    canvas.itemconfig(title_text, fill=theme["red"])
    canvas.itemconfig(sub_text, fill=theme["muted"])


def on_toggle_theme():
    toggle_theme()
    apply_theme()
    if is_dark():
        theme_button.config(text="Light Mode☀️")
    else:
        theme_button.config(text="🌙 Dark Mode")


def on_generate():
    password = generate_password()
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    generate_password_button.config(text="Copied!", state=DISABLED, fg="#ffcccc")
    window.after(2000, lambda: generate_password_button.config(text="Generate Password", state=NORMAL, fg="white"))


# ---------------- BUTTONS ---------------- #
generate_password_button = Button(window, text="Generate Password", font=FONT, bg=RED, fg="white",
                                  relief="flat", cursor="hand2", padx=8, pady=7, command=on_generate)
generate_password_button.grid(row=4, column=2, sticky="EW", pady=10, padx=(10, 0))

find_password_button = Button(window, text="Find Password", font=FONT, bg=RED, fg="white",
                              relief="flat", cursor="hand2",
                              command=lambda: find_password(website_entry))
find_password_button.grid(row=2, column=2, sticky="EW", pady=10, padx=(10, 0))

add_button = Button(window, text="Add", font=FONT_BOLD, bg=BLUE, fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda: save_password(website_entry, email_entry, password_entry))
add_button.grid(row=5, column=1, columnspan=2, sticky="EW", pady=(20, 0))

view_button = Button(window, text="View All Passwords", font=FONT, bg=BLUE, fg="white",
                     relief="flat", cursor="hand2", command=view_all_passwords)
view_button.grid(row=6, column=1, columnspan=2, sticky="EW", pady=(8, 0))

change_password_button = Button(window, text="Change Master Password", font=FONT, bg="#888888", fg="white",
                                relief="flat", cursor="hand2", command=change_master_password)
change_password_button.grid(row=7, column=1, columnspan=2, sticky="EW", pady=(8, 0))

theme_button = Button(window, text="🌙 Dark Mode", font=FONT, bg="#888888", fg="white",
                      relief="flat", cursor="hand2", command=on_toggle_theme)
theme_button.grid(row=8, column=1, columnspan=2, sticky="EW", pady=(8, 0))


# ---------------- INIT ---------------- #
setup_tray(window)

apply_theme()

if is_dark():
    theme_button.config(text="Light Mode☀️")

window.columnconfigure(1, weight=1)


# ---------------- RUN ---------------- #
try:
    window.mainloop()
finally:
    remove_lock()