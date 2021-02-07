class Crypto():
    def __init__(self, rsiMax=70, rsiMin=30, rsiPeriod=14):
        self.balance = 129.02
        self.startBalance = self.balance
        self.position = False
        self.closes = []
        self.belowRsiMin = False

        self.rsiPeriod = rsiPeriod
        self.rsiMax = rsiMax
        self.rsiMin = rsiMin

    def buy(self, amount):
        self.balance -= amount

    def sell(self, amount):
        self.balance += amount

    def setPosition(self, newPos):
        self.position = newPos

    def addClose(self, newClose):
        if (len(self.closes) > 14):
            self.closes.pop(0)
        self.closes.append(newClose)

    def setBelowRsiMin(self, newBelow):
        self.belowRsiMin = newBelow
