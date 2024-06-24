# transaction_manager.py
from datetime import datetime
class TransactionManager:
    def __init__(self):
        self.accounts = {}
        self.transaction_history = []

    def load_accounts(self):
        # Load account data from file or initialize if file doesn't exist
        try:
            with open("Transactions.txt", "r") as file:
                for line in file:
                    account, balance = line.strip().split(":")
                    self.accounts[account] = float(balance)
        except FileNotFoundError:
            # Create initial accounts data if file doesn't exist
            self.accounts = {
                "user1": 0,
                "user2": 0,
            }
            self.save_accounts()

    def save_accounts(self):
        # Save account data to file
        with open("Transactions.txt", "w") as file:
            for account, balance in self.accounts.items():
                file.write(f"{account}:{balance}\n")

    def deposit(self, account, amount):
        # Perform deposit operation
        if account in self.accounts:
            self.accounts[account] += amount
            self.save_accounts()
            self.add_transaction(account, amount, "deposit")
        else:
            # Handle case where account doesn't exist
            raise ValueError(f"Account '{account}' does not exist.")
        
    def withdraw(self, account, amount):
        # Perform withdrawal operation
        if account in self.accounts:
            if self.accounts[account] >= amount:
                self.accounts[account] -= amount
                self.save_accounts()
                self.add_transaction(account, amount, "withdrawal")
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError(f"Account '{account}' does not exist.")

    def transfer(self, from_account, to_account, amount):
        # Perform transfer operation
        if from_account in self.accounts and to_account in self.accounts:
            if self.accounts[from_account] >= amount:
                self.accounts[from_account] -= amount
                self.accounts[to_account] += amount
                self.save_accounts()
                self.add_transaction(from_account, amount, "transfer", to_account)
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError("One or both accounts do not exist.")

    def get_balance(self, account):
        # Get current balance of an account
        return self.accounts.get(account, 0)
def add_transaction(self, account, amount, transaction_type, to_account=None):
        # Add transaction to history with timestamp
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
        self.save_transaction_history()

def save_transaction_history(self):
        # Save transaction history to a file
        with open("TransactionHistory.txt", "w") as file:
            for transaction in self.transaction_history:
                file.write(f"{transaction['timestamp']} - {transaction['transaction_type']}: "
                           f"{transaction['amount']} to {transaction['account']}")
                if transaction['transaction_type'] == 'transfer':
                    file.write(f" from {transaction['account']} to {transaction['to_account']}")
                file.write("\n")

def download_transaction_history(self):
        # Provide a way to download transaction history
        try:
            with open("TransactionHistory.txt", "r") as file:
                transaction_history_content = file.read()
                return transaction_history_content
        except FileNotFoundError:
            return "Transaction history not found."


if __name__ == "__main__":
    # Example usage
    transaction_manager = TransactionManager()
    transaction_manager.deposit("user1", 100)
    transaction_manager.withdraw("user1", 50)
    transaction_manager.transfer("user1", "user2", 30)

    print("Current balance of user1:", transaction_manager.get_balance("user1"))
    print("Current balance of user2:", transaction_manager.get_balance("user2"))

    transaction_history_content = transaction_manager.download_transaction_history()
    print("\nTransaction History:")
    print(transaction_history_content)