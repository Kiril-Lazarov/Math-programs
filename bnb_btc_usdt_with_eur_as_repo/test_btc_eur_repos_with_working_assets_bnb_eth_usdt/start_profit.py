import time

from binance.client import Client

# from binance.enums import *

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)


def get_working_assets_prices():
    bnb_eth_price = float(client.get_symbol_ticker(symbol='BNBETH')['price'])
    eth_eur_price = float(client.get_symbol_ticker(symbol='ETHEUR')['price'])
    bnb_eur_price = float(client.get_symbol_ticker(symbol='BNBEUR')['price'])
    return bnb_eth_price, eth_eur_price, bnb_eur_price


def get_btc_prices():
    bnb_btc_price = float(client.get_symbol_ticker(symbol='BNBBTC')['price'])
    eth_btc_price = float(client.get_symbol_ticker(symbol='ETHBTC')['price'])
    btc_eur_price = float(client.get_symbol_ticker(symbol='BTCEUR')['price'])
    xrp_btc_price = float(client.get_symbol_ticker(symbol='XRPBTC')['price'])
    trx_btc_price =  float(client.get_symbol_ticker(symbol='TRXBTC')['price'])
    return bnb_btc_price, eth_btc_price, btc_eur_price, xrp_btc_price,trx_btc_price


def get_xrp_prices():
    xrp_bnb_price = float(client.get_symbol_ticker(symbol='XRPBNB')['price'])
    xrp_eth_price = float(client.get_symbol_ticker(symbol='XRPETH')['price'])
    xrp_eur_price = float(client.get_symbol_ticker(symbol='XRPEUR')['price'])
    return xrp_bnb_price, xrp_eth_price, xrp_eur_price


def get_usdt_prices():
    bnb_usdt_price = float(client.get_symbol_ticker(symbol='BNBUSDT')['price'])
    eth_usdt_price = float(client.get_symbol_ticker(symbol='ETHUSDT')['price'])
    eur_usdt_price = float(client.get_symbol_ticker(symbol='EURUSDT')['price'])
    return bnb_usdt_price, eth_usdt_price, eur_usdt_price


def get_trx_prices():
    trx_bnb_price = float(client.get_symbol_ticker(symbol='TRXBNB')['price'])
    trx_eth_price = float(client.get_symbol_ticker(symbol='TRXETH')['price'])
    trx_eur_price = float(client.get_symbol_ticker(symbol='TRXEUR')['price'])
    return trx_bnb_price, trx_eth_price, trx_eur_price


def get_total_trx(bnb_qty, eth_qty, eur_qty):
    total = bnb_qty / trx_bnb_price + eth_qty / trx_eth_price + eur_qty / trx_eur_price
    profit = (total / trx_base - 1) * 100
    return total, profit


def get_total_usdt(bnb_qty, eth_qty, eur_qty):
    total = 0
    total += bnb_qty * bnb_usdt_price + eth_qty * eth_usdt_price + eur_qty * eur_usdt_price
    profit = (total / usdt_base - 1) * 100
    return total, profit


def get_total_btc(bnb_qty, eth_qty, eur_qty):
    total = 0
    total += bnb_qty * bnb_btc_price + eth_qty * eth_btc_price + eur_qty / btc_eur_price
    profit = (total / btc_base - 1) * 100
    return total, profit


def get_total_xrp(bnb_qty, eth_qty, eur_qty):
    total = 0
    total += bnb_qty / xrp_bnb_price + eth_qty / xrp_eth_price + eur_qty / xrp_eur_price
    profit = (total / xrp_base - 1) * 100
    return total, profit


def get_other_prices():
    btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    xrp_usdt_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
    trx_usdt_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
    return btc_usdt_price, xrp_usdt_price, trx_usdt_price


def calc_total_profit(bnb_qty, eth_qty, eur_qty,btc_usdt_price,
                      xrp_usdt_price, trx_usdt_price,bnb_usdt_price,
                      eth_usdt_price, eur_usdt_price, usdt_profit_base):
    total_usdt = bnb_qty * bnb_usdt_price + eth_qty* eth_usdt_price + eur_qty * eur_usdt_price\
                + trx_repo * trx_usdt_price + xrp_repo* xrp_usdt_price + btc_repo* btc_usdt_price + usdt_repo
    profit_percentage = (total_usdt/usdt_profit_base - 1) * 100
    if profit_percentage >= total_profit_level:
        is_total_profit = True
    else:
        is_total_profit = False
    return total_usdt, is_total_profit


bnb_eth_price, eth_eur_price, bnb_eur_price = get_working_assets_prices()
bnb_btc_price, eth_btc_price, btc_eur_price,xrp_btc_price,trx_btc_price = get_btc_prices()
bnb_usdt_price, eth_usdt_price, eur_usdt_price = get_usdt_prices()
xrp_bnb_price, xrp_eth_price, xrp_eur_price = get_xrp_prices()
trx_bnb_price, trx_eth_price, trx_eur_price = get_trx_prices()

print(bnb_eth_price, eth_eur_price, bnb_eur_price)
print(bnb_btc_price, eth_btc_price, btc_eur_price)
print(bnb_usdt_price, eth_usdt_price, eur_usdt_price)
print(trx_bnb_price, trx_eth_price, trx_eur_price)
usdt_init = 1200
usdt_base = 1200
usdt_profit_base = 1200
bnb_qty = usdt_init / 3 / bnb_usdt_price
eth_qty = usdt_init / 3 / eth_usdt_price
eur_qty = usdt_init / 3 / eur_usdt_price
btc_init = 0.06080
xrp_init = 3133.159
trx_init = 19373.59

btc_base = bnb_qty * bnb_btc_price + eth_qty * eth_btc_price + eur_qty / btc_eur_price
xrp_base = bnb_qty / xrp_bnb_price + eth_qty / xrp_eth_price + eur_qty / xrp_eur_price
trx_base = bnb_qty / trx_bnb_price + eth_qty / trx_eth_price + eur_qty / trx_eur_price
print(bnb_qty, eth_qty, eur_qty)
print(get_total_usdt(bnb_qty, eth_qty, eur_qty))
print(get_total_btc(bnb_qty, eth_qty, eur_qty))
print(get_total_xrp(bnb_qty, eth_qty, eur_qty))
print(get_total_trx(bnb_qty, eth_qty, eur_qty))
level = 0.05
total_profit_level = 0.5
usdt_repo = 0
btc_repo = 0
xrp_repo = 0
trx_repo = 0

is_profit = False
start = time.time()

while True:
    end = time.time()
    bnb_eth_price, eth_eur_price, bnb_eur_price = get_working_assets_prices()
    bnb_btc_price, eth_btc_price, btc_eur_price,xrp_btc_price,trx_btc_price = get_btc_prices()
    bnb_usdt_price, eth_usdt_price, eur_usdt_price = get_usdt_prices()
    xrp_bnb_price, xrp_eth_price, xrp_eur_price = get_xrp_prices()
    trx_bnb_price, trx_eth_price, trx_eur_price = get_trx_prices()

    btc_usdt_price, xrp_usdt_price, trx_usdt_price= get_other_prices()
    usdt_total, usdt_profit = get_total_usdt(bnb_qty, eth_qty, eur_qty)
    btc_total, btc_profit = get_total_btc(bnb_qty, eth_qty, eur_qty)
    xrp_total, xrp_profit = get_total_xrp(bnb_qty, eth_qty, eur_qty)
    trx_total, trx_profit = get_total_trx(bnb_qty, eth_qty, eur_qty)
    total_usdt, is_total_profit = calc_total_profit(bnb_qty, eth_qty, eur_qty,btc_usdt_price,
                      xrp_usdt_price, trx_usdt_price,bnb_usdt_price,
                      eth_usdt_price, eur_usdt_price,usdt_profit_base)
    if is_total_profit:
        print(f'$$$$$$$$$$$$$$$$$$$ РЕКАЛИБРИРАНЕ USDT $$$$$$$$$$$$$$$$$$$$$')
        print(f'Total USDT: {total_usdt:.2f}')
        usdt_profit_base = total_usdt
        if trx_repo * trx_usdt_price>=12:
            trx_repo = 0
        else:
            total_usdt -= trx_repo * trx_usdt_price
        if xrp_repo * xrp_usdt_price >=12:
            xrp_repo = 0
        else:
            total_usdt-=  xrp_repo * xrp_usdt_price
        if btc_repo * btc_usdt_price >=12:
            btc_repo = 0
        else:
            total_usdt -= btc_repo * btc_usdt_price
        print(f'Total USDT: {total_usdt:.2f}')
        usdt_repo = 0
        bnb_qty = total_usdt/3/bnb_usdt_price
        eth_qty = total_usdt/3/eth_usdt_price
        eur_qty = total_usdt/3/eur_usdt_price
        usdt_base = total_usdt

        print(f'USDT base: {usdt_base}\nUSDT profit base: {usdt_profit_base}')
        trx_base = usdt_base / trx_usdt_price
        xrp_base = usdt_base/xrp_usdt_price
        btc_base = usdt_base/btc_usdt_price
        print(bnb_qty, eth_qty, eur_qty)
    else:
        if usdt_profit >= level:
            is_profit = True
            diff = usdt_total - usdt_base
            print(f'DIff на USDT profit: {diff} USDT')
            usdt_repo += diff/2
            usdt_base += diff/2
            bnb_qty = usdt_base / 3 / bnb_usdt_price
            eth_qty = usdt_base / 3 / eth_usdt_price
            eur_qty = usdt_base / 3 / eur_usdt_price
            btc_base = usdt_base / btc_usdt_price
            xrp_base = usdt_base / xrp_usdt_price
            trx_base = usdt_base / trx_usdt_price

        elif btc_profit >= level:
            is_profit = True
            diff = btc_total - btc_base
            print(f'Diff на BTC profit: {diff} BTC')
            btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            btc_repo += diff/2
            btc_base += diff/2
            bnb_qty = btc_base / 3 / bnb_btc_price
            eth_qty = btc_base / 3 / eth_btc_price
            eur_qty = btc_base / 3 * btc_eur_price
            usdt_base = btc_base * btc_usdt_price
            xrp_base = btc_base / float(client.get_symbol_ticker(symbol='XRPBTC')['price'])
            trx_base = btc_base / float(client.get_symbol_ticker(symbol='TRXBTC')['price'])

        elif xrp_profit >= level:
            is_profit = True
            diff = xrp_total - xrp_base
            print(f'Diff на XRP profit: {diff} XRP')
            xrp_usdt_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
            xrp_repo += diff/2
            xrp_base += diff/2
            bnb_qty = (xrp_base / 3) * xrp_bnb_price
            eth_qty = (xrp_base / 3) * xrp_eth_price
            eur_qty = (xrp_base / 3) * xrp_eur_price
            usdt_base = xrp_base * xrp_usdt_price
            btc_base = xrp_base * float(client.get_symbol_ticker(symbol='XRPBTC')['price'])
            trx_base = xrp_base / float(client.get_symbol_ticker(symbol='TRXXRP')['price'])
        elif trx_profit >= level:
            is_profit = True
            diff = trx_total - trx_base
            print(f'Diff на TRX profit: {diff} TRX')
            trx_usdt_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
            trx_repo += diff/2
            trx_base += diff/2
            bnb_qty = trx_base / 3 * trx_bnb_price
            eth_qty = trx_base / 3 * trx_eth_price
            eur_qty = trx_base / 3 * trx_eur_price
            usdt_base = trx_base * trx_usdt_price
            btc_base = trx_base * float(client.get_symbol_ticker(symbol='TRXBTC')['price'])
            xrp_base = trx_base * float(client.get_symbol_ticker(symbol='TRXXRP')['price'])

        if is_profit:
            # btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            # xrp_usdt_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
            # trx_usdt_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])
            is_profit = False
            print('$$$$$$$$$$$   ПЕЧАЛБА   $$$$$$$$$$$$$$')
            print(
                f'Състояния на репота:\nUSDT repo: {usdt_repo:.2f}\nBTC repo: {btc_repo:.5f} {btc_repo * btc_usdt_price:.2f} USDT\n'
                f'XRP repo: {xrp_repo:.2f} {xrp_repo * xrp_usdt_price:.2f} USDT\n'
                f'TRX repo: {trx_repo:.2f} {trx_repo * trx_usdt_price:.2f} USDT')
            print(f'Бази:\nUSDT base : {usdt_base:.2f} Печалба {(usdt_total / usdt_init - 1) * 100:.2f}%\n'
                  f'BTC base: {btc_base:.5f} Печалба: {(btc_total / btc_init - 1) * 100:.2f}%\n'
                  f'XRP base: {xrp_base:.2f} Печалба: {(xrp_total / xrp_init - 1) * 100:.2f}%\n'
                  f'TRX base: {trx_base:.2f} Печалба: {(trx_total / trx_init - 1) * 100:.2f}%')
            total_profit_usdt = btc_repo * btc_usdt_price + xrp_repo * xrp_usdt_price \
                                + trx_repo * trx_usdt_price + usdt_repo + bnb_qty * bnb_usdt_price + eth_qty * eth_usdt_price \
                                + eur_qty * eur_usdt_price
            total_profit_btc = btc_repo + usdt_repo / btc_usdt_price + xrp_repo * xrp_btc_price + trx_repo * trx_btc_price\
                                + bnb_qty * bnb_btc_price + eth_qty * eth_usdt_price + eur_qty/btc_eur_price
            print(f'Абсолютна печалба в USDT: {total_profit_usdt:.2f} {(total_profit_usdt / usdt_init - 1) * 100:.2f}%')
            print(f'Абсолютна печалба в BTC: {total_profit_btc:.2f} {(total_profit_btc / btc_init - 1) * 100:.2f}%')
    if end - start >= 120:
        print('****************************')
        print(f'BTC profit: {btc_profit:.2f}%\nUSDT profit: {usdt_profit:.2f}%\nXRP profit:'
              f' {xrp_profit:.2f}%\nTRX profit: {trx_profit:.2f}%')
        start = time.time()
    time.sleep(3)
