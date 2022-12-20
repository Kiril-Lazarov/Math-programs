from binance.client import Client
from binance.enums import *

import time

from real_usdt_trade.main_asset import MainAsset
#
api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
btc_qty = float(client.get_asset_balance('BTC')['free'])
price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
if btc_qty * price >= 20:
    quantity = float(f'{btc_qty * 0.9:.5f}')
    client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                        quantity=quantity)
    print(f'Добавяне на стартова стойност BTC: {quantity}')

initial_usdt_qty = 1299.46
quantity = float(client.get_asset_balance('USDT')['free'])
print(f'USDT: {quantity:.2f}')
usdt = MainAsset('USDT', quantity)


# btc_init = btc_qty + usdt.qty / float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
initial_btc_qty = 0.06073848

usdt.prices_list.append(price)
print(f'Следваща горна цена: {usdt.prices_list[-1] * usdt.PRICE_LEVEL_PRCTG:.2f}\n'
      f'Следваща долна цена: {usdt.prices_list[0] / usdt.PRICE_LEVEL_PRCTG:.2f}')


def profit_info(price):
    btc_qty = float(client.get_asset_balance('BTC')['free'])
    total_usdt = usdt.qty + btc_qty * price
    total_btc = btc_qty + usdt.qty/ price
    return f'Печалба BTC: {(total_btc/initial_btc_qty - 1) * 100:.2f}%\n' \
           f'Печалба USDT: {(total_usdt/ initial_usdt_qty -1) * 100:.2f}%'


print('Processing...')
while True:
    price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    check_for_price = usdt.add_price(price)
    if check_for_price != '':
        usdt_for_app = usdt.get_trade_quantity()
        btc_trade_qty = usdt_for_app/price
        btc_trade_qty = float(f'{btc_trade_qty:.5f}')
        print(usdt.append_right_obj(usdt.create_object(btc_trade_qty, price))) if check_for_price == 'Right' \
            else print(usdt.append_left_obj(usdt.create_object(btc_trade_qty, price)))
        usdt.qty = float(client.get_asset_balance('USDT')['free'])
        usdt.executed_orders += 1
        # usdt.prices_list = [obj.init_price for obj in usdt.obj_list]
        print(f'Price list: {usdt.prices_list}')

    if usdt.check_for_execution(price):
        print(profit_info(price))


    time.sleep(1)



