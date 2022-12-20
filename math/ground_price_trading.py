from collections import deque
import time
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

# Стартови променливи
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])

number_trades = 10
transaction_count = 0
profit_percentage_defalut = 1.005

busd_active_quantity = 844.30  # текущо активно количество BUSD
btc_active_quantity = 0.02651651# текущо активно количество BTC
busd_active_quantity = (busd_active_quantity + btc_active_quantity*ground_price) / 2
print(f'Начално активно количество BUSD: {busd_active_quantity}')
btc_active_quantity = busd_active_quantity / ground_price
print(f'Начално активно количество BTC: {btc_active_quantity}')
init_btc_active = btc_active_quantity  # запазване на стартовото активно количество BTC
init_busd_active = busd_active_quantity  # запазване на стартовото активно количество BUSD
overall_btc = btc_active_quantity + busd_active_quantity / ground_price  # Равностойност в BTC
print(f'Начално общо количество BTC: {overall_btc:.8f}')
overall_busd = busd_active_quantity + btc_active_quantity * ground_price  # Равностойност в BUSD
print(f'Начално общо количество BUSD: {overall_busd:.2f}')



btc_repo = deque()  # хранилище за чакащи печалба изтъргувани количества BTC. Съдържа BUSD
busd_repo = deque()  # хранилище за чакащи печалба изтъргувани количества BUSD, Съдържа BTC
asset = ''  # определя коя валута се търгува понастоящем
btc_trade_price_list = deque()  # дек за вече търгувани цени за BTC
busd_trade_price_list = deque()  # дек за вече търгувани цени за BUSD


def split_active_quantity(asset):
    global btc_active_quantity
    global busd_active_quantity
    global ground_price
    global btc_repo
    global busd_repo
    global btc_trade_price_list
    global busd_trade_price_list
    global trade_qty_btc
    global trade_qty_busd
    print()
    print('РАЗДЕЛЯНЕ!!!')
    print()
    if asset == 'BTC':
        print('BTC -> BUSD')
        busd_active_quantity = (busd_active_quantity + btc_active_quantity*curr_price)/2
        print(f'Активен BUSD: {busd_active_quantity}')
        btc_active_quantity = busd_active_quantity / curr_price
        print(f'Активен BTC: {btc_active_quantity}')
        trade_qty_btc = btc_active_quantity / number_trades
        compare_quantities(curr_price)

    else:
        print('BUSD -> BTC')
        btc_active_quantity = (btc_active_quantity + busd_active_quantity /curr_price)/2
        print(f'Активен BTC: {btc_active_quantity}')
        busd_active_quantity = btc_active_quantity * curr_price
        print(f'Активен BUSD: {busd_active_quantity}')
        trade_qty_busd = busd_active_quantity / number_trades
        compare_quantities(curr_price)
    btc_repo = deque()
    busd_repo = deque()
    btc_trade_price_list = deque()
    busd_trade_price_list = deque()
    ground_price = curr_price
    print(f'Нова базова цена: {ground_price}')


def compare_quantities(trading_price):
    print()
    print(f'Активен BTC: {btc_active_quantity:.8f}  Печалба: {(btc_active_quantity / init_btc_active - 1) * 100:.2f}%')
    print(
        f'Активен BUSD: {busd_active_quantity:.2f}  Печалба: {(busd_active_quantity / init_busd_active - 1) * 100:.2f}%')
    curr_overall_btc = btc_active_quantity + busd_active_quantity / trading_price
    curr_overall_busd = busd_active_quantity + btc_active_quantity * trading_price
    print(f'Равностойност BTC: {curr_overall_btc:.8f}  Печалба: {(curr_overall_btc / overall_btc - 1) * 100:.2f}%')
    print(f'Равностойност BUSD: {curr_overall_busd:.2f} Печалба: {(curr_overall_busd / overall_busd - 1) * 100:.2f}%')


# Множител определящ какво количество от наличната валута ще се търгува на база определения вече максимален брой поръчки
def factor(trade_list):
    return 1 / (number_trades - len(trade_list))


# Изпълнява поръчка само ако има валутна наличност и цената е позволена
def execute_order(asset, profit_percentage):
    global btc_active_quantity
    global busd_active_quantity
    global transaction_count
    transaction_count += 1
    print()
    print('ИЗПЪЛНЕНИЕ!!!')
    print(f'Транзакция номер: {transaction_count}')
    print(f'Процент печалба: {profit_percentage}')
    print()
    if asset == 'BTC':
        print(f'Поръчка BTC номер: {len(btc_trade_price_list) + 1}')
        if len(btc_trade_price_list) != 0:
            trading_price = curr_price
            trade_quantity = btc_active_quantity * factor(btc_trade_price_list)
            print(f"{trade_quantity:.8f} BTC -> ", end='')
            btc_active_quantity -= trade_quantity
            trade_quantity *= trading_price
            busd_active_quantity += trade_quantity
            btc_repo.append({trading_price / profit_percentage: trade_quantity})
            btc_trade_price_list.append(trading_price)
            print(f'{trade_quantity:.2f} BUSD на цена: {trading_price:.2f}')
        else:
            trading_price = curr_price
            trade_quantity = btc_active_quantity * factor(btc_trade_price_list)
            print(f"{trade_quantity:.8f} BTC -> ", end='')
            btc_active_quantity -= trade_quantity
            trade_quantity *= trading_price
            busd_active_quantity += trade_quantity
            btc_repo.append({trading_price / profit_percentage: trade_quantity})
            btc_trade_price_list.append(trading_price)
            print(f'{trade_quantity:.2f} BUSD на цена: {trading_price:.2f}')


    else:
        print(f'Поръчка BUSD номер: {len(busd_trade_price_list) + 1}')
        if len(busd_trade_price_list) != 0:
            trading_price = curr_price
            trade_quantity = busd_active_quantity * factor(busd_trade_price_list)
            print(f"{trade_quantity:.2f} BUSD -> ", end='')
            busd_active_quantity -= trade_quantity
            trade_quantity /= trading_price
            btc_active_quantity += trade_quantity
            busd_trade_price_list.appendleft(trading_price)
            busd_repo.appendleft({trading_price * profit_percentage: trade_quantity})
            print(f'{trade_quantity:.8f} BTC на цена: {trading_price:.2f}')

        else:
            trading_price = curr_price
            trade_quantity = busd_active_quantity * factor(busd_trade_price_list)
            print(f"{trade_quantity:.2f} BUSD -> ", end='')
            busd_active_quantity -= trade_quantity
            trade_quantity /= trading_price
            btc_active_quantity += trade_quantity
            busd_trade_price_list.appendleft(trading_price)
            busd_repo.appendleft({trading_price * profit_percentage: trade_quantity})
            print(f'{trade_quantity:.8f} BTC на цена: {trading_price:.2f}')

    compare_quantities(trading_price)


# Проверява и изпълнява
def partial_profit(curr_price):
    global btc_active_quantity
    global busd_active_quantity
    if len(btc_repo) != 0:
        for price, qty in btc_repo[-1].items():
            if curr_price <= price:
                print()
                print('ПЕЧАЛБА!!!!')
                print(f'От BTC на цена: {curr_price:.2f}')
                busd_active_quantity -= qty
                btc_active_quantity += qty / price
                btc_trade_price_list.pop()
                btc_repo.pop()
                compare_quantities(curr_price)

    if len(busd_repo) != 0:
        for price, qty in busd_repo[0].items():
            if curr_price >= price:
                print()
                print('ПЕЧАЛБА!!!!')
                print(f'От BUSD на цена: {curr_price:.2f}')
                busd_active_quantity += qty * price
                btc_active_quantity -= qty
                busd_trade_price_list.popleft()
                busd_repo.popleft()
                compare_quantities(curr_price)


# Проверка дали текущата цена е в дековете с вече търгувани цени
def check_available_prices(asset, curr_price, profit_percentage):
    if asset == 'BTC':
        if len(btc_trade_price_list) != 0:
            if curr_price >= btc_trade_price_list[-1] * profit_percentage:
                return True
            else:
                return  False

        else:
            if curr_price< ground_price * profit_percentage:
                return False
            else:
                return True

    elif asset == 'BUSD':
        if len(busd_trade_price_list) != 0:
            if curr_price <= busd_trade_price_list[0] / profit_percentage:
                return True
            else:
                return False

        else:
            if curr_price > ground_price / profit_percentage:
                return False
            else:
                return True




print(f'Начална базова цена: {ground_price}')


def define_profit_percentage():
    avg_true = client.get_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_15MINUTE)
    average_value = 0
    for data in avg_true[496:]:
        average_value += (float(data[2]) - float(data[3]))
        # print(f'high: {data[2]}')
        # print(f'low: {data[3]}')
        # print('-------')
    average_value /= 4
    average_value/= curr_price
    average_value += 1

    return average_value


while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    if curr_price > ground_price:
        asset = 'BTC'
    elif curr_price < ground_price:
        asset = 'BUSD'
    partial_profit(curr_price)
    if curr_price == ground_price:
        continue
    if transaction_count == 0:
        profit_percentage = profit_percentage_defalut
    else:
        curr_percentage = define_profit_percentage()
        if (curr_percentage - 1) / 2 +1  <= profit_percentage_defalut:
            profit_percentage = profit_percentage_defalut
        else:
            profit_percentage = curr_percentage
    is_price_available = check_available_prices(asset, curr_price, profit_percentage)
    if is_price_available:

        if asset == 'BTC':
            execute_order(asset, profit_percentage)
            if len(btc_trade_price_list) == number_trades:
                split_active_quantity(asset)
        else:
            execute_order(asset, profit_percentage)
            if len(busd_trade_price_list) == number_trades:
                split_active_quantity(asset)
    time.sleep(1)