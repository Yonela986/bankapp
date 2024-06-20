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


# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
# import csv

# class BankingApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.configure(background="#1bcccc")
#         self.main_frame = ttk.Frame(self)
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         # Calculate the position to center the window
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()
#         x_coordinate = (screen_width - 500) // 2  # Center horizontally
#         y_coordinate = (screen_height - 200) // 2  # Center vertically

#         self.geometry(f"500x450+{x_coordinate}+{y_coordinate}")  # Set window position

#         # Create a style object
#         self.style = ttk.Style()
#         self.style.configure("Background.TFrame", background="#1bcccc")  

#         # Create the main frame with the configured style
#         self.main_frame = ttk.Frame(self, style="Background.TFrame")
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         # Configure other widget styles
#         self.style.configure("TLabel", font=("Helvetica", 12))  
#         self.style.configure("TEntry", font=("Helvetica", 12))  
#         self.style.configure("TButton", font=("Helvetica", 12))  

#         self.balance = 0
#         self.transactions = []  

#         # Title
#         self.title_label = tk.Label(self.main_frame, text="Banking App", font=("Arial", 28), background="#1bcccc")
#         self.title_label.pack(pady=(5, 5))

#         # Subtitle
#         self.subtitle_label = tk.Label(self.main_frame, text="Welcome to Your Banking App", font=("Arial", 12), background="#1bcccc")
#         self.subtitle_label.pack(pady=(3, 10)) 

#         # Available Balance
#         self.balance_label = tk.Label(self.main_frame, text=f"Available Balance: R{self.balance}", font=("Arial", 12), background="#1bcccc")
#         self.balance_label.pack(pady=5)

#          # Deposit Button
#         self.deposit_button = tk.Button(self.main_frame, text="Deposit", command=self.open_deposit_page)
#         self.deposit_button.pack(pady=5)

#          # Withdraw Button
#         self.withdraw_button = tk.Button(self.main_frame, text="Withdraw", command=self.open_withdrawal_page)
#         self.withdraw_button.pack(pady=5)

#         # Transfer Button
#         self.transfer_button = tk.Button(self.main_frame, text="Transfer", command=self.update_balances)
#         self.transfer_button.pack(pady=5)
        
#         # Transaction Button
#         self.transaction_button = tk.Button(self.main_frame, text="View Transactions", command=self.show_transactions)
#         self.transaction_button.pack(pady=5)

#         # Download Statement Button
#         self.download_button = tk.Button(self.main_frame, text="Download Statement", command=self.download_statement)
#         self.download_button.pack(pady=5)
#     def open_deposit_page(self):
#         deposit_page = DepositPage(self, transaction_type="Deposit")
#         self.wait_window(deposit_page)
       
            
#     def open_withdrawal_page(self):
#         withdrawal_page = DepositPage(self, transaction_type="Withdrawal")
#         self.wait_window(withdrawal_page)
     
#     def update_balance(self, amount, transaction_type):
#         if transaction_type == "Deposit":
#             self.balance += amount
#             self.transactions.append(f"Deposit: +R{amount}")
#         elif transaction_type == "Withdrawal":
#             if amount > self.balance:
#                 messagebox.showerror("Error", "Insufficient funds.")
#             else:
#                 self.balance -= amount
#                 self.transactions.append(f"Withdrawal: -R{amount}")
#         self.balance_label.config(text=f"Available Balance: R{self.balance}")

#     def show_transactions(self):
#         transaction_window = TransactionWindow(self, self.transactions)

#     def download_statement(self):
#         with open("Transactions.txt", "w") as file:
#             for transaction in self.transactions:
#                 file.write(transaction + "\n")
#         messagebox.showinfo("Download Complete", "Statement has been downloaded to Transactions.txt")

# class DepositPage(tk.Toplevel):
#     def __init__(self, master, transaction_type):
#         super().__init__(master)

#         self.title(transaction_type.capitalize())
#         self.geometry("300x150")

#         self.amount_label = tk.Label(self, text=f"Enter {transaction_type.lower()} amount:")
#         self.amount_label.pack(pady=5)

#         self.amount_entry = tk.Entry(self)
#         self.amount_entry.pack(pady=5)

#         self.transaction_button = tk.Button(self, text=transaction_type.capitalize(), command=self.process_transaction)
#         self.transaction_button.pack(pady=5)

#         self.amount = None
#         self.transaction_type = transaction_type
        
