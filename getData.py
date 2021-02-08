import config
import csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

candles = client.get_historical_klines(
    "ETHUSDT", Client.KLINE_INTERVAL_5MINUTE, '1 Jan, 2020', '1 Feb, 2020')

csvFile = open('./historical/1month5min.csv', 'w', newline='')

csvWriter = csv.writer(csvFile, delimiter=',')

for candle in candles:
    csvWriter.writerow(candle)
