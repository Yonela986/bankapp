
import tkinter as tk
from tkinter import ttk, messagebox
import re
import string
import secrets
from tkinter import simpledialog
import bcrypt # type: ignore

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(background="light blue") 
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
        self.style.configure("Background.TFrame", background="light blue")  # Set background color for the frame

        # Create the main frame with the configured style
        self.main_frame = ttk.Frame(self, style="Background.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure other widget styles
        self.style.configure("TLabel", font=("Helvetica", 12), background="light blue")  # Set background color for labels
        self.style.configure("TEntry", font=("Helvetica", 12))  # Set font for entry widgets
        self.style.configure("TButton", font=("Helvetica", 12))  # Set font for buttons

        # Username label and entry
        self.username_label = ttk.Label(self.main_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = ttk.Label(self.main_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Space between password entry and login button
        space_label = ttk.Label(self.main_frame, text="")
        space_label.grid(row=2, column=0, columnspan=2)

        # Center all widgets vertically and horizontally
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Login button
        self.login_button = ttk.Button(self.main_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Forgot Password link
        self.forgot_password_label = ttk.Label(self, text="Forgot Password?", foreground="blue", cursor="hand2")
        self.forgot_password_label.pack(pady=5)
        self.forgot_password_label.bind("<Button-1>", self.forgot_password)

        # Sign up link
        self.sign_up_label = ttk.Label(self, text="Don't have an account? Sign up", foreground="blue", cursor="hand2")
        self.sign_up_label.pack(pady=5)
        self.sign_up_label.bind("<Button-1>", self.show_registration_page)

    def login(self):
        # Retrieve username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check if username and password are valid (dummy authentication)
        if username == "admin" and password == "password":
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid username or password. Please try again.")
      
    def forgot_password(self, event):
         messagebox.showinfo("Forgot Password", "Please contact support to reset your password.")
    
    def show_registration_page(self, event):
       messagebox.showinfo("Sign Up", "Redirecting to sign up page...")
       registration_window = tk.Toplevel(self)
       registration_page = RegistrationPage(registration_window)

class RegistrationPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Registration Page')

        # Username label and entry
        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password label and entry
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(self.master)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create password button
        self.create_password_button = tk.Button(self.master, text="Create Password", command=self.create_password)
        self.create_password_button.grid(row=2, column=1, padx=5, pady=5)

        # Generate password button
        self.generate_password_button = tk.Button(self.master, text="Generate Password", command=self.generate_random_password)
        self.generate_password_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

        # Login button
        self.register_button = tk.Button(self.master, text="Register", command=self.register)
        self.register_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

     

    # def generate_random_password(self):
    #     # Define the characters to use in the password
    #     characters = string.ascii_letters + string.digits + string.punctuation
    #     # Generate a random password with 12 characters
    #     random_password = ''.join(secrets.choice(characters) for _ in range(12))
    #     # Update the password entry with the generated password
    #     self.password_entry.delete(0, tk.END)
    #     self.password_entry.insert(0, random_password)
def generate_random_password():
    """Generate a random password."""
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, password)

    def create_password(self):
        new_password = simpledialog.askstring("Create Password", "Enter your password:", show="*")
        if new_password and self.validate_password(new_password):
            # Update the password entry with the new password
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, new_password)
              
    def validate_password(self, password):
        # Password accepted, at least 8 characters long, containing at least one uppercase letter,
        # one lowercase letter, one digit, and one special character
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if re.match(pattern, password):
            return True
        else:
            messagebox.showerror('Invalid Password', 'Password must be at least 8 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character')
            return False

    def validate_username(self, username):
        # Pattern for acceptable username
        pattern = r'^[a-zA-Z0-9_]{4,20}$'
        return re.match(pattern, username)

    def register(self):
        username = self.username_entry.get()
        entered_password = self.password_entry.get()
        # In a real-world application, retrieve the hashed password for the given username from the database
        hashed_password_from_database = b'$2b$12$E9OfQryI01plbgz8onmQSO.uMzx4NUQBFLfAUp5JhXbYI6jBdtTve'  # Example hashed password
        # hashed_password = bcrypt.hashpw(entered_password.encode(), bcrypt.gensalt())
        # messagebox.showinfo('Registration', f'Username: {username}, Hashed Password: {hashed_password}')

        if self.validate_username(username):
            if bcrypt.checkpw(entered_password.encode(), hashed_password_from_database) or self.validate_password(entered_password):
                messagebox.showinfo('Register', 'Register successful!')
            else:
                messagebox.showerror('Register', 'Invalid username or password')
        else:
            messagebox.showerror('Register', 'Invalid username')

    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()

