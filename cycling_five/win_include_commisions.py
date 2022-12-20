import time

from binance.client import Client
from binance.enums import *

from cycling_five.cycling_asset import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)


def get_bnb_prices():
    dict = {}
    bnb_index = assets.index(bnb)
    for idx in range(len(assets)):
        obj = assets[idx]
        if obj.name != 'BNB':
            if assets.index(obj) < bnb_index:
                symbol = f'{obj.name}BNB'
            else:
                symbol = f'BNB{obj.name}'
            dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
    return dict


def get_usdt_prices():
    dict = {}
    for idx in range(len(assets)):
        obj = assets[idx]
        if obj.name != 'USDT':
            if obj.name == 'BRL':
                symbol = f'USDT{obj.name}'
            else:
                symbol = f'{obj.name}USDT'

            dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
    return dict


def get_bnb_tax(obj, bnb_index, come_from):
    if assets.index(obj) < bnb_index:
        symbol_for_taxes = f'{obj.name}BNB'
        tax = obj.qty * 0.00075 * bnb_prices_dict[symbol_for_taxes]
    elif assets.index(obj) > bnb_index:
        symbol_for_taxes = f'BNB{obj.name}'
        tax = obj.qty * 0.00075 / bnb_prices_dict[symbol_for_taxes]
    else:
        tax = obj.qty * 0.00075
    return tax


def get_total_usdt():
    total_qty = 0
    total_taxes = 0
    bnb_index = assets.index(bnb)
    test_bnb_qty = bnb.qty
    for obj in assets_on_inhale:
        if obj.name != 'BNB':
            total_qty += obj.qty * usdt_prices_dict[f'{obj.name}USDT']
            tax = get_bnb_tax(obj, bnb_index, 'USDT')
            total_taxes += tax
            test_bnb_qty -= tax

        else:

            tax = get_bnb_tax(obj, bnb_index, 'USDT')
            test_bnb_qty -= tax
            total_taxes += tax
            total_qty += test_bnb_qty * bnb_prices_dict[f'{obj.name}USDT']

    total_profit = (total_qty / usdt_base_qty - 1) * 100
    return total_profit, total_qty, total_taxes


def exhale_usdt(usdt_quantity):
    trade_qty = usdt_quantity / 4
    usdt_index = assets.index(usdt)
    total_taxes = 0
    test_bnb_qty = bnb.qty
    bnb_index = assets.index(bnb)
    for obj in assets_on_exhale:
        if obj.name == 'BNB':
            tax = get_bnb_tax(obj,bnb_index,'USDT')
            total_taxes += tax
            obj.qty = trade_qty / bnb_prices_dict['BNBUSDT']
            obj.qty -= tax
        else:
            if assets.index(obj) < usdt_index:
                obj.qty = trade_qty / usdt_prices_dict[f'{obj.name}USDT']

            else:
                obj.qty = trade_qty * usdt_prices_dict[f'USDT{obj.name}']
            tax = get_bnb_tax(obj, bnb_index, 'USDT')
            total_taxes += tax
            bnb.qty -= tax
    print(f'OT exhale_usdt total_taxes: {total_taxes} ({total_taxes * bnb_prices_dict["BNBUSDT"]})')
    return '-----------USDT ИЗДИШВАНЕ-----------'


def exhale_btc(btc_quantity):
    trade_qty = btc_quantity / 4
    btc_index = assets.index(btc)

    for obj in assets:
        if obj.name != 'BTC':
            if assets.index(obj) < btc_index:
                obj.qty = trade_qty / btc_prices_dict[f'{obj.name}BTC']
            else:
                obj.qty = trade_qty * btc_prices_dict[f'BTC{obj.name}']
        else:
            obj.qty = trade_qty
    return '-----------BTC ИЗДИШВАНЕ-----------'


def get_btc_prices():
    dict = {}
    btc_index = assets.index(btc)
    for obj in assets:
        if obj.name != 'BTC':
            if assets.index(obj) < btc_index:
                symbol = f'{obj.name}BTC'
            else:
                symbol = f'BTC{obj.name}'
            dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
    return dict


def get_total_btc():
    total = 0
    btc_index = assets.index(btc)
    total_taxes = 0
    test_bnb_qty = bnb.qty
    bnb_index = assets.index(bnb)
    for obj in assets_on_inhale:
        if obj.name != 'BNB':
            if assets.index(obj) < btc_index:
                symbol = f'{obj.name}BTC'
                tax = get_bnb_tax(obj, bnb_index, 'BTC')
                total_taxes += tax
                test_bnb_qty -= tax
                total += obj.qty * btc_prices_dict[symbol]
            else:
                symbol = f'BTC{obj.name}'
                tax = get_bnb_tax(obj, bnb_index, 'BTC')
                total_taxes += tax
                test_bnb_qty -= tax
                total += obj.qty / btc_prices_dict[symbol]
        else:
            tax = get_bnb_tax(obj, bnb_index, 'BTC')
            test_bnb_qty -= tax
            total_taxes += tax
            total += test_bnb_qty * bnb_prices_dict['BNBBTC']
    total_profit = ((total / btc_base_qty) - 1) * 100
    return total_profit, total, total_taxes


