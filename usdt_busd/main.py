import time

from asset_migration.asset import Asset
from binance.client import Client
from binance.enums import *

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )
# usdt = 100
# print(0.01*float(client.get_symbol_ticker(symbol='BTCUSDT')['price']))
# print(0.01*float(client.get_symbol_ticker(symbol='BTCBUSD')['price']))

def get_precise_qty(obj_qty, precise_num):
    obj_qty = str(obj_qty)
    obj_qty = obj_qty.split('.')
    right_side = obj_qty[-1][:precise_num]
    result = obj_qty[0] + '.' + right_side
    if precise_num == 0:
        result = obj_qty[0]
    return result

init_usdt = 600.81
print('Processing...')
while True:
    is_ordered = False
    price = float(client.get_symbol_ticker(symbol='BUSDUSDT')['price'])
    # print(f'Текуща цена: {price}')
    if price >=1:
        busd_qty = float(f'{float(client.get_asset_balance("BUSD")["free"]):.0f}')
        # print(f'Свободно количество BUSD: {busd_qty}')
        # print(f'Заключено количество BUSD:{client.get_asset_balance("BUSD")["locked"]}')
        if busd_qty >11:
            is_ordered = True
            busd_qty = get_precise_qty(busd_qty, 0)
            client.create_order(
                symbol='BUSDUSDT',
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=float(busd_qty),
                price=str(price))
            print('-------ПОСТАВЯНЕ НА ПОРЪЧКА--------')
            print(f'Посока нагоре BUSD: {busd_qty} цена: {price:.2f}')
    elif price <= 1:

        usdt_qty =  float(client.get_asset_balance('USDT')['free'])
        # print('-------ПОСТАВЯНЕ НА ПОРЪЧКА--------')
        # print(f'Посока надолу USDT: {usdt_qty} цена: {price:.2f}')
        # print(f'Свободно количество USDT: {usdt_qty}')
        # print(f'Заключено количество USDT:{client.get_asset_balance("USDT")["locked"]} ')

        if usdt_qty > 11:
            is_ordered = True
            usdt_qty/= price
            busd_qty = get_precise_qty(usdt_qty, 0)
            client.create_order(
                symbol='BUSDUSDT',
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=float(busd_qty),
                price=str(price))
            print('-------ПОСТАВЯНЕ НА ПОРЪЧКА--------')
            print(f'Посока надолу USDT: {usdt_qty} цена: {price:.2f}')
    if is_ordered:
        total_usdt = float(client.get_asset_balance('USDT')['free']) + float(client.get_asset_balance('USDT')['locked'])
        total_busd = float(client.get_asset_balance('BUSD')['free']) + float(client.get_asset_balance('BUSD')['locked'])
        total_usdt += float(f'{total_busd/price:.2f}')
        print(f'Общо количество USDT: {total_usdt}')
        print(f'Начално количество USDT: {init_usdt}')
        print(f'Печалба {(total_usdt/ init_usdt - 1)* 100:.2f}%')


    time.sleep(1)