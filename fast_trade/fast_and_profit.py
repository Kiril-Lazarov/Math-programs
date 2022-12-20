from collections import deque
import time
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)


def initialize_price_levels(ground_price, asset, init_step_percentage):
    final_list = [ground_price]
    if asset == 'BTC':
        for i in range(number_trades):
            if i < 3:
                init_step_percentage = init_step_percentage
            elif i < 5:
                init_step_percentage += 0.0003
            elif i < 8:
                init_step_percentage += 0.0005
            else:
                init_step_percentage += 0.008
            final_list.append(final_list[i] * init_step_percentage)
    else:
        for i in range(number_trades):
            if i < 3:
                init_step_percentage = init_step_percentage
            elif i < 5:
                init_step_percentage += 0.0003
            elif i < 8:
                init_step_percentage += 0.0005
            else:
                init_step_percentage += 0.008

            final_list.append(final_list[i] / init_step_percentage)
    return final_list[1:]


print('Processing...')
transaction_count = 0
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
print(f'ground_price: {ground_price}')
init_step_percentage = 1.001
asset = ''
number_trades = 8
btc_active_qty = 0.02651
busd_active_qty = 844
init_btc_overall_qty = btc_active_qty + busd_active_qty / ground_price
init_busd_overall_qty = init_btc_overall_qty * ground_price
btc_active_qty = init_btc_overall_qty/2
busd_active_qty = btc_active_qty * ground_price
init_active_btc = btc_active_qty
init_active_busd = busd_active_qty
new_overall_btc = init_btc_overall_qty
new_overall_busd = init_busd_overall_qty
print(f'Init btc: {init_btc_overall_qty}')
print(f'Init busd: {init_busd_overall_qty}')
print(f'Start BTC active: {btc_active_qty}')
print(f'Start BUSD active: {busd_active_qty}')
btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)
busd_prices_list = initialize_price_levels(ground_price, 'BUSD', init_step_percentage)
initialize_price_levels(ground_price, 'BUSD', init_step_percentage)
# print(btc_prices_list)
# print(busd_prices_list)


def define_qty(asset, length_btc, length_busd):
    # factor = 0
    # a = 0
    # if asset == 'BTC':
    #     if number_trades - length_btc > 8:
    #         a = 8
    #     elif number_trades - length_btc > 7:
    #         a = 6
    #     elif number_trades - length_btc > 3:
    #         a = 3
    #     factor = 1 / (number_trades + a - (8 - length_btc))
    #
    # elif asset == 'BUSD':
    #     if number_trades - length_busd > 8:
    #         a = 8
    #     elif number_trades - length_busd > 7:
    #         a = 6
    #     elif number_trades - length_busd > 3:
    #         a = 3
    #     factor = 1 / (number_trades + a - (8 - length_busd))
    return 0.2


def execution(price, asset, curr_price):
    print()
    print(f'CURR price: {curr_price}')
    global btc_active_qty
    global busd_active_qty
    global transaction_count
    transaction_count+=1
    print()
    print(f'Поръчка номер: {transaction_count}')
    if asset == 'BTC':
        qty = define_qty(asset, len(btc_prices_list), len(busd_prices_list)) * btc_active_qty
        btc_active_qty -= qty
        busd_active_qty += qty * curr_price
        print(f'Транзакция {qty:.8f} BTC -> {qty * curr_price:.2f} BUSD на цена: {curr_price:.2f}')

    elif asset == 'BUSD':
        qty = define_qty(asset, len(btc_prices_list), len(busd_prices_list)) * busd_active_qty
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


