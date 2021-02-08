import config
from binance.client import Client
import json
from prettytable import PrettyTable
import pprint
import requests

client = Client(config.API_KEY, config.API_SECRET)

info = client.get_account()

t = PrettyTable(['ASSET', 'AMOUNT', 'PRICE', 'VALUE'])

balances = info['balances']

totalBalance = 0

for balance in balances:
    amt = float(balance['free'])
    if amt > 0:

        avgPrice = client.get_avg_price(
            symbol='{}BUSD'.format(balance['asset']))

        value = float(balance['free']) * float(avgPrice['price'])
        totalBalance += value

        t.add_row([balance['asset'], balance['free'], avgPrice['price'], value])

r = requests.get(
    'https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json')
data = r.json()
rate = data['observations'][len(data['observations']) - 1]['FXUSDCAD']['v']

t.add_row(['', '', '', ''])
t.add_row(['', '', 'BUSD', totalBalance])
t.add_row(['', '', 'CAD', totalBalance * float(rate)])

print(t)
