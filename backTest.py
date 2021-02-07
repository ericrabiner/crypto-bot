import numpy
from prettytable import PrettyTable
from crypto import Crypto
from strategies import RsiBasic, RsiParabolic

# data = numpy.genfromtxt(
#     './historical/2020_01_01-2021-02-07.csv', delimiter=',')

data = numpy.genfromtxt(
    './historical/2020_01_01-2020-02-01.csv', delimiter=',')

closePrices = data[:, 4]

crypto = Crypto()
RsiBasic(crypto, closePrices)
# RsiParabolic(crypto, closePrices)

# If still in position, sell.
if (crypto.position):
    crypto.sell(float(data[len(data) - 1, 4]))

startMarketPrice = data[0, 4]
endMarketPrice = data[len(data) - 1, 4]
marketPercentage = ((endMarketPrice - startMarketPrice) /
                    startMarketPrice) * 100

balancePercentage = ((crypto.balance - crypto.startBalance) /
                     crypto.startBalance) * 100

t = PrettyTable(['', 'Start Price', 'End Price', '%'])
t.add_row(['Market', round(startMarketPrice, 2), round(endMarketPrice, 2),
           (round(marketPercentage, 2))])
t.add_row(['Balance', round(crypto.startBalance, 2), round(crypto.balance, 2),
           (round(balancePercentage, 2))])

print(t)
