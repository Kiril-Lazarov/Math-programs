import time

from binance.client import Client
from binance.enums import *

from real_brahma_breath_trade.brahma_asset import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

asset_price_precision = {'BNBUSDT': (3, 1), 'BNBBTC': (3, 6), 'XRPBTC': (0, 6), 'XRPUSDT': (0, 2),
                         'ETHBTC': (4, 6), 'ETHUSDT': (4, 2), 'BTCEUR': (5, 2), 'EURUSDT': (1, 2)}


def get_precise_num(symbol, position):
    if position == 'base':
        return asset_price_precision[symbol][0]
    elif position == 'quote':
        return asset_price_precision[symbol][1]


def get_precise_qty(obj_qty, precise_num):
    obj_qty = str(obj_qty)
    obj_qty = obj_qty.split('.')
    right_side = obj_qty[-1][:precise_num]
    result = obj_qty[0] + '.' + right_side
    if precise_num == 0:
        result = obj_qty[0]
    return float(result)


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


def inhale_usdt():
    print('От inhale_usdt:')
    usdt_idx = assets.index(usdt)
    for obj in assets_on_inhale:
        if assets.index(obj) < usdt_idx:
            symbol = f'{obj.name}USDT'
            trade_qty = float(client.get_asset_balance(obj.name)['free'])
            number = get_precise_num(symbol, 'base')
            trade_qty = float(get_precise_qty(trade_qty, number))
            client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
    return '-------ЗАВЪРШЕНО USDT ВДИШВАНЕ-------'


def exhale_usdt(usdt_quantity):
    print('От exhale USDT:')
    trade_qty = usdt_quantity / 3
    usdt_index = assets.index(usdt)
    symbol = ''
    number = 0
    copy_trade_qty = 0
    for obj in assets_on_exhale:
        print(obj.name)
        if obj.name != assets_on_exhale[-1].name:

            if assets.index(obj) < usdt_index:
                symbol = f'{obj.name}USDT'
                price = usdt_prices_dict[symbol]
                copy_trade_qty = trade_qty / price
                number = get_precise_num(symbol, 'base')

                copy_trade_qty = get_precise_qty(copy_trade_qty, number)

        else:
            symbol = f'{obj.name}USDT'
            number = get_precise_num(symbol, 'base')
            print(f'Precise number: {number}')
            price = float(client.get_symbol_ticker(symbol=symbol)['price'])
            print(f'Цена {price}')
            trade_qty = float(client.get_asset_balance('USDT')['free'])
            copy_trade_qty = trade_qty / (price * 1.005)
            print(f'Количество: {trade_qty}')
            print(f'copy_trade_qty: {copy_trade_qty}')
            copy_trade_qty = get_precise_qty(copy_trade_qty, number)
            print(f'Precise copy trade qty: {copy_trade_qty}')
            print(symbol, trade_qty)

        client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                            quantity=copy_trade_qty)
        time.sleep(0.1)
        obj.qty = float(client.get_asset_balance(f'{obj.name}')['free'])
        print(f'{obj.name} {copy_trade_qty}')
    return '-----------ЗАВЪРШЕНО USDT ИЗДИШВАНЕ-----------'


def inhale_btc():
    print('От inhale BTC:')
    btc_index = assets.index(btc)
    for obj in assets_on_inhale:
        if assets.index(obj) < btc_index:
            symbol = f'{obj.name}BTC'
            trade_qty = float(client.get_asset_balance(obj.name)['free'])
            number = get_precise_num(symbol, 'base')
            trade_qty = float(get_precise_qty(trade_qty, number))
            client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
        elif assets.index(obj) > btc_index:
            symbol = f'BTC{obj.name}'
            trade_qty = float(client.get_asset_balance(obj.name)['free'])
            number = get_precise_num(symbol, 'base')
            price = float(client.get_symbol_ticker(symbol=symbol)['price'])
            trade_qty /= (price * 1.002)
            trade_qty = float(get_precise_qty(trade_qty, number))
            client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
    return '-----------ЗАВЪРШЕНО BTC ВДИШВАНЕ-----------'


