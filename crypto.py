class Crypto():
    def __init__(self):
        self.balance = 10000.00
        self.position = False
        self.closes = []

    def buy(self, amount):
        self.balance -= amount

    def sell(self, amount):
        self.balance += amount

    def getBalance(self):
        return self.balance

    def getPosition(self):
        return self.position

    def setPosition(self, newPos):
        self.position = newPos

    def getCloses(self):
        return self.closes

    def append(self, newClose):
        self.closes.append(newClose)
