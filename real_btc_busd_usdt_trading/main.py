import time

from binance.client import Client
from asset import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

btc = Asset('BTC', float(client.get_asset_balance('BTC')['free']))
busd = Asset('BUSD', float(client.get_asset_balance('BUSD')['free']))
usdt = float(client.get_asset_balance('USDT')['free'])
initial_total_qty = 1299.46


def take_absolute_profit():
    usdt = float(client.get_asset_balance('USDT')['free'])
    busd = float(client.get_asset_balance('BUSD')['free'])
    btc = float(client.get_asset_balance('BTC')['free'])
    btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    busd_usdt_price = float(client.get_symbol_ticker(symbol='BUSDUSDT')['price'])
    total = usdt + btc * btc_usdt_price + busd * busd_usdt_price
    return f'Начален USDT: {initial_total_qty}\nТекущ USDT: {total:.2f}\n' \
           f'Печалба: {((total/ initial_total_qty - 1)* 100)}%', f'{total:.2f}', f'{btc_usdt_price:.2f}'

btc.total_init = btc.total_base = btc.take_total_qty(btc, busd)
busd.total_init = busd.total_base = busd.take_total_qty(busd, btc)
print('Processing...')
print(f'Начални:\nBTC: {btc.qty}\nBUSD: {busd.qty:.2f}\nUSDT: {usdt:.2f}')
print(f'Начални базови:\nBTC base{btc.total_base}\nBUSD base: {busd.total_base:.2f}\n')
print(busd.next_prices(busd, btc, busd.profit_percentage))
print(btc.next_prices(btc, busd, btc.profit_percentage))
print(take_absolute_profit()[0])
print(take_absolute_profit()[1])
transactions_count = 0


def append_data(value, price):
    with open('data.txt', 'a') as file:
        file.write(f', ({price}, {value})')


def get_trade_numbers():
    with open('trade_numbers.txt') as file:
        numbers = file.read().split(', ')
        return numbers[0], numbers[1]

def set_trade_numbers(btc_num, busd_num):
    with open('trade_numbers.txt', 'w') as file:
        file.write(f'{btc_num}, {busd_num}')
    return f'Успешно сетнати:\nBTC trade_num: {btc_num}\nBUSD trade_num: {busd_num}'

btc.number_trades, busd.number_trades = get_trade_numbers()
print(btc.number_trades)
print(busd.number_trades)

while True:
    if btc.check_for_increase(btc, busd):
        btc.increase_level(btc)
        print(btc.next_prices(btc, busd, btc.profit_percentage))
        print(btc.next_prices(btc, busd, btc.execution_percentage))
    if btc.check_for_execution(btc, busd):
        transactions_count += 1
        print(busd.execution(busd, btc, transactions_count))
        print(busd.next_prices(busd, btc, busd.profit_percentage))
        print(btc.next_prices(btc, busd, btc.profit_percentage))
        print(Asset.profit_info(btc, busd))
        print(take_absolute_profit()[0])
        profit, value, price = take_absolute_profit()
        append_data(value, price)
        print(set_trade_numbers(btc.number_trades, busd.number_trades))
        print(profit)
        print(btc)
        print(busd)

    if busd.check_for_increase(busd, btc):
        busd.increase_level(busd)
        print(busd.next_prices(busd, btc, busd.profit_percentage))
        print(busd.next_prices(busd, btc, busd.execution_percentage))
    if busd.check_for_execution(busd, btc):
        transactions_count += 1
        print(btc.execution(btc, busd, transactions_count))
        print(busd.next_prices(busd, btc, busd.profit_percentage))
        print(btc.next_prices(btc, busd, btc.profit_percentage))
        print(Asset.profit_info(btc, busd))
        profit, value, price = take_absolute_profit()
        append_data(value, price)
        print(set_trade_numbers(btc.number_trades, busd.number_trades))
        print(profit)
        print(btc)
        print(busd)

    time.sleep(1)