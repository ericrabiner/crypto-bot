import talib
import numpy
from prettytable import PrettyTable
from datetime import date
from crypto import Crypto

data = numpy.genfromtxt(
    './historical/2020_01_01-2021-02-07.csv', delimiter=',')

closePrices = data[:, 4]

crypto = Crypto()

for close in closePrices:
    closes = crypto.getCloses()
    position = crypto.getPosition()
    crypto.addClose(float(close))

    if len(closes) > crypto.getRsiPeriod():
        npCloses = numpy.array(closes)
        rsi = talib.RSI(npCloses, crypto.getRsiPeriod())
        lastRSI = rsi[-1]
        # print("RSI: " + str(lastRSI))

        if lastRSI > crypto.getRsiMax() and position:
            crypto.setPosition(False)
            crypto.sell(float(close))
            # f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
            # f.write("S " + str(close) + " " +
            #         str(crypto.getBalance()) + "\n")
            # f.close()

        if lastRSI < crypto.getRsiMin() and not position:
            crypto.setPosition(True)
            crypto.buy(float(close))
            # f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
            # f.write("B " + str(close) + " " +
            #         str(crypto.getBalance()) + "\n")
            # f.close()

# If still in position, sell.
if (position):
    crypto.sell(float(data[len(data) - 1, 4]))

startMarketPrice = data[0, 4]
endMarketPrice = data[len(data) - 1, 4]
marketPercentage = ((endMarketPrice - startMarketPrice) /
                    startMarketPrice) * 100

balancePercentage = ((crypto.getBalance() - crypto.getStartBalance()) /
                     crypto.getStartBalance()) * 100


t = PrettyTable(['', 'Start Price', 'End Price', '%'])
t.add_row(['Market', round(startMarketPrice, 2), round(endMarketPrice, 2),
           (round(marketPercentage, 2))])
t.add_row(['Balance', round(crypto.getStartBalance(), 2), round(crypto.getBalance(), 2),
           (round(balancePercentage, 2))])

print(t)
