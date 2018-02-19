#!/usr/bin/python
# -*- coding: utf-8 -*-

# bittrex_websocket/examples/ticker_updates.py
# Stanislav Lazarov

# Sample script to show how subscribe_to_ticker_update() works.
# Overview:
#   Creates a custom ticker_updates_container dict through on_open method.
#   Subscribes to N tickers to get their general information.
#   When information is received, checks if the ticker is in ticker_updates_container and adds it if not.
#   Disconnects when it has the information for each ticker.

from __future__ import print_function

from time import sleep

from bittrex_websocket.websocket_client import BittrexSocket

import requests
import json


def main():
    class MySocket(BittrexSocket):
        def __init__(self):
            super(MySocket, self).__init__()
            self.ticker_updates_container = {}

        def on_open(self):
            self.ticker_updates_container = {}

        def notify_slack(self, market, high, low, volume):
            print(str(market) + ': ' + str(high) + ', ' + str(low) + ', ' + str(volume))
            res = requests.post('https://hooks.slack.com/services/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',
                data=json.dumps({
                    'username': 'tickerbot',
                    'icon_emoji': ':female-technologist:',
                    'text': '*' + str(market) + ' report*: :arrow_up_small: :' + '{:.8f}'.format(high) + ' :arrow_down_small: : ' + '{:.8f}'.format(low) + ' :signal_strength: : ' + '{:.8f}'.format(volume),
                }), headers={'Content-Type': 'application/json'})
            if res.status_code != 200:
                print(res.text)

        def on_ticker_update(self, msg):
            name = msg['MarketName']
            if name not in self.ticker_updates_container:
                self.ticker_updates_container[name] = msg
                self.notify_slack(name, msg['High'], msg['Low'], msg['Volume'])

    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log('bittrex-log.log')
    # Define tickers
    tickers = ['BTC-ZCL', 'BTC-ETH', 'BTC-ADA', 'BTC-XLM', 'BTC-QTUM',
               'BTC-ICX', 'BTC-SIA', 'BTC-XMR', 'BTC-DNT']
    # Subscribe to ticker information
    ws.subscribe_to_ticker_update(tickers)

    while True:
        if len(ws.ticker_updates_container) < len(tickers):
            sleep(1)
        else:
            ws.ticker_updates_container = {}
            sleep(60)


if __name__ == "__main__":
    main()
