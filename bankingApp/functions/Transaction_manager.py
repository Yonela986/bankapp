# transaction_manager.py
import json
from datetime import datetime

class TransactionManager:
    def __init__(self):
        self.accounts = {}
        self.transaction_history = []
    def load_accounts(self):
        try:
            with open("users.json", "r") as file:
                self.accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.accounts = {}

    def save_accounts(self):
        with open("users.json", "w") as file:
            json.dump(self.accounts, file, indent=4)

    def deposit(self, account, amount):
        if account in self.accounts:
            self.accounts[account]['balance'] += amount
            self.add_transaction(account, amount, "deposit")
            self.save_accounts()
        else:
            raise ValueError(f"Account '{account}' does not exist.")

    def withdraw(self, account, amount):
        if account in self.accounts:
            if self.accounts[account]['balance'] >= amount:
                self.accounts[account]['balance'] -= amount
                self.add_transaction(account, amount, "withdrawal")
                self.save_accounts()
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError(f"Account '{account}' does not exist.")

    def transfer(self, from_account, to_account, amount):
        if from_account in self.accounts and to_account in self.accounts:
            if self.accounts[from_account]['balance'] >= amount:
                self.accounts[from_account]['balance'] -= amount
                self.accounts[to_account]['balance'] += amount
                self.add_transaction(from_account, amount, "transfer", to_account)
                self.save_accounts()
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError("One or both accounts do not exist.")

    def add_transaction(self, account, amount, transaction_type, to_account=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            "timestamp": timestamp,
            "account": account,
            "amount": amount,
            "transaction_type": transaction_type,
        }
        if transaction_type == "transfer":
            transaction["to_account"] = to_account
        self.transaction_history.append(transaction)

    def get_transactions(self, account):
        return [f"{t['timestamp']} - {t['transaction_type'].capitalize()}: R{t['amount']:.2f}" +
                (f" to {t['to_account']}" if t['transaction_type'] == 'transfer' else "")
                for t in self.transaction_history if t['account'] == account]
    
    def download_transaction_history(self):
        transaction_content = "\n".join([
            f"{transaction['timestamp']} - {transaction['transaction_type']}: R{transaction['amount']:.2f}" +
            (f" to {transaction['to_account']}" if transaction['transaction_type'] == 'transfer' else "")
            for transaction in self.transaction_history
        ])
        return transaction_content
    
    def get_balance(self, account):
        return self.accounts.get(account, {}).get('balance', 0)
    
    def view_transaction_history(self):
        return self.transaction_history
    
if __name__ == "__main__":
    manager = TransactionManager()
    manager.load_accounts()
    manager.deposit("user1", 100)
    manager.withdraw("user1", 50)
    manager.transfer("user1", "user2", 30)
    
    print("Transaction History:")
    print(manager.view_transaction_history())
    
    downloaded_history = manager.download_transaction_history()
    print("\nDownloaded Transaction History:")
    print(downloaded_history)