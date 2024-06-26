# transaction_manager.py
import json
from datetime import datetime
from tkinter import messagebox

class TransactionManager:
    def __init__(self):
        self.accounts = {}
        self.transaction_history = []
        self.load_accounts()
        self.load_transactions()

    def load_accounts(self):
        try:
            with open("users.json", "r") as file:
                self.accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.accounts = {}

    def save_accounts(self):
        with open("users.json", "w") as file:
            json.dump(self.accounts, file, indent=4)

    def load_transactions(self):
        try:
            with open("transactions.json", "r") as file:
                self.transaction_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.transaction_history = []

    def save_transactions(self):
        with open("transactions.json", "w") as file:
            json.dump(self.transaction_history, file, indent=4)

    def get_balance(self, account):
        if account not in self.accounts:
            raise ValueError(f"Account '{account}' does not exist.")
        return self.accounts[account].get('balance', 0)

    def deposit(self, account, amount):
        if account not in self.accounts:
            raise ValueError(f"Account '{account}' does not exist.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        if 'balance' not in self.accounts[account]:
            self.accounts[account]['balance'] = 0
        self.accounts[account]['balance'] += amount
        self.add_transaction(account, amount, "deposit")
        self.save_accounts()

    def withdraw(self, account, amount):
        if account not in self.accounts:
            raise ValueError(f"Account '{account}' does not exist.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        balance = self.get_balance(account)
        if balance < amount:
            raise ValueError("Insufficient funds.")
        
        self.accounts[account]['balance'] -= amount
        self.add_transaction(account, amount, "withdrawal")
        self.save_accounts()

    def transfer(self, from_account, to_account, amount):
        if from_account not in self.accounts or to_account not in self.accounts:
            raise ValueError("One or both accounts do not exist.")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        
        if self.get_balance(from_account) < amount:
            raise ValueError("Insufficient funds for transfer.")
        
        self.accounts[from_account]['balance'] -= amount
        self.accounts[to_account]['balance'] = self.get_balance(to_account) + amount
        self.add_transaction(from_account, amount, "transfer", to_account)
        self.save_accounts()

    def add_transaction(self, account, amount, transaction_type, to_account=None):
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "account": account,
            "amount": amount,
            "transaction_type": transaction_type,
        }
        if transaction_type == "transfer":
            transaction["to_account"] = to_account
        self.transaction_history.append(transaction)
        self.save_transactions()

    def get_transactions(self, account):
        return [
            f"{t['timestamp']} - {t['transaction_type'].capitalize()}: R{t['amount']:.2f}" +
            (f" to {t['to_account']}" if t['transaction_type'] == 'transfer' else "")
            for t in self.transaction_history if t['account'] == account
        ]

    def download_transaction_history(self):
        return "\n".join([
            f"{t['timestamp']} - {t['transaction_type'].capitalize()}: R{t['amount']:.2f}" +
            (f" to {t['to_account']}" if t['transaction_type'] == 'transfer' else "")
            for t in self.transaction_history
        ])

    def view_transaction_history(self, current_user):
        transactions = self.get_transactions(current_user)
        if not transactions:
            return "No transactions found."
        return "\n".join(transactions)

if __name__ == "__main__":
    manager = TransactionManager()
    try:
        manager.deposit("user1", 100)
        manager.withdraw("user1", 50)
        manager.transfer("user1", "user2", 30)
        
        print("Transaction History:")
        print(manager.view_transaction_history("user1"))
        
        downloaded_history = manager.download_transaction_history()
        print("\nDownloaded Transaction History:")
        print(downloaded_history)
    except ValueError as e:
        print(f"Error: {e}")

# # transaction_manager.py
# import json
# from datetime import datetime
# from tkinter import messagebox

# class TransactionManager:
#     def __init__(self):
#         self.accounts = {}
#         self.transaction_history = []
#         self.load_accounts()
#         self.load_transactions()
        
#     def save_transactions(self):
#         with open("transactions.json", "w") as file:
#             json.dump(self.transaction_history, file, indent=4)
            
#     def load_transactions(self):
#         try:
#             with open("users.json", "r") as file:
#                 self.transaction_history = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             self.transaction_history = []
                   
#     def load_accounts(self):
#         try:
#             with open("users.json", "r") as file:
#                 self.accounts = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             self.accounts = {}

#     def save_accounts(self):
#         with open("users.json", "w") as file:
#             json.dump(self.accounts, file, indent=4)

#     def deposit(self, account, amount):
#         if account in self.accounts:
#             if 'balance' not in self.accounts[account]:
#                 self.accounts[account]['balance'] = 0
#             self.accounts[account]['balance'] += amount
#             self.add_transaction(account, amount, "deposit")
#             self.save_accounts()
#         else:
#             raise ValueError(f"Account '{account}' does not exist.")

#     def withdraw(self, account, amount):
#         if account in self.accounts:
#             if 'balance' not in self.accounts[account]:
#                 self.accounts[account]['balance'] = 0
#             if self.accounts[account]['balance'] >= amount:
#                 self.accounts[account]['balance'] -= amount
#                 self.add_transaction(account, amount, "withdrawal")
#                 self.save_accounts()
#             else:
#                 raise ValueError("Insufficient funds.")
#         else:
#             raise ValueError(f"Account '{account}' does not exist.")

#     def transfer(self, from_account, to_account, amount):
#         if from_account in self.accounts and to_account in self.accounts:
#             if 'balance' not in self.accounts[from_account]:
#                 self.accounts[from_account]['balance'] = 0
#             if 'balance' not in self.accounts[to_account]:
#                 self.accounts[to_account]['balance'] = 0
#             if self.accounts[from_account]['balance'] >= amount:
#                 self.accounts[from_account]['balance'] -= amount
#                 self.accounts[to_account]['balance'] += amount
#                 self.add_transaction(from_account, amount, "transfer", to_account)
#                 self.save_accounts()
#             else:
#                 raise ValueError("Insufficient funds.")
#         else:
#             raise ValueError("One or both accounts do not exist.")

#     def add_transaction(self, account, amount, transaction_type, to_account=None):
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         transaction = {
#             "timestamp": timestamp,
#             "account": account,
#             "amount": amount,
#             "transaction_type": transaction_type,
#         }
#         if transaction_type == "transfer":
#             transaction["to_account"] = to_account
#         self.transaction_history.append(transaction)

#     def get_transactions(self, account):
#         return [f"{t['timestamp']} - {t['transaction_type'].capitalize()}: R{t['amount']:.2f}" +
#                 (f" to {t['to_account']}" if t['transaction_type'] == 'transfer' else "")
#                 for t in self.transaction_history if t['account'] == account]
    
#     def download_transaction_history(self):
#         transaction_content = "\n".join([
#             f"{transaction['timestamp']} - {transaction['transaction_type']}: R{float(transaction['amount']):.2f}" +
#             (f" to {transaction['to_account']}" if transaction['transaction_type'] == 'transfer' else "")
#             for transaction in self.transaction_history
#         ])
#         return transaction_content
    
#     def get_balance(self, account):
#         if account in self.accounts:
#             return self.accounts[account].get('balance', 0)
#         else:
#             raise ValueError(f"Account '{account}' does not exist.")
    
#     def view_transaction_history(self):
#         transactions = self.transaction_manager.get_transactions(self.current_user)
#         if not transactions:
#             messagebox.showinfo("Transactions", "No transactions found.")
#         else:
#             transaction_message = "\n".join(transactions)
#             messagebox.showinfo("Transactions", transaction_message)
    
# if __name__ == "__main__":
#     manager = TransactionManager()
#     manager.load_accounts()
#     manager.deposit("user1", 100)
#     manager.withdraw("user1", 50)
#     manager.transfer("user1", "user2", 30)
    
#     print("Transaction History:")
#     print(manager.view_transaction_history())
    
#     downloaded_history = manager.download_transaction_history()
#     print("\nDownloaded Transaction History:")
#     print(downloaded_history)