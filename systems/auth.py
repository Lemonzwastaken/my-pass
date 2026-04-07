import hashlib
import os
from tkinter import *

MASTER_PASSWORD_FILE = "master.txt"


#HASH PASS
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()





#SETUP MASTER PASSWORD
def setup_master_password(window):
    def disable_event():
        os._exit(0)

    setup = Toplevel()
    setup.protocol("WM_DELETE_WINDOW", disable_event)
    setup.grab_set()
    setup.lift()
    setup.title("Set Master Password")
    setup.config(padx=40, pady=30, bg="#f0f2f5")

    Label(setup, text="Set Master Password", font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#2d2d2d").pack(pady=(0, 15))
    Label(setup, text="Enter master password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()
    entry1 = Entry(setup, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                   highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    entry1.pack(ipady=6, pady=5)
    entry1.focus()

    Label(setup, text="Confirm master password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()
    entry2 = Entry(setup, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                   highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    entry2.pack(ipady=6, pady=5)

    error_label = Label(setup, text="", font=("Helvetica", 9), bg="#f0f2f5", fg="#e05c5c")
    error_label.pack()

    def confirm_setup(event=None):
        if entry1.get() == "":
            error_label.config(text="Password cannot be empty")
        elif len(entry1.get()) < 2:
            error_label.config(text="Password must be at least 2 characters")
        elif entry1.get() != entry2.get():
            error_label.config(text="Passwords do not match")
        else:
            with open(MASTER_PASSWORD_FILE, "w") as f:
                f.write(hash_password(entry1.get()))
            setup.destroy()

    Button(setup, text="Set Password", font=("Helvetica", 11), bg="#4a90d9", fg="white",
           relief="flat", cursor="hand2", command=confirm_setup).pack(fill="x", padx=20, pady=(5, 0))
    Button(setup, text="Close", font=("Helvetica", 11), bg="#888888", fg="white",
           relief="flat", cursor="hand2", command=disable_event).pack(fill="x", padx=20, pady=(5, 0))
    entry2.bind("<Return>", confirm_setup)
    setup.wait_window()




#CHECK MASTER PASSWORD
def check_master_password():
    def disable_event():
        os._exit(0)

    login = Toplevel()
    login.protocol("WM_DELETE_WINDOW", disable_event)
    login.grab_set()
    login.lift()
    login.title("Login")
    login.config(padx=40, pady=30, bg="#f0f2f5")

    Label(login, text="Welcome Back!", font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#2d2d2d").pack(pady=(0, 15))
    Label(login, text="Enter master password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()

    entry = Entry(login, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                  highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    entry.pack(ipady=6, pady=5)
    entry.focus()

    error_label = Label(login, text="", font=("Helvetica", 9), bg="#f0f2f5", fg="#e05c5c")
    error_label.pack()

    def attempt_login(event=None):
        if len(entry.get()) < 1:
            error_label.config(text="Please enter a password")
            return
        with open(MASTER_PASSWORD_FILE, "r") as file:
            hashed_pass = file.read()
        if hash_password(entry.get()) == hashed_pass:
            login.destroy()
        else:
            error_label.config(text="Incorrect password")
            entry.delete(0, END)

    Button(login, text="Unlock", font=("Helvetica", 11), bg="#4a90d9", fg="white",
           relief="flat", cursor="hand2", command=attempt_login).pack(fill="x", padx=20, pady=(5, 0))
    Button(login, text="Close", font=("Helvetica", 11), bg="#888888", fg="white",
           relief="flat", cursor="hand2", command=disable_event).pack(fill="x", padx=20, pady=(5, 0))
    entry.bind("<Return>", attempt_login)
    login.wait_window()



#CHANGE MASTER PASSWORD
def change_master_password():
    change = Toplevel()
    change.grab_set()
    change.lift()
    change.title("Change Password")
    change.config(padx=40, pady=30, bg="#f0f2f5")

    Label(change, text="Change Master Password", font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#2d2d2d").pack(pady=(0, 15))
    Label(change, text="Current password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()
    current_entry = Entry(change, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                          highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    current_entry.pack(ipady=6, pady=5)
    current_entry.focus()

    Label(change, text="New password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()
    new_entry = Entry(change, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                      highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    new_entry.pack(ipady=6, pady=5)

    Label(change, text="Confirm new password:", font=("Helvetica", 11), bg="#f0f2f5", fg="#2d2d2d").pack()
    confirm_entry = Entry(change, show="*", font=("Helvetica", 11), relief="flat", highlightthickness=1,
                          highlightbackground="#c0c0c0", highlightcolor="#4a90d9", width=25)
    confirm_entry.pack(ipady=6, pady=5)

    error_label = Label(change, text="", font=("Helvetica", 9), bg="#f0f2f5", fg="#e05c5c")
    error_label.pack()

    def confirm_change(event=None):
        with open(MASTER_PASSWORD_FILE, "r") as f:
            saved_hash = f.read()
        if hash_password(current_entry.get()) != saved_hash:
            error_label.config(text="Current password is incorrect")
            current_entry.delete(0, END)
        elif len(new_entry.get()) < 2:
            error_label.config(text="New password too short")
        elif new_entry.get() != confirm_entry.get():
            error_label.config(text="New passwords do not match")
        else:
            with open(MASTER_PASSWORD_FILE, "w") as f:
                f.write(hash_password(new_entry.get()))
            change.destroy()
            from tkinter import messagebox
            messagebox.showinfo(title="Success", message="\n  Master password changed successfully!  \n")

    Button(change, text="Change Password", font=("Helvetica", 11), bg="#4a90d9", fg="white",
           relief="flat", cursor="hand2", command=confirm_change).pack(fill="x", padx=20, pady=(5, 0))
    confirm_entry.bind("<Return>", confirm_change)