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
        self.transaction_type = tk.StringVar(value="Income") # set default transaction type to Income so category dropdown is populated
        self.income_categories = ["Salary", "Investments", "Miscellaneous"] 
        self.expense_categories = ["Bills", "Food", "Entertainment"]
        self.total = 0
        self.transactions_list = [] # list for transaction storage

        # Begin button creation and set default selections with update
        self.create_buttons()
        self.add_images() # add images or alt text if not found
        self.update_categories() # sets first dropdown set on app start

    def create_buttons(self):
        """Welcome to the button factory, also includes input field for $"""
        self.income_radio = tk.Radiobutton(self.root, text="Income", variable=self.transaction_type, value="Income", command=self.update_categories)
        self.income_radio.grid(row=1, column=0, padx=5, pady=5)

        self.expense_radio = tk.Radiobutton(self.root, text="Expense", variable=self.transaction_type, value="Expense", command=self.update_categories)
        self.expense_radio.grid(row=1, column=1, padx=5, pady=5)

        self.category_label = tk.Label(self.root, text="Select Category:")
        self.category_label.grid(row=2, columnspan=2)

        self.category_combobox = ttk.Combobox(self.root, state="readonly") # set field to readonly, no typing needed
        self.category_combobox.grid(row=3, columnspan=2, pady=5)

        self.amount_label = tk.Label(self.root, text="Enter Amount ($):")
        self.amount_label.grid(row=4, column=0)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=4, column=1)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_entry)
        self.submit_button.grid(row=5, columnspan=2, pady=5)

        self.summary_label = tk.Label(self.root, text="")
        self.summary_label.grid(row=6, columnspan=2)

        self.total_label = tk.Label(self.root, text="Total Finances: $0")
        self.total_label.grid(row=7, columnspan=2)

        self.view_transactions_button = tk.Button(self.root, text="View Transaction History", command=self.open_transaction_window)
        self.view_transactions_button.grid(row=8, columnspan=2)
    
    def add_images(self):
        """Adds image to main window, alternate text if not found"""
        try:
            self.image_main = tk.PhotoImage(file="budgetbuddylogo.png")
        except Exception as i:
            print(f"Error loading logo image: {i}") # display logo image error
            self.image_main = None # set to none

        # Labels for images and alt text
        self.image_main_label = tk.Label(self.root, image=self.image_main, compound="center") # set label as image

        if self.image_main:
            self.image_main_label.grid(row=0, columnspan=2, pady=5) # image placement
        else:
            self.image_main_label.config(text="[Image: Budget Buddy Logo]") # alt text
            self.image_main_label.grid(row=0, columnspan=2, pady=5) # placement

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
        
        # Clear input fields
        self.amount_entry.delete(0, tk.END) # clears entry field, (start, end)
        self.category_combobox.set("") # resets category field

        # Check if all fields have been filled. If not, popout message
        if not category or not amount:
            tkinter.messagebox.showerror("Error", "Please select a category and enter an amount.") # (Title, Message)
        else:
            try:
                amount = float(amount) # convert input to float for computing
                if amount < 0: # check for negative input
                    tkinter.messagebox.showerror("Error", "Please enter a positive dollar amount. (Select Expense if not Income)")
                    return
            except ValueError:
                tkinter.messagebox.showerror("Error", "Please enter a numeric amount.")
                return
            self.transactions_list.append((transaction_type, category, amount)) # add transaction to running list
            if transaction_type == "Income":
                self.total += amount
            else:
                self.total -= amount # subtract if income is not selected
            self.summary_label.config(text=f"{transaction_type} - {category}: ${amount}") # show summary of recent transaction
            
            # Color logic for running total 
            if self.total < 0:
                self.total_label.config(text=f"Total Finances: ${self.total:.2f}", background="red") # turn background red if negative
            elif self.total > 0:
                self.total_label.config(text=f"Total Finances: ${self.total:.2f}", background="green") # remain green if positive
            else:
                self.total_label.config(text=f"Total Finances: ${self.total:.2f}", background="yellow") # turn yellow if recently hitting zero

    def open_transaction_window(self):
        """Handler for when 'View Transaction History' button is pressed"""
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transaction History")

        # try load image 
        try:
            self.image_search = tk.PhotoImage(file="search.png") 
        except Exception as i:
            print(f"Error loading transaction history image: {i}")
            self.image_search = None # set to none

        # Create frame for image and title
        frame = tk.Frame(transactions_window) # add frame to window
        frame.pack(pady=5)

        # Create label for title
        history_label = tk.Label(frame, text="Viewing History", padx=10) # add label to frame
        history_label.pack(side=tk.LEFT) # align title to the left of image

        # Create an image label for window
        self.image_search_label = tk.Label(frame, image=self.image_search, compound="center")
        if self.image_search:
            self.image_search_label.pack(side=tk.LEFT)  # add to the left of title
        else:
            self.image_search_label.config(text="[Image: Search icon]") # alt text
            self.image_search_label.pack(side=tk.LEFT) 

        # Define category colors
        category_colors = {
            "Salary" : "#DFF2BF",          # light green
            "Investments" : "#498AE3",     # light blue 
            "Miscellaneous" : "#177F75",   # blue-green
            "Bills" : "#E58A9B",           # Monopoly Bill Pink
            "Food" : "#FFBF7E",            # light orange
            "Entertainment" : "#d19ff3",   # light purple
        }

        for index, (transaction_type, category, amount) in enumerate(self.transactions_list): # enumerate "numbers" the transactions in the list, creating tuples
            background_color = category_colors.get(category, "#FFFFFF") # get color for current category, default is white
            transaction_text = f"{index + 1}: {transaction_type} - {category}: ${amount}" # setup for transaction layout and add +1 to index since start zero
            transaction_label = tk.Label(transactions_window, text=transaction_text, anchor="w", justify="left", bg = background_color) # align to left side of window, assign color
            transaction_label.pack(fill="x", padx=5, pady=2) # fills out width of window
            
if __name__ == "__main__":
    root = tk.Tk()
    app = Budget_Buddy(root)
    root.mainloop()
# End of Program