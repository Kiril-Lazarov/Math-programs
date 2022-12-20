from binance.client import Client
import time
from matplotlib import pyplot as plt

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

price_summation = 0
start = time.time()
counter  = 0
while True:
    counter +=1
    price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    price_summation += price
    end = time.time()

    if end - start >= 60:
        price_summation /= counter
        print(counter)
        break
print(price_summation)
