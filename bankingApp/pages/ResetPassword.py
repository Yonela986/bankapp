import tkinter as tk
from tkinter import messagebox

class ResetPasswordPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Reset Password", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.new_password_label = tk.Label(self, text="New Password:")
        self.new_password_label.pack()

        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.pack(pady=5)

        self.confirm_password_label = tk.Label(self, text="Confirm Password:")
        self.confirm_password_label.pack()

        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=5)

        self.reset_button = tk.Button(self, text="Reset Password", command=self.reset_password)
        self.reset_button.pack(pady=10)

    def reset_password(self):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Basic validation
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please enter both new and confirm passwords.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            return

        # Assuming you have a function to reset the password in your application/database
        # Replace the print statement with actual code to reset the password
        print(f"Resetting password to: {new_password}")

        # After resetting password, navigate back to Login page
        self.master.show_login_page()

# Example usage
if __name__ == "__main__":
    class PasswordReset(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Reset Password")
            self.geometry("300x250")
            self.current_page = None
            self.show_login_page()

        def show_login_page(self):
            if self.current_page:
                self.current_page.destroy()
            # self.current_page = Login(self) # type: ignore
            self.current_page.pack(fill=tk.BOTH, expand=True)

        def show_reset_password_page(self):
            if self.current_page:
                self.current_page.destroy()
            self.current_page = ResetPasswordPage(self)
            self.current_page.pack(fill=tk.BOTH, expand=True)

    app = PasswordReset()
    app.mainloop()
