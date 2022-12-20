import time

from binance.client import Client

import carrusel3.methods
from carrusel3.asset import Asset
from carrusel3.methods import Methods

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)
method = Methods
price_busd_eth = float(client.get_symbol_ticker(symbol='ETHBUSD')['price'])
price_busd_btc = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])

eth = Asset(500 / price_busd_eth, 0, 'ETH', 0)
btc = Asset(500 / price_busd_btc, 0, 'BTC', 0)
busd = Asset(500, 500, 'BUSD', 2)
print(repr(eth))
print(repr(btc))
print(repr(busd))

objects = [eth, btc, busd]
pairs = ['ETHBTC', 'ETHBUSD', 'BTCBUSD']
profit_percentage = 1.001
transaction_count = 1

while True:
    for obj in objects:
        if obj.number == 2:
            print('\n-----------РАЗДЕЛЯНЕ-----------')
            method.split(obj, objects, transaction_count)
            transaction_count +=2
        else:
            if obj.number == 1:
                if method.check_for_profit(obj, objects, profit_percentage, transaction_count):
                    transaction_count += 1
    time.sleep(5)
