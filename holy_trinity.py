import time

from asset_migration.asset import Asset
from binance.client import Client
from binance.enums import *

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )

eth = 0.349013
btc = 0.02361782
busd = 500

profit_percentage = 0.05

ethbusd = float(client.get_symbol_ticker(symbol='ETHBUSD')['price'])
btcbusd = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
ethbtc = float(client.get_symbol_ticker(symbol='ETHBTC')['price'])

init_btc= eth*ethbtc + busd/btcbusd
init_eth = eth + busd/ethbusd
init_busd = busd + eth* ethbusd

base_btc = init_btc
base_eth = init_eth
base_busd = init_busd

active_busd_init = busd
active_eth_init = eth
print(f'Начален общ ETH: {init_eth}  активен ETH: {eth}')
print(f'Начален общ BTC: {init_btc}')
print(f'Начален общ BUSD: {init_busd} активен BUSD: {busd}')
transaction_count = 0
while True:

    is_profit = False
    ethbusd = float(client.get_symbol_ticker(symbol='ETHBUSD')['price'])
    btcbusd = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    # ethbtc = float(client.get_symbol_ticker(symbol='ETHBTC')['price'])

    # total_btc = eth * ethbtc + busd / btcbusd
    # total_eth = eth + busd / ethbusd
    # total_busd = busd + eth * ethbusd

    total_busd = eth*ethbusd + btc*btcbusd
    # profit_eth = float(f'{(total_eth / base_eth - 1) * 100:.2f}')
    # profit_btc = float(f'{(total_btc / base_btc - 1) * 100:.2f}')
    profit_busd = float(f'{(total_busd / base_busd - 1) * 100:.2f}')

    # if profit_eth >= profit_percentage:
    #     is_profit = True
    #     print('-------ПЕЧАЛБА-------')
    #     eth = total_eth / 2
    #     busd = eth * ethbusd
    #     base_eth = total_eth
    # if profit_btc >= profit_percentage:
    #     is_profit = True
    #     print('-------ПЕЧАЛБА-------')
    #     btc_to_trade = total_btc / 2
    #     eth = btc_to_trade / ethbtc
    #     busd = btc_to_trade * btcbusd
    #     base_btc = total_btc
    if profit_busd >= profit_percentage:
        is_profit = True
        print('-------ПЕЧАЛБА-------')
        base_busd = total_busd
        busd = total_busd / 2
        eth = busd / ethbusd
        # base_busd = total_busd
        btc = busd/btcbusd
    if is_profit:
        transaction_count+=1
        print(f'Поръчка номер: {transaction_count}')
        #
        # print(f'Начален общ ETH: {init_eth}  активен ETH: {eth} Печалба активен ETH: {(eth/active_eth_init-1)*100:.2f}%')
        # print(f'Начален общ BTC: {init_btc}')
        print(f'Начален общ BUSD: {init_busd} активен BUSD: {busd} Печалба активен BUSD: {(busd/active_busd_init -1)*100:.2f}%')
        print(f'Активен BTC: {btc}')
        print(f'Активен ETH: {eth}')

        # print(f'Курс ETH/BTC: {ethbtc}')
        print(f'Курс ETH/BUSD: {ethbusd}')
        print(f'Курс BTC/BUSD: {btcbusd}')

        # print(f'Печалба ETH: {(total_eth / init_eth - 1) * 100:.2f}%')
        # print(f'Печалба BTC: {(total_btc / init_btc - 1) * 100:.2f}%')
        print(f'Печалба BUSD: {(total_busd / init_busd - 1) * 100:.2f}%')

    time.sleep(2)