def curr_profits(btc_total, usdt_total, word):
    btc_profit = (btc_total / btc_init_qty - 1) * 100
    usdt_profit = (usdt_total / usdt_init_qty - 1) * 100
    return f'{word}\nBTC: {btc_profit:.2f}%\nUSDT: {usdt_profit:.2f}%'


# usdt_trx_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
usdt_xrp_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
usdt_bnb_price = float(client.get_symbol_ticker(symbol='BNBUSDT')['price'])
usdt_eth_price = float(client.get_symbol_ticker(symbol='ETHUSDT')['price'])
usdt_btc_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
usdt_eur_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
# usdt_brl_price = float(client.get_symbol_ticker(symbol='USDTBRL')['price'])
# win = Asset('WIN', 200 / usdt_win_price)
# trx = Asset('TRX', 200 / usdt_trx_price)
xrp = Asset('XRP', 300 / usdt_xrp_price)
bnb = Asset('BNB', 300 / usdt_bnb_price)
eth = Asset('ETH', 300 / usdt_eth_price)
btc = Asset('BTC', 300 / usdt_btc_price)

eur = Asset('EUR', 300 / usdt_eur_price)
usdt = Asset('USDT', 300)
# brl = Asset('BRL', 200 * usdt_brl_price)

level = 0.07
assets = [xrp, bnb, eth, btc, eur, usdt]
assets_on_exhale = [bnb, xrp, eth, eur]
assets_on_inhale = [xrp, eth, eur, bnb]
# base_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
usdt_init_qty = 1200
usdt_base_qty = usdt_init_qty
usdt_prices_dict = get_usdt_prices()
btc_prices_dict = get_btc_prices()
bnb_prices_dict = get_bnb_prices()

exhale_usdt(usdt_init_qty)
print('-------НАЧАЛНИ КОЛИЧЕСТВА-------')
[print(str(obj)) for obj in assets]

btc_init_qty = usdt_init_qty/ btc_prices_dict['BTCUSDT']
btc_base_qty = btc_init_qty


is_profit = False
start = time.time()
btc_repo = 0
usdt_repo = 0
while True:
    end = time.time()
    usdt_prices_dict = get_usdt_prices()
    btc_prices_dict = get_btc_prices()
    bnb_prices_dict = get_bnb_prices()
    usdt_profit, usdt_total_qty, usdt_bnb_tax = get_total_usdt()
    btc_profit, btc_total_qty, btc_bnb_tax = get_total_btc()

    if usdt_profit >= level:
        is_profit = True

        print(f'Стартиране печалба на USDT\n Base: {usdt_base_qty} Curr: {usdt_total_qty}'
              f' diff: {usdt_total_qty - usdt_base_qty}')
        print(exhale_usdt(usdt_base_qty))
        print(f'USDT base след издишване: {get_total_usdt()[1]}\nПлатени такси: {usdt_bnb_tax*usdt_prices_dict["BNBUSDT"]:.2f} USDT')
        usdt_repo += (usdt_total_qty - usdt_base_qty)
        btc_base_qty = usdt_total_qty / btc_prices_dict['BTCUSDT']
        print(f'Общо в BTC repo:{btc_repo}\nUSDT base: {usdt_base_qty}')

    if btc_profit >= level:
        is_profit = True
        print(f'Стартиране печалба на BTC\n Base: {btc_base_qty} Curr: {btc_total_qty}'
              f' diff: {btc_total_qty - btc_base_qty}')
        print(exhale_btc(btc_base_qty))
        print(f'BTC base след издишване: {get_total_btc()[1]}')
        btc_repo += (btc_total_qty - btc_base_qty)
        usdt_base_qty = btc_total_qty * usdt_prices_dict['BTCUSDT']
        print(f'Общо в BTC repo:{btc_repo}\nUSDT base: {usdt_base_qty}\nПлатени такси {btc_bnb_tax:.8f} BTC '
              f'({btc_bnb_tax*usdt_prices_dict["BNBUSDT"]:.2f}) USDT')

    if is_profit:
        is_profit = False
        word = '---------ПЕЧАЛБИ---------'
        print(curr_profits(btc_total_qty, usdt_total_qty, word))
        [print(str(obj)) for obj in assets_on_inhale]
        print(
            f'Общо в USDT repo: {usdt_repo:.2f}\nUSDT base: {usdt_base_qty}\nBTC base: {btc_base_qty}\nОбщо в BTC repo: {btc_repo}'
            f' (еквивалент в USDT {btc_repo * btc_prices_dict["BTCUSDT"]:.2f}')

    if end - start >= 600:
        word = '---------НАСТОЯЩИ ПЕЧАЛБИ----------'
        print(curr_profits(btc_total_qty, usdt_total_qty, word))
        print(f'USDT taxes: {usdt_bnb_tax * usdt_prices_dict["BNBUSDT"]:.2f}\n'
              f'BTC taxes: {btc_bnb_tax} ({btc_bnb_tax * usdt_prices_dict["BNBUSDT"]:.2f}) USDT')
        start = time.time()

    time.sleep(5)
