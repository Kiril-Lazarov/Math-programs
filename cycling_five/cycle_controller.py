import time

from binance.client import Client
from binance.enums import *

from cycling_five.cycling_asset import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
def get_usdt_prices():
    dict = {}
    for idx in range(len(assets)):
        obj = assets[idx]
        if obj.name != 'USDT':
            if obj.name =='BRL':
                symbol = f'USDT{obj.name}'
            else:
                symbol= f'{obj.name}USDT'

            dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
    return dict
# usdt_win_price = float(client.get_symbol_ticker(symbol='WINUSDT')['price'])
usdt_trx_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
usdt_xrp_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
usdt_eth_price = float(client.get_symbol_ticker(symbol='ETHUSDT')['price'])
usdt_btc_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
usdt_eur_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
usdt_brl_price = float(client.get_symbol_ticker(symbol='USDTBRL')['price'])
# win = Asset('WIN', 200 / usdt_win_price)
trx = Asset('TRX', 200 / usdt_trx_price)
xrp = Asset('XRP', 200 / usdt_xrp_price)
eth = Asset('ETH', 200 / usdt_eth_price)
btc = Asset('BTC', 200 / usdt_btc_price)

eur = Asset('EUR', 200 / usdt_eur_price)
usdt = Asset('USDT', 200)
brl = Asset('BRL', 200 * usdt_brl_price)

level = 1.001
assets = [trx, xrp, eth, btc, eur, usdt, brl]
base_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])


# def get_all_prices_dict():
#     dict = {}
#     for idx in range(len(assets)-1):
#         first, second = assets[idx], assets[idx + 1]
#         symbol = f'{first.name}{second.name}'
#         dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
#     return dict



def get_prices(base_price):
    print(f'Горна цена: {base_price * level:.2f}')
    print(f'Base price: {base_price:.2f}')
    print(f'Долна цена: {base_price / level:.2f}')


get_prices(base_price)

def assign_buffers_to_qty():
    for obj in assets:
        obj.qty = obj.buffer_qty
    return '**********ПРИРАВНЕНИ БУФЕРИ КЪМ КОЛИЧЕСТВА***********'

def set_asset_buffers(direction):
    if direction == 'down':
        reversed_assets = list(reversed(assets))
        # print(f'-------НАДОЛУ--------')
        for i in range(8):
            if i < 7:
                trade_obj = reversed_assets[i]
                next_obj = reversed_assets[i + 1]
                next_obj.buffer_qty = trade_obj.qty / float(client.get_symbol_ticker(
                    symbol=f'{next_obj.name}{trade_obj.name}')['price'])
            else:
                trade_obj = reversed_assets[7]
                next_obj = reversed_assets[0]
                next_obj.buffer_qty = trade_obj.qty * float(client.get_symbol_ticker(
                    symbol=f'{trade_obj.name}{next_obj.name}')['price'])


    else:
        # print(f'-------НАГОРЕ--------')
        for i in range(8):
            if i < 7:
                trade_obj = assets[i]
                next_obj = assets[i + 1]
                next_obj.buffer_qty = trade_obj.qty * float(client.get_symbol_ticker(
                    symbol=f'{trade_obj.name}{next_obj.name}')['price'])
            else:
                trade_obj = assets[7]
                next_obj = assets[0]
                next_obj.buffer_qty = trade_obj.qty / float(client.get_symbol_ticker(
                    symbol=f'{next_obj.name}{trade_obj.name}')['price'])
    # for x in assets:
    #     x.qty = x.buffer_qty
    # [print(str(x)) for x in assets]


def get_total_usdt(prop):
    total_qty = 0

    for obj in assets:
        if prop == 'qty':
            qty = obj.qty
        else:
            qty = obj.buffer_qty
        if obj.name != 'USDT':
            if obj.name != 'BRL':
                total_qty += qty * usdt_prices_dict[f'{obj.name}USDT']
            else:
                total_qty +=  qty / usdt_prices_dict[f'USDT{obj.name}']
        else:
            total_qty += qty
    # print(f'Total_qty: {total_qty}')
    total_profit = (total_qty / usdt_base_qty - 1) * 100
    return total_profit, total_qty

def get_total_btc():
    total = 0
    btc_index = assets.index(btc)
    for obj in assets:
        if obj.name != 'BTC':
            if assets.index(obj) < btc_index:
                symbol = f'{obj.name}BTC'
                total += obj.qty * btc_prices_dict[symbol]
            else:
                symbol = f'BTC{obj.name}'
                total += obj.qty / btc_prices_dict[symbol]
        else:
            total += obj.qty

    total_profit = ((total / btc_base_qty) - 1) * 100
    return total_profit, total


