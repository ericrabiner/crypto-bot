import talib
import numpy
from datetime import date
from crypto import Crypto

data = numpy.genfromtxt(
    './historical/2020_01_01-2021-07-02.csv', delimiter=',')

closePrices = data[:, 4]

crypto = Crypto()

for close in closePrices:
    closes = crypto.getCloses()
    position = crypto.getPosition()
    crypto.append(float(close))

    if len(closes) > crypto.getRsiPeriod():
        npCloses = numpy.array(closes)
        rsi = talib.RSI(npCloses, crypto.getRsiPeriod())
        lastRSI = rsi[-1]
        print("RSI: " + str(lastRSI))

        if lastRSI > crypto.getRsiMax() and position:
            crypto.setPosition(False)
            crypto.sell(float(close))
            f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
            f.write("S " + str(close) + " " +
                    str(crypto.getBalance()) + "\n")
            f.close()

        if lastRSI < crypto.getRsiMin() and not position:
            crypto.setPosition(True)
            crypto.buy(float(close))
            f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
            f.write("B " + str(close) + " " +
                    str(crypto.getBalance()) + "\n")
            f.close()
