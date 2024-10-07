"""Welcome to the testing grounds, put into seperate file for organization"""

import tkinter as tk
from budgetbuddy import Budget_Buddy # imports Budget_Buddy class

# Testing Data kinda works
test_transactions = [ 
    {"transaction_type": None, "category": "Salary", "amount": 5000},            # test for transaction_type     # Fail
    {"transaction_type": "Income", "category": "***TEST***", "amount": 500},     # test for category             # Fail
    {"transaction_type": "Income", "category": "", "amount": 500},               # test two for category         # PASS
    {"transaction_type": "Expense", "category": "Bills", "amount": -500},        # test for negative amount      # PASS
    {"transaction_type": "Expense", "category": "Food", "amount": "250.00"},     # test for non-integer          # Expected
    {"transaction_type": "Income", "category": "Miscellaneous", "amount": "a"},  # test two for non-integer      # PASS
    {"transaction_type": "Expense", "category": "Entertainment", "amount": ""},  # test for no input             # PASS

    {"transaction_type": "Income", "category": "Salary", "amount": 5000},        # normal transaction
    {"transaction_type": "Expense", "category": "Bills", "amount": 500.00},      # input as float
]

# Function to simulate transactions
def simulate_transactions(app):
    for transaction in test_transactions:
        app.transaction_type.set(transaction["transaction_type"])       # Set the transaction type
        app.category_combobox.set(transaction["category"])              # Set the category
        app.amount_entry.delete(0, tk.END)                              # Clear the entry field
        app.amount_entry.insert(0, str(transaction["amount"]))          # Enter the amount
        app.submit_entry()                                              # Submit the entry

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = Budget_Buddy(root)
    simulate_transactions(app)  # Run simulation
    root.mainloop()
# End of Testing

"""Lots of manual testing took place"""
# validate transaction type is selected (forces income default)
# validate category is selected (pushes error message if transaction type and category are not both selected)
# validate $ input (only accepts numerical values, error message otherwise)
# validate input is always positive (error message if negative, suggest expense)