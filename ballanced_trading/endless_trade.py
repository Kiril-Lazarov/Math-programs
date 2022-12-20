from ballanced_trading.constant_profit_strategy import Bitcoin, Busd, General
import time
from collections import deque

from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)
buffer = General()

class ThisStrategy():
    def check_price(self, asset):
        if asset == 'BTC':
            if curr_price >= btc.next_price:
                this.execute_order('BTC', curr_price)
        elif asset == 'BUSD':
            this.execute_order('BUSD', curr_price)

    def execute_order(self, asset, curr_price):
        pass

number_trades = 10
price_percentage = 1.001
profit_percentage = 1.0015
transaction_count = 0
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
this = ThisStrategy()
initial_btc = 0.02651
initial_busd = 844
init_btc_overall_qty = buffer.calculate_overall('BTC', ground_price)
init_busd_overall_qty = buffer.calculate_overall('BUSD', ground_price)
btc = Bitcoin(init_btc_overall_qty, buffer.create_new_price('BTC', ground_price))
busd = Busd(0, buffer.create_new_price('BUSD', ground_price))
asset = 'BTC'
while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    # curr_price = float(input('Въведи цена: '))
    if btc.btc_trades_count == number_trades:
        asset = 'BUSD'
    if busd.busd_trades_count == number_trades:
        asset = 'BTC'