#     def process_transaction(self):
#         try:
#             amount = float(self.amount_entry.get())
#             if amount <= 0:
#                 messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
#             else:
#                 if self.transaction_type == "Deposit":
#                     self.master.update_balance(amount, self.transaction_type)
#                     self.destroy()
#                 else:
#                    self.withdraw()
#         except ValueError:
#             messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")


#     def deposit(self):
#         amount = float(self.amount_entry.get())
#         self.master.update_balance(amount, "Deposit")
#         self.destroy()
            
#     def withdraw(self):
#         amount = float(self.amount_entry.get())
#         self.master.update_balance(amount, "Withdrawal")
#         self.destroy()
        
# accounts = {
#     'user1': {'balance': 1000},
#     'user2': {'balance': 500},
# }
        
# def transfer_funds(from_account, to_account, amount):
#     if amount <= accounts[from_account]['balance']:
#         accounts[from_account]['balance'] -= amount
#         accounts[to_account]['balance'] += amount
#         messagebox.showinfo("Transfer Successful", f"Transferred {amount} to {to_account}")
#         update_balances()
#     else:
#         messagebox.showerror("Insufficient Funds", "You don't have enough balance for this transfer")

# def update_balances():
#     balance_label_user1.config(text=f"Balance: {accounts['user1']['balance']}") # type: ignore
#     balance_label_user2.config(text=f"Balance: {accounts['user2']['balance']}") # type: ignore

# def transfer(self):
#     from_account = self.from_account_entry.get()  
#     to_account = self.to_account_entry.get()     
#     amount = float(self.amount_entry.get())       

#     # Call the transfer_funds function with the entered values
#     transfer_funds(from_account, to_account, amount)
#     pass
# def update_balances():
#     # Update the balance labels in the UI with the new balances
#     balance_label_user1.config(text=f"Balance: {accounts['user1']['balance']}") # type: ignore
#     balance_label_user2.config(text=f"Balance: {accounts['user2']['balance']}") # type: ignore


# class TransactionWindow(tk.Toplevel):
#     def __init__(self, master, transactions):
#         super().__init__(master)
#         self.title("Transactions")
#         self.geometry("400x300")

#         self.transaction_tree = ttk.Treeview(self, columns=("Transaction",))
#         self.transaction_tree.heading("#0", text="Index")
#         self.transaction_tree.heading("Transaction", text="Transaction")

#         for idx, transaction in enumerate(transactions):
#             self.transaction_tree.insert("", "end", text=idx, values=(transaction,))

#         self.transaction_tree.pack(expand=True, fill=tk.BOTH)

# class DatabaseManager:
#     def __init__(self, bank_data_file, transaction_file):
#         self.bank_data_file = bank_data_file
#         self.transaction_file = transaction_file

#     def get_balance(self):
#         with open(self.bank_data_file, "r") as file:
#             return float(file.read())

#     def update_balance(self, new_balance):
#         with open(self.bank_data_file, "w") as file:
#             file.write(str(new_balance))

#     def log_transaction(self, transaction_info):
#         with open(self.transaction_file, "a") as file:
#             file.write(transaction_info + "\n")

#     def get_transactions(self):
#         with open(self.transaction_file, "r") as file:
#             transactions = []
#             for line in file:
#                 transaction = line.strip().split(", ")
#                 transactions.append({
#                     "Date": transaction[0],
#                     "Type": transaction[1],
#                     "Amount": transaction[2],
#                     "Notes": transaction[3]
#                 })
#             return transactions

#     def export_transactions_to_csv(self, csv_file="transactions.csv"):
#         with open(self.transaction_file, "r") as input_file, open(csv_file, "w", newline="") as output_file:
#             csv_writer = csv.writer(output_file)
#             csv_writer.writerow(["Date", "Type", "Amount", "Notes"])
#             for line in input_file:
#                 transaction = line.strip().split(", ")
#                 csv_writer.writerow(transaction)
#                  # Write transaction data to a CSV file
#         with open("Transactions.txt", "w", newline="") as csvfile:
#             fieldnames = ["Date", "Description", "Amount"]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             writer.writeheader()
#             for transaction in transaction:
#                 writer.writerow(transaction)

#         # Inform the user that the download is complete
#         tk.messagebox.showinfo("Download Complete", "Transactions have been downloaded to transactions.csv")

# if __name__ == "__main__":
#     app = BankingApp()
#     app.mainloop()
