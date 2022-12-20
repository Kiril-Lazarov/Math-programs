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

def get_precise_qty(obj_qty, precise_num):
    obj_qty = str(obj_qty)
    obj_qty = obj_qty.split('.')
    right_side = obj_qty[-1][:precise_num]
    result = obj_qty[0] + '.' + right_side
    if precise_num == 0:
        result = obj_qty[0]
    return float(result)


def make_btc_bnb_buy_order(btc_qty, bnb_btc_price):
    trade_qty = btc_qty / (bnb_btc_price * 1.005)
    trade_qty = get_precise_qty(trade_qty, 3)
    client.create_order(symbol='BNBBTC', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                        quantity=trade_qty)


    return f'-------ИЗПЪЛНЕНИЕ-------\n{btc_qty} BTC -> {btc_qty / bnb_btc_price} BNB на цена: {bnb_btc_price}'


def make_usdt_bnb_buy_order(usdt_qty, bnb_usdt_price):
    trade_qty = usdt_qty / (bnb_usdt_price * 1.005)
    trade_qty = get_precise_qty(trade_qty, 3)
    client.create_order(symbol='BNBUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                        quantity=trade_qty)

    return f'-------ИЗПЪЛНЕНИЕ-------\n{usdt_qty} USDT -> {usdt_qty / bnb_usdt_price} BNB на цена: {bnb_usdt_price}'

def make_bnb_usdt_sell_order(bnb_qty, bnb_usdt_price):
    trade_qty = get_precise_qty(bnb_qty, 3)
    client.create_order(symbol='BNBUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                        quantity=trade_qty)

    result = trade_qty * bnb_usdt_price
    return f'-------ИЗПЪЛНЕНИЕ-------\n{trade_qty} BNB - > {result:.2f} USDT'


def make_bnb_btc_sell_order(bnb_qty, bnb_btc_price):
    trade_qty = get_precise_qty(bnb_qty, 3)
    client.create_order(symbol='BNBBTC', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                        quantity=trade_qty)

    result = trade_qty * bnb_btc_price
    return f'-------ИЗПЪЛНЕНИЕ-------\n{trade_qty} BNB - > {result:.5f} BTC'

def check_initial_conditions():
    usdt_base = 0
    btc_base = 0
    bnb_qty = 0

    bnb_usdt_price, bnb_btc_price, btc_usdt_price = get_prices()
    usdt_qty = float(client.get_asset_balance('USDT')['free'])
    btc_qty = float(client.get_asset_balance('BTC')['free'])

    if usdt_qty >= 11 and btc_qty * btc_usdt_price >= 11:
        print(make_btc_bnb_buy_order(btc_qty, bnb_btc_price))
        print(make_usdt_bnb_buy_order(usdt_qty, bnb_usdt_price))
        bnb_qty = float(client.get_asset_balance('BNB')['free'])
        usdt_base = bnb_qty * bnb_usdt_price
        btc_base = bnb_qty * bnb_btc_price
        with open('bnb_data.txt', 'w') as file:
            file.write(f'{bnb_qty}, {usdt_base}, {btc_base}')
        print(f'USDT base: {usdt_base}\nBTC base: {btc_base}\nBNB qty: {bnb_qty}')

    if usdt_qty >= 11 and btc_qty * btc_usdt_price < 11:
        print(make_usdt_bnb_buy_order(usdt_qty, bnb_usdt_price))
        bnb_qty = float(client.get_asset_balance('BNB')['free'])
        usdt_base = bnb_qty * bnb_usdt_price
        btc_base = bnb_qty * bnb_btc_price + btc_qty
        with open('bnb_data.txt', 'w') as file:
            file.write(f'{bnb_qty}, {usdt_base}, {btc_base}')
        print(f'USDT base: {usdt_base}\nBTC base: {btc_base}\nBNB qty: {bnb_qty}')

    if usdt_qty < 11 and btc_qty * btc_usdt_price >= 11:
        print(make_btc_bnb_buy_order(btc_qty, bnb_btc_price))
        bnb_qty = float(client.get_asset_balance('BNB')['free'])
        usdt_base = bnb_qty * bnb_usdt_price + usdt_qty
        btc_base = bnb_qty * bnb_btc_price
        with open('bnb_data.txt', 'w') as file:
            file.write(f'{bnb_qty}, {usdt_base}, {btc_base}')
        print(f'USDT base: {usdt_base}\nBTC base: {btc_base}\nBNB qty: {bnb_qty}')

    if usdt_qty< 11 and btc_qty * btc_usdt_price <11:
        with open('bnb_data.txt') as file:
            f = file.read().split(', ')
            bnb_qty, usdt_base, btc_base = f
        bnb_qty = float(bnb_qty)
        usdt_base = float(usdt_base)
        btc_base = float(btc_base)
        print(f'Нищо не е конвертирано:\nUSDT base: {usdt_base}\nBTC base: {btc_base}\nBNB qty: {bnb_qty}')

    return usdt_base, btc_base, bnb_qty

def get_next_profit_prices(usdt_base, btc_base, bnb_qty):
    next_usdt_profit_price = (usdt_base * level)/ bnb_qty
    next_btc_profit_price = (btc_base * level)/ bnb_qty
    return f'Следваща цена за печалба на USDT: {next_usdt_profit_price:.1f}. Очаквана сума: {usdt_base *level} USDT\n' \
           f'Следваща цена за печалба на BTC: {next_btc_profit_price:.6f}. Очаквана сума: {btc_base * level} BTC'

def get_bases_and_repos(usdt_base, btc_base, usdt_repo, btc_repo,btc_usdt_price):
    btc_base_usdt_eq =  btc_base * btc_usdt_price
    btc_repo_eq = btc_repo * btc_usdt_price
    return f'USDT base: {usdt_base:.2f}\nBTC base: {btc_base:.5f}({btc_base_usdt_eq:.2f} USDT)\n' \
           f'USDT repo: {usdt_repo:.2f}\nBTC repo: {btc_repo:.5f} ({btc_repo_eq:.2f} USDT)' \


def get_total_usdt_profit():
    total_usdt = usdt_repo + btc_repo * btc_usdt_price + bnb_qty * bnb_usdt_price
    return f'Total USDT: {total_usdt:.2f} печалба: {(total_usdt / usdt_init - 1) * 100:.2f}%'


usdt_base, btc_base, bnb_qty = check_initial_conditions()
level = 1.0003
usdt_init = 33.64
print(get_next_profit_prices(usdt_base, btc_base, bnb_qty))


usdt_repo = float(client.get_asset_balance('USDT')['free'])
btc_repo = float(client.get_asset_balance('BTC')['free'])
start = time.time()




while True:
    end = time.time()
    bnb_usdt_price, bnb_btc_price, btc_usdt_price = get_prices()
    if bnb_qty * bnb_usdt_price >= usdt_base * level:
        print(make_bnb_usdt_sell_order(bnb_qty, bnb_usdt_price))
        time.sleep(0.1)
        print(make_usdt_bnb_buy_order(usdt_base,bnb_usdt_price))
        bnb_qty = float(client.get_asset_balance('BNB')['free'])
        btc_base = bnb_qty * bnb_btc_price
        usdt_repo = float(client.get_asset_balance('USDT')['free'])
        print(get_bases_and_repos(usdt_base, btc_base, usdt_repo, btc_repo, btc_usdt_price))
        print(get_total_usdt_profit())
        print(get_next_profit_prices(usdt_base, btc_base, bnb_qty))

    if bnb_qty * bnb_btc_price >= btc_base * level:
        print(make_bnb_btc_sell_order(bnb_qty, bnb_btc_price))
        time.sleep(0.1)
        print(make_btc_bnb_buy_order(btc_base, bnb_btc_price))
        bnb_qty = float(client.get_asset_balance('BNB')['free'])
        usdt_base = bnb_qty * bnb_usdt_price
        btc_repo = float(client.get_asset_balance('BTC')['free'])
        print(get_bases_and_repos(usdt_base, btc_base, usdt_repo, btc_repo, btc_usdt_price))
        print(get_total_usdt_profit())
        print(get_next_profit_prices(usdt_base, btc_base, bnb_qty))

    if end - start >= 600:
        start = time.time()
        print(get_total_usdt_profit())
    time.sleep(1)
