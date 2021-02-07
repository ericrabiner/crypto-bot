import websocket
import json
import pprint
import talib
import numpy
# import config
# from binance.client import Client
# from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
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


class Crypto():
    def __init__(self):
        self.balance = 10000.00
        self.position = False
        self.closes = []

    def buy(self, amount):
        self.balance -= amount

    def sell(self, amount):
        self.balance += amount

    def getBalance(self):
        return self.balance

    def getPosition(self):
        return self.position

    def setPosition(self, newPos):
        self.position = newPos

    def getCloses(self):
        return self.closes

    def append(self, newClose):
        self.closes.append(newClose)


def main():

    crypto = Crypto()

    def onOpen(ws):
        print('opened connection')

    def onClose(ws):
        print('closed connection')

    def onMessage(ws, message):
        # print('received message')

        jsonMessage = json.loads(message)
        # pprint.pprint(jsonMessage)
        candle = jsonMessage['k']
        isCandleClosed = candle['x']
        # isCandleClosed = True
        close = candle['c']

        if isCandleClosed:
            closes = crypto.getCloses()
            position = crypto.getPosition()
            crypto.append(float(close))

            if len(closes) > RSI_PERIOD:
                npCloses = numpy.array(closes)
                rsi = talib.RSI(npCloses, RSI_PERIOD)
                lastRSI = rsi[-1]
                print("RSI: " + str(lastRSI))

                if lastRSI > RSI_OVERBOUGHT and position:
                    crypto.setPosition(False)
                    crypto.sell(float(close))
                    f = open("log2.txt", "a")
                    f.write("S " + close + " " +
                            str(crypto.getBalance()) + "\n")
                    f.close()

                if lastRSI < RSI_OVERSOLD and not position:
                    crypto.setPosition(True)
                    crypto.buy(float(close))
                    f = open("log2.txt", "a")
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
