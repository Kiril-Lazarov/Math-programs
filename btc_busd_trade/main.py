from binance.client import Client

import time
from asset import Asset

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)


def get_initial_qties():
    price = Asset.take_curr_price('BTCBUSD')
    btc = Asset('BTC', Asset.get_qty('BTC'))
    busd = Asset('BUSD', Asset.get_qty('BUSD'))
    if btc.qty * price > 100:
        btc.on_charge = True
        busd.qty = btc.qty * price
        busd.init_qty = busd.qty

    elif busd.qty > 100:
        busd.on_charge = True
        btc.qty = busd.qty / price
        btc.init_qty = btc.qty

    return btc, busd


btc, busd = get_initial_qties()


class Main(Asset):

    @classmethod
    def get_profits(cls):
        return f'Начален BTC: {btc.init_qty}\nТекущ BTC: {btc.qty}\n' \
               f'Печалба: {(btc.qty / btc.init_qty - 1) * 100:.2f}%\n' \
               f'Начален BUSD: {busd.init_qty}\nТекущ BUSD: {busd.qty}\n' \
               f'Печaлба: {(busd.qty / busd.init_qty - 1) * 100:.2f}%'

    @classmethod
    def check_time(cls, start, end):
        if end - start >= time_interval_const:
            return True
        return False


transaction_count = 0
add_count = 0
time_interval_const = 600
start = time.time()

print(f'Начален BTC: {btc.qty}')
print(f'Начален активен BTC: {btc.init_qty}')
print(f'Начален BUSD: {busd.init_qty}')
print(f'Начален активен BUSD: {busd.qty}')
asset_on_charge_obj = ''
other_obj = ''
if btc.on_charge:
    print('BTC on charge')
    asset_on_charge_obj = btc
    other_obj = busd
elif busd.on_charge:
    print('BUSD on charge')
    asset_on_charge_obj = busd
    other_obj = btc
print(Asset.get_next_price(asset_on_charge_obj, other_obj))

while True:
    asset_on_charge = 'BUSD' if busd.on_charge else 'BTC'
    if Asset.check_for_profit(asset_on_charge, btc, busd):
        transaction_count += 1

        print(f'Поръчка номер: {transaction_count}')
        print(Asset.execution(asset_on_charge, btc, busd))
        print(Main.get_profits())
        asset_on_charge_obj = btc if btc.on_charge else busd
        other_obj = busd if asset_on_charge_obj == btc else btc
        print(Asset.get_next_price(asset_on_charge_obj, other_obj))
        start = time.time()
    end = time.time()
    if Main.check_time(start, end):
        print(Main.add_quantity(add_count, btc, busd))
        print(Main.get_profits())
        asset_on_charge_obj = btc if btc.on_charge else busd
        other_obj = busd if asset_on_charge_obj == btc else btc
        print(Asset.get_next_price(asset_on_charge_obj, other_obj))
        start = time.time()

    time.sleep(2)
