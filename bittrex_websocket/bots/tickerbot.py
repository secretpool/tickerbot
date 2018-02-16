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

        def on_ticker_update(self, msg):
            name = msg['MarketName']
            if name not in self.ticker_updates_container:
                self.ticker_updates_container[name] = msg
                # Print to slack

        def notify_slack(url, title):
            print(url + ' | ' + title)
            res = requests.post('https://hooks.slack.com/services/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',
                data=json.dumps({
                    'username': 'tickerbot',
                    'icon_emoji': ':moneybag:',
                    'text': '',
                }), headers={'Content-Type': 'application/json'})
            if res.status_code != 200:
                print(res.text)

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
