import tkinter as tk
from tkinter import messagebox
import random
import pyperclip

#PASSWORD GENERATOR

def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8,10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    return password

def save_pass():
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(index=0, string=f"{password}")
    pyperclip.copy(password)
    generate_button.configure(text="Copied to Clipboard", state="disabled", fg="red")
    window.after(2000, lambda:generate_button.configure(text="Generate", state="normal", fg="white")) 
    
#SAVE PASSWORD
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if website != "" and email != "" and password != "":
        check = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?")
        if check:
            entry = f"{website} | {email} | {password}\n"

            with open("passwords.txt", mode="r") as file:
                contents = file.readlines()

            if entry not in contents:
                with open("passwords.txt", mode="a") as file:
                    file.write(entry)
                
                # CLEAR CONTENTS
                website_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                
                # Give focus back to the first entry
                website_entry.focus()

            else:   
                add.configure(text="Entry already exists", state="disabled", fg="red")
                window.after(2000, lambda:add.configure(text="Add", state="normal", fg="white"))
    else:
            add.configure(text="Please make a proper entry", state="disabled", fg="red")
            window.after(2000, lambda:add.configure(text="Add", state="normal", fg="white"))

# WINDOW
window = tk.Tk()
window.title("MyPass")
window.config(padx=40, pady=30, bg="#f5f5f5")

FONT = ("Helvetica", 11)
LABEL_COLOR = "#333333"
BG = "#f5f5f5"

# CANVAS
canvas = tk.Canvas(width=200, height=200, highlightthickness=0, bg=BG)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# LABELS
for text, row in [("Website:", 1), ("Email/Username:", 2), ("Password:", 3)]:
    tk.Label(text=text, font=FONT, bg=BG, fg=LABEL_COLOR, anchor="e").grid(
        row=row, column=0, sticky="E", pady=6, padx=(0, 10))

# ENTRIES
website_entry = tk.Entry(font=FONT)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW", pady=6)

email_entry = tk.Entry(font=FONT)
email_entry.insert(index=0, string="Dummy email")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=6)

password_entry = tk.Entry(font=FONT)
password_entry.grid(row=3, column=1, sticky="EW", pady=6)

# BUTTONS
generate_button = tk.Button(text="Generate", font=FONT, bg="#e05c5c", fg="white", relief="flat", cursor="hand2", command=save_pass)
generate_button.grid(row=3, column=2, sticky="EW", pady=6, padx=(6, 0))

add = tk.Button(text="Add", font=FONT, bg="#4a90d9", fg="white", relief="flat", cursor="hand2", command=save_password)
add.grid(row=4, column=1, columnspan=2, sticky="EW", pady=(14, 0))

window.columnconfigure(1, weight=1)
window.mainloop()