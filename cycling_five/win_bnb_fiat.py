import time

from binance.client import Client
# from binance.enums import *

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
    usdt_idx = assets.index(usdt)
    for idx in range(len(assets)):
        obj = assets[idx]
        if obj.name != 'USDT':
            if assets.index(obj) < usdt_idx:
                symbol = f'{obj.name}USDT'
            else:
                symbol = f'USDT{obj.name}'
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
    usdt_idx = assets.index(usdt)
    test_bnb_qty = bnb.qty
    for obj in assets_on_inhale:
        if obj.name != 'BNB':
            if assets.index(obj) < usdt_idx:
                symbol = f'{obj.name}USDT'
                total_qty += obj.qty * usdt_prices_dict[symbol]
                tax = get_bnb_tax(obj, bnb_index, 'USDT')
                total_taxes += tax
                test_bnb_qty -= tax
            elif assets.index(obj) > usdt_idx:
                symbol = f'USDT{obj.name}'
                total_qty += obj.qty / usdt_prices_dict[symbol]
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
    trade_qty = usdt_quantity / 6
    usdt_index = assets.index(usdt)
    total_taxes = 0
    test_bnb_qty = bnb.qty
    bnb_index = assets.index(bnb)
    for obj in assets_on_exhale:
        if obj.name == 'BNB':
            tax = get_bnb_tax(obj, bnb_index, 'USDT')
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


# def exhale_btc(btc_quantity):
#     trade_qty = btc_quantity / 4
#     btc_index = assets.index(btc)
#
#     for obj in assets:
#         if obj.name != 'BTC':
#             if assets.index(obj) < btc_index:
#                 obj.qty = trade_qty / btc_prices_dict[f'{obj.name}BTC']
#             else:
#                 obj.qty = trade_qty * btc_prices_dict[f'BTC{obj.name}']
#         else:
#             obj.qty = trade_qty
#     return '-----------BTC ИЗДИШВАНЕ-----------'


# def get_btc_prices():
#     dict = {}
#     btc_index = assets.index(btc)
#     for obj in assets:
#         if obj.name != 'BTC':
#             if assets.index(obj) < btc_index:
#                 symbol = f'{obj.name}BTC'
#             else:
#                 symbol = f'BTC{obj.name}'
#             dict[symbol] = float(client.get_symbol_ticker(symbol=symbol)['price'])
#     return dict


# def get_total_btc():
#     total = 0
#     btc_index = assets.index(btc)
#     total_taxes = 0
#     test_bnb_qty = bnb.qty
#     bnb_index = assets.index(bnb)
#     for obj in assets_on_inhale:
#         if obj.name != 'BNB':
#             if assets.index(obj) < btc_index:
#                 symbol = f'{obj.name}BTC'
#                 tax = get_bnb_tax(obj, bnb_index, 'BTC')
#                 total_taxes += tax
#                 test_bnb_qty -= tax
#                 total += obj.qty * btc_prices_dict[symbol]
#             else:
#                 symbol = f'BTC{obj.name}'
#                 tax = get_bnb_tax(obj, bnb_index, 'BTC')
#                 total_taxes += tax
#                 test_bnb_qty -= tax
#                 total += obj.qty / btc_prices_dict[symbol]
#         else:
#             tax = get_bnb_tax(obj, bnb_index, 'BTC')
#             test_bnb_qty -= tax
#             total_taxes += tax
#             total += test_bnb_qty * bnb_prices_dict['BNBBTC']
#     total_profit = ((total / btc_base_qty) - 1) * 100
#     return total_profit, total, total_taxes


def curr_profits(usdt_total, word):
    # btc_profit = (btc_total / btc_init_qty - 1) * 100
    usdt_profit = (usdt_total / usdt_init_qty - 1) * 100
    return f'{word}\nUSDT: {usdt_profit:.2f}%'


usdt_gbp_price = float(client.get_symbol_ticker(symbol='GBPUSDT')['price'])
usdt_aud_price = float(client.get_symbol_ticker(symbol='AUDUSDT')['price'])
usdt_bnb_price = float(client.get_symbol_ticker(symbol='BNBUSDT')['price'])
usdt_brl_price = float(client.get_symbol_ticker(symbol='USDTBRL')['price'])
usdt_rub_price = float(client.get_symbol_ticker(symbol='USDTRUB')['price'])
usdt_eur_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
# usdt_brl_price = float(client.get_symbol_ticker(symbol='USDTBRL')['price'])
# win = Asset('WIN', 200 / usdt_win_price)
# trx = Asset('TRX', 200 / usdt_trx_price)
# aud = Asset('AUD', 200 / usdt_aud_price)
bnb = Asset('BNB', 200 / usdt_bnb_price)
brl = Asset('BRL', 200 * usdt_brl_price)
rub = Asset('RUB', 200 * usdt_rub_price)

eur = Asset('EUR', 200 / usdt_eur_price)
usdt = Asset('USDT', 200)
gbp = Asset('GBP', 200 / usdt_gbp_price)

level = 0.1
assets = [bnb, aud, gbp, eur, usdt, brl, rub]
assets_on_exhale = [bnb, aud, gbp, eur, brl, rub]
assets_on_inhale = [aud, gbp, eur, brl, rub, bnb]
# base_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
usdt_init_qty = 1200
usdt_base_qty = usdt_init_qty
usdt_prices_dict = get_usdt_prices()
# btc_prices_dict = get_btc_prices()
bnb_prices_dict = get_bnb_prices()

exhale_usdt(usdt_init_qty)
print('-------НАЧАЛНИ КОЛИЧЕСТВА-------')
[print(str(obj)) for obj in assets]

# btc_init_qty = usdt_init_qty/ btc_prices_dict['BTCUSDT']
# btc_base_qty = btc_init_qty


is_profit = False
start = time.time()
btc_repo = 0
usdt_repo = 0
while True:
    end = time.time()
    usdt_prices_dict = get_usdt_prices()

    # btc_prices_dict = get_btc_prices()
    bnb_prices_dict = get_bnb_prices()

    usdt_profit, usdt_total_qty, usdt_bnb_tax = get_total_usdt()
    # btc_profit, btc_total_qty, btc_bnb_tax = get_total_btc()

    if usdt_profit >= level:
        print(exhale_usdt(usdt_total_qty))
        usdt_repo += (usdt_total_qty - usdt_profit)
        usdt_base_qty = usdt_total_qty
    if end - start >= 600:
        word = '---------НАСТОЯЩИ ПЕЧАЛБИ----------'
        print(curr_profits(usdt_total_qty, word))
        print(f'USDT base след издишване: {get_total_usdt()[1]:.2f}')
        print(f'USDT repo: {usdt_repo:.2f}\nUSDT base qty: {usdt_base_qty:.2f}')
        start = time.time()

    time.sleep(5)
