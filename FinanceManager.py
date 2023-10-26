import pandas as pd
import datetime

class FinanceManager:

    def __init__(self, value=0, filepath=None):
        self.balance = value
        self.columns = ['amount', 'date', 'description', 'new_balance']
        self.transactions = pd.DataFrame(columns=self.columns)
        self.filepath = filepath
        self.budget = None

    def Initialize_empty_file(self, name, amount):
        # Create a file in the Saved Balances folder
        file_name = F"Saved Balances/{name}.txt"
        self.balance = amount
        with open(file_name, "x") as f:
            # In the first line of the file, write the amount of money available
            f.write(f"amount:{amount} \n")
            # In the second line, write the transaction history
            f.write("transactions:\n")
            # In the third line, write the budget division
            f.write("budgets:\n")
        self.add_transaction(0, datetime.datetime.now(), 'Initial Balance')

    def Load_file(self):
        name = self.filepath
        # Create a file in the Saved Balances folder
        file_name = f"Saved Balances/{name}"
        with open(file_name, "r") as f:
            # In the first line of the file, write the amount of money available
            self.balance = float(f.readline().split("amount:")[1].removesuffix("\n"))
            # In the second line, write the transaction history
            transactions = f.readline().split("transactions:")[1].removesuffix("\n").split(" | ")
            self.load_transactions(transactions)
            # In the third line, write the budget division
            self.budget = f.readline().split(":")[1].removesuffix("\n")
    
    def load_transactions(self, transactions):
        for transaction in transactions:
            transaction = transaction.strip()
            if transaction=='':
                continue
            transaction = transaction.split(',')
            self.add_transaction(int(transaction[0]), transaction[1], transaction[2])

    def get_balance(self):
        return self.balance
    
    def return_n_transactions(self, n):
        return self.transactions.tail(n)
    
    def return_n_balances(self, n):
        return self.transactions.tail(n)['new_balance'].tolist()
    
    def remove_last_transaction(self):
        self.balance -= self.transactions.tail(1)['amount'].tolist()[0]
        self.transactions = self.transactions.drop(self.transactions.tail(1).index)

    def add_negative_transaction(self, amount, date, description):
        self.add_transaction(-amount, date, description)
    
    def add_transaction(self, amount, date, description):
        self.balance += float(amount)
        new_transaction = pd.DataFrame(data=[[amount, date, description, self.balance]], columns=self.columns)
        self.transactions = pd.concat([self.transactions.dropna(), new_transaction.dropna()], ignore_index=True, axis=0)
        self.save_transaction((amount, date, description, self.balance))

    def save_transaction(self, transaction):
        with open(f"Saved Balances/{self.filepath}", 'r') as f:
            lines = f.readlines()        
            # Find the index of the line that says "transactions:"
        transaction_index = None
        for i, line in enumerate(lines):
            if line.startswith("transactions:"):
                transaction_index = i
                break        
        # Modify the line with the new transaction
        if transaction_index is not None:
            lines[0] = f"amount: {self.balance}\n"
            #remove the newline character from the end of the line
            lines[transaction_index] = lines[transaction_index].replace('\n', '')
            lines[transaction_index] = lines[transaction_index] + f" | {transaction[0]},{transaction[1]},{transaction[2]},{transaction[3]}\n"
        # Write the modified contents back to the file
        with open(f"Saved Balances/{self.filepath}", 'w') as f:
            f.writelines(lines)
            
# test the save function

fm = FinanceManager(100, filepath='ewew.txt')
fm.add_transaction(10, datetime.datetime.now(), 'test')
fm.add_transaction(10, datetime.datetime.now(), 'test')