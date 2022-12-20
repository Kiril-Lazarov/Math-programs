import time

from binance.client import Client
api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

eur_usdt_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
btc_eur_price = float(client.get_symbol_ticker(symbol='BTCEUR')['price'])
eur_qty = 100
usdt_qty = eur_qty * eur_usdt_price
btc_qty = eur_qty / btc_usdt_price
eur_init = 300
usdt_init = usdt_qty + eur_qty * eur_usdt_price + btc_qty * btc_usdt_price
btc_init = btc_qty + eur_qty / btc_eur_price + usdt_qty / btc_usdt_price
print(f'Начален USDT: {usdt_qty:.2f}\nНачален BTC: {btc_qty:.5f}\nНачален EUR: {eur_qty:.2f}')
print(f'USDT init: {usdt_init:.2f}\nBTC init: {btc_init:.5f}\nEUR init: {eur_init:.2f}')

while True:
    eur_usdt_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
    btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    btc_eur_price =  float(client.get_symbol_ticker(symbol='BTCEUR')['price'])
    curr_usdt =  usdt_qty + eur_qty * eur_usdt_price + btc_qty * btc_usdt_price
    curr_btc = btc_qty + eur_qty / btc_eur_price + usdt_qty / eur_usdt_price
    curr_eur= eur_qty + usdt_qty/ eur_usdt_price + btc_qty * btc_eur_price
    print('------------------------')
    print(f'USDT Печалба: {(curr_usdt / usdt_init - 1) * 100:.2f}%\n'
          f'BTC Печалба: {(curr_btc / btc_init - 1) * 100:.2f}%\n'
          f'EUR Печалба: {(curr_eur/ eur_init - 1) * 100:2f}%')
    print(f'BTCEUR: {btc_eur_price} EURUSDT: {eur_usdt_price} BTCUSDT: {btc_usdt_price} ')

    time.sleep(300)