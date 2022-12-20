from asset import Asset

from general_methods import GeneralMethods
from binance.client import Client
from binance.enums import *
import time

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)
# asset_pairs_list = ['LTC/EUR','ETH/EUR', 'BTC/EUR', 'EUR/BUSD', 'LTC/ETH', 'LTC/BTC', 'LTC/BUSD', 'ETH/BTC', 'ETH/BUSD', 'BTC/BUSD']

asset_pairs_list = ['TRX/ETH', 'TRX/BTC', 'TRX/EUR', 'TRX/BUSD', 'ETH/EUR', 'BTC/EUR', 'EUR/BUSD', 'ETH/BTC',
                    'ETH/BUSD', 'BTC/BUSD']
access = GeneralMethods

transaction_count = 0
renorm_counter = 0
add_counter = 0
profit_percentage = 1.005

prices_dict = {}


def take_all_prices(prices_list):
    # global prices_dict
    for pairs in prices_list:
        joined_pair = ''.join(pairs.split('/'))
        prices_dict[pairs] = float(client.get_symbol_ticker(symbol=joined_pair)['price'])
    return prices_dict



prices_dict = take_all_prices(asset_pairs_list)
# busd_start_qty = float(client.get_asset_balance(asset= 'BUSD')['free'])
# busd = Asset(busd_start_qty, 'BUSD')
# xrp = Asset(access.multiply(busd.total_quantity, 1 / prices_dict["XRP/BUSD"]), 'XRP')
# eth = Asset(access.multiply(busd.total_quantity, 1 / prices_dict['ETH/BUSD']), 'ETH')
# btc = Asset(access.multiply(busd.total_quantity, 1 / prices_dict['BTC/BUSD']), 'BTC')
# trx = Asset(access.multiply(busd.total_quantity, 1 / prices_dict['TRX/BUSD']), 'TRX')
# eur  = Asset(access.multiply(busd.total_quantity, 1 / prices_dict["EUR/BUSD"]), 'EUR')
# ltc  = Asset(access.multiply(busd.total_quantity, 1 / prices_dict["LTC/BUSD"]), 'LTC')


asset_on_charge, asset_qty = access.get_asset_on_charge()

asset_order_list = ['TRX', 'ETH', 'BTC', 'EUR', "BUSD"]
primary_object_list = []
for asset in asset_order_list:
    primary_object_list.append(GeneralMethods.initialize_objects(asset_on_charge,
                                                                 asset_qty, asset, primary_object_list,
                                                                 prices_dict, asset_order_list))
trx, eth, btc, eur, busd = primary_object_list
obj_list = [trx, eth, btc, eur, busd]

print('Processing...')
print(f'Начален TRX: {trx.total_quantity}')
# print(f'Начален XRP: {xrp.total_quantity}')
print(f'Начален ETH: {eth.total_quantity}')
print(f'Начален BTC: {btc.total_quantity}')
print(f'Начален EUR: {eur.total_quantity}')
print(f'Начален BUSD: {busd.total_quantity}')
print(access.next_prices(asset_on_charge, {'TRX': trx.total_quantity, 'ETH': eth.total_quantity,
                                           'BTC': btc.total_quantity, 'EUR': eur.total_quantity,
                                           'BUSD': busd.total_quantity}, asset_pairs_list,
                         profit_percentage))
start = time.time()
while True:
    prices_dict = take_all_prices(asset_pairs_list)

    previous_asset = asset_on_charge
    asset_on_charge, price, pair = access.check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage,
                                                           asset_pairs_list)
    end = time.time()
    if asset_on_charge != previous_asset:
        transaction_count += 1
        start = time.time()
        print(access.execution_report(previous_asset, asset_on_charge, price, transaction_count, pair, obj_list))
        print(f'Текуща активна валута: {asset_on_charge}')
        print(f'TRX: {trx.total_quantity} Печалба: {(trx.total_quantity / trx.init_qty - 1) * 100:.2f}%')
        # print(f'XRP: {xrp.total_quantity} Печалба: {(xrp.total_quantity / xrp.init_qty - 1) * 100:.2f}%')
        print(f'ETH: {eth.total_quantity} Печалба: {(eth.total_quantity / eth.init_qty - 1) * 100:.2f}%')
        print(f'BTC: {btc.total_quantity} Печалба: {(btc.total_quantity / btc.init_qty - 1) * 100:.2f}%')
        print(f'EUR: {eur.total_quantity} Печалба: {(eur.total_quantity / eur.init_qty - 1) * 100:.2f}%')
        print(f'BUSD: {busd.total_quantity} Печалба: {(busd.total_quantity / busd.init_qty - 1) * 100:.2f}%')
        print(access.next_prices(asset_on_charge,
                                 {'TRX': trx.total_quantity, 'ETH': eth.total_quantity,
                                  'BTC': btc.total_quantity, 'EUR': eur.total_quantity, 'BUSD': busd.total_quantity},
                                 asset_pairs_list,
                                 profit_percentage))

        asset = float(client.get_asset_balance(asset="BNB")["free"])
        busd_price = float(client.get_symbol_ticker(symbol="BNBBUSD")['price'])
        print(f'BNB за комисионни: {asset} = {asset * busd_price} BUSD')
        GeneralMethods.check_for_bnb_commission()

    end = time.time()
    if end - start >= 7200:
        add_counter += 1
        # print(access.normalize_quantities(asset_on_charge, obj_list, prices_dict))
        print('--------ДОБАВЯНЕ НА КОЛИЧЕСТВО---------')
        print(f'Добавяне номер: {add_counter}')
        for obj in obj_list:
            if obj.name == asset_on_charge:
                print(f'Старо количество {asset_on_charge}: {obj.total_quantity}')
                if asset_on_charge != 'BUSD':
                    pair = f'{asset_on_charge}USDT'
                    price = float(client.get_symbol_ticker(symbol=pair)['price'])
                    quantity = 11 / price
                    precise_num = GeneralMethods.get_accuracy_num(pair)[0]
                    quantity = GeneralMethods.get_precise_qty(quantity, precise_num)
                    client.create_order(symbol=pair, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                        quantity=quantity)
                else:
                    pair = f'{asset_on_charge}USDT'
                    client.create_order(symbol=pair, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                        quantity=11)
                obj.total_quantity = float(client.get_asset_balance(asset=asset_on_charge)['free'])
                print(f'Ново количество {asset_on_charge}: {obj.total_quantity}')
                print(GeneralMethods.normalize_quantities(asset_on_charge, obj_list, prices_dict))

        print(access.next_prices(asset_on_charge, {'TRX': trx.total_quantity, 'ETH': eth.total_quantity,
                                                   'BTC': btc.total_quantity, 'EUR': eur.total_quantity,
                                                   'BUSD': busd.total_quantity}, asset_pairs_list,
                                 profit_percentage))

        start = time.time()
        # renorm_counter =   transaction_count
    time.sleep(2)
