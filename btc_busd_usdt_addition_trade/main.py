from binance.client import Client

import time
from asset import Asset

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)

transactions_count = 0
busd = Asset('BUSD', 100)
btc = Asset('BTC',busd.qty / float(client.get_symbol_ticker(symbol= 'BTCBUSD')['price']))
# btc = Asset('BTC',busd.qty/ 22000)
btc.init_qty = btc.take_total_qty(btc,busd)
btc.base_qty = btc.init_qty
busd.init_qty = busd.take_total_qty(busd, btc)
busd.base_qty = busd.init_qty
print(busd)
print(btc)
print(client.get_symbol_ticker(symbol= 'BTCBUSD')['price'])
print(busd.next_prices(busd, btc, busd.profit_percentage))
print(btc.next_prices(btc, busd, btc.profit_percentage))
print(Asset.profit_info(btc, busd))


while True:
    if btc.check_for_increase(btc, busd):
        btc.increase_level(btc)
        print(btc.next_prices(btc,busd,btc.profit_percentage))
        print(btc.next_prices(btc, busd, btc.execution_percentage))
    if btc.check_for_execution(btc, busd):
        transactions_count += 1
        print(busd.execution(busd, btc, transactions_count))
        print(busd.next_prices(busd, btc, busd.profit_percentage))
        print(btc.next_prices(btc, busd, btc.profit_percentage))
        print(Asset.profit_info(btc, busd))
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
        print(btc)
        print(busd)

    time.sleep(1)


