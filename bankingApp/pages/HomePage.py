import tkinter as tk
from tkinter import PhotoImage, simpledialog, messagebox
import re
import string
import secrets
import bcrypt # type: ignore
from Register import Register  

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HomePage")
        
        # # Load background image
        bg_image = PhotoImage(file="pages/images/istockphoto-1158779061-612x612.jpg")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Calculate the center of the window
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        x_center = (self.winfo_screenwidth() // 2) - (window_width // 2)
        y_center = (self.winfo_screenheight() // 2) - (window_height // 2)
        
  # Registration button
        register_button = tk.Button(self, text="Register", command=self.show_register)
        register_button.pack(pady=10)

        # Login button
        login_button = tk.Button(self, text="Login", command=self.show_login)
        login_button.pack(pady=10)

    def show_register(self):
        root = tk.Tk()
        self.destroy()

        # Create and display the registration window
        register_window = tk.Toplevel()
        register_window.title("Registration Page")
        #     root = tk.Tk()
        #  root.title('Registration Page')

        # Username label and entry
        username_label = tk.Label(root, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        username_entry = tk.Entry(root)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password label and entry
        password_label = tk.Label(root, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        password_entry = tk.Entry(root)
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create password button
        create_password_button = tk.Button(root, text="Create Password", command=lambda: self.create_password(password_entry))
        create_password_button.grid(row=2, column=1, padx=5, pady=5)

        # Generate password button
        generate_password_button = tk.Button(root, text="Generate Password", command=self.generate_random_password)
        generate_password_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

        # Register button
        register_button = tk.Button(root, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get()))
        register_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        # Clear button
        clear_button = tk.Button(root, text="Clear", command=lambda: self.clear_entries(username_entry, password_entry))
        clear_button.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)

    def generate_random_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(secrets.choice(characters) for _ in range(12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, random_password)

    def create_password(self, password_entry):
        new_password = simpledialog.askstring("Create Password", "Enter your password:", show="*")
        if new_password and self.validate_password(new_password):
            password_entry.delete(0, tk.END)
            password_entry.insert(0, new_password)

    def validate_password(self, password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, password):
            messagebox.showerror('Error', 'Password must be at least 8 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character')
            return False
        return True

    def register(self, username, password):
        # Example hashed password (replace this with actual hashed password retrieval from database)
        hashed_password_from_database = b'$2b$12$E9OfQryI01plbgz8onmQSO.uMzx4NUQBFLfAUp5JhXbYI6jBdtTve'

        if not self.validate_username(username):
            messagebox.showerror('Error', 'Invalid username')
            return

        if bcrypt.checkpw(password.encode(), hashed_password_from_database) or self.validate_password(password):
            messagebox.showinfo('Success', 'Register successful!')
        else:
            messagebox.showerror('Error', 'Invalid username or password')

    def validate_username(self, username):
        pattern = r'^[a-zA-Z0-9_]{4,20}$'
        return re.match(pattern, username)

    def clear_entries(self, username_entry, password_entry):
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
