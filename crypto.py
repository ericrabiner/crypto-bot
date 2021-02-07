class Crypto():
    def __init__(self, rsiMax=70, rsiMin=30, rsiPeriod=14):
        self.balance = 129.02
        self.startBalance = self.balance
        self.position = False
        self.closes = []

        self.rsiPeriod = rsiPeriod
        self.rsiMax = rsiMax
        self.rsiMin = rsiMin

    def buy(self, amount):
        self.balance -= amount

    def sell(self, amount):
        self.balance += amount

    def getBalance(self):
        return self.balance

    def getStartBalance(self):
        return self.startBalance

    def getPosition(self):
        return self.position

    def setPosition(self, newPos):
        self.position = newPos

    def getCloses(self):
        return self.closes

    def addClose(self, newClose):
        if (len(self.closes) > 14):
            self.closes.pop(0)
        self.closes.append(newClose)

    def getRsiPeriod(self):
        return self.rsiPeriod

    def getRsiMax(self):
        return self.rsiMax

    def getRsiMin(self):
        return self.rsiMin
