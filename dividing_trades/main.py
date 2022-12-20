from busd import Busd
from btc import Bitcoin

from trade_methods import TradeMethods
from binance.client import Client
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)
curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
print(f'curr price: {curr_price}')

trade_number = 20
profit_percentage = 1.0007195
profit_step = 0.00003
profit_level = 0.07
init_btc = 0.06839651 / 2
init_busd = init_btc * curr_price
transaction_count = 0
print(f'init_btc: {init_btc}')
print(f'init_busd: {init_busd}')

access = TradeMethods()

busd = Busd(init_btc)
btc = Bitcoin(init_busd)
btc.quantity = init_btc
busd.quantity = init_busd
btc.btc_base_total_qty = init_btc + init_busd / curr_price
busd.busd_base_total_qty = init_busd + init_btc * curr_price
total_init_btc = btc.btc_base_total_qty
total_init_busd = busd.busd_base_total_qty
btc.btc_profit_percentage = profit_percentage
busd.busd_profit_percentage = profit_percentage

print(btc.btc_base_total_qty)
print(busd.busd_base_total_qty)
access.next_execution_prices(curr_price, btc.btc_base_total_qty, btc.quantity, busd.busd_base_total_qty,
                             busd.quantity, btc.btc_profit_percentage, busd.busd_profit_percentage)

while True:
    # curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    curr_price = float(input('Въведи цена: '))
    curr_total_btc, curr_total_busd = access.get_total_quantities(curr_price, btc.quantity, busd.quantity)
    is_execution = False
    if curr_total_btc / btc.btc_base_total_qty >= btc.btc_profit_percentage:
        is_execution = True
        btc.quantity, busd.quantity = access.execution(curr_price, btc.quantity, btc.btc_trades_number, busd.quantity,
                                                       busd.busd_trades_number,
                                                       trade_number, 'BUSD')
        if busd.busd_trades_number < -100:
            busd.busd_trades_number = 0
            btc.btc_trades_number = 0
        else:
            btc.btc_trades_number = btc.sumation(btc.btc_trades_number, -1)
            busd.busd_trades_number = busd.sumation(busd.busd_trades_number, 1)
        btc.btc_base_total_qty = curr_total_btc

    if curr_total_busd / busd.busd_base_total_qty >= busd.busd_profit_percentage:
        is_execution = True
        btc.quantity, busd.quantity = access.execution(curr_price, btc.quantity, btc.btc_trades_number, busd.quantity,
                                                       busd.busd_trades_number,
                                                       trade_number, 'BTC')
        if btc.btc_trades_number < -100:
            btc.btc_trades_number = 0
            busd.busd_trades_number = 0
        else:
            btc.btc_trades_number = btc.sumation(btc.btc_trades_number, 1)
            busd.busd_trades_number = busd.sumation(busd.busd_trades_number, -1)
        busd.busd_base_total_qty = curr_total_busd

    is_split = access.check_for_split(total_init_btc, btc.quantity, btc.btc_reached_profit,
                                      total_init_busd, busd.quantity, busd.busd_reached_profit,
                                      curr_price, profit_level)
    if is_split[0] or abs(btc.btc_trades_number)==30:
        btc.quantity, busd.quantity = access.split(curr_price, btc.quantity, busd.quantity)
        btc.btc_base_total_qty, busd.busd_base_total_qty = access.get_total_quantities(curr_price, btc.quantity,
                                                                                       busd.quantity)
        btc.btc_reached_profit = is_split[1]
        busd.busd_reached_profit = is_split[2]
        btc.btc_trades_number, busd.busd_trades_number = 0, 0
    if is_execution or is_split[0]:
        btc.btc_profit_percentage, busd.busd_profit_percentage = \
            access.change_profit_percentage(btc.btc_trades_number, busd.busd_trades_number,
                                            profit_percentage,profit_step, curr_price)



        access.next_execution_prices(curr_price, btc.btc_base_total_qty, btc.quantity, busd.busd_base_total_qty,
                                     busd.quantity, btc.btc_profit_percentage, busd.busd_profit_percentage)

        transaction_count += 1
        print(f'Поръчка номер: {transaction_count}')
        print(f'Активен BTC: {btc.quantity:.8f}\nОбщо BTC: {curr_total_btc:.8f}')
        print(f'Базов BTC: {btc.btc_base_total_qty:.8f}')
        print(f'Начален BTC: {init_btc * 2:.8f} печалба: {(curr_total_btc / total_init_btc - 1) * 100:.2f}%')
        print(f'Активен BUSD: {busd.quantity:.2f}\nОбщо BUSD: {curr_total_busd:.2f}')
        print(f'Базов BUSD: {busd.busd_base_total_qty:.2f}')
        print(f'Начален BUSD: {init_busd * 2:.2f} печалба: {(curr_total_busd / total_init_busd - 1) * 100:.2f}%')
        print(f'Поредна BTC поръчка: {btc.btc_trades_number}\nПоредна BUSD поръчка: {busd.busd_trades_number}')
        print(f'BTC процент печалба: {btc.btc_profit_percentage}\nBUSD процент печалба: {busd.busd_profit_percentage}')

    time.sleep(1)
