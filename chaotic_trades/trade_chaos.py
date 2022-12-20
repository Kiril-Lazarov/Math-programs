import time
from binance.client import Client
import random
import datetime
api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

btc_trades_count_for_qty = 0
busd_trades_count_for_qty = 0
btc_trades_count_for_prices = 0
busd_trades_count_for_prices = 0

print('Processing...')
transaction_count = 0
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
print(f'ground_price: {ground_price}')
init_step_percentage = 1.005

number_trades = 3
btc_active_qty = 0.02651
busd_active_qty = 844
init_btc_overall_qty = btc_active_qty + busd_active_qty / ground_price
init_busd_overall_qty = init_btc_overall_qty * ground_price
btc_active_qty = init_btc_overall_qty / 2
busd_active_qty = btc_active_qty * ground_price
init_active_btc = btc_active_qty
init_active_busd = busd_active_qty
base_btc_active = init_active_btc
base_busd_active = init_active_busd
base_overall_btc_qty = btc_active_qty + busd_active_qty / ground_price
base_overall_busd_qty = init_btc_overall_qty * ground_price
print(f'Init btc: {init_btc_overall_qty}')
print(f'Init busd: {init_busd_overall_qty}')
print(f'Start BTC active: {btc_active_qty}')
print(f'Start BUSD active: {busd_active_qty}')


def execution(asset, curr_price):
    print()
    e = datetime.datetime.now()
    print("Час: = %s:%s:%s" % (e.hour, e.minute, e.second))
    print(f'CURR price: {curr_price}')
    global btc_active_qty
    global busd_active_qty
    global transaction_count
    transaction_count += 1
    print()
    print(f'Поръчка номер: {transaction_count}')
    if asset == 'BTC':
        qty = btc_active_qty / number_trades
        btc_active_qty -= qty
        busd_active_qty += qty * curr_price
        print(f'Транзакция {qty:.8f} BTC -> {qty * curr_price:.2f} BUSD на цена: {curr_price:.2f}')

    elif asset == 'BUSD':
        qty = busd_active_qty / number_trades
        busd_active_qty -= qty
        btc_active_qty += qty / curr_price
        print(f'Транзакция {qty:.2f} BUSD -> {qty / curr_price:.8f} BTC на цена: {curr_price:.2f}')
    print()
    print(f'Активен BTC: {btc_active_qty} печалба: {(btc_active_qty / init_active_btc - 1) * 100:.2f}%')
    print(f'Активен BUSD: {busd_active_qty} печалба: {(busd_active_qty / init_active_busd - 1) * 100:.2f}%')
    curr_overall_btc = btc_active_qty + busd_active_qty / curr_price
    curr_overall_busd = busd_active_qty + btc_active_qty * curr_price
    print(f'Тотал BUSD: {curr_overall_busd:.2f} печалба: {(curr_overall_busd / init_busd_overall_qty - 1) * 100:.2f}%')
    print(f'Тотал BTC: {curr_overall_btc:.8f} печалба: {(curr_overall_btc / init_btc_overall_qty - 1) * 100:.2f}%')


def check_for_profit():
    global base_overall_btc_qty
    global base_overall_busd_qty
    global btc_active_qty
    global busd_active_qty
    global is_profit
    curr_total_btc = btc_active_qty + busd_active_qty / curr_price
    curr_total_busd = busd_active_qty + btc_active_qty * curr_price
    relation_curr_init_overall_btc = (curr_total_btc / base_overall_btc_qty - 1) * 100
    relation_curr_init_overall_busd = (curr_total_busd / base_overall_busd_qty - 1) * 100
    if relation_curr_init_overall_btc > 0 and relation_curr_init_overall_busd > 0:
        base_overall_btc_qty = curr_total_btc
        base_overall_busd_qty = curr_total_busd
        btc_active_qty = curr_total_btc / 2
        busd_active_qty = btc_active_qty * curr_price
        is_profit = True
        print()
        print('--------------ПЕЧАЛБА!!!--------------')
        print()
        e = datetime.datetime.now()
        print("Час: = %s:%s:%s" % (e.hour, e.minute, e.second))
        print(f'Нов активен BTC: {btc_active_qty:.8f} печалба: {(btc_active_qty / init_active_btc - 1) * 100:.2f}%')
        print(f'Нов активен BUSD: {busd_active_qty:.2f} печалба: {(busd_active_qty / init_active_busd - 1) * 100:.2f}%')
        print(f'Ново базово общо количество BTC: {base_overall_btc_qty:.8f}')
        print(f'Ново базово общо количество BUSD: {base_overall_busd_qty:.2f}')
        time.sleep(30)
        asset = random.choice(['BTC', 'BUSD'])
        execution(asset, curr_price)


start = time.time()
asset = random.choice(['BTC', 'BUSD'])
execution(asset, ground_price)
is_profit = False
while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    # curr_price = float(input())

    end = time.time()

    if end - start >= 3600:
        asset = random.choice(['BTC', 'BUSD'])
        execution(asset, curr_price)
        print(f'Base overall btc quantity: {base_overall_btc_qty}')
        print(f'Init btc quantity: {init_btc_overall_qty}')
        print(f'Base overall busd quantity: {base_overall_busd_qty}')
        print(f'Init busd quantity: {init_busd_overall_qty}')
        start = time.time()
        is_profit = False
    if not is_profit:
        check_for_profit()


    time.sleep(120)

