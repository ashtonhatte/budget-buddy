"""
Author: Ashton Hatte
Date written: 9/24/2024
Assignment: Python Tkinter GUI Application Project
Description: Program creates a simple budgeting application with categories and a transaction history page.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class Budget_Buddy:
    """A simple budgeting application"""
    def __init__(self, root):
        """Initialize Window and Global Variables"""
        # Create window and title
        self.root = root
        self.root.title("Budget Buddy")
        self.root.resizable(False, False)

        # Category Variables
        self.transaction_type = tk.StringVar(value=None) # set default transaction type to None (fills both radio at first)
        self.income_categories = ["Salary", "Investments"] 
        self.expense_categories = ["Bills", "Food", "Entertainment"]
        self.total = 0
        self.transactions_list = [] # list for transaction storage

        # Begin button creation and set default selections with update
        self.create_buttons()
        self.update_categories()

    def create_buttons(self):
        """Welcome to the button factory, also includes input field for $"""
        self.income_radio = tk.Radiobutton(self.root, text="Income", variable=self.transaction_type, value="Income", command=self.update_categories)
        self.income_radio.grid(row=0, column=0, padx=5, pady=5)

        self.expense_radio = tk.Radiobutton(self.root, text="Expense", variable=self.transaction_type, value="Expense", command=self.update_categories)
        self.expense_radio.grid(row=0, column=1, padx=5, pady=5)

        self.category_label = tk.Label(self.root, text="Select Category:")
        self.category_label.grid(row=1, columnspan=2)

        self.category_combobox = ttk.Combobox(self.root, state="readonly") # set field to readonly, no typing needed
        self.category_combobox.grid(row=2, columnspan=2, pady=5)

        self.amount_label = tk.Label(self.root, text="Enter Amount ($):")
        self.amount_label.grid(row=3, column=0)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=3, column=1)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_entry)
        self.submit_button.grid(row=4, columnspan=2, pady=5)

        self.summary_label = tk.Label(self.root, text="")
        self.summary_label.grid(row=5, columnspan=2)

        self.total_label = tk.Label(self.root, text="Total Finances: $0")
        self.total_label.grid(row=6, columnspan=2)

        self.view_transactions_button = tk.Button(self.root, text="View Transaction History", command=self.open_transaction_window)
        self.view_transactions_button.grid(row=7, columnspan=2)

    def update_categories(self):
        """Handler for when 'Income' or 'Expense' radio-buttons are selected, changes available categories in dropdown menu"""
        selected_type = self.transaction_type.get()
        if selected_type == "Income":
            self.category_combobox['values'] = self.income_categories
        elif selected_type == "Expense":
            self.category_combobox['values'] = self.expense_categories

    def submit_entry(self):
        """Handler for 'Submit' button is used after all user info is filled"""
        # Get variable values
        transaction_type = self.transaction_type.get()
        category = self.category_combobox.get()
        amount = self.amount_entry.get()

        # Check if all fields have been filled. If not, popout message
        if not category or not amount:
            tkinter.messagebox.showinfo("Error", "Please select a category and enter an amount.") # (Title, Message)
        else:
            amount = float(amount) # convert input to float for computing
            self.transactions_list.append((transaction_type, category, amount)) # add transaction to running list
            if transaction_type == "Income":
                self.total += amount
            else:
                self.total -= amount # subtract if income is not selected
            self.summary_label.config(text=f"{transaction_type} - {category}: ${amount}") # show summary of recent transaction

            if self.total < 0:
                self.total_label.config(text=f"Total Finances: ${self.total:.2f}", background="red") # turn background red if negative
            else:
                self.total_label.config(text=f"Total Finances: ${self.total:.2f}", background="green") # remain green if positive

    def open_transaction_window(self):
        """Handler for when 'View Transaction History' button is pressed"""
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transaction History")

        ###STOPPING POINT###
        # need loop for writing transaction to new page 
            
if __name__ == "__main__":
    root = tk.Tk()
    app = Budget_Buddy(root)
    root.mainloop()
# End of Program
