import talib
import numpy
from datetime import date


def RsiBasic(crypto, closePrices):
    # Buy: if RSI < 30
    # Sell: if RSI > 70
    for close in closePrices:
        crypto.addClose(float(close))

        if len(crypto.closes) > crypto.rsiPeriod:
            npCloses = numpy.array(crypto.closes)
            rsi = talib.RSI(npCloses, crypto.rsiPeriod)
            lastRSI = rsi[-1]
            # print("RSI: " + str(lastRSI))

            if lastRSI > crypto.rsiMax and crypto.position:
                crypto.setPosition(False)
                crypto.sell(float(close))
                f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
                f.write("S " + str(close) + " " +
                        str(crypto.balance) + "\n")
                f.close()

            if lastRSI < crypto.rsiMin and not crypto.position:
                crypto.setPosition(True)
                crypto.buy(float(close))
                f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
                f.write("B " + str(close) + " " +
                        str(crypto.balance) + "\n")
                f.close()


def RsiParabolic(crypto, closePrices):
    # Buy: if 1st RSI < 30 & 2nd RSI > 30 (parabola)
    # Sell: if RSI > 70
    for close in closePrices:
        crypto.addClose(float(close))

        if len(crypto.closes) > crypto.rsiPeriod:
            npCloses = numpy.array(crypto.closes)
            rsi = talib.RSI(npCloses, crypto.rsiPeriod)
            lastRSI = rsi[-1]
            # print("RSI: " + str(lastRSI))

            if lastRSI > crypto.rsiMax and crypto.position:
                crypto.setPosition(False)
                crypto.sell(float(close))
                # f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
                # f.write("S " + str(close) + " " +
                #         str(crypto.balance) + "\n")
                # f.close()

            if lastRSI < crypto.rsiMin and not crypto.position:
                crypto.setBelowRsiMin(True)

            if crypto.belowRsiMin and lastRSI > crypto.rsiMin and not crypto.position:
                crypto.setPosition(True)
                crypto.buy(float(close))
                # f = open('./logs/{}_backtest.txt'.format(date.today()), "a+")
                # f.write("B " + str(close) + " " +
                #         str(crypto.balance) + "\n")
                # f.close()