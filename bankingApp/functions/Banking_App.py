import tkinter as tk
from tkinter import messagebox
from Transaction_manager import TransactionManager
import json

class BankingApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"Banking App - Welcome, {username}")
        self.geometry("400x300")
 #Load user data
        self.user_data =  self.load_user_data()
        if self.user_data:
            #Initialize Transaction Manager 
            self.transaction_manager = TransactionManager()
            self.transaction_manager.load_accounts()
            
            if 'balance' not in self.user_data:
                self.user_data['balance'] = -100
            
                self.create_widgets()
        else:
            messagebox.showerror("Error", "Failed to load user data.")
            self.destroy()
    def load_user_data(self):
        user_data = {}
        try:
            with open("users.json", "r") as file:
                try:
                    user_data = json.load(file)
                    if not isinstance(user_data, dict):
                        messagebox.showerror("Error", "Invalid JSON format in user data file.")
                        user_data = {}
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON format in user data file.")
                    user_data = {}
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
        return user_data
    def save_user_data(self):
        if users is None:
            users = {self.username: self.user_data}
        try:
            with open("users.json", "w") as file:
                json.dump(self.user_data, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
    def create_widgets(self):
       # Labels
        self.label_welcome = tk.Label(self, text=f"Welcome, {self.username}!", font=("Arial", 18))
        self.label_welcome.pack(pady=10)

        # Display balance
        self.label_balance = tk.Label(self, text=f"Available Balance: R{self.user_data.get('balance', 0)}", font=("Arial", 12))
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
        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found.")
        else:
            transaction_details = "\n".join(transactions)
            messagebox.showinfo("Transactions", transaction_details)
    def deduct_registration_fee(self):
        # Deduct registration fee from user's balance
        registration_fee = 100
        self.user_data['balance'] -= registration_fee
        self.save_user_data()
        # amount = 100
        # transaction = f"Registration Fee: -R{amount}"
        # self.user_data.setdefault("transactions", []).append(transaction)
        # self.save_user_data({self.username: self.user_data})
        # self.label_balance.config(text=f"Available Balance: R{self.user_data['balance'] + amount}")
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
        amount_str = self.entry_amount.get().strip()
        if not amount_str:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return
        # Update balance in user data
        if 'balance' in self.master.user_data:
            self.master.user_data["balance"] += amount
        else:
            messagebox.showerror("Error", "Balance data not found. Please reload the application.")
            return
        # Update transactions
        transaction = f"Deposit: +R{amount}"
        self.master.user_data.setdefault("transactions", []).append(transaction)
        # Save updated data to JSON file
        self.master.save_user_data()
        # Show success message
        messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
        # Update balance label in BankingApp window
        self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
        # Close the DepositPage window
        self.destroy()
        
    def save_user_data(self):
        try:
            with open("users.json", "r+") as file:
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
        amount_str = self.entry_amount.get().strip()
        if not amount_str:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        # Check if 'balance' exists in user_data (should have been set by BankingApp)
        if 'balance' in self.master.user_data:
            # Check if sufficient balance
            if amount > self.master.user_data["balance"]:
                messagebox.showerror("Withdrawal Error", "Insufficient funds.")
                return

            # Update balance in user data
            self.master.user_data["balance"] -= amount
        else:
            messagebox.showerror("Error", "Balance data not found. Please reload the application.")
            return

        # Update transactions
        transaction = f"Withdrawal: -R{amount}"
        self.master.user_data.setdefault("transactions", []).append(transaction)
        # Save updated data to JSON file
        self.master.save_user_data()
        # Show success message
        messagebox.showinfo("Withdrawal", f"Withdrawal of R{amount} successful.")
        # Update balance label in BankingApp window
        self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
        # Close the WithdrawPage window
        self.destroy()
    def save_user_data(self):
        try:
            with open("users.json", "r+") as file:
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
        amount_str = self.entry_amount.get().strip()
        recipient = self.entry_recipient.get().strip()

        if not amount_str or not recipient:
            messagebox.showerror("Error", "Please enter both amount and recipient.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        # Check if 'balance' exists in sender's user_data (should have been set by BankingApp)
        if 'balance' in self.master.user_data:
            # Check if recipient exists in users.json
            try:
                with open("users.json", "r") as file:
                    users = json.load(file)
                    if recipient not in users:
                        messagebox.showerror("Transfer Error", "Recipient user does not exist.")
                        return

                    # Check if recipient's data includes 'balance'
                    if 'balance' not in users[recipient]:
                        messagebox.showerror("Transfer Error", f"Recipient {recipient} has no balance data.")
                        return

                    # Check if sufficient balance
                    if amount > self.master.user_data["balance"]:
                        messagebox.showerror("Transfer Error", "Insufficient funds.")
                        return

                    # Update balance in sender's user data
                    self.master.user_data["balance"] -= amount
                    # Update transactions for sender
                    transaction_sender = f"Transfer to {recipient}: -R{amount}"
                    self.master.user_data.setdefault("transactions", []).append(transaction_sender)

                    # Update balance in recipient's user data
                    users[recipient]["balance"] += amount
                    # Update transactions for recipient
                    transaction_recipient = f"Transfer from {self.master.username}: +R{amount}"
                    users[recipient].setdefault("transactions", []).append(transaction_recipient)

                    # Save updated data to JSON file
                    self.master.save_user_data(users)

                    # Show success message
                    messagebox.showinfo("Transfer", f"Transfer of R{amount} to {recipient} successful.")
                    # Update balance label in BankingApp window
                    self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
                    # Close the TransferPage window
                    self.destroy()

            except FileNotFoundError:
                messagebox.showerror("Error", "User data file not found.")
                return
        else:
            messagebox.showerror("Error", "Balance data not found. Please reload the application.")
            return

    def save_user_data(self, users):
        try:
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")

if __name__ == "__main__":
    username = "username"
    login_page = BankingApp(username)
    login_page.mainloop()