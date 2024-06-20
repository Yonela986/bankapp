# transaction_manager.py

class TransactionManager:
    def __init__(self):
        self.accounts = {}

    def load_accounts(self):
        # Load account data from file or initialize if file doesn't exist
        try:
            with open("Transaction.txt", "r") as file:
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
        with open("Transaction.txt", "w") as file:
            for account, balance in self.accounts.items():
                file.write(f"{account}:{balance}\n")

    def deposit(self, account, amount):
        # Perform deposit operation
        if account in self.accounts:
            self.accounts[account] += amount
            self.save_accounts()
        else:
            # Handle case where account doesn't exist
            raise ValueError(f"Account '{account}' does not exist.")
        
    def withdraw(self, account, amount):
        # Perform withdrawal operation
        if account in self.accounts:
            if self.accounts[account] >= amount:
                self.accounts[account] -= amount
                self.save_accounts()
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
            else:
                raise ValueError("Insufficient funds.")
        else:
            raise ValueError("One or both accounts do not exist.")

    def get_balance(self, account):
        # Get current balance of an account
        return self.accounts.get(account, 0)
