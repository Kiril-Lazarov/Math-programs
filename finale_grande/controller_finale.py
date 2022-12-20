from binance.client import Client
from binance.enums import *
import time
from finale_grande.asset_finale import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
initial_usdt_qty = 1299.46
initial_btc_qty = initial_usdt_qty / price
btc = Asset('BTC', 0.00000001, initial_btc_qty)
usdt = Asset('USDT', 1299.46, initial_usdt_qty)

def get_obj_on_charge(btc, usdt, price):

    if btc.qty * price > usdt.qty:
        print('On charge BTC')
        return btc, usdt
    elif usdt.qty / price >= btc.qty:
        print('On charge USDT')
        return usdt, btc

btc.base_qty = btc.get_total_qty(usdt, price)
usdt.base_qty = usdt.get_total_qty(btc, price)
obj_on_charge, other_obj = get_obj_on_charge(btc,usdt,price)
btc.base_price = price
print(f'BTC: {btc.qty}')
print(f'BTC: {btc.base_qty}')
print(f'USDT: {usdt.qty}')
print(f'USDT: {usdt.base_qty}')
print(price)
print(other_obj.next_prices(obj_on_charge))
print(obj_on_charge.next_prices(other_obj))


while True:
    price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])

    if obj_on_charge.executed_orders != obj_on_charge.max_trades_num:
        if not obj_on_charge.prices_list:
            # print(f'Ot if na 42 red\nprices_list predi {obj_on_charge.prices_list}')
            print(obj_on_charge.trade_execution(price, other_obj, btc, usdt))
            obj_on_charge.prices_list.append(price)
            # print(f'Ot if na 42 red\nprices_list sled {obj_on_charge.prices_list}')
        if obj_on_charge.add_price(price):
            # print('Ot else na 43 red')
            print(obj_on_charge.prices_list)
            print(obj_on_charge.trade_execution(price,other_obj, btc,usdt))
            print(other_obj.next_prices(obj_on_charge))
            print(obj_on_charge.next_prices(other_obj))
            print(f'Следваща горна цена: {obj_on_charge.prices_list[-1] * obj_on_charge.TRADE_LEVEL_STEP:.2f}\n'
                  f'Следваща долна цена: {obj_on_charge.prices_list[0] / obj_on_charge.TRADE_LEVEL_STEP:.2f}')
    else:
        if obj_on_charge.execution_level is None:
            # print('Ot else na 51 red')
            # print(f'Predi change obj_on_charge: {obj_on_charge.name}\n'
            #       f'other_object {other_obj.name}')
            obj_on_charge, other_obj = obj_on_charge.change_asset_on_charge(obj_on_charge, other_obj, btc, usdt, price)
            print(obj_on_charge.get_info(btc, usdt, price))
            # print(f'SLED change obj_on_charge: {obj_on_charge.name}\n'
            #       f'other_object {other_obj.name}')

    if obj_on_charge.execution_level is not None:
        # print('Ot if na 55 red')
        if obj_on_charge.executed_orders != obj_on_charge.max_trades_num:
            print(obj_on_charge.convert_all_qty(price, other_obj))
        if obj_on_charge.check_for_execution(price, btc, usdt, obj_on_charge.execution_level, True):
            print(obj_on_charge.profit_execution(price, btc, usdt, other_obj))

    obj_on_charge.check_for_increase(price, other_obj)

    if other_obj.check_for_execution(price, btc, usdt, other_obj.profit_percentage, False):
        # print('Ot else na 62 red')
        print(other_obj.profit_execution_other_obj(price,btc, usdt, obj_on_charge))
        # print(f'Predi change obj_on_charge: {obj_on_charge.name}\n'
        #       f'other_object {other_obj.name}')
        obj_on_charge, other_obj = obj_on_charge.change_asset_on_charge(obj_on_charge, other_obj, btc, usdt, price)
        # print(f'Sled change obj_on_charge: {obj_on_charge.name}\n'
        #       f'other_object {other_obj.name}')
        print(f'-------СМЯНА-------\nГлавна валута: {obj_on_charge.name} {obj_on_charge.qty}\n'
              f'{obj_on_charge.name} base: {obj_on_charge.base_qty}\n'
              f'Втора валута: {other_obj.name} {other_obj.qty}\n'
              f'{other_obj.name} base: {other_obj.base_qty}')

    time.sleep(1)

