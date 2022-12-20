from asset import Asset

from general_methods import GeneralMethods
from binance.client import Client
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)
asset_pairs_list = ['TRX/XRP','TRX/ETH','TRX/BTC','TRX/BUSD','XRP/ETH',
                    'XRP/BTC', 'XRP/BUSD', 'ETH/BTC', 'ETH/BUSD', 'BTC/BUSD']
access = GeneralMethods

transaction_count = 0
renorm_counter = 0
profit_percentage = 1.003
profit_step = 0.00005

prices_dict = {}
def take_all_prices(prices_list):
    global prices_dict
    for pairs in prices_list:
        joined_pair = ''.join(pairs.split('/'))
        prices_dict[pairs] = float(client.get_symbol_ticker(symbol=joined_pair)['price'])
    return prices_dict



# prices_dict = {}
prices_dict = take_all_prices(asset_pairs_list)
print(prices_dict)
busd = Asset(300, 'BUSD')
xrp = Asset(access.multiply(busd.quantity, 1 / prices_dict["XRP/BUSD"]), 'XRP')
eth = Asset(access.multiply(busd.quantity, 1 / prices_dict['ETH/BUSD']), 'ETH')
btc = Asset(access.multiply(busd.quantity, 1 / prices_dict['BTC/BUSD']), 'BTC')
trx = Asset(access.multiply(busd.quantity, 1 / prices_dict['TRX/BUSD']), 'TRX')
obj_list = [trx,xrp, eth, btc, busd]
asset_on_charge = busd.name
print('Processing...')
print(f'Начален TRX: {trx.quantity}')
print(f'Начален XRP: {xrp.quantity}')
print(f'Начален ETH: {eth.quantity}')
print(f'Начален BTC: {btc.quantity}')
print(f'Начален BUSD: {busd.quantity}')
print(access.next_prices(asset_on_charge, {'TRX': trx.quantity, 'XRP': xrp.quantity, 'ETH': eth.quantity,
                                           'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                         profit_percentage))
start = time.time()
while True:
    prices_dict = take_all_prices(asset_pairs_list)


    previous_asset = asset_on_charge
    asset_on_charge, price = access.check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage, profit_step)
    end = time.time()
    if asset_on_charge != previous_asset:
        transaction_count+=1
        start = time.time()
        print(access.execution_report(previous_asset, asset_on_charge, price, transaction_count))
        print(f'Текуща активна валута: {asset_on_charge}')
        print(f'TRX: {trx.quantity} Печалба: {(trx.quantity / trx.init_qty - 1) * 100:.2f}%')
        print(f'XRP: {xrp.quantity} Печалба: {(xrp.quantity/ xrp.init_qty - 1)* 100:.2f}%')
        print(f'ETH: {eth.quantity} Печалба: {(eth.quantity/ eth.init_qty - 1)* 100:.2f}%')
        print(f'BTC: {btc.quantity} Печалба: {(btc.quantity/ btc.init_qty - 1)* 100:.2f}%')
        print(f'BUSD: {busd.quantity} Печалба: {(busd.quantity/ busd.init_qty - 1)* 100:.2f}%')
        print(access.next_prices(asset_on_charge, {'TRX': trx.quantity,'XRP': xrp.quantity, 'ETH': eth.quantity,
                                                   'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                                 profit_percentage))

    end = time.time()
    if end - start >= 20:
        # print(access.normalize_quantities(asset_on_charge, obj_list, prices_dict))
        print('--------ДОБАВЯНЕ НА КОЛИЧЕСТВО---------')

        for obj in obj_list:
            if obj.name == asset_on_charge:
                print(f'Старо количество {asset_on_charge}: {obj.quantity}')
                if asset_on_charge != 'BUSD':
                    obj.quantity += 10 / float(client.get_symbol_ticker(symbol= f'{asset_on_charge}BUSD')['price'])
                else:
                    obj.quantity += 10
                print(f'Ново количество {asset_on_charge}: {obj.quantity}')
        print(access.next_prices(asset_on_charge, {'TRX': trx.quantity, 'XRP': xrp.quantity, 'ETH': eth.quantity,
                                                   'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                                 profit_percentage))

        start = time.time()
        # renorm_counter =   transaction_count
    time.sleep(1)
