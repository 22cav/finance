import pandas as pd

class FinanceManager:
    def __init__(self, value):
        self.balance = value
        self.columns = ['amount', 'date', 'description', 'new_balance']
        self.transactions = pd.DataFrame(columns=self.columns)

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
        self.balance += amount
        new_balance = self.balance
        self.transactions = pd.concat([self.transactions, pd.DataFrame(data=[[amount, date, description, new_balance]], columns=self.columns)], ignore_index=True)


s = FinanceManager(100)
s.add_transaction(-10, '2019-01-01', 'test')
s.add_transaction(-10, '2019-01-01', 'test')
print(s.return_n_transactions(2))


