import tkinter as tk
from tkinter import PhotoImage

def show_register():

    login_frame.pack_forget()

    register_frame.pack()

 

def show_login():

    register_frame.pack_forget()

    login_frame.pack()

 

root = tk.Tk()

root.title("Main Page")

 

# Load the background image

bg_image = PhotoImage(file="bankingApp\\images\\download.png")

 

# Create a label to hold the background image

bg_label = tk.Label(root, image=bg_image)

bg_label.place(x=0, y=0, relwidth=1, relheight=1)

 

# Create frames for register and login screens

register_frame = tk.Frame(root, bg='white')

login_frame = tk.Frame(root, bg='white')

 

# Register screen widgets

register_label = tk.Label(register_frame, text="Please Register ", font=('Arial', 24))

register_label.pack(pady=20)

 

# Login screen widgets

login_label = tk.Label(login_frame, text="Please Login", font=('Arial', 24))

login_label.pack(pady=20)

 

# Buttons to switch between screens

register_button = tk.Button(root, text="Register", command=show_register)

register_button.pack(side=tk.LEFT, padx=50, pady=20)

 

login_button = tk.Button(root, text="Login", command=show_login)

login_button.pack(side=tk.RIGHT, padx=20, pady=20)

 

show_login()

root.mainloop()