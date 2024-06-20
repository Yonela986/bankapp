# gui.py
import tkinter as tk
from tkinter import messagebox
from Transaction_manager import TransactionManager
import json
# from .Login import LoginPage

class BankingApp(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.title(f"Banking App - Welcome, {username}")
        self.geometry("400x300")

        self.username = username
        
        self.load_user_data()

        self.transaction_manager = TransactionManager()
        self.transaction_manager.load_accounts()

        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_welcome = tk.Label(self, text=f"Welcome, {self.username}!", font=("Arial", 18))
        self.label_welcome.pack(pady=10)

        self.label_balance = tk.Label(self, text=f"Available Balance: R{self.user_data['balance']}", font=("Arial", 12))
        self.label_balance.pack(pady=5)

        # Buttons
        self.btn_deposit = tk.Button(self, text="Deposit", command=self.open_deposit_page)
        self.btn_deposit.pack(pady=5)

        self.btn_withdraw = tk.Button(self, text="Withdraw", command=self.open_withdraw_page)
        self.btn_withdraw.pack(pady=5)

        self.btn_transfer = tk.Button(self, text="Transfer", command=self.open_transfer_page)
        self.btn_transfer.pack(pady=5)

        self.btn_view_transactions = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.btn_view_transactions.pack(pady=5)
        
    def open_deposit_page(self):
        deposit_page = DepositPage(self)
        deposit_page.grab_set()

    def open_withdraw_page(self):
        withdraw_page = WithdrawPage(self)
        withdraw_page.grab_set()

    def open_transfer_page(self):
        transfer_page = TransferPage(self)
        transfer_page.grab_set()

    def view_transactions(self):
        transactions = self.user_data.get("transactions", [])
        transaction_details = "\n".join(transactions)
        messagebox.showinfo("Transactions", transaction_details)

class DepositPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Deposit")
        self.geometry("300x150")

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for deposit amount
        self.label_amount = tk.Label(self, text="Enter deposit amount:")
        self.label_amount.pack(pady=5)

        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        # Button to confirm deposit
        self.btn_deposit = tk.Button(self, text="Deposit", command=self.process_deposit)
        self.btn_deposit.pack(pady=5)

    def process_deposit(self):
        amount = float(self.entry_amount.get())
        # Update balance in user data
        self.master.user_data["balance"] += amount
        # Update transactions
        transaction = f"Deposit: +R{amount}"
        self.master.user_data.setdefault("transactions", []).append(transaction)
        # Save updated data to JSON file
        self.save_user_data()
        # Show success message
        messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
        # Update balance label in BankingApp window
        self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
        # Close the DepositPage window
        self.destroy()

    def save_user_data(self):
        try:
            with open("data/users.json", "r+") as file:
                users = json.load(file)
                users[self.master.username] = self.master.user_data
                file.seek(0)
                json.dump(users, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")

class WithdrawPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Withdraw")
        self.geometry("300x150")

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for withdrawal amount
        self.label_amount = tk.Label(self, text="Enter withdrawal amount:")
        self.label_amount.pack(pady=5)

        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        # Button to confirm withdrawal
        self.btn_withdraw = tk.Button(self, text="Withdraw", command=self.process_withdrawal)
        self.btn_withdraw.pack(pady=5)

    def process_withdrawal(self):
        amount = float(self.entry_amount.get())
        # Check if sufficient balance
        if amount > self.master.user_data["balance"]:
            messagebox.showerror("Withdrawal Error", "Insufficient funds.")
        else:
            # Update balance in user data
            self.master.user_data["balance"] -= amount
            # Update transactions
            transaction = f"Withdrawal: -R{amount}"
            self.master.user_data.setdefault("transactions", []).append(transaction)
            # Save updated data to JSON file
            self.save_user_data()
            # Show success message
            messagebox.showinfo("Withdrawal", f"Withdrawal of R{amount} successful.")
            # Update balance label in BankingApp window
            self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
            # Close the WithdrawPage window
            self.destroy()

    def save_user_data(self):
        try:
            with open("data/users.json", "r+") as file:
                users = json.load(file)
                users[self.master.username] = self.master.user_data
                file.seek(0)
                json.dump(users, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")

class TransferPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Transfer")
        self.geometry("300x150")

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for transfer details
        self.label_amount = tk.Label(self, text="Enter transfer amount:")
        self.label_amount.pack(pady=5)

        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        self.label_recipient = tk.Label(self, text="Enter recipient username:")
        self.label_recipient.pack(pady=5)

        self.entry_recipient = tk.Entry(self)
        self.entry_recipient.pack(pady=5)

        # Button to confirm transfer
        self.btn_transfer = tk.Button(self, text="Transfer", command=self.process_transfer)
        self.btn_transfer.pack(pady=5)

    def process_transfer(self):
        amount = float(self.entry_amount.get())
        recipient = self.entry_recipient.get().strip()

        # Check if recipient exists in users
        try:
            with open("data/users.json", "r") as file:
                users = json.load(file)
                if recipient not in users:
                    messagebox.showerror("Transfer Error", "Recipient user does not exist.")
                    return
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")

        # Check if sufficient balance
        if amount > self.master.user_data["balance"]:
            messagebox.showerror("Transfer Error", "Insufficient funds.")
        else:
            # Update balance in user data for sender
            self.master.user_data["balance"] -= amount
            # Update transactions for sender
            transaction_sender = f"Transfer to {recipient}: -R{amount}"
            self.master.user_data.setdefault("transactions", []).append(transaction_sender)

            # Update balance in user data for recipient
            users[recipient]["balance"] += amount
            # Update transactions for recipient
            transaction_recipient = f"Transfer from {self.master.username}: +R{amount}"
            users[recipient].setdefault("transactions", []).append(transaction_recipient)

            # Save updated data to JSON file
            self.save_user_data(users)
            # Show success message
            messagebox.showinfo("Transfer", f"Transfer of R{amount} to {recipient} successful.")
            # Update balance label in BankingApp window
            self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
            # Close the TransferPage window
            self.destroy()

    def save_user_data(self, users):
        try:
            with open("data/users.json", "w") as file:
                json.dump(users, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")

if __name__ == "__main__":
    login_page = BankingApp()
    login_page.mainloop()