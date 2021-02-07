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

        self.binanceFee = 0.001
        self.numTrades = 0
        self.tradeCost = 0

    def buy(self, amount):
        self.balance -= amount
        self.numTrades += 1
        self.tradeCost += amount * self.binanceFee

    def sell(self, amount):
        self.balance += amount
        self.numTrades += 1
        self.tradeCost += amount * self.binanceFee

    def setPosition(self, newPos):
        self.position = newPos

    def addClose(self, newClose):
        if (len(self.closes) > 14):
            self.closes.pop(0)
        self.closes.append(newClose)

    def setBelowRsiMin(self, newBelow):
        self.belowRsiMin = newBelow
