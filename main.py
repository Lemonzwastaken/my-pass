import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import pandas as pd
import os
import sys

EXCEL_FILE = "passwords.xlsx"

def resource_path(relative_path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=["Website", "Email/Username", "Password"])

def save_data(df):
    # Save to Excel
    df.to_excel(EXCEL_FILE, index=False)
    
    # Save to TXT
    with open("passwords.txt", "w") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Website']} | {row['Email/Username']} | {row['Password']}\n")

def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'
    password_list = (
        [random.choice(letters) for _ in range(random.randint(8, 10))] +
        [random.choice(symbols) for _ in range(random.randint(2, 4))] +
        [random.choice(numbers) for _ in range(random.randint(2, 4))]
    )
    random.shuffle(password_list)
    return "".join(password_list)

def save_pass():
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    generate_button.configure(text="Copied!", state="disabled", fg="red")
    window.after(2000, lambda: generate_button.configure(text="Generate", state="normal", fg="white"))

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not all([website, email, password]):
        add.configure(text="Fill all fields!", state="disabled", fg="red")
        window.after(2000, lambda: add.configure(text="Add", state="normal", fg="white"))
        return

    check = messagebox.askokcancel(title=website, message=f"Save these details?\nEmail: {email}\nPassword: {password}")
    if not check:
        return

    df = load_data()
    duplicate = ((df["Website"] == website) & (df["Email/Username"] == email) & (df["Password"] == password)).any()
    if duplicate:
        add.configure(text="Already exists!", state="disabled", fg="red")
        window.after(2000, lambda: add.configure(text="Add", state="normal", fg="white"))
        return

    new_row = pd.DataFrame([{"Website": website, "Email/Username": email, "Password": password}])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

    website_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    website_entry.focus()

# WINDOW
window = tk.Tk()
window.title("MyPass")
window.config(padx=40, pady=30, bg="#f5f5f5")

FONT = ("Helvetica", 11)
BG = "#f5f5f5"

# LOGO
canvas = tk.Canvas(width=200, height=200, bg=BG, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 10))
logo = tk.PhotoImage(file=resource_path("mypass_logo.png"))
logo = logo.subsample(3, 3)  # divides size by 3, adjust number as needed
canvas.create_image(100, 80, image=logo)
canvas.create_text(100, 170, text="MyPass",
                   font=("Helvetica", 20, "bold"), fill="#e05c5c")
canvas.create_text(100, 190, text="your passwords, saved tight",
                   font=("Helvetica", 8), fill="#999999")

# LABELS
for text, row in [("Website:", 1), ("Email/Username:", 2), ("Password:", 3)]:
    tk.Label(text=text, font=FONT, bg=BG, fg="#333333").grid(
        row=row, column=0, sticky="E", pady=6, padx=(0, 10))

# ENTRIES
website_entry = tk.Entry(font=FONT)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW", pady=6)

email_entry = tk.Entry(font=FONT)
email_entry.insert(0, "your@email.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=6)

password_entry = tk.Entry(font=FONT)
password_entry.grid(row=3, column=1, sticky="EW", pady=6)

# BUTTONS
generate_button = tk.Button(text="Generate", font=FONT, bg="#e05c5c", fg="white",
                            relief="flat", cursor="hand2", command=save_pass)
generate_button.grid(row=3, column=2, sticky="EW", pady=6, padx=(6, 0))

add = tk.Button(text="Add", font=FONT, bg="#4a90d9", fg="white",
                relief="flat", cursor="hand2", command=save_password)
add.grid(row=4, column=1, columnspan=2, sticky="EW", pady=(14, 0))

window.columnconfigure(1, weight=1)
window.mainloop()