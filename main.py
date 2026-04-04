import tkinter

window = tkinter.Tk()
window.config(padx=20, pady=20)

canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
logo = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo)
canvas.grid(row=0, column=1)

#Website
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)

website_text = tkinter.Entry(width=35)
website_text.grid(row=1, column=1, columnspan=2)

#EMAIL/USERNAME
email_username = tkinter.Label(text="Email/Username:")
email_username.grid(row=2, column=0)

email_username_text = tkinter.Entry(width=35)
email_username_text.grid(row=2, column=1, columnspan=2)

#PASSWORD
password = tkinter.Label(text="Password:")
password.grid(row=3, column=0)

password_text = tkinter.Entry(width=21)
password_text.grid(row=3, column=1)

password_generate = tkinter.Button(text="Generate Password")
password_generate.grid(row=3, column=2)

#ADD BUTTON
add = tkinter.Button(text="Add", width=36)
add.grid(row=4, column=1, columnspan=2)



window.mainloop()