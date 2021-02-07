import websocket
import json
import pprint
import talib
import numpy
from datetime import date
# import config
# from binance.client import Client
# from binance.enums import *
from crypto import Crypto

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

# TRADE_SYMBOL = 'ETHUSD'
# TRADE_QUANTITY = 0.05

# client = Client(config.API_KEY, config.API_SECRET, tld='us')

# def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         # order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False

#     return True


def main():

    crypto = Crypto(60, 40)

    def onOpen(ws):
        print('opened connection')

    def onClose(ws):
        print('closed connection')

    def onMessage(ws, message):
        # print('received message')

        jsonMessage = json.loads(message)
        candle = jsonMessage['k']
        isCandleClosed = candle['x']
        close = candle['c']

        if isCandleClosed:
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
                    f = open('./logs/{}.txt'.format(date.today()), "a+")
                    f.write("S " + close + " " +
                            str(crypto.getBalance()) + "\n")
                    f.close()

                if lastRSI < crypto.getRsiMin() and not position:
                    crypto.setPosition(True)
                    crypto.buy(float(close))
                    f = open('./logs/{}.txt'.format(date.today()), "a+")
                    f.write("B " + close + " " +
                            str(crypto.getBalance()) + "\n")
                    f.close()

    ws = websocket.WebSocketApp(SOCKET,
                                on_open=onOpen,
                                on_close=onClose,
                                on_message=onMessage)
    ws.run_forever()


if __name__ == "__main__":
    main()
