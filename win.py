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
def get_total_usdt():
    total_qty = 0
    for obj in assets:
        if obj.name != 'USDT':
            if obj.name != 'BRL':
                total_qty += obj.qty * usdt_prices_dict[f'{obj.name}USDT']
            else:
                total_qty +=  obj.qty / usdt_prices_dict[f'USDT{obj.name}']
        else:
            total_qty += obj.qty

    total_profit = (total_qty / usdt_base_qty - 1) * 100
    return total_profit, total_qty
def exhale_usdt(usdt_quantity):
    trade_qty = usdt_quantity/7
    usdt_index = assets.index(usdt)

    for obj in assets:
        if obj.name != 'USDT':
            if assets.index(obj) < usdt_index:
                obj.qty = trade_qty / usdt_prices_dict[f'{obj.name}USDT']
            else:
                obj.qty = trade_qty * usdt_prices_dict[f'USDT{obj.name}']
        else:
            obj.qty = trade_qty
    return '-----------USDT ИЗДИШВАНЕ-----------'
def exhale_btc(btc_quantity):
    trade_qty = btc_quantity /7
    btc_index = assets.index(btc)

    for obj in assets:
        if obj.name != 'BTC':
            if assets.index(obj) < btc_index:
                obj.qty = trade_qty/ btc_prices_dict[f'{obj.name}BTC']
            else:
                obj.qty = trade_qty * btc_prices_dict[f'BTC{obj.name}']
        else:
            obj.qty = trade_qty
    return '-----------BTC ИЗДИШВАНЕ-----------'
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
def curr_profits(btc_total, usdt_total,word):
    btc_profit = (btc_total/btc_init_qty - 1) * 100
    usdt_profit = (usdt_total/usdt_init_qty - 1)* 100
    return f'{word}\nBTC: {btc_profit:.2f}%\nUSDT: {usdt_profit:.2f}%'

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

level = 0.03
assets = [trx, xrp, eth, btc, eur, usdt, brl]
base_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
usdt_init_qty = 1400
usdt_base_qty = usdt_init_qty
print('-------НАЧАЛНИ КОЛИЧЕСТВА-------')
[print(str(obj)) for obj in assets]

usdt_prices_dict = get_usdt_prices()
btc_prices_dict = get_btc_prices()

btc_init_qty = usdt_init_qty / usdt_btc_price
btc_base_qty = btc_init_qty
print(f'BTC base: {btc_base_qty}')
is_profit = False
start = time.time()
btc_repo = 0
usdt_repo = 0
while True:
    end = time.time()
    usdt_prices_dict = get_usdt_prices()
    btc_prices_dict = get_btc_prices()
    usdt_profit, usdt_total_qty = get_total_usdt()
    btc_profit, btc_total_qty = get_total_btc()

    if usdt_profit >= level:
        is_profit = True
        print(f'Стартиране печалба на USDT\n Base: {usdt_base_qty} Curr: {usdt_total_qty}'
              f' diff: {usdt_total_qty - usdt_base_qty}')
        print(exhale_usdt(usdt_base_qty))
        print(f'USDT base след издишване: {get_total_usdt()[1]}')
        usdt_repo += (usdt_total_qty - usdt_base_qty)
        btc_base_qty = get_total_btc()[1]
        print(f'Общо в BTC repo:{btc_repo}\nUSDT base: {usdt_base_qty}')

    if btc_profit >= level:
        is_profit = True
        print(f'Стартиране печалба на BTC\n Base: {btc_base_qty} Curr: {btc_total_qty}'
              f' diff: {btc_total_qty - btc_base_qty}')
        print(exhale_btc(btc_base_qty))
        print(f'BTC base след издишване: {get_total_btc()[1]}')
        btc_repo += (btc_total_qty - btc_base_qty)
        usdt_base_qty = get_total_usdt()[1]
        print(f'Общо в BTC repo:{btc_repo}\nUSDT base: {usdt_base_qty}')


    if is_profit:
        is_profit = False
        word = '---------ПЕЧАЛБИ---------'
        print(curr_profits(btc_total_qty, usdt_total_qty,word))
        [print(str(obj)) for obj in assets]
        print(f'Общо в USDT repo: {usdt_repo:.2f}\nUSDT base: {usdt_base_qty}\nBTC base: {btc_base_qty}\nОбщо в BTC repo: {btc_repo}'
              f' (еквивалент в USDT {btc_repo * btc_prices_dict["BTCUSDT"]}')

    if end - start >= 60:
        word = '---------НАСТОЯЩИ ПЕЧАЛБИ----------'
        print(curr_profits(btc_total_qty, usdt_total_qty, word))
        start = time.time()

    time.sleep(5)