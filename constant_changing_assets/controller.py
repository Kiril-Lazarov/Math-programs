from binance.client import Client
from binance.enums import *
import time
from constant_changing_assets.asset import Asset
import pickle

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
initial_usdt_qty = 1299.46
initial_btc_qty = 0.06073848
btc = Asset('BTC', float(client.get_asset_balance('BTC')['free']))
usdt = Asset('USDT', float(client.get_asset_balance('USDT')['free']))
print(f'Начални:\nBTC: {btc.qty}\nUSDT: {usdt.qty}')


def get_obj_on_charge(btc, usdt):
    price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
    if btc.qty * price > usdt.qty:
        print(f'On charge BTC')
        return btc
    elif usdt.qty / price >= btc.qty:
        print(f'On charge USD')
        return usdt


def profit_info(price):
    btc_qty = float(client.get_asset_balance('BTC')['free'])
    usdt_qty = float(client.get_asset_balance('USDT')['free'])
    total_usdt = usdt_qty + btc_qty * price
    total_btc = btc_qty + usdt_qty / price
    return f'BTC: {total_btc} печалба : {(total_btc / initial_btc_qty - 1) * 100:.2f}%\n' \
           f'USDT: {total_usdt} печалба USDT: {(total_usdt / initial_usdt_qty - 1) * 100:.2f}%'


def check_data():
    with open('data.txt', 'r') as file:
        if file.read() == '':
            print('Няма инцициализиран обект')
            return True, ''
        with open('data.txt', 'rb') as file:
            obj_on_charge = pickle.load(file)

            final_data = []
            for obj in obj_on_charge.obj_list:
                final_data.append(obj.qty)
            final_data = '\n'.join([str(x) for x in final_data])
            print(f'Има инициализиран обект:{obj_on_charge.name}: {obj_on_charge.qty}\nЧакащи поръчки: {final_data}')
            return False, obj_on_charge


def convert_opposite_asset(obj_on_charge, price):
    if obj_on_charge.name == 'USDT':
        if btc.qty * price > 12:
            trade_qty = float(btc.get_precise_qty(btc.qty, 5))
            client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
        usdt.qty = float(client.get_asset_balance('USDT')['free'])
        btc.qty = float(client.get_asset_balance('BTC')['free'])
        return f'-------КОНВЕРТИРАНЕ-------\nBTC: {btc.qty}\nUSDT: {usdt.qty}'

    else:
        if usdt.qty > 12:
            trade_qty = usdt.qty / (price * 1.001)
            trade_qty = usdt.get_precise_qty(trade_qty, 5)
            client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
        usdt.qty = float(client.get_asset_balance('USDT')['free'])
        btc.qty = float(client.get_asset_balance('BTC')['free'])
        return f'-------КОНВЕРТИРАНЕ-------\nBTC: {btc.qty}\nUSDT: {usdt.qty}'


statement, obj_on_charge =  check_data()
if statement:
    obj_on_charge = get_obj_on_charge(btc, usdt)
    print(convert_opposite_asset(obj_on_charge, price))
    obj_on_charge.prices_list.append(price)
    print(f'On charge: {obj_on_charge.name} qty: {obj_on_charge.qty}')
    print(obj_on_charge.prices_list)
    print(f'Следваща горна цена: {obj_on_charge.prices_list[-1] * obj_on_charge.TRADE_LEVEL_STEP:.2f}\n'
          f'Следваща долна цена: {obj_on_charge.prices_list[0] / obj_on_charge.TRADE_LEVEL_STEP:.2f}')
    obj_on_charge.update_data(obj_on_charge)



while True:
    price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    if obj_on_charge.max_trades_num - obj_on_charge.executed_orders == 0 \
            and not [obj.execution_level for obj in obj_on_charge.obj_list if obj.execution_level is not None]:
        obj_on_charge = obj_on_charge.change_object_on_charge(price)
        obj_on_charge.update_data(obj_on_charge)
    if obj_on_charge.max_trades_num - obj_on_charge.executed_orders > 0:
        check_for_price = obj_on_charge.add_price(price)
        if check_for_price != '':
            qty_to_append = obj_on_charge.get_trade_quantity()
            print(obj_on_charge.append_right_obj(
                obj_on_charge.create_object(qty_to_append, price))) if check_for_price == 'Right' \
                else print(obj_on_charge.append_left_obj(obj_on_charge.create_object(qty_to_append, price)))
            obj_on_charge.executed_orders += 1
            obj_on_charge.qty = float(client.get_asset_balance(obj_on_charge.name)['free'])
            obj_on_charge.update_data(obj_on_charge)
            print(f'Price list: {obj_on_charge.prices_list}')
    if obj_on_charge.check_for_execution(price):
        obj_on_charge.update_data(obj_on_charge)
        print(profit_info(price))

    time.sleep(2)