def exhale_btc(btc_quantity):
    trade_qty = btc_quantity / 3
    btc_index = assets.index(btc)

    for obj in assets_on_exhale:
        if obj.name != assets_on_exhale[-1].name:
            if assets.index(obj) < btc_index:
                symbol = f'{obj.name}BTC'
                price = float(client.get_symbol_ticker(symbol=symbol)['price'])
                copy_trade_qty = trade_qty / price
                number = get_precise_num(symbol, 'base')
                copy_trade_qty = get_precise_qty(copy_trade_qty, number)
                client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                    quantity=copy_trade_qty)
        else:
            symbol = f'{obj.name}BTC'
            price = float(client.get_symbol_ticker(symbol=symbol)['price'])
            print(f'Цена {price}')
            trade_qty = float(client.get_asset_balance('BTC')['free'])
            print(f'Количество: {trade_qty}')
            copy_trade_qty = trade_qty / (price * 1.005)
            print(f'copy_trade_qty: {copy_trade_qty}')
            number = get_precise_num(symbol, 'base')
            print(f'Precise number: {number}')
            copy_trade_qty = get_precise_qty(copy_trade_qty, number)
            print(f'Precise copy trade qty: {copy_trade_qty}')
            client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=copy_trade_qty)
        time.sleep(0.1)
        obj.qty = float(client.get_asset_balance(f'{obj.name}')['free'])
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


def set_new_asset_quantities(xrp, bnb, eth):
    xrp.qty = float(client.get_asset_balance('XRP')['free'])
    bnb.qty = float(client.get_asset_balance('BNB')['free'])
    eth.qty = float(client.get_asset_balance('ETH')['free'])


def convert_btc_repo(btc_repo):
    btc_repo = get_precise_qty(btc_repo, 5)
    client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                        quantity=btc_repo)
    return f'---------КОНВЕРТИРАН BTC-----------\n{btc_repo}'


def convert_usdt(usdt_repo):
    usdt_repo /= (usdt_prices_dict['BTCUSDT'] * 1.005)
    usdt_repo = get_precise_qty(usdt_repo, 5)
    client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                        quantity=btc_repo)
    return f'---------КОНВЕРТИРАН USDT-----------\n{usdt_repo}'


def get_start_quantities():
    with open('brahma_data.txt') as file:
        f = file.read().split(', ')
        print(f)
        if len(f) == 0:
            pass

        else:

            xrp_qty, bnb_qty, eth_qty = f
            xrp = Asset('XRP', float(xrp_qty))
            bnb = Asset('BNB', float(bnb_qty))
            eth = Asset('ETH', float(eth_qty))
            usdt_init = xrp.qty * float(client.get_symbol_ticker(symbol='XRPUSDT')['price']) + \
                        bnb.qty * float(client.get_symbol_ticker(symbol='BNBUSDT')['price']) + \
                        eth.qty * float(client.get_symbol_ticker(symbol='ETHUSDT')['price'])
            btc_init = usdt_init / float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            return xrp, bnb, eth, usdt_init, btc_init


# usdt_trx_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
# usdt_xrp_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
# usdt_bnb_price = float(client.get_symbol_ticker(symbol='BNBUSDT')['price'])
# usdt_eth_price = float(client.get_symbol_ticker(symbol='ETHUSDT')['price'])
# usdt_btc_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
# usdt_eur_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
# usdt_brl_price = float(client.get_symbol_ticker(symbol='USDTBRL')['price'])
# win = Asset('WIN', 200 / usdt_win_price)
# trx = Asset('TRX', 200 / usdt_trx_price)
# xrp = Asset('XRP', 0)
# bnb = Asset('BNB', 0)
# eth = Asset('ETH', 0)
btc = Asset('BTC', 1)
xrp, bnb, eth, usdt_init_qty, btc_init_qty = get_start_quantities()
# eur = Asset('EUR', 300 / usdt_eur_price)
usdt = Asset('USDT', 1)
# brl = Asset('BRL', 200 * usdt_brl_price)

level = 0.03
assets = [xrp, bnb, eth, btc, usdt]
assets_on_exhale = [bnb, xrp, eth]
assets_on_inhale = [xrp, eth, bnb]
# base_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
# usdt_init_qty = float(client.get_asset_balance('USDT')['free'])
usdt_base_qty = usdt_init_qty
# usdt_prices_dict = get_usdt_prices()
# btc_prices_dict = get_btc_prices()
# bnb_prices_dict = get_bnb_prices()

# print(exhale_usdt(usdt_init_qty))
# set_new_asset_quantities(xrp, bnb, eth)
print('-------НАЧАЛНИ КОЛИЧЕСТВА-------')
[print(str(obj)) for obj in assets_on_inhale]

# btc_init_qty = usdt_init_qty / btc_prices_dict['BTCUSDT']
btc_base_qty = btc_init_qty

is_profit = False
start = time.time()
btc_repo = float(client.get_asset_balance('BTC')['free'])
print(f'BTC repo след началото: {btc_repo}')
usdt_repo = float(client.get_asset_balance('USDT')['free'])
print(f'USDT repo след началото: {usdt_repo}')
print(f'USDT init: {usdt_init_qty}')
print(f'BTC init: {btc_init_qty}')
while True:
    end = time.time()
    usdt_prices_dict = get_usdt_prices()
    btc_prices_dict = get_btc_prices()
    bnb_prices_dict = get_bnb_prices()
    usdt_profit, usdt_total_qty, usdt_bnb_tax = get_total_usdt()
    btc_profit, btc_total_qty, btc_bnb_tax = get_total_btc()

    if usdt_profit >= level:
        is_profit = True
        print(f'Стартиране печалба на USDT\n Base: {usdt_base_qty} Curr: {usdt_total_qty}')
        print(inhale_usdt())
        if (btc_repo * btc_prices_dict['BTCUSDT'] >= 20 and usdt_repo >= 20):
            print(convert_btc_repo(btc_repo))
            usdt_base_qty = float(client.get_asset_balance('USDT')['free'])
        print(f'USDT base: {usdt_base_qty}')
        print(exhale_usdt(usdt_base_qty))
        usdt_repo = float(client.get_asset_balance('USDT')['free'])
        set_new_asset_quantities(xrp, bnb, eth)
        btc_base_qty = usdt_base_qty / btc_prices_dict['BTCUSDT']
        print(f'Нов BTC base: {btc_base_qty}')

    if btc_profit >= level:
        is_profit = True
        print(f'Стартиране печалба на BTC\n Base: {btc_base_qty} Curr: {btc_total_qty}')
        print(inhale_btc())
        if (btc_repo * btc_prices_dict['BTCUSDT'] >= 20 and usdt_repo >= 20):
            print(convert_usdt(usdt_repo))
            btc_base_qty = float(client.get_asset_balance('BTC')['free'])

        print(f'BTC base: {btc_base_qty}')
        print(exhale_btc(btc_base_qty))
        set_new_asset_quantities(xrp, bnb, eth)
        usdt_base_qty = btc_base_qty * btc_prices_dict['BTCUSDT']
        print(f'Нов USDT base: {usdt_base_qty}')

    if is_profit:
        is_profit = False
        word = '---------СЪСТОЯНИЕ НА ВАЛУТИТЕ---------'
        print(curr_profits(btc_total_qty, usdt_total_qty, word))
        [print(str(obj)) for obj in assets_on_inhale]
        print(
            f'Общо в USDT repo: {usdt_repo:.2f}\nUSDT base: {usdt_base_qty}\nBTC base: {btc_base_qty}\nОбщо в BTC repo: {btc_repo}'
            f' (еквивалент в USDT {btc_repo * btc_prices_dict["BTCUSDT"]:.2f}')
        with open('brahma_data.txt', 'w') as file:
            file.write(f'{xrp.qty}, {bnb.qty}, {eth.qty}')

    if end - start >= 600:
        word = '---------НАСТОЯЩИ ПЕЧАЛБИ----------'
        print(curr_profits(btc_total_qty, usdt_total_qty, word))
        print(f'USDT taxes: {usdt_bnb_tax * usdt_prices_dict["BNBUSDT"]:.2f}\n'
              f'BTC taxes: {btc_bnb_tax} ({btc_bnb_tax * usdt_prices_dict["BNBUSDT"]:.2f}) USDT')
        start = time.time()

    time.sleep(5)


