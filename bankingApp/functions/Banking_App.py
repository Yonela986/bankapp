import tkinter as tk
from tkinter import messagebox
import json
from Transaction_manager import TransactionManager

class BankingApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"Banking App - Welcome, {username}")
        self.geometry("400x300")
        self.transaction_manager = self.initialize_transaction_manager()
        self.create_widgets()
        self.update_balance()

    def initialize_transaction_manager(self):
        try:
            manager = TransactionManager()
            manager.load_accounts()
            return manager
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize TransactionManager: {e}")
            raise

    def create_widgets(self):
        self.label_welcome = tk.Label(self, text=f"Welcome, {self.username}!", font=("Arial", 18))
        self.label_welcome.pack(pady=10)

        self.label_balance = tk.Label(self, text="", font=("Arial", 12))
        self.label_balance.pack(pady=5)

        buttons = [
            ("Deposit", self.open_deposit_page),
            ("Withdraw", self.open_withdraw_page),
            ("Transfer", self.open_transfer_page),
            ("View Transactions", self.view_transactions),
            ("Load Transactions", self.load_transactions),
            ("Download Transactions", self.download_transactions)
        ]

        for text, command in buttons:
            tk.Button(self, text=text, command=command).pack(pady=5)

        self.create_transaction_listbox()

    def create_transaction_listbox(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.listbox_transactions = tk.Listbox(frame, width=50, height=10)
        self.listbox_transactions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox_transactions.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_transactions.config(yscrollcommand=scrollbar.set)

    def update_balance(self):
        balance = self.transaction_manager.get_balance(self.username)
        self.label_balance.config(text=f"Available Balance: R{balance:.2f}")

    def open_deposit_page(self):
        DepositPage(self)

    def open_withdraw_page(self):
        WithdrawPage(self)

    def open_transfer_page(self):
        TransferPage(self)

    def view_transactions(self):
        transactions = self.transaction_manager.get_transactions(self.username)
        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found.")
        else:
            transaction_message = "\n".join(transactions)
            messagebox.showinfo("Transactions", transaction_message)

    def load_transactions(self):
        self.listbox_transactions.delete(0, tk.END)
        transactions = self.transaction_manager.get_transactions(self.username)
        for transaction in transactions:
            self.listbox_transactions.insert(tk.END, transaction)

    def download_transactions(self):
        try:
            transactions_content = self.transaction_manager.download_transaction_history()
            filename = f"{self.username}_TransactionHistory.txt"
            with open(filename, "w") as file:
                file.write(transactions_content)
            messagebox.showinfo("Download", f"Transaction history downloaded to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading transaction history: {str(e)}")

class TransactionPage(tk.Toplevel):
    def __init__(self, master, title, button_text, process_func):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.process_func = process_func
        self.create_widgets(button_text)

    def create_widgets(self, button_text):
        tk.Label(self, text="Enter amount:").pack(pady=5)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)
        tk.Button(self, text=button_text, command=self.process_transaction).pack(pady=5)

    def process_transaction(self):
        amount_str = self.entry_amount.get().strip()
        if not amount_str:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
            self.process_func(amount)
            self.master.update_balance()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class DepositPage(TransactionPage):
    def __init__(self, master):
        super().__init__(master, "Deposit", "Deposit", self.process_deposit)

    def process_deposit(self, amount):
        self.master.transaction_manager.deposit(self.master.username, amount)
        messagebox.showinfo("Deposit", f"Deposit of R{amount:.2f} successful.")

class WithdrawPage(TransactionPage):
    def __init__(self, master):
        super().__init__(master, "Withdraw", "Withdraw", self.process_withdrawal)

    def process_withdrawal(self, amount):
        self.master.transaction_manager.withdraw(self.master.username, amount)
        messagebox.showinfo("Withdrawal", f"Withdrawal of R{amount:.2f} successful.")

class TransferPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Transfer")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter transfer amount:").pack(pady=5)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        tk.Label(self, text="Enter recipient username:").pack(pady=5)
        self.entry_recipient = tk.Entry(self)
        self.entry_recipient.pack(pady=5)

        tk.Button(self, text="Transfer", command=self.process_transfer).pack(pady=5)

    def process_transfer(self):
        amount_str = self.entry_amount.get().strip()
        recipient = self.entry_recipient.get().strip()

        if not amount_str or not recipient:
            messagebox.showerror("Error", "Please enter both amount and recipient.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
            self.master.transaction_manager.transfer(self.master.username, recipient, amount)
            messagebox.showinfo("Transfer", f"Transfer of R{amount:.2f} to {recipient} successful.")
            self.master.update_balance()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    username = "username"
    app = BankingApp(username)
    app.mainloop()
# import tkinter as tk
# from tkinter import messagebox
# import traceback
# from Transaction_manager import TransactionManager 
# import json


# class BankingApp(tk.Tk):
#     def __init__(self, username):
#         super().__init__()
#         self.username = username
#         self.title(f"Banking App - Welcome, {username}")
#         self.geometry("400x300")
#         self.user_data = self.load_user_data()

    
#     #Ensure user_data is a dictionary
#         if not isinstance(self.user_data, dict):
#          self.user_data = {"balance": 0}
    
#     # Ensure balance exists
#         if 'balance' not in self.user_data:
#           self.user_data['balance'] = 0
    
#     # Initialize Transaction Manager 
#         try:
#             self.transaction_manager = TransactionManager()
#             self.transaction_manager.load_accounts()
#         except Exception as e:
#            print(f"Error initializing TransactionManager: {e}")
#            messagebox.showerror("Error",  f"Failed to initialize TransactionManager: {e}" )
#         # You might want to show a messagebox here as well
    
#         self.save_user_data()  # Save the initial data
#         self.create_widgets()
       
#     def load_user_data(self):
#         user_data = {}
#         try:
#             with open("users.json", "r") as file:
#                 try:
#                     all_user_data = json.load(file)
#                     if not isinstance(all_user_data, dict):
#                         messagebox.showerror("Error", "Invalid JSON format in user data file.")
#                     else:
#                         user_data = all_user_data.get(self.username, {})
#                 except FileNotFoundError:
#                    messagebox.showerror("Error", "User data file not found.")
#         except json.JSONDecodeError:
#              messagebox.showerror("Error", "Invalid JSON format in user data file.")
#              return user_data
         
#     def save_user_data(self):
#         try:
#             with open("users.json", "r") as file:
#              all_users_data = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             all_users_data = {}
    
#         all_users_data[self.username] = self.user_data
    
#         with open("users.json", "w") as file:
#             json.dump(all_users_data, file, indent=4)
    
 
#     def create_widgets(self):
#         # Labels
#         self.label_welcome = tk.Label(self, text=f"Welcome, {self.username}!", font=("Arial", 18))
#         self.label_welcome.pack(pady=10)

#         # Display balance
#         self.label_balance = tk.Label(self, text=f"Available Balance: R{self.user_data.get('balance', 0)}", font=("Arial", 12))
#         self.label_balance.pack(pady=5)

#         # Buttons
#         self.btn_deposit = tk.Button(self, text="Deposit", command=self.open_deposit_page)
#         self.btn_deposit.pack(pady=5)

#         self.btn_withdraw = tk.Button(self, text="Withdraw", command=self.open_withdraw_page)
#         self.btn_withdraw.pack(pady=5)

#         self.btn_transfer = tk.Button(self, text="Transfer", command=self.open_transfer_page)
#         self.btn_transfer.pack(pady=5)

#         self.btn_view_transactions = tk.Button(self, text="View Transactions", command=self.view_transactions)
#         self.btn_view_transactions.pack(pady=5)

#         self.frame_transactions = tk.Frame(self)
#         self.frame_transactions.pack(pady=10)

#         self.listbox_transactions = tk.Listbox(self.frame_transactions, width=50, height=10)
#         self.listbox_transactions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         scrollbar = tk.Scrollbar(self.frame_transactions, orient=tk.VERTICAL, command=self.listbox_transactions.yview)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.listbox_transactions.config(yscrollcommand=scrollbar.set)

#         # Load transactions button
#         btn_load_transactions = tk.Button(self, text="Load Transactions", command=self.load_transactions)
#         btn_load_transactions.pack(pady=10)

#         # Download transactions button
#         btn_download_transactions = tk.Button(self, text="Download Transactions", command=self.download_transactions)
#         btn_download_transactions.pack()
        
#     def open_deposit_page(self):
#         deposit_page = DepositPage(self)
#         deposit_page.grab_set()
        
#     def open_withdraw_page(self):
#         withdraw_page = WithdrawPage(self)
#         withdraw_page.grab_set()
        
#     def open_transfer_page(self):
#         transfer_page = TransferPage(self)
#         transfer_page.grab_set()
        
#     def view_transactions(self):
#         transactions = self.transaction_manager.get_transactions(self.username)
#         if not transactions:
#             messagebox.showinfo("Transactions", "No transactions found.")
#         else:
#             #transaction_details = []
#             # for transaction in transactions:
#             #     transaction_str = f"{transaction['transaction_type']} - R{transaction['amount']} ({transaction['timestamp']})"
#             #     transaction_details.append(transaction_str)

#             transaction_message = "\n".join(transactions)
#             messagebox.showinfo("Transactions", transaction_message)
            
            
#     def load_transactions(self):
#         self.listbox_transactions.delete(0, tk.END)
#         transactions = self.transaction_manager.get_transactions(self.username)
#         for transaction in transactions:
#             self.listbox_transactions.insert(tk.END, transaction)
#         # self.listbox_transactions.delete(0, tk.END)
#         # transactions = self.transaction_manager.get_transaction(self.username)
#         # for transaction in transactions:
#         #     transaction_str = f"{transaction['transaction_type']} - R{transaction['amount']} ({transaction['timestamp']})"
#         #     self.listbox_transactions.insert(tk.END, transaction_str)
#                 # f"{transaction['transaction_type']} - R{transaction['amount']} ({transaction['timestamp']})")

#     def download_transactions(self):
#         try:
#             transactions_content = self.transaction_manager.download_transaction_history()
#             filename = f"{self.username}_TransactionHistory.txt"
#             with open(filename, "w") as file:
#                file.write(transactions_content)
#             messagebox.showinfo("Download", f"Transaction history downloaded to {filename}")
#         except Exception as e:
#             traceback.print_exc()
#             messagebox.showerror("Error", f"An error occurred while downloading transaction history: {str(e)}")
# class DepositPage(tk.Toplevel):
#     def __init__(self, master):
#         super().__init__(master)

#         self.title("Deposit")
#         self.geometry("300x150")

#         self.create_widgets()

#     def create_widgets(self):
#         # Label and Entry for deposit amount
#         self.label_amount = tk.Label(self, text="Enter deposit amount:")
#         self.label_amount.pack(pady=5)

#         self.entry_amount = tk.Entry(self)
#         self.entry_amount.pack(pady=5)

#         # Button to confirm deposit
#         self.btn_deposit = tk.Button(self, text="Deposit", command=self.process_deposit)
#         self.btn_deposit.pack(pady=5)

#     def process_deposit(self):
#         amount_str = self.entry_amount.get().strip()
#         if not amount_str:
#             messagebox.showerror("Error", "Please enter a valid amount.")
#             return
#         try:
#             amount = float(amount_str)
#             if amount <= 0:
#                 raise ValueError("Amount must be a positive number.")
#             self.master.transaction_manager.deposit(self.master.username, amount)
#             messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
#             self.master.update_balance()
#             self.destroy()
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         #     return
#         # # Update balance in user data
#         # # master = self.master
#         # if 'balance' in self.master.user_data:
#         #     self.master.user_data["balance"] += amount
#         # else:
#         #     messagebox.showerror("Error", "Balance data not found. Please reload the application.")
#         #     return
#         # # Update transactions
#         # transaction_details = f"Deposit: +R{amount}"
#         # self.master.transaction_manager.add_transaction(amount, "Deposit", transaction_details)
#         # # Save updated data to JSON file
#         # self.master.save_user_data()
#         # # Show success message
#         # messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
#         # # Update balance label in BankingApp window
#         # self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
#         # # Close the DepositPage window
#         # self.destroy()
        
#     def save_user_data(self):
#         try:
#             with open("users.json", "r+") as file:
#                 users = json.load(file)
#                 users[self.master.username] = self.master.user_data
#                 file.seek(0)
#                 json.dump(users, file, indent=4)
#                 file.truncate()
#         except FileNotFoundError:
#             messagebox.showerror("Error", "User data file not found.")
            
# class WithdrawPage(tk.Toplevel):
#     def __init__(self, master):
#         super().__init__(master)

#         self.title("Withdraw")
#         self.geometry("300x150")

#         self.create_widgets()

#     def create_widgets(self):
#         # Label and Entry for withdrawal amount
#         self.label_amount = tk.Label(self, text="Enter withdrawal amount:")
#         self.label_amount.pack(pady=5)

#         self.entry_amount = tk.Entry(self)
#         self.entry_amount.pack(pady=5)

#         # Button to confirm withdrawal
#         self.btn_withdraw = tk.Button(self, text="Withdraw", command=self.process_withdrawal)
#         self.btn_withdraw.pack(pady=5)

#     def process_withdrawal(self):
#         amount_str = self.entry_amount.get().strip()
#         if not amount_str:
#             messagebox.showerror("Error", "Please enter a valid amount.")
#             return

#         try:
#             amount = float(amount_str)
#             if amount <= 0:
#                 raise ValueError("Amount must be a positive number.")
#             self.master.transaction_manager.deposit(self.master.username, amount)
#             messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
#             self.master.update_balance()
#             self.destroy()
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#             return

#         # # Check if 'balance' exists in user_data (should have been set by BankingApp)
#         # if 'balance' in self.master.user_data:
#         #     # Check if sufficient balance
#         #     if amount > self.master.user_data["balance"]:
#         #         messagebox.showerror("Withdrawal Error", "Insufficient funds.")
#         #         return

#         #     # Update balance in user data
#         #     self.master.user_data["balance"] -= amount
#         # else:
#         #     messagebox.showerror("Error", "Balance data not found. Please reload the application.")
#         #     return

#         # # Update transactions
#         # transaction_details = f"Withdrawal: -R{amount}"
#         # self.master.transaction_manager.add_transaction(amount, "Withdrawal", transaction_details)

#         # # self.master.user_data.setdefault("transactions", []).append(transaction)
#         # # Save updated data to JSON file
#         # self.master.save_user_data()
#         # # Show success message
#         # messagebox.showinfo("Withdrawal", f"Withdrawal of R{amount} successful.")
#         # # Update balance label in BankingApp window
#         # self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
#         # # Close the WithdrawPage window
#         # self.destroy()
#     def save_user_data(self):
#         try:
#             with open("users.json", "r+") as file:
#                 users = json.load(file)
#                 users[self.master.username] = self.master.user_data
#                 file.seek(0)
#                 json.dump(users, file, indent=4)
#                 file.truncate()
#         except FileNotFoundError:
#             messagebox.showerror("Error", "User data file not found.")
       
# class TransferPage(tk.Toplevel):
#     def __init__(self, master):
#         super().__init__(master)

#         self.title("Transfer")
#         self.geometry("300x150")

#         self.create_widgets()

#     def create_widgets(self):
#          # Label and Entry for transfer details
#         self.label_amount = tk.Label(self, text="Enter transfer amount:")
#         self.label_amount.pack(pady=5)

#         self.entry_amount = tk.Entry(self)
#         self.entry_amount.pack(pady=5)

#         self.label_recipient = tk.Label(self, text="Enter recipient username:")
#         self.label_recipient.pack(pady=5)

#         self.entry_recipient = tk.Entry(self)
#         self.entry_recipient.pack(pady=5)

#         # Button to confirm transfer
#         self.btn_transfer = tk.Button(self, text="Transfer", command=self.process_transfer)
#         self.btn_transfer.pack(pady=5)

#     def process_transfer(self):
#         amount_str = self.entry_amount.get().strip()
#         recipient = self.entry_recipient.get().strip()

#         if not amount_str or not recipient:
#             messagebox.showerror("Error", "Please enter both amount and recipient.")
#             return

#         try:
#             amount = float(amount_str)
#             if amount <= 0:
#                 raise ValueError("Amount must be a positive number.")
#             self.master.transaction_manager.deposit(self.master.username, amount)
#             messagebox.showinfo("Deposit", f"Deposit of R{amount} successful.")
#             self.master.update_balance()
#             self.destroy()
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#             return

#         # # Check if 'balance' exists in sender's user_data (should have been set by BankingApp)
#         # if 'balance' in self.user_data:
#         #     # Check if recipient exists in users.json
#         #     try:
#         #         with open("users.json", "r") as file:
#         #             users = json.load(file)
#         #             if recipient not in users:
#         #                 messagebox.showerror("Transfer Error", "Recipient user does not exist.")
#         #                 return

#         #             # Check if recipient's data includes 'balance'
#         #             if 'balance' not in users[recipient]:
#         #                 messagebox.showerror("Transfer Error", f"Recipient {recipient} has no balance data.")
#         #                 return

#         #             # Check if sufficient balance
#         #             if amount > self.user_data["balance"]:
#         #                 messagebox.showerror("Transfer Error", "Insufficient funds.")
#         #                 return

#         #             # Update balance in sender's user data
#         #             self.user_data["balance"] -= amount
#         #             # Update transactions for sender
#         #             transaction_sender = f"Transfer to {recipient}: -R{amount}"
#         #             self.master.transaction_manager.add_transaction(amount, "Transfer", transaction_sender)

#         #             # self.user_data.setdefault("transactions", []).append(transaction_sender)

#         #             # Update balance in recipient's user data
#         #             users[recipient]["balance"] += amount
#         #             # Update transactions for recipient
#         #             transaction_recipient = f"Transfer from {self.master.username}: +R{amount}"
#         #             users[recipient].setdefault("transactions", []).append(transaction_recipient)

#         #             # Save updated data to JSON file
#         #             self.master.save_user_data(users)

#         #             # Show success message
#         #             messagebox.showinfo("Transfer", f"Transfer of R{amount} to {recipient} successful.")
#         #             # Update balance label in BankingApp window
#         #             self.master.label_balance.config(text=f"Available Balance: R{self.master.user_data['balance']}")
#         #             # Close the TransferPage window
#         #             self.destroy()

#         #     except FileNotFoundError:
#         #         messagebox.showerror("Error", "User data file not found.")
#         #         return
#         # else:
#         #     messagebox.showerror("Error", "Balance data not found. Please reload the application.")
#         #     return

#     def save_user_data(self, users):
#         try:
#             with open("users.json", "w") as file:
#                 json.dump(users, file, indent=4)
#         except FileNotFoundError:
#             messagebox.showerror("Error", "User data file not found.")

        
# if __name__ == "__main__":
#     username = "username"
#     app = BankingApp(username)
#     app.mainloop()
    
    