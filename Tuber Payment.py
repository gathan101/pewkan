import os
from datetime import datetime

# File to store transactions
TRANSACTION_FILE = "transactions.txt"

# Ensure the transactions file exists
if not os.path.exists(TRANSACTION_FILE):
    with open(TRANSACTION_FILE, "w") as f:
        pass  # Create an empty file if it doesn't exist


def make_payment(customer_name: str, amount: float, method: str):
    """
    Record a payment transaction.

    Parameters:
        customer_name (str): Name of the customer.
        amount (float): Payment amount, must be positive.
        method (str): Payment method ("cash" or "Kredit").

    Returns:
        str: Success or error message.
    """
    if amount <= 0:
        return "Error: Payment amount must be positive."

    if method.lower() not in ["cash", "Kredit"]:
        return "Error: Invalid payment method. Use 'cash' or 'Kredit'."

    if not customer_name.strip():
        return "Error: Customer name cannot be empty."

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = f"{date},{customer_name},{amount:.2f},{method}\n"

    try:
        with open(TRANSACTION_FILE, "a") as f:
            f.write(transaction)
        return "Payment recorded successfully."
    except IOError as e:
        return f"Error: Unable to record transaction. {str(e)}"


def view_transactions():
    """
    Display all recorded transactions in chronological order.

    Returns:
        list: A list of transaction records.
    """
    try:
        with open(TRANSACTION_FILE, "r") as f:
            transactions = f.readlines()

        if not transactions:
            print("No transactions found.")
            return []

        print("\nTransaction History:")
        print("Date & Time            | Customer         | Amount (IDR)   | Method")
        print("-" * 70)

        for transaction in transactions:
            # Split line into components and handle missing fields
            parts = transaction.strip().split(",")
            if len(parts) == 4:
                date, customer_name, amount, method = parts
            elif len(parts) == 3:  # Handle old data without `customer_name`
                date, amount, method = parts
                customer_name = "Unknown"
            else:
                print(f"Skipping invalid transaction line: {transaction.strip()}")
                continue

            print(f"{date} | {customer_name:<15} | Rp{float(amount):>10,.2f} | {method.capitalize()}")

        return transactions
    except IOError as e:
        print(f"Error: Unable to read transactions. {str(e)}")
        return []



def generate_report():
    """
    Generate a summary report of transactions.

    Returns:
        str: Summary report.
    """
    try:
        with open(TRANSACTION_FILE, "r") as f:
            transactions = f.readlines()

        if not transactions:
            return "No transactions available for the report."

        total_amount = 0
        transaction_count = 0
        method_summary = {"cash": 0, "Kredit": 0}

        for transaction in transactions:
            _, _, amount, method = transaction.strip().split(",")
            amount = float(amount)
            total_amount += amount
            transaction_count += 1
            method_summary[method] += amount

        report = (
            f"\nSummary Report:\n"
            f"Total Amount Received: Rp{total_amount:,.2f}\n"
            f"Total Transactions: {transaction_count}\n"
            f"Breakdown by Payment Method:\n"
            f"  Cash: Rp{method_summary['cash']:,.2f}\n"
            f"  Kredit: Rp{method_summary['Kredit']:,.2f}\n"
        )
        print(report)
        return report
    except IOError as e:
        return f"Error: Unable to generate report. {str(e)}"


def display_menu():
    """
    Display the menu and handle user choices.
    """
    while True:
        print("\nOffline Payment System (Rupiah)")
        print("1. Make Payment")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                customer_name = input("Enter customer name: ").strip()
                amount = float(input("Enter payment amount (IDR): "))
                method = input("Enter payment method (cash/Kredit): ").lower()
                print(make_payment(customer_name, amount, method))
            except ValueError:
                print("Error: Invalid amount. Please enter a number.")
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the system
if __name__ == "__main__":
    display_menu()
