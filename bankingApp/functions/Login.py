import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import json
from User_Manager import RegistrationPage  
from Banking_App import BankingApp  


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure() 
        label = ttk.Label(self, text="Please Login", font=("Helvetica", 12, "bold"))
        label.pack(padx=10, pady=5)

        # Create the main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Calculate the position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width - 500) // 2  # Center horizontally
        y_coordinate = (screen_height - 200) // 2  # Center vertically

        self.geometry(f"500x450+{x_coordinate}+{y_coordinate}")  # Set window position

        # Create a style object
        self.style = ttk.Style()
        self.style.configure("Background.TFrame")  # Set background color for the frame

        # Create the main frame with the configured style
        self.main_frame = ttk.Frame(self, style="Background.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure other widget styles
        self.style.configure("TLabel", font=("Helvetica", 12))  # Set background color for labels
        self.style.configure("TEntry", font=("Helvetica", 12))  # Set font for entry widgets
        self.style.configure("TButton", font=("Helvetica", 12))  # Set font for buttons

        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        self.label_username = tk.Label(self.main_frame, text="Username:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.main_frame)
        self.entry_username.pack()
       
        # Password label and entry
        self.label_password = tk.Label(self.main_frame, text="Password:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.main_frame, show="*")
        self.entry_password.pack()

        # Login button
        self.btn_login = tk.Button(self.main_frame, text="Login", width=10, command=self.login)
        self.btn_login.pack(pady=10)

        # Sign Up button
        self.btn_signup = tk.Button(self.main_frame, text="Sign Up", width=10, command=self.signup)
        self.btn_signup.pack()
        
        # Forgot Password button
        self.btn_forgot_password = tk.Button(self.main_frame, text="Forgot Password?", width=15, command=self.forgot_password)
        self.btn_forgot_password.pack(pady=10)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        try:
            with open("users.json", "r") as file:
                users = json.load(file)

                if username in users:
                    if "password" in users[username] and users[username]["password"] == password:
                        messagebox.showinfo("Login Successful", f"Welcome, {username.capitalize()}!")
                        self.destroy()  # Close the login window
                        app = BankingApp(username)  # Instantiate BankingApp with username
                        app.mainloop()
                    else:
                        messagebox.showerror("Login Failed", "Invalid username or password.")
                        # Clear the password entry
                        self.entry_password.delete(0, tk.END)
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password.")
                    # Clear both username and password entries
                    self.entry_username.delete(0, tk.END)
                    self.entry_password.delete(0, tk.END)

        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")

    def signup(self):
        # Hide the login page
        self.withdraw()
        messagebox.showinfo('You are being directed to the Registration Page')

        # Show the registration page
        registration_page = RegistrationPage(self)
        registration_page.mainloop()
        
    def forgot_password(self):
        username = self.entry_username.get().strip()

        try:
            with open("users.json", "r+") as file:
                try:
                    users = json.load(file)
                    if not isinstance(users, dict):
                        users = {}  # Initialize as empty dictionary if loaded data is not a dictionary
                except (json.JSONDecodeError, ValueError):
                    users = {}  # Handle cases where file is empty or not valid JSON

                if username in users:
                    # Generate a new random password
                    new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
                    users[username]["password"] = new_password

                    # Update users.json with new password
                    file.seek(0)
                    json.dump(users, file, indent=4)
                    file.truncate()

                    # Show the new password to the user
                    messagebox.showinfo("New Password Generated", f"Your new password is: {new_password}")
                else:
                    messagebox.showerror("Username not found", "Username does not exist. Please enter a valid username.")

        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")



if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
