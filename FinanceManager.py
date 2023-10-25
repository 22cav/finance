class FinanceManager:
    def __init__(self, value):
        self.money = value
        self.transactions = []

    def balance(self):
        return self.money