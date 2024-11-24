import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.balance = 0  # Initial balance
        self.file_name = "expenses.csv"  # File to save transactions

        # Load previous balance from file (if exists)
        self.load_balance()

        # GUI Setup
        self.root = root
        self.root.title("Expense Tracker")

        # Label for Total Amount
        self.total_label = tk.Label(root, text="Total Amount:", font=("Arial", 12))
        self.total_label.grid(row=0, column=0, padx=10, pady=5)

        self.total_entry = tk.Entry(root, width=20, font=("Arial", 12))
        self.total_entry.grid(row=0, column=1, padx=10, pady=5)

        # Button to Set Balance
        self.set_balance_btn = tk.Button(root, text="Set Amount", font=("Arial", 12), command=self.set_balance)
        self.set_balance_btn.grid(row=0, column=2, padx=10, pady=5)

        # Label for Spend Amount
        self.spend_label = tk.Label(root, text="Spent Amount:", font=("Arial", 12))
        self.spend_label.grid(row=1, column=0, padx=10, pady=5)

        self.spend_entry = tk.Entry(root, width=20, font=("Arial", 12))
        self.spend_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to Subtract Spend Amount
        self.spend_btn = tk.Button(root, text="Add Expense", font=("Arial", 12), command=self.add_expense)
        self.spend_btn.grid(row=1, column=2, padx=10, pady=5)

        # Label for Remaining Balance
        self.balance_label = tk.Label(root, text=f"Remaining Balance: ₹{self.balance:.2f}", font=("Arial", 14), fg="green")
        self.balance_label.grid(row=2, column=0, columnspan=3, pady=20)

        # Button to Download CSV
        self.download_btn = tk.Button(root, text="Download Transactions", font=("Arial", 12), command=self.download_file)
        self.download_btn.grid(row=3, column=0, columnspan=3, pady=10)

    def load_balance(self):
        """Load balance and transactions from the file."""
        try:
            with open(self.file_name, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.balance = float(row["Balance"])
        except FileNotFoundError:
            pass  # File doesn't exist yet, start fresh

    def save_transaction(self, transaction_type, amount):
        """Save a transaction to the file with time and date."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_name, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Transaction Type", "Amount", "Balance"])
            if file.tell() == 0:  # If file is empty, write header
                writer.writeheader()
            writer.writerow({"Date": now, "Transaction Type": transaction_type, "Amount": amount, "Balance": self.balance})

    def set_balance(self):
        """Set the total amount."""
        try:
            self.balance = float(self.total_entry.get())
            self.update_balance_label()
            self.save_transaction("Set Amount", self.balance)
            messagebox.showinfo("Success", "Total amount set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def add_expense(self):
        """Subtract spent amount and save the transaction."""
        try:
            spend = float(self.spend_entry.get())
            if spend > self.balance:
                messagebox.showwarning("Warning", "Insufficient balance!")
            else:
                self.balance -= spend
                self.update_balance_label()
                self.save_transaction("Expense", spend)
                messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def update_balance_label(self):
        """Update the balance display."""
        self.balance_label.config(text=f"Remaining Balance: ₹{self.balance:.2f}")

    def download_file(self):
        """Download the CSV file to a chosen location."""
        try:
            dest_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Transactions File"
            )
            if dest_path:
                with open(self.file_name, "r") as source, open(dest_path, "w", newline="") as destination:
                    destination.write(source.read())
                messagebox.showinfo("Success", f"File downloaded to {dest_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not download file: {e}")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

