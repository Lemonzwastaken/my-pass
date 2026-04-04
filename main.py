import tkinter as tk


#SAVE PASSWORD







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
        row=row, column=0, sticky="E", pady=6, padx=(0, 10)
    )

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
generate_password = tk.Button(text="Generate", font=FONT, bg="#e05c5c", fg="white", relief="flat", cursor="hand2")
generate_password.grid(row=3, column=2, sticky="EW", pady=6, padx=(6, 0))

add = tk.Button(text="Add", font=FONT, bg="#4a90d9", fg="white", relief="flat", cursor="hand2", command=save_password)
add.grid(row=4, column=1, columnspan=2, sticky="EW", pady=(14, 0))

window.columnconfigure(1, weight=1)
window.mainloop()