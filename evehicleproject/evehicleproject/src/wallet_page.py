import tkinter as tk
from tkinter import ttk

class WalletPage:
    def __init__(self, root):
        self.root = root
        self.root.title('Wallet Page')
        
        # self.root.geometry('600x600')
        # self.root.configure(bg='white')

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.wallet_frame = tk.LabelFrame(self.frame, text='Wallet Info',padx=10,pady=10)
        self.wallet_frame.grid(row=0,column=0,sticky='news')
        self.wallet_balance = 0.00

        # Create a custom style for the labels and buttons with black foreground
        style = ttk.Style()
        style.configure('TButton', foreground='black', background='white')
        style.configure('TLabel', foreground='black', background='white')

        self.user_label = ttk.Label(self.wallet_frame, text=f'Hello user...', style='TLabel')
        self.user_label.grid(row=0,column=0)

        # Wallet balance label
        self.balance_label = ttk.Label(self.wallet_frame, text=f'Wallet Balance: £{self.wallet_balance:.2f}', style='TLabel')
        self.balance_label.grid(row=1,column=0)

        # Add funds button
        self.add_funds_button = ttk.Button(self.wallet_frame, text='Add Funds', command=self.open_add_funds_page, style='TButton',width=40)
        self.add_funds_button.grid(row=2,column=0,sticky='news')


        self.transaction_frame = tk.LabelFrame(self.frame, text= 'Previous Transactions: ', padx=10, pady=10)
        self.transaction_frame.grid(row=1,column=0,sticky='news')

        # Listbox to display last 3 transactions with padding
        self.transaction_list = tk.Listbox(self.transaction_frame,width=40, height=3)
        self.transaction_list.pack()

        # Add sample transactions
        self.transaction_list.insert(0, "Transaction 1: -£50")
        self.transaction_list.insert(1, "Transaction 2: +£10")
        self.transaction_list.insert(2, "Transaction 3: -£30")

    def open_add_funds_page(self):
        self.add_funds_window = tk.Toplevel(self.root)
        self.add_funds_window.title('Add Funds')

        # Create widgets for the Add Funds page
        add_funds_label = ttk.Label(self.add_funds_window, text='Enter Amount')
        add_funds_label.pack()

        add_funds_entry = ttk.Entry(self.add_funds_window)
        add_funds_entry.pack()

        add_funds_button = ttk.Button(self.add_funds_window, text='Add Funds', command=lambda: self.add_funds(add_funds_entry), style='TButton')
        add_funds_button.pack()

        add_funds_result_label = ttk.Label(self.add_funds_window, text='')
        add_funds_result_label.pack()

    def add_funds(self, entry_widget):
        try:
            amount = float(entry_widget.get())
            self.wallet_balance += amount
            self.update_wallet_balance()
            entry_widget.delete(0, 'end')
            self.add_funds_window.destroy()
        except ValueError:
            # Handle invalid input
            pass

    def update_wallet_balance(self):
        self.balance_label.config(text=f'Wallet Balance: £{self.wallet_balance:.2f}')
    def run(self):
        self.root.mainloop()

# # if __name__ == '__main__':
#     root = tk.Tk()
#     wallet_page = WalletPage(root)
#     root.mainloop()