def back_to_source(usdt_quantity):
    trade_qty = usdt_quantity/8
    for idx in range (len(assets)):
        obj = assets[idx]
        if obj.name != 'USDT':
            if obj.name != 'BRL':
                obj.qty = trade_qty * usdt_prices_dict[f'{obj.name}USDT']
            else:
                obj.qty = trade_qty / usdt_prices_dict[f'USDT{obj.name}']
        else:
            obj.qty = trade_qty
    return '-----------ИЗДИШВАНЕ-----------'

usdt_init_qty = 1400
usdt_base_qty = usdt_init_qty
print('-------НАЧАЛНИ КОЛИЧЕСТВА-------')
[print(str(obj)) for obj in assets]
start = time.time()


def get_btc_prices():
    dict = {}
    btc_index = assets.index(btc)
    for obj in assets:
        if obj.name !='BTC':
            if assets.index(obj) < btc_index:
                symbol= f'{obj.name}BTC'
            else:
                symbol = f'BTC{obj.name}'
            dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
    return dict
usdt_prices_dict = get_usdt_prices()
btc_prices_dict = get_btc_prices()
# print(btc_prices_dict)
# print(btc_prices_dict['BTCUSDT'])
btc_init_qty = usdt_init_qty / btc_prices_dict['BTCUSDT']
btc_base_qty = btc_init_qty
print(f'BTC base: {btc_base_qty}')
while True:
    # btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    # btc_usdt_price = float(input('Въведи цена: '))
    # if btc_usdt_price >= base_price * level:
    #     trade_all('up')
    #     base_price = btc_usdt_price
    #     print(get_total_usdt())
    #     get_prices(base_price)
    # elif btc_usdt_price <= base_price / level:
    #     trade_all('down')
    #     base_price = btc_usdt_price
    #     print(get_total_usdt())
    #     get_prices(base_price)
    # if btc_usdt_price > base_price:
    #     trade_all('up')
    #     print(get_total_usdt())
    #     # base_price = btc_usdt_price
    # if btc_usdt_price< base_price:
    #     trade_all('up')
    #     print(get_total_usdt())
    #     # base_price = btc_usdt_price
    end =  time.time()

    # all_prices_dict = get_all_prices_dict()
    usdt_prices_dict = get_usdt_prices()
    btc_prices_dict = get_btc_prices()
    print('Total BTC')
    btc_profit, btc_total =  get_total_btc()

    print(f'{btc_total:.5f} Печалба: {btc_profit:.2f}%')
    print('Total USDT')
    usdt_profit, usdt_total = get_total_usdt('qty')

    print(f'{usdt_total:.2f} Печалба: {usdt_profit:.2f}%')
    print(f'Равностойност на BTC в USDT: {btc_total * usdt_prices_dict["BTCUSDT"]}')
    # profit, quantity = get_total_usdt("qty")
    # if end - start >= 300:
    #     print('///////////////////////////')
    #     print('///////////////////////////')
    #     print('Total USDT profit')
    #     print(f'{profit:.2f}%')
    # if quantity / usdt_base_qty >= level:
    #     print(back_to_source(quantity))
    #     print(f'Крайна печалба: {(quantity/1600 - 1)* 100:.2f}%')
    #     usdt_base_qty = quantity
    #     for obj in assets:
    #         print(str(obj))
    # set_asset_buffers('up')
    # profit_up, quantity_up = get_total_usdt("buffer")
    # if end - start >= 300:
    #     print('------След UP проверка-------')
    #     print('Total USDT profit')
    #     print(f'{profit_up:.2f}%')
    #
    # if quantity_up / usdt_base_qty >= level:
    #     print('Печалба след up')
    #     print(assign_buffers_to_qty())
    #     print(f'Крайна печалба: {(quantity_up / 1600 - 1) * 100:.2f}%')
    #     usdt_base_qty = quantity_up
    #     for obj in assets:
    #         print(str(obj))
    #
    # set_asset_buffers('down')
    # profit_down, quantity_down = get_total_usdt("buffer")
    # if end - start >= 300:
    #     print('------След DOWN проверка-------')
    #     print('Total USDT profit')
    #     print(f'{profit_down:.2f}%')
    #     start = time.time()
    # if quantity_down / usdt_base_qty >= level:
    #     print('Печалба след down')
    #     print(assign_buffers_to_qty())
    #     print(f'Крайна печалба: {(quantity_down / 1600 - 1) * 100:.2f}%')
    #     usdt_base_qty = quantity_down
    #     for obj in assets:
    #         print(str(obj))



    time.sleep(5)
