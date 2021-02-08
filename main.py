import websocket
import json
import talib
import numpy
from datetime import date
# import config
from crypto import Crypto
from strategies import RsiBasic, RsiParabolic

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"


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
            crypto.addClose(float(close))
            RsiBasic(crypto, float(close))

    ws = websocket.WebSocketApp(SOCKET,
                                on_open=onOpen,
                                on_close=onClose,
                                on_message=onMessage)
    ws.run_forever()


if __name__ == "__main__":
    main()
