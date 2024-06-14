import tkinter as tk
import random
import string
from tkinter import messagebox

def generate_password():
    """Generate a random password."""
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, password)

def register():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if any field is empty
    if not (username and email and password):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Check email format
    if not ("@" in email and "." in email):
        messagebox.showerror("Error", "Invalid email address!")
        return

    # Save registration details (You can implement saving to a database here)

    messagebox.showinfo("Success", "Registration successful!")
    # Redirect to login page
    # You can implement this using the .withdraw() method on the current window
    # and then opening the login page window.

# Create main window
root = tk.Tk()
root.title("Registration Page")

# Username
tk.Label(root, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

# Email
tk.Label(root, text="Email:").grid(row=1, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1)

# Password
tk.Label(root, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1)

# Generate password button
generate_password_btn = tk.Button(root, text="Generate Password", command=generate_password)
generate_password_btn.grid(row=2, column=2)

# Register button
register_btn = tk.Button(root, text="Register", command=register)
register_btn.grid(row=3, column=0, columnspan=3)

root.mainloop()

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import re
# import string
# import secrets
# import bcrypt # type: ignore

# class RegForm:

#     def __init__(self, root):
#         self.root = root
#         root.title('Registration Page')


#         # Username label and entry

#         self.username_label = tk.Label(root, text="Username:")
#         self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         self.username_entry = tk.Entry(root)
#         self.username_entry.grid(row=0, column=1, padx=5, pady=5)

       
#         # Password label and entry

#         self.password_label = tk.Label(root, text="Password:")
#         self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
#         self.password_entry = tk.Entry(root)
#         self.password_entry.grid(row=1, column=1, padx=5, pady=5)

#          # Create password button
#         self.create_password_button = tk.Button(root, text="Create Password", command=self.create_password)
#         self.create_password_button.grid(row=2, column=1, padx=5, pady=5)


#         # Generate password button
#         self.generate_password_button = tk.Button(root, text="Generate Password", command=self.generate_random_password)
#         self.generate_password_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

 

#         # Login button
#         self.register_button = tk.Button(root, text="Register", command=self.register)
#         self.register_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

 

#         # Clear button

#         self.clear_button = tk.Button(root, text="Clear", command=self.clear_entries)
#         self.clear_button.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)

 

#     def generate_random_password(self):

#         # Define the characters to use in the password

#         characters = string.ascii_letters + string.digits + string.punctuation

       

#         # Generate a random password with 12 characters

#         random_password = ''.join(secrets.choice(characters) for _ in range(12))

       

#         # Update the password entry with the generated password

#         self.password_entry.delete(0, tk.END)

#         self.password_entry.insert(0, random_password)

       

#     def create_password(self):

#             new_password = simpledialog.askstring("Create Password", "Enter your password:", show="*")

#             if new_password and self.validate_password(new_password):

#             # Update the password entry with the new password

#               self.password_entry.delete(0, tk.END)

#               self.password_entry.insert(0, new_password)

 

#     def validate_password(self, password):

#         # Password accepted, at least 8 characters long, containing at least one uppercase letter,

#         # one lowercase letter, one digit, and one special character

#         pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

#         if password == pattern:

#             if password == '':

#                 messagebox.showerror('Please enter Password')

#             else:

#              return re.match(pattern, password)

#         else:

#             messagebox.showerror('Password must be at least 8 characters long, containing at least one uppercase letter, one lowercase and digit with one special character ')

 

#     def validate_username(self, username):

#         # Pattern for acceptable username

#         pattern = r'^[a-zA-Z0-9_]{4,20}$'

#         return re.match(pattern, username)

 

#     def register(self):

#         username = self.username_entry.get()

#         entered_password = self.password_entry.get()

       

#         # In a real-world application, retrieve the hashed password for the given username from the database

#         hashed_password_from_database = b'$2b$12$E9OfQryI01plbgz8onmQSO.uMzx4NUQBFLfAUp5JhXbYI6jBdtTve'  # Example hashed password

       

#         if self.validate_username(username):

#             if bcrypt.checkpw(entered_password.encode(), hashed_password_from_database) or self.validate_password(entered_password):

#                 messagebox.showinfo('Register', 'Register successful!')

#             else:

#                 messagebox.showerror('Register', 'Invalid username or password')

#         else:

#             messagebox.showerror('Register', 'Invalid username')

 

#     def clear_entries(self):

#         self.username_entry.delete(0, tk.END)

#         self.password_entry.delete(0, tk.END)

 

# # Create the main window

# root = tk.Tk()

# register_form = RegForm(root)

 

# # Run the main event loop

# root.mainloop()