def split_qtyes(curr_price, asset):
    global btc_active_qty
    global busd_active_qty
    global ground_price
    global btc_prices_list
    global busd_prices_list
    if asset == 'BTC':
        total_busd = busd_active_qty + btc_active_qty * curr_price
        print(f'Тотал BUSD: {total_busd:.2f} печалба: {(total_busd / init_busd_overall_qty - 1) * 100:.2f}%')
        total_btc = total_busd / curr_price
        print(f'Тотал BTC: {total_btc:.8f} печалба: {(total_btc / init_btc_overall_qty - 1) * 100:.2f}%')
        total_busd /= 2
        btc_active_qty = total_busd / curr_price
        busd_active_qty = total_busd
    elif asset == 'BUSD':
        total_btc = btc_active_qty + busd_active_qty / curr_price
        print(f'Тотал BTC: {total_btc:.8f} печалба: {(total_btc / init_btc_overall_qty - 1) * 100:.2f}%')
        total_busd = total_btc * curr_price
        print(f'Тотал BUSD: {total_busd:.2f} печалба: {(total_busd / init_busd_overall_qty - 1) * 100:.2f}%')
        total_btc /= 2
        busd_active_qty = total_btc * curr_price
        btc_active_qty = total_btc
    print(f'BTC актив: {btc_active_qty:.8f}')
    print(f'BUSD актив: {busd_active_qty:.2f}')
    ground_price = curr_price
    busd_prices_list = initialize_price_levels(ground_price, 'BUSD', init_step_percentage)
    btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)
    print()
    print(f'Ground price: {ground_price:.2f}')


while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    if curr_price > ground_price:
        asset = 'BTC'
        if curr_price >= btc_prices_list[0]:
            execution(btc_prices_list[0], asset, curr_price)
            del btc_prices_list[0]
            if len(busd_prices_list) != number_trades:
                print()
                print('ПЕЧАЛБА!!!')
                print()
                curr_overall_btc = btc_active_qty + busd_active_qty / curr_price
                curr_overall_busd = busd_active_qty + btc_active_qty * curr_price
                print(f'Активен BTC: {btc_active_qty} печалба: {(btc_active_qty/init_active_btc - 1)*100:.2f}%')
                print(f'Активен BUSD: {busd_active_qty} печалба: {(busd_active_qty/init_active_busd - 1)*100:.2f}%')
                print(
                    f'Тотал BUSD: {curr_overall_busd:.2f} печалба: {(curr_overall_busd / init_busd_overall_qty - 1) * 100:.2f}%')
                print(
                    f'Тотал BTC: {curr_overall_btc:.8f} печалба: {(curr_overall_btc / init_btc_overall_qty - 1) * 100:.2f}%')
                busd_prices_list = initialize_price_levels(ground_price, 'BUSD', init_step_percentage)

    elif curr_price < ground_price:
        asset = 'BUSD'
        if curr_price <= busd_prices_list[0]:
            execution(busd_prices_list[0], asset, curr_price)
            del busd_prices_list[0]
            # print(f'New busd list: {busd_prices_list}')
            if len(btc_prices_list) != number_trades:
                print()
                print('ПЕЧАЛБА!!!')
                print()
                curr_overall_btc = btc_active_qty + busd_active_qty / curr_price
                curr_overall_busd = busd_active_qty + btc_active_qty * curr_price
                print(f'Активен BTC: {btc_active_qty} печалба: {(btc_active_qty/init_active_btc - 1)*100:.2f}%')
                print(f'Активен BUSD: {busd_active_qty} печалба: {(busd_active_qty/init_active_busd - 1)*100:.2f}%')
                print(
                    f'Тотал BUSD: {curr_overall_busd:.2f} печалба: {(curr_overall_busd / init_busd_overall_qty - 1) * 100:.2f}%')
                print(
                    f'Тотал BTC: {curr_overall_btc:.8f} печалба: {(curr_overall_btc / init_btc_overall_qty - 1) * 100:.2f}%')
                btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)

    if len(btc_prices_list) == number_trades - 6 or len(busd_prices_list) == number_trades -6:
        print()
        print("СМЯНА GROUND LEVEL!!!", end='\n')
        # if len(btc_prices_list) == 0:
        #     split_qtyes(curr_price, "BUSD")
        ground_price = curr_price
        busd_prices_list = initialize_price_levels(ground_price, 'BUSD', init_step_percentage)
        btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)
        print()
        print(f'Ground price: {ground_price:.2f}')