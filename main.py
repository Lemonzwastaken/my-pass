from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import hashlib

#FIX BUILD PROBLEM
import sys
import os

def resource_path(relative_path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

MASTER_PASSWORD_FILE = "master.txt"

#---------------------------FIND PASSWORD---------------------------#

def find_password():
    try:
        with open("passwords.json", "r") as file:
            website = website_entry.get()
            data = json.load(file)
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title="Details", message=f"Website:   {website}\n\nEmail:      {email}\n\nPassword:  {password}\n")
            else:
                messagebox.showinfo(title="Oops", message=f"\n  No details found for '{website}'.  \n")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="\n  No data file found.\n  Please save some passwords first.  \n")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    generate_password_button.config(text="Copied!", state=DISABLED, fg="#ffcccc")
    window.after(2000, lambda: generate_password_button.config(text="Generate Password", state=NORMAL, fg="white"))

#---------------------------- MASTER PASSWORD ---------------------------------#

#HASING PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_master_password(password):
    with open(MASTER_PASSWORD_FILE, "w") as masterpass:
        masterpass.write(hash_password(password))


#SETTING UP MASTERPASSWORD
def setup_master_password():


    def disable_event():
        pass
    
    
    setup = Toplevel()
    setup.protocol("WM_DELETE_WINDOW", disable_event)
    setup.grab_set()
    setup.lift()
    setup.title("Set Master Password")
    setup.config(padx=40, pady=30)

    Label(setup, text="Enter master password:").pack()
    entry1 = Entry(setup, show="*")
    entry1.pack()

    Label(setup, text="Confirm master password:").pack()
    entry2 = Entry(setup, show="*")
    entry2.pack()

    error_label = Label(setup, text="", fg="red")
    error_label.pack()

    def confirm_setup():
        if entry1.get() == "":
            error_label.config(text="Password cannot be empty")
        elif len(entry1.get()) < 2:
            error_label.config(text="Password cannot be less than 2 letters")
        else:
            if entry1.get() != entry2.get():
                error_label.config(text="Passwords do not match")

            else:
                with open("master.txt", "w") as masterfile:
                    masterfile.write(hash_password(entry1.get()))
                setup.destroy()

    Button(setup, text="Set Password", command=confirm_setup).pack()

#CHECKING FOR MASTERPASSWORD
def check_master_password():


    def disable_event():
        pass
    

    login = Toplevel()
    login.protocol("WM_DELETE_WINDOW", disable_event)
    login.grab_set()
    login.lift()
    login.title("Login")
    login.config(padx=40, pady=30)
    Label(login, text="Enter master password:").pack()
    
    entry = Entry(login, show="*")
    entry.pack()
    
    error_label = Label(login, text="", fg="red")
    error_label.pack()

    def attempt_login():
        if len(entry.get()) < 1:
            error_label.config(text="Please enter a password")
            return

        with open("master.txt", "r") as file:
            hashed_pass = file.read()

        if hash_password(entry.get()) == hashed_pass:
            login.destroy()
        else:
            error_label.config(text="Incorrect password")
            entry.delete(0, END)

    Button(login, text="Unlock", command=attempt_login).pack()









# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="\n  Please make sure no fields are empty.  \n")
    else:
        try:
            with open("passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        if website in data:
            is_ok = messagebox.askquestion(title="Already exists", message=f"\n '{website}' already has a saved password. \n\n Do you want to overwrite it? \n")
            if is_ok:
                data.update(new_data)

                with open("passwords.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)


                website_entry.delete(0, END)
                password_entry.delete(0, END)
            else:
                return

        else:
            is_ok = messagebox.askokcancel(title=website, message=f"\n  Website:   {website}\n\n  Email:      {email}\n\n  Password:  {password}\n\n  Save these details?\n")
            if is_ok:
                data.update(new_data)
                with open("passwords.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)


                website_entry.delete(0, END)
                password_entry.delete(0, END)
            else:
                return


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("MyPass")
window.config(padx=50, pady=40, bg="#f0f2f5")

FONT = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")
BG = "#f0f2f5"
RED = "#e05c5c"
BLUE = "#4a90d9"
TEXT = "#2d2d2d"
MUTED = "#999999"

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
canvas.create_text(LOGO_W // 2, 240, text="MyPass", font=("Helvetica", 22, "bold"), fill=RED)
canvas.create_text(LOGO_W // 2, 262, text="your passwords, locked tight", font=("Helvetica", 8), fill=MUTED)

# Divider
Frame(window, height=1, bg="#d0d0d0").grid(row=1, column=0, columnspan=3, sticky="EW", pady=(5, 20))

# Labels
website_label = Label(window, text="Website:", font=FONT_BOLD, bg=BG, fg=TEXT)
website_label.grid(row=2, column=0, sticky="E", pady=10, padx=(0, 14))
email_label = Label(window, text="Email/Username:", font=FONT_BOLD, bg=BG, fg=TEXT)
email_label.grid(row=3, column=0, sticky="E", pady=10, padx=(0, 14))
password_label = Label(window, text="Password:", font=FONT_BOLD, bg=BG, fg=TEXT)
password_label.grid(row=4, column=0, sticky="E", pady=10, padx=(0, 14))

# Entries
website_entry = styled_entry(window, width=21)
website_entry.grid(row=2, column=1, sticky="EW", pady=10, ipady=7)
website_entry.focus()

email_entry = styled_entry(window, width=35)
email_entry.grid(row=3, column=1, columnspan=2, sticky="EW", pady=10, ipady=7)
email_entry.insert(0, "yourname@mail.com")

password_entry = styled_entry(window, width=21)
password_entry.grid(row=4, column=1, sticky="EW", pady=10, ipady=7)

# Buttons
generate_password_button = Button(window, text="Generate Password", font=FONT, bg=RED, fg="white",
                                  relief="flat", cursor="hand2", activebackground="#c94444",
                                  activeforeground="white", padx=8, pady=7, command=generate_password)
generate_password_button.grid(row=4, column=2, sticky="EW", pady=10, padx=(10, 0))

find_password_button = Button(window, text="Find Password", font=FONT, bg=RED, fg="white",
                              relief="flat", cursor="hand2", activebackground="#c94444",
                              activeforeground="white", padx=8, pady=7, command=find_password)
find_password_button.grid(row=2, column=2, sticky="EW", pady=10, padx=(10, 0))

add_button = Button(window, text="Add", width=36, font=FONT_BOLD, bg=BLUE, fg="white",
                    relief="flat", cursor="hand2", activebackground="#357abd",
                    activeforeground="white", pady=10, command=save)
add_button.grid(row=5, column=1, columnspan=2, sticky="EW", pady=(20, 0))


check_master_password()


window.columnconfigure(1, weight=1)
window.mainloop()