class Account:
    def __init__(self, owner, balance):
        self.o = owner
        self.b = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        else:
            self.balance -= amount
            return self.balance

B, W = map(int, input().split())
acc = Account("User", B)
result = acc.withdraw(W)
print(result)
