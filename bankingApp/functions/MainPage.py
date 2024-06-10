import tkinter as tk
from tkinter import messagebox

class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")

        self.balance = ''  
        self.transactions = []  

        # Title
        self.title_label = tk.Label(self, text="Banking App", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Subtitle
        self.subtitle_label = tk.Label(self, text="Welcome to Your Banking App", font=("Arial", 12))
        self.subtitle_label.pack(pady=5)

        # Available Balance
        self.balance_label = tk.Label(self, text=f"Available Balance: R{self.balance}", font=("Arial", 12))
        self.balance_label.pack(pady=5)

        # Deposit Button
        self.deposit_button = tk.Button(self, text="Deposit", command=self.open_deposit_page)
        self.deposit_button.pack(pady=5)

        # Transaction Button
        self.transaction_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.transaction_button.pack(pady=5)

    def open_deposit_page(self):
        deposit_page = DepositPage(self)
        self.wait_window(deposit_page)
        if deposit_page.amount:
            self.update_balance(deposit_page.amount, "Deposit")

    def update_balance(self, amount, transaction_type):
        if transaction_type == "Deposit":
            self.balance += amount
            self.transactions.append(f"Deposit: +R{amount}")
        elif transaction_type == "Withdrawal":
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -R{amount}")
        self.balance_label.config(text=f"Available Balance: R{self.balance}")

    def view_transactions(self):
        TransactionHistory(self, self.transactions)

class DepositPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Deposit")
        self.geometry("300x150")

        self.amount_label = tk.Label(self, text="Enter deposit amount:")
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(pady=5)

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.amount = None

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
            else:
                self.master.amount = amount
                self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

class TransactionHistory(tk.Toplevel):
    def __init__(self, master, transactions):
        super().__init__(master)

        self.title("Transaction History")
        self.geometry("300x200")

        self.transactions_label = tk.Label(self, text="Transaction History", font=("Arial", 12))
        self.transactions_label.pack(pady=5)

        self.transactions_text = tk.Text(self, height=10, width=30)
        self.transactions_text.pack(pady=5)

        self.download_button = tk.Button(self, text="Download Statements", command=self.download_statements)
        self.download_button.pack(pady=5)

        for transaction in transactions:
            self.transactions_text.insert(tk.END, f"{transaction}\n")

    def download_statements(self):
        with open("transaction_history.txt", "w") as file:
            file.write(self.transactions_text.get("1.0", tk.END))
        messagebox.showinfo("Success", "Transaction history downloaded successfully.")

if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()
