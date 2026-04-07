from tkinter import *
import os


from systems.password_generator import generate_password
from systems.auth import setup_master_password, check_master_password, change_master_password, MASTER_PASSWORD_FILE
from systems.passwords import find_password, save_password, view_all_passwords
from systems.tray import setup_tray
from systems.themes import *

#THIS IS ONLY FOR FIXING THE FINAL BUILD
def resource_path(relative_path):
    base = os.path.dirname(os.path.abspath(__file__))  # stays in current folder
    return os.path.join(base, relative_path)

import pyperclip

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("MyPass")
window.config(padx=50, pady=20, bg="#f0f2f5")
window.withdraw()

if os.path.exists(MASTER_PASSWORD_FILE):
    check_master_password()
else:
    setup_master_password(window)

window.deiconify()


theme = get_theme()
BG   = theme["bg"]
TEXT = theme["text"]
RED  = theme["red"]
BLUE = theme["blue"]
MUTED = theme["muted"]


FONT = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")

def styled_entry(parent, **kwargs):
    return Entry(parent, font=FONT, relief="flat", bg="white", fg=TEXT,
                 insertbackground=TEXT, highlightthickness=1,
                 highlightbackground="#c0c0c0", highlightcolor=BLUE, **kwargs)

# Canvas / Logo
LOGO_W, LOGO_H = 280, 320
canvas = Canvas(window, width=LOGO_W, height=LOGO_H, bg=BG, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 5))
logo_img = PhotoImage(file=resource_path("mypass_logo.png"))
logo_img = logo_img.subsample(2, 2)
canvas.create_image(LOGO_W // 2, 115, image=logo_img)
title_text = canvas.create_text(LOGO_W // 2, 240, text="MyPass", font=("Helvetica", 22, "bold"), fill=RED)
sub_text = canvas.create_text(LOGO_W // 2, 262, text="your passwords, locked tight", font=("Helvetica", 8), fill=MUTED)

# Divider
Frame(window, height=1, bg="#d0d0d0").grid(row=1, column=0, columnspan=3, sticky="EW", pady=(5, 20))

# Labels
Label(window, text="Website:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=2, column=0, sticky="E", pady=10, padx=(0, 14))
Label(window, text="Email/Username:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=3, column=0, sticky="E", pady=10, padx=(0, 14))
Label(window, text="Password:", font=FONT_BOLD, bg=BG, fg=TEXT).grid(row=4, column=0, sticky="E", pady=10, padx=(0, 14))

# Entries
website_entry = styled_entry(window, width=21)
website_entry.grid(row=2, column=1, sticky="EW", pady=10, ipady=7)
website_entry.focus()

email_entry = styled_entry(window, width=35)
email_entry.grid(row=3, column=1, columnspan=2, sticky="EW", pady=10, ipady=7)
email_entry.insert(0, "yourname@mail.com")

password_entry = styled_entry(window, width=21)
password_entry.grid(row=4, column=1, sticky="EW", pady=10, ipady=7)

# Button commands

def apply_theme():
    theme = get_theme()
    
    window.config(bg=theme["bg"])
    canvas.config(bg=theme["bg"])
    
    # update all labels
    for widget in window.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg=theme["bg"], fg=theme["text"])
        elif isinstance(widget, Frame):
            widget.config(bg=theme["bg"])
    
    # update entries
    for entry in [website_entry, email_entry, password_entry]:
        entry.config(bg=theme["entry_bg"], fg=theme["text"],
                     highlightbackground=theme["border"],
                     insertbackground=theme["text"])
    
    # update canvas text
    canvas.itemconfig(title_text, fill=theme["red"])
    canvas.itemconfig(sub_text, fill=theme["muted"])

def on_toggle_theme():
    toggle_theme()
    apply_theme()
    if is_dark():
        theme_button.config(text="Light Mode☀️")
    else:
        theme_button.config(text="🌙Dark Mode")



def on_generate():
    password = generate_password()
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    generate_password_button.config(text="Copied!", state=DISABLED, fg="#ffcccc")
    window.after(2000, lambda: generate_password_button.config(text="Generate Password", state=NORMAL, fg="white"))

# Buttons
generate_password_button = Button(window, text="Generate Password", font=FONT, bg=RED, fg="white",
                                  relief="flat", cursor="hand2", activebackground="#c94444",
                                  activeforeground="white", padx=8, pady=7, command=on_generate)
generate_password_button.grid(row=4, column=2, sticky="EW", pady=10, padx=(10, 0))

find_password_button = Button(window, text="Find Password", font=FONT, bg=RED, fg="white",
                              relief="flat", cursor="hand2", activebackground="#c94444",
                              activeforeground="white", padx=8, pady=7,
                              command=lambda: find_password(website_entry))
find_password_button.grid(row=2, column=2, sticky="EW", pady=10, padx=(10, 0))

add_button = Button(window, text="Add", font=FONT_BOLD, bg=BLUE, fg="white",
                    relief="flat", cursor="hand2", activebackground="#357abd",
                    activeforeground="white", pady=3,
                    command=lambda: save_password(website_entry, email_entry, password_entry))
add_button.grid(row=5, column=1, columnspan=2, sticky="EW", pady=(20, 0))

view_button = Button(window, text="View All Passwords", font=FONT, bg=BLUE, fg="white",
                     relief="flat", cursor="hand2", activebackground="#357abd",
                     activeforeground="white", pady=3, command=view_all_passwords)
view_button.grid(row=6, column=1, columnspan=2, sticky="EW", pady=(8, 0))

change_password_button = Button(window, text="Change Master Password", font=FONT, bg="#888888", fg="white",
                                relief="flat", cursor="hand2", activebackground="#666666",
                                activeforeground="white", pady=3, command=change_master_password)
change_password_button.grid(row=7, column=1, columnspan=2, sticky="EW", pady=(8, 0))

theme_button = Button(window, text="🌙 Dark Mode", font=FONT, bg="#888888", fg="white",
                      relief="flat", cursor="hand2", activebackground="#666666",
                      activeforeground="white", pady=3, command=on_toggle_theme)
theme_button.grid(row=8, column=1, columnspan=2, sticky="EW", pady=(8, 0))

# Setup tray
setup_tray(window)

window.columnconfigure(1, weight=1)
window.mainloop()