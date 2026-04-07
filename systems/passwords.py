import json
from tkinter import *
from tkinter import messagebox, ttk
import pyperclip

DATA_FILE = "passwords.json"

def find_password(website_entry):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            website = website_entry.get()
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title="Details", message=f"Website:   {website}\n\nEmail:      {email}\n\nPassword:  {password}\n")
            else:
                messagebox.showinfo(title="Oops", message=f"\n  No details found for '{website}'.  \n")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="\n  No data file found.\n  Please save some passwords first.  \n")

def save_password(website_entry, email_entry, password_entry):
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="\n  Please make sure no fields are empty.  \n")
        return

    try:
        with open(DATA_FILE, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    if website in data:
        is_ok = messagebox.askquestion(title="Already exists", message=f"\n '{website}' already has a saved password. \n\n Do you want to overwrite it? \n")
        if is_ok != "yes":
            return
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"\n  Website:   {website}\n\n  Email:      {email}\n\n  Password:  {password}\n\n  Save these details?\n")
        if not is_ok:
            return

    data.update(new_data)
    with open(DATA_FILE, "w") as data_file:
        json.dump(data, data_file, indent=4)
    website_entry.delete(0, END)
    password_entry.delete(0, END)

def view_all_passwords():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="\n  No data file found.\n  Please save some passwords first.  \n")
        return

    view = Toplevel()
    view.title("All Passwords")
    view.config(padx=20, pady=20, bg="#f0f2f5")
    view.grab_set()
    view.lift()

    Label(view, text="Saved Passwords", font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#2d2d2d").pack(pady=(0, 10))

    cols = ("Website", "Email/Username", "Password")
    tree = ttk.Treeview(view, columns=cols, show="headings", height=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Helvetica", 10), rowheight=28, bg="white", fieldbackground="white")
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), bg="#e05c5c", fg="white")
    style.map("Treeview", background=[("selected", "#4a90d9")])

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="w")

    def refresh_tree():
        tree.delete(*tree.get_children())
        try:
            with open(DATA_FILE, "r") as file:
                d = json.load(file)
            for w, details in d.items():
                tree.insert("", END, values=(w, details["email"], details["password"]))
        except FileNotFoundError:
            pass

    refresh_tree()

    scrollbar = ttk.Scrollbar(view, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_double_click(event):
        item = tree.focus()
        if item:
            password = tree.item(item)["values"][2]
            pyperclip.copy(str(password))
            messagebox.showinfo(title="Copied", message="\n  Password copied to clipboard!  \n")

    def delete_selected():
        item = tree.focus()
        if not item:
            messagebox.showinfo(title="Oops", message="\n  Please select an entry to delete.  \n")
            return
        website = tree.item(item)["values"][0]
        confirm = messagebox.askokcancel(title="Delete", message=f"\n  Delete password for '{website}'?  \n")
        if confirm:
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                del data[website]
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=4)
                refresh_tree()
            except (FileNotFoundError, KeyError):
                pass

    tree.bind("<Double-1>", on_double_click)

    btn_frame = Frame(view, bg="#f0f2f5")
    btn_frame.pack(fill="x", pady=(10, 0))

    Button(btn_frame, text="Delete Selected", font=("Helvetica", 10), bg="#e05c5c", fg="white",
           relief="flat", cursor="hand2", pady=6, command=delete_selected).pack(side="left", padx=(0, 5))
    Label(btn_frame, text="Double-click a row to copy password", font=("Helvetica", 8),
          bg="#f0f2f5", fg="#999999").pack(side="left")