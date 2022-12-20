import time
from collections import deque

from binance.client import Client
from endless_trading.btc import Bitcoin
from endless_trading.busd import Busd
from endless_trading.general import General

api_key = ''
api_secret = ''

number_trades = 12
price_percentage = 1.003
profit_percentage = 1.0027
total_profit_percentage = 1
transaction_count = 0
init_btc = 0.06839651
print(f'Начално количество BTC: {init_btc}')

client = Client(api_key, api_secret)
acces = General()
btc = Bitcoin(init_btc)
btc.btc_base_total_qty = init_btc
busd = Busd(0)
asset = 'BTC'


def print_quantities():
    curr_total_btc = btc.quantity + busd.quantity/curr_price
    curr_total_busd = busd.quantity + btc.quantity * curr_price
    print(f'Количество BTC: {btc.quantity:.8f} Печалба: {(curr_total_btc/init_btc - 1)*100:.2f}%')
    print(f'Кoличество BUSD: {busd.quantity:.2f} Печалба: {(curr_total_busd/init_busd -1)*100:.2f}%')
    print(f'Текуща равностойност BTC: {curr_total_btc:.8f}')
    print(f'Начално количество BTC: {init_btc}')
    print(f'Текуща равностойност BUSD: {curr_total_busd:.2f}')
    print(f'Начално количество BUSD: {init_busd:.2f}')


def execution():
    print(f'\n-------ИЗПЪЛНЕНИЕ-------')
    if asset == 'BTC':
        qty = btc.quantity * acces.factor(btc.btc_trades_number, number_trades)
        btc.quantity = acces.sumation(btc.quantity, -qty)
        busd.quantity = acces.sumation(busd.quantity, qty * curr_price)
        btc.btc_trades_number = acces.sumation(btc.btc_trades_number, 1)
        if curr_price >= btc.btc_price_list[-1] * price_percentage:
            btc.btc_waiting_profit.append((qty * curr_price, curr_price / profit_percentage))
            btc.btc_price_list.append(curr_price)
        elif curr_price <= btc.btc_price_list[0] / price_percentage:
            btc.btc_waiting_profit.appendleft((qty * curr_price, curr_price / profit_percentage))
            btc.btc_price_list.appendleft(curr_price)
        print(f'\n{qty:.8f} BTC -> {qty * curr_price:.2f} BUSD на цена: {curr_price:.2f}')
        if btc.btc_waiting_profit:
            print(f'Горна граница цена: {btc.btc_price_list[-1]*profit_percentage}')
            print(f'Долна граница цена: {btc.btc_price_list[0]/profit_percentage}')
            print(f'Поредна BTC поръчка: {btc.btc_trades_number}')
            print(f'Слeдваща горна цена: {curr_price * price_percentage}')
            print(f'Следваща долна цена за печалба: {btc.btc_waiting_profit[-1][1]}')
    else:
        qty = busd.quantity * acces.factor(busd.busd_trades_number, number_trades)
        busd.quantity = acces.sumation(busd.quantity, -qty)
        btc.quantity = acces.sumation(btc.quantity, qty / curr_price)
        busd.busd_trades_number = acces.sumation(busd.busd_trades_number, 1)
        if curr_price >= busd.busd_price_list[-1] * price_percentage:
            busd.busd_waiting_profit.append((qty / curr_price, curr_price * profit_percentage))
            busd.busd_price_list.append(curr_price)
        elif curr_price <= busd.busd_price_list[0] / price_percentage:
            busd.busd_waiting_profit.appendleft((qty / curr_price, curr_price * profit_percentage))
            busd.busd_price_list.appendleft(curr_price)
        print(f'\n{qty:.2f} BUSD -> {qty / curr_price:.8f} BTC на цена: {curr_price:.2f}')
        if busd.busd_waiting_profit:
            print(f'Горна граница цена: {busd.busd_price_list[-1]*profit_percentage:.2f}')
            print(f'Долна граница цена: {busd.busd_price_list[0]/profit_percentage:.2f}')
            print(f'Поредна BUSD поръчка: {busd.busd_trades_number}')
            print(f'Следваща горна цена за печалба: {busd.busd_waiting_profit[0][1]:.2f"}')
            print(f'Следваща долна цена: {curr_price / price_percentage:.2f}')
    print_quantities()


def check_profit():
    if asset == 'BTC':
        if curr_price <= btc.btc_waiting_profit[-1][-1]:
            print(f'\n-------ПЕЧАЛБА-------')
            qty = btc.btc_waiting_profit[-1][0]
            btc.quantity = acces.sumation(btc.quantity, qty / curr_price)
            busd.quantity = acces.sumation(busd.quantity, -qty)
            btc.btc_waiting_profit.pop()
            btc.btc_price_list.pop()
            btc.btc_trades_number = acces.sumation(btc.btc_trades_number, -1)
            print(f'\n{qty:.2f} BUSD -> {qty / curr_price:.8f} BTC на цена: {curr_price:.2f}')
            print(f'Поредна BTC поръчка: {btc.btc_trades_number}')
            print_quantities()


    else:
        if curr_price >= busd.busd_waiting_profit[0][-1]:
            print(f'\n-------ПЕЧАЛБА-------')
            qty = busd.busd_waiting_profit[0][0]
            busd.quantity = acces.sumation(busd.quantity, qty * curr_price)
            btc.quantity = acces.sumation(btc.quantity, - qty)
            busd.busd_waiting_profit.popleft()
            busd.busd_price_list.popleft()
            busd.busd_trades_number = acces.sumation(busd.busd_trades_number, -1)
            print(f'\n{qty:.8f} BTC -> {qty * curr_price:.2f} BUSD на цена: {curr_price:.2f}')
            print(f'Поредна BUSD поръчка: {busd.busd_trades_number}')
            print_quantities()

curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
init_busd = init_btc*curr_price
busd.busd_base_total_qty = init_busd
print(f'Начално количества BUSD: {init_busd:.2f}')
btc.btc_price_list = deque([curr_price])
print(f'Слeдваща горна цена: {curr_price * price_percentage}')
print(f'Следваща долна цена: {curr_price / price_percentage}')
execution()


def check_for_total_profit():
    global asset
    is_profit = False
    curr_total_btc = btc.quantity + busd.quantity/curr_price
    curr_total_busd = busd.quantity + btc.quantity* curr_price
    if (curr_total_btc / btc.btc_base_total_qty - 1)*100>= total_profit_percentage:
        is_profit = True
        asset = 'BUSD'
        btc.btc_base_total_qty = curr_total_btc
        busd.quantity = curr_total_busd
        btc.btc_price_list = deque([curr_price])
        btc.btc_price_list = deque([])
        btc.quantity = 0

    if (curr_total_busd / busd.busd_base_total_qty -1) * 100 >=total_profit_percentage:
        is_profit = True
        asset = 'BTC'
        busd.busd_base_total_qty = curr_total_busd
        btc.quantity = curr_total_btc
        btc.btc_price_list = deque([curr_price])
        busd.busd_price_list = deque([])
        busd.quantity = 0
        pass
    if is_profit:
        print(f'\n-------ТОТАЛНА ПЕЧАЛБА-------\n')
        print(f'Текуща цена: {curr_price:.2f}\n')
        print(f'Нова валута: {asset}')
        btc.btc_trades_number = 0
        busd.busd_trades_number = 0
        btc.btc_waiting_profit = deque([])
        busd.busd_waiting_profit = deque([])
        print_quantities()



while True:
    # curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    curr_price = float(input('Въведи цена: '))
    if asset == 'BTC':

        asset, is_change_asset = acces.check_number_trades(asset, btc.btc_trades_number, number_trades)
        if is_change_asset:
            btc.btc_trades_number = 0
            btc.btc_waiting_profit = deque([])
            btc.btc_price_list = deque([])
            busd.busd_price_list.append(curr_price)
    else:

        asset, is_change_asset = acces.check_number_trades(asset, busd.busd_trades_number, number_trades)
        if is_change_asset:
            busd.busd_trades_number = 0
            busd.busd_waiting_profit = deque([])
            busd.busd_price_list = deque([])
            btc.btc_price_list.append(curr_price)
    # проверка дали трябва да се изпълнява нова поръчка
    if btc.btc_price_list:
        if acces.check_for_trade(curr_price, btc.btc_price_list, price_percentage):
            transaction_count += 1
            print(f'\nПоръчка номер: {transaction_count}')
            execution()
    if busd.busd_price_list:
        if acces.check_for_trade(curr_price, busd.busd_price_list, price_percentage):
            transaction_count += 1
            print(f'\nПоръчка номер: {transaction_count}')
            execution()
    # проверка дали има печалби
    if btc.btc_waiting_profit or busd.busd_waiting_profit:
        check_profit()
    check_for_total_profit()
    time.sleep(1)
