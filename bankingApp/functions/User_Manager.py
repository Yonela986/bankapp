import tkinter as tk
from tkinter import messagebox
import json
import random
import string

class RegistrationPage(tk.Tk):
    def __init__(self, login_page):
        super().__init__()
        self.login_page = login_page  # Reference to the login page

        self.title("Registration Page")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        # ID Number label and entry
        self.label_id_number = tk.Label(self, text="ID Number:")
        self.label_id_number.pack(pady=10)
        self.entry_id_number = tk.Entry(self)
        self.entry_id_number.pack()

        # Password label and entry (generated)
        self.label_password = tk.Label(self, text="Generated Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        # Generate Password button
        self.btn_generate_password = tk.Button(self, text="Generate Password", width=15, command=self.generate_password)
        self.btn_generate_password.pack(pady=10)

        # Register button
        self.btn_register = tk.Button(self, text="Register", width=10, command=self.register)
        self.btn_register.pack(pady=20)

    def generate_password(self):
        # Generate a random password of length 8 consisting of letters and digits
        password_characters = string.ascii_letters + string.digits
        generated_password = ''.join(random.choice(password_characters) for _ in range(8))
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, generated_password)

    def register(self):
        username = self.entry_username.get().strip()
        id_number = self.entry_id_number.get().strip()
        password = self.entry_password.get()

        if not username or not id_number or not password:
            messagebox.showerror("Registration Error", "Please fill in all fields.")
            return

        # Check if username is already taken
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                if username in users:
                    messagebox.showerror("Registration Failed", "Username already exists. Please choose another.")
                    return
        except FileNotFoundError:
            users = {}

        # Store username, id_number, and generated password in users.json
        users[username] = {"id_number": id_number, "password": password}
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        # Store the registration details in BankData.txt
        with open("BankData.txt", "a") as file:
            file.write(f"Username: {username}, ID Number: {id_number}, Password: {password}\n")

        # Show registration success message
        messagebox.showinfo("Registration Successful", "User registered successfully.")

        # Clear fields after registration
        self.entry_username.delete(0, tk.END)
        self.entry_id_number.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        # Close the registration window and show the login page
        self.destroy()
        self.login_page.deiconify()

if __name__ == "__main__":
    login_page = tk.Tk()
    login_page.withdraw()  # Hide the login page initially
    registration_page = RegistrationPage(login_page)
    registration_page.mainloop()


# # user_manager.py

# class UserManager:
#     def __init__(self):
#         self.users = {}  # Initialize an empty dictionary

#     def load_users(self):
#         # Load user data from file
#         try:
#             with open("BankData.txt", "r") as file:
#                 for line in file:
#                     username, password = line.strip().split(":")
#                     self.users[username] = password
#         except FileNotFoundError:
#             # Create initial user data if file doesn't exist
#             self.users = {
#                 "admin": "admin123",  # Default admin user
#             }
#             self.save_users()

#     def save_users(self):
#         # Save user data to file
#         with open("BankData.txt", "w") as file:
#             for username, password in self.users.items():
#                 file.write(f"{username}:{password}\n")

#     def register_user(self, username, password):
#         # Register a new user
#         if username not in self.users:
#             self.users[username] = password
#             self.save_users()
#             return True
#         else:
#             return False

#     def verify_user(self, username, password):
#         # Verify user credentials
#         return self.users.get(username) == password
