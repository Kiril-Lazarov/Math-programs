# from collections import deque
import time
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

btc_trades_count = 0
busd_trades_count = 0
def initialize_price_levels(ground_price, init_step_percentage, btc_count, busd_count):
    # final_list = [ground_price]
    # if asset == 'BTC':
    #     for i in range(number_trades):
    #         if i < 3:
    #             init_step_percentage += 0.002
    #         elif i < 5:
    #             init_step_percentage += 0.0003
    #         elif i < 8:
    #             init_step_percentage += 0.0004
    #         else:
    #             init_step_percentage += 0.005
    #         final_list.append(final_list[i] * init_step_percentage)
    #
    #
    # else:
    #     for i in range(number_trades):
    #         if i < 3:
    #             init_step_percentage += 0.002
    #         elif i < 5:
    #             init_step_percentage += 0.0003
    #         elif i < 8:
    #             init_step_percentage += 0.0004
    #         else:
    #             init_step_percentage += 0.005
    #
    #         final_list.append(final_list[i] / init_step_percentage)
    final_list = [ground_price / (init_step_percentage + busd_count * 0.005),
                                  ground_price * (init_step_percentage + btc_count * 0.005)]
    print(f'Следващи цени: {final_list}')
    return final_list


print('Processing...')
transaction_count = 0
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
print(f'ground_price: {ground_price}')
init_step_percentage = 1.005
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
prices_list = initialize_price_levels(ground_price, init_step_percentage, btc_trades_count, busd_trades_count)



def define_qty(trades_count):
    return 1/(number_trades - trades_count)


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
        qty = define_qty(btc_trades_count) * btc_active_qty
        btc_active_qty -= qty
        busd_active_qty += qty * curr_price
        print(f'Транзакция {qty:.8f} BTC -> {qty * curr_price:.2f} BUSD на цена: {curr_price:.2f}')

    elif asset == 'BUSD':
        qty = define_qty(busd_trades_count) * busd_active_qty
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





while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    if curr_price > ground_price:
        asset = 'BTC'
        if curr_price >= prices_list[-1]:
            execution(prices_list[-1], asset, curr_price)
            btc_trades_count +=1
            busd_trades_count -=1
            print(f'BTC trade counter: {btc_trades_count}')
            print(f'BUSD trade counter: {busd_trades_count}')
            ground_price = curr_price
            prices_list = initialize_price_levels(ground_price, init_step_percentage, btc_trades_count, 0)


    elif curr_price < ground_price:
        asset = 'BUSD'
        if curr_price <= prices_list[0]:
            execution(prices_list[0], asset, curr_price)
            busd_trades_count+=1
            btc_trades_count -= 1
            print(f'BTC trade counter: {btc_trades_count}')
            print(f'BUSD trade counter: {busd_trades_count}')
            ground_price = curr_price
            prices_list = initialize_price_levels(ground_price, init_step_percentage, 0, busd_trades_count)
            # del busd_prices_list[0]
            # print(f'New busd list: {busd_prices_list}')
            # if len(btc_prices_list) != number_trades:
            #     print()
            #     print('ПЕЧАЛБА!!!')
            #     print()
            #     curr_overall_btc = btc_active_qty + busd_active_qty / curr_price
            #     curr_overall_busd = busd_active_qty + btc_active_qty * curr_price
            #     print(f'Активен BTC: {btc_active_qty} печалба: {(btc_active_qty/init_active_btc - 1)*100:.2f}%')
            #     print(f'Активен BUSD: {busd_active_qty} печалба: {(busd_active_qty/init_active_busd - 1)*100:.2f}%')
            #     print(
            #         f'Тотал BUSD: {curr_overall_busd:.2f} печалба: {(curr_overall_busd / init_busd_overall_qty - 1) * 100:.2f}%')
            #     print(
            #         f'Тотал BTC: {curr_overall_btc:.8f} печалба: {(curr_overall_btc / init_btc_overall_qty - 1) * 100:.2f}%')
            #     btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)

    # if len(btc_prices_list) == number_trades - 4 or len(busd_prices_list) == number_trades -4:
    #     print()
    #     print("СМЯНА GROUND LEVEL!!!", end='\n')
    #     # if len(btc_prices_list) == 0:
    #     #     split_qtyes(curr_price, "BTC")
    #     # elif len(busd_prices_list) == 0:
    #     #     split_qtyes(curr_price, "BUSD")
    #     ground_price = curr_price
    #     busd_prices_list = initialize_price_levels(ground_price, 'BUSD', init_step_percentage)
    #     btc_prices_list = initialize_price_levels(ground_price, 'BTC', init_step_percentage)
    #     print()
    #     print(f'Ground price: {ground_price:.2f}')
    time.sleep(1)