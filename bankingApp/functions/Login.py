import tkinter as tk
from tkinter import messagebox
import json
from User_Manager import RegistrationPage  # Import the RegistrationPage class

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Page")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        # Password label and entry
        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        # Login button
        self.btn_login = tk.Button(self, text="Login", width=10, command=self.login)
        self.btn_login.pack(pady=10)

        # Sign Up button
        self.btn_signup = tk.Button(self, text="Sign Up", width=10, command=self.signup)
        self.btn_signup.pack()

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        try:
            with open("users.json", "r") as file:
                users = json.load(file)

                if username in users and users[username]["password"] == password:
                    messagebox.showinfo("Login Successful", f"Welcome, {username.capitalize()}!")
                    self.destroy()  # Close the login window
                    # Add your code here to open the main application or another window
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password.")
                    # Clear the password entry
                    self.entry_password.delete(0, tk.END)

        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")

    def signup(self):
        # Hide the login page
        self.withdraw()

        # Show the registration page
        registration_page = RegistrationPage(self)
        registration_page.mainloop()

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
