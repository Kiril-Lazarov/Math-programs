from binance.enums import *
from binance.client import Client
import time

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)
# #
# # # print(client.get_account_status(user_name = 'Anonymous-User-0fa8e', user_id = 40055004))
# # print(client.get_asset_balance(asset='USDT')['free'])
# # print(client.get_asset_balance(asset='BTC')['free'])
# # # print(client.get_asset_balance(asset='BUSD')['free'])
# # btc_qty = client.get_asset_balance(asset= 'BTC')['free']
# # btc_qty = ''.join(list(btc_qty[:7]))
# #
# # # curr_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
# # # print(f'Цена: {20/curr_price:.5f}')
# # order = client.order_market_sell(
# #     symbol='BTCUSDT',
# #     quantity=float(btc_qty))
# # print(client.get_asset_balance(asset='USDT')['free'])
# # print(client.get_asset_balance(asset='BTC')['free'])
# # print(client.get_asset_balance(asset='BNB')['free'])
# #
# #
# # amount = 100.000234234
# # precision = 5
# # amt_str = "{:0.0{}f}".format(amount, precision)
# # print(amt_str)

# print('--------------------')
# # order = client.order_limit_sell(symbol='TRXBUSD', quantity= 660, price= '0.08')
# qty = 46.05/21000
# client.create_order(symbol='BTCBUSD', side = SIDE_BUY, type= ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC,
#                     quantity= float(f'{qty:.5f}'), price= '21000')
# print(client.get_open_orders(symbol='BTCBUSD'))
# # print(client.get_ticker())

#

# trx = 200
# dot = 1.8329
# trxeth = float(client.get_symbol_ticker(symbol="TRXETH")['price'])
# doteth = float(client.get_symbol_ticker(symbol="DOTETH")['price'])
# dotbusd = float(client.get_symbol_ticker(symbol="DOTBUSD")['price'])
# trxbusd = float(client.get_symbol_ticker(symbol="TRXBUSD")['price'])
# print(f'DOTETH: {doteth}')
# print(f'TRXETH {trxeth}')
# print(f'TRXBUSD {trxbusd}')
# print(f'DOTBUSD {dotbusd}')
# newethdot =  trx*trxeth/doteth
# newbusddot = trx*trxbusd/dotbusd
# print(f'TRXDOT през ETH:{trx*trxeth/doteth}')
# print(f'TRXDOT през BUSD:{trx*trxbusd/dotbusd}')
# print(f'DOTTRX  през ETH: {newethdot*doteth/trxeth}')
# print(f'DOTTRX  през BUSD: {newbusddot*dotbusd/trxbusd}')



# print(client.get_symbol_info(symbol="ETHBUSD"))
# print(client.get_symbol_info(symbol="XRPBUSD"))
# print(client.get_symbol_info(symbol="BTCBUSD"))
# data = client.get_my_trades(symbol='XRPBUSD')[-1]
# print(data)
# print(data['price'])
# print(data['qty'])
# print(data['quoteQty'])
# print(client.get_my_trades(symbol='BTCUSDT')[-1])
# print(client.get_my_trades(symbol='BTCUSDT')[-1]['price'])
# print(client.get_my_trades(symbol='BTCUSDT')[-1]['quoteQty'])
#
# busd = 500
# eth = 0.01400494
# btc = 0.01
# eur = 200
# ethbusd = float(client.get_symbol_ticker(symbol='ETHBUSD')['price'])
# btcbusd = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
# # ethbtc = float(client.get_symbol_ticker(symbol='ETHBTC')['price'])
# eurbusd = float(client.get_symbol_ticker(symbol='EURBUSD')['price'])
# etheur = float(client.get_symbol_ticker(symbol='ETHEUR')['price'])
#
#
# print(f'НАчален BTC: {busd/btcbusd}')
# print(f'Начален ETH: {busd/ethbusd}')
# print(f'Начален BUSD: {eur*eurbusd}')
# print(f'Обръщане на eth в busd{eur/etheur*ethbusd}')

# client.order_limit_sell(symbol='BUSDUSDT', qty=600.81, price='1.0000')
# order = client.create_order(
#     symbol='BUSDUSDT',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=600.81,
#     price='1.000')



print(client.get_asset_balance(asset='BUSD'))



