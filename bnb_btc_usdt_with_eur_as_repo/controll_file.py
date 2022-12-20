import time

from binance.client import Client
from binance.enums import *

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

def get_prices():
    bnb_usdt_price = float(client.get_symbol_ticker(symbol='BNBUSDT')['price'])
    bnb_btc_price = float(client.get_symbol_ticker(symbol='BNBBTC')['price'])
    btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    return bnb_usdt_price, bnb_btc_price, btc_usdt_price

def get_euro_prices():
    eur_usdt_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
    btc_eur_price = float(client.get_symbol_ticker(symbol='BTCEUR')['price'])
    bnb_eur_price = float(client.get_symbol_ticker(symbol='BNBEUR')['price'])
    return eur_usdt_price, btc_eur_price, bnb_eur_price

def get_curr_quantities(usdt_qty, btc_qty, bnb_qty):
    curr_usdt = usdt_qty + btc_qty * btc_usdt_price + bnb_qty * bnb_usdt_price
    curr_btc = btc_qty + usdt_qty / btc_usdt_price + bnb_qty * bnb_btc_price
    curr_bnb = bnb_qty + btc_qty / bnb_btc_price + usdt_qty / bnb_usdt_price
    return curr_usdt, curr_btc, curr_bnb

def calc_profits(curr_usdt, curr_btc, curr_bnb):
    usdt_profit = (curr_usdt/ usdt_base - 1) * 100
    btc_profit = (curr_btc/ btc_base - 1) * 100
    bnb_profit = (curr_bnb/ bnb_base - 1) * 100
    return usdt_profit, btc_profit, bnb_profit



bnb_usdt_price, bnb_btc_price, btc_usdt_price = get_prices()
eur_usdt_price, btc_eur_price, bnb_eur_price = get_euro_prices()

eur_repo = 0

eur_init = 1200
eur_base = 1200
usdt_qty = eur_init / 3 * eur_usdt_price
btc_qty = eur_init/ 3 / btc_eur_price
bnb_qty =  eur_init/ 3 / bnb_eur_price

usdt_base, btc_base, bnb_base = get_curr_quantities(usdt_qty, btc_qty, bnb_qty)

level = 0.1
# eur_profit_level = 0.5
print(f'USDT: {usdt_qty:.2f}\nBTC: {btc_qty:.5f}\nBNB: {bnb_qty:.3f}\nUSDT base: {usdt_base:.2f}\n'
      f'BTC base: {btc_base:.5f}\nBNB base: {bnb_base:.3f}')




is_profit = False


def get_total_eur():
    total = eur_repo + btc_qty * btc_eur_price + bnb_qty * bnb_eur_price + usdt_qty/ eur_usdt_price
    total_profit_base = (total/eur_base - 1) * 100
    total_profit_init = (total/ eur_init - 1) * 100
    return f'Количество EUR: {total:.2f}\nПечалба спрямо base: {total_profit_base:.2f}%\n' \
           f'Печалба спрямо init: {total_profit_init:.2f}%',total, total_profit_base

start = time.time()
while True:
    end = time.time()
    eur_usdt_price, btc_eur_price, bnb_eur_price = get_euro_prices()
    bnb_usdt_price, bnb_btc_price, btc_usdt_price = get_prices()
    curr_usdt, curr_btc, curr_bnb =  get_curr_quantities(usdt_qty, btc_qty, bnb_qty)
    usdt_profit, btc_profit, bnb_profit = calc_profits(curr_usdt, curr_btc, curr_bnb)
    a, total_eur, eur_profit = get_total_eur()
    if eur_profit >= level:
        print(f'-----------EUR ПЕЧАЛБА------------\nTotal EUR: {total_eur:.2f}\nEUR profit: {eur_profit:.2f}%')
        usdt_qty = total_eur / 3 * eur_usdt_price
        btc_qty = total_eur / 3 / btc_eur_price
        bnb_qty = total_eur / 3 / bnb_eur_price
        # usdt_base, btc_base, bnb_base = get_curr_quantities(usdt_qty, btc_qty, bnb_qty)
        eur_repo = 0
        eur_base = total_eur
        print(f'USDT: {usdt_qty:.2f}\nBTC: {btc_qty:.5f}\nBNB: {bnb_qty:.3f}\nUSDT base: {usdt_base:.2f}\n'
              f'BTC base: {btc_base:.5f}\nBNB base: {bnb_base:.3f}\n-------------------')
    if usdt_profit >= level:
        is_profit = True
        total_usdt = usdt_qty + btc_qty * btc_usdt_price + bnb_qty * bnb_usdt_price
        # diff = total_usdt - usdt_base
        # result = diff / eur_usdt_price
        # eur_repo += result
        usdt_base = total_usdt
        print(f'------------ПЕЧАЛБА--------------\nTotal USDT: {total_usdt:.2f}')
        # print(f'Печалба в USDT: {diff:.2f}\nПечалба в EUR: {result:.2f}')
        usdt_qty = usdt_base / 3
        btc_qty = usdt_qty/btc_usdt_price
        bnb_qty = usdt_qty/ bnb_usdt_price
        # usdt_base, btc_base, bnb_base = get_curr_quantities(usdt_qty, btc_qty, bnb_qty)
    if btc_profit >= level:
        is_profit = True
        total_btc = btc_qty + usdt_qty / btc_usdt_price + bnb_qty * bnb_btc_price
        # diff = total_btc - btc_base
        # result = diff * btc_eur_price
        print(f'------------ПЕЧАЛБА--------------\nTotal BTC: {total_btc:.2f}')
        # print(f'Печалба в BTC: {diff:.5f}\nПечалба в EUR: {result:.2f}')
        # eur_repo += result
        btc_base = total_btc
        btc_qty = btc_base /3
        usdt_qty = btc_qty* btc_usdt_price
        bnb_qty = btc_qty / bnb_btc_price

    if bnb_profit >= level:
        is_profit = True
        total_bnb = bnb_qty + btc_qty / bnb_btc_price + usdt_qty / bnb_usdt_price
        # diff = total_bnb - bnb_base
        # result = diff * bnb_eur_price
        print(f'------------ПЕЧАЛБА--------------\nTotal BNB: {total_bnb:.3f}')
        # print(f'Печалба в BNB: {diff:.3f}\nПечалба в EUR: {result:.2f}')
        # eur_repo += result
        bnb_base = total_bnb
        bnb_qty = bnb_base / 3
        btc_qty = bnb_qty * bnb_btc_price
        usdt_qty = bnb_qty * bnb_usdt_price


    if is_profit:
        is_profit = False
        print('---------------------------')
        # usdt_base, btc_base, bnb_base = get_curr_quantities(usdt_qty, btc_qty, bnb_qty)
        print(f'USDT: {usdt_qty:.2f}\nBTC: {btc_qty:.5f}\nBNB: {bnb_qty:.3f}\nUSDT base: {usdt_base:.2f}\n'
              f'BTC base: {btc_base:.5f}\nBNB base: {bnb_base:.3f}\n-------------------')
        # print(f'EUR repo: {eur_repo:.2f}')
        print(get_total_eur()[0])
    if end - start >= 10:
        start = time.time()
        print('***************************')
        print(f'USDT profit: {usdt_profit:.2f}%\nBTC profit: {btc_profit:.2f}%\nBNB profit: {bnb_profit:.2f}%')
        print(f'BTCEUR: {btc_eur_price} EURUSDT: {eur_usdt_price} BTCUSDT: {btc_usdt_price} ')
        print(get_total_eur()[0])
    time.sleep(3)