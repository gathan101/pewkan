import sys
import os

from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
        QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
from datetime import datetime

# File to store transactions
TRANSACTION_FILE = "transactions.txt"

# Ensure the transactions file exists
if not os.path.exists(TRANSACTION_FILE):
    with open(TRANSACTION_FILE, "w") as f:
        pass  # Create an empty file if it doesn't exist


class PaymentSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Payment System")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Fields
        self.customer_name_input = QLineEdit(self)
        self.customer_name_input.setPlaceholderText("Enter customer name")
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount (IDR)")

        # Dropdown for payment method
        self.payment_method_dropdown = QComboBox(self)
        self.payment_method_dropdown.addItems(["Select Method", "Credit Card", "Debit Card"])

        # Buttons
        self.make_payment_button = QPushButton("Make Payment", self)
        self.make_payment_button.clicked.connect(self.make_payment)
        self.view_transactions_button = QPushButton("View Transactions", self)
        self.view_transactions_button.clicked.connect(self.view_transactions)
        self.generate_report_button = QPushButton("Generate Report", self)
        self.generate_report_button.clicked.connect(self.generate_report)

        # Transaction Table
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(4)
        self.transaction_table.setHorizontalHeaderLabels(["Date", "Customer", "Amount (IDR)", "Method"])

        # Layout Setup
        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(self.customer_name_input)
        layout.addWidget(QLabel("Payment Amount (IDR):"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Payment Method:"))
        layout.addWidget(self.payment_method_dropdown)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.make_payment_button)
        button_layout.addWidget(self.view_transactions_button)
        button_layout.addWidget(self.generate_report_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.transaction_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def make_payment(self):
        """
        Handle making a payment.
        """
        customer_name = self.customer_name_input.text().strip()
        amount_text = self.amount_input.text().strip()
        payment_method = self.payment_method_dropdown.currentText().lower()

        if not customer_name:
            QMessageBox.warning(self, "Input Error", "Customer name cannot be empty.")
            return
        if not amount_text or not amount_text.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
            return
        if payment_method not in ["Credit Card", "Debit Card"]:
            QMessageBox.warning(self, "Input Error", "Please select a valid payment method.")
            return

        amount = float(amount_text)
        if amount <= 0:
            QMessageBox.warning(self, "Input Error", "Amount must be greater than zero.")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = f"{date},{customer_name},{amount:.2f},{payment_method}\n"

        try:
            with open(TRANSACTION_FILE, "a") as f:
                f.write(transaction)
            QMessageBox.information(self, "Success", "Payment recorded successfully.")
            self.customer_name_input.clear()
            self.amount_input.clear()
            self.payment_method_dropdown.setCurrentIndex(0)  # Reset dropdown to "Select Method"
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Unable to record transaction: {str(e)}")

    def view_transactions(self):
        """
        Display all recorded transactions in the table.
        """
        self.transaction_table.setRowCount(0)  # Clear existing rows

        try:
            with open(TRANSACTION_FILE, "r") as f:
                transactions = f.readlines()

            if not transactions:
                QMessageBox.information(self, "Info", "No transactions found.")
                return

            for row_index, transaction in enumerate(transactions):
                parts = transaction.strip().split(",")
                if len(parts) == 4:
                    date, customer_name, amount, method = parts
                elif len(parts) == 3:  # Handle old data
                    date, amount, method = parts
                    customer_name = "Unknown"
                else:
                    continue

                self.transaction_table.insertRow(row_index)
                self.transaction_table.setItem(row_index, 0, QTableWidgetItem(date))
                self.transaction_table.setItem(row_index, 1, QTableWidgetItem(customer_name))
                self.transaction_table.setItem(row_index, 2, QTableWidgetItem(f"Rp{float(amount):,.2f}"))
                self.transaction_table.setItem(row_index, 3, QTableWidgetItem(method.capitalize()))
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Unable to read transactions: {str(e)}")

    def generate_report(self):
        """
        Generate a summary report of transactions.
        """
        try:
            with open(TRANSACTION_FILE, "r") as f:
                transactions = f.readlines()

            if not transactions:
                QMessageBox.information(self, "Info", "No transactions available for the report.")
                return

            total_amount = 0
            transaction_count = 0
            method_summary = {"Credit Card": 0, "Debit Card": 0}

            for transaction in transactions:
                parts = transaction.strip().split(",")
                if len(parts) < 3:
                    continue
                _, _, amount, method = parts
                amount = float(amount)
                total_amount += amount
                transaction_count += 1
                method_summary[method] += amount

            report = (
                f"Total Amount Received: Rp{total_amount:,.2f}\n"
                f"Total Transactions: {transaction_count}\n"
                f"Breakdown by Payment Method:\n"
                f"Credit Card: Rp{method_summary['Credit Card']:,.2f}\n"
                f"Debit Card: Rp{method_summary['Debit Card']:,.2f}\n"
            )
            QMessageBox.information(self, "Report", report)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Unable to generate report: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaymentSystem()
    window.show()
    sys.exit(app.exec_())
