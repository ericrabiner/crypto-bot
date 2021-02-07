import numpy
from prettytable import PrettyTable
from crypto import Crypto
from strategies import RsiBasic, RsiParabolic


def calcGain(start, end):
    return ((end - start) / start) * 100


# data = numpy.genfromtxt(
#     './historical/2020_01_01-2021-02-07.csv', delimiter=',')

data = numpy.genfromtxt(
    './historical/2020_01_01-2020-02-01.csv', delimiter=',')

closePrices = data[:, 4]

crypto = Crypto()
for close in closePrices:
    crypto.addClose(float(close))
    RsiBasic(crypto, close)
    # RsiParabolic(crypto, close)


# If still in position, sell.
if (crypto.position):
    crypto.sell(float(data[len(data) - 1, 4]))

startMarketPrice = data[0, 4]
endMarketPrice = data[len(data) - 1, 4]
marketPercentage = calcGain(startMarketPrice, endMarketPrice)
balancePercentage = calcGain(crypto.startBalance, crypto.balance)


t = PrettyTable(['', 'Start Price', 'End Price', '%'])
t.add_row(['Market', round(startMarketPrice, 2), round(endMarketPrice, 2),
           (round(marketPercentage, 2))])
t.add_row(['Balance', round(crypto.startBalance, 2), round(crypto.balance, 2),
           (round(balancePercentage, 2))])
t.add_row(['', '', '', ''])
t.add_row(['', 'Num Trades', 'Cost', ''])
t.add_row(['', crypto.numTrades, crypto.tradeCost, ''])
t.add_row(['', '', '', ''])
balanceWithFees = round(crypto.balance, 2) - round(crypto.tradeCost, 2)
t.add_row(['Balance', '', balanceWithFees, round(
    calcGain(crypto.startBalance, balanceWithFees), 2)])

print(t)
