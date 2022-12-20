from binance.client import Client
from assets import  Assets
import time

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)
# eth = Assets('ETH', 0.13, True)
# btc = Assets('BTC', 1)
# eur = Assets('EUR', 1)
# busd = Assets('BUSD', 100, True)
# assets = [eth, btc, eur, busd]

asset_pairs_list = ['ETH/EUR', 'BTC/EUR', 'EUR/BUSD', 'ETH/BTC', 'ETH/BUSD', 'BTC/BUSD']

mig_obj1 =Assets('ETH', 0.12898)
mig_obj2 = Assets('BUSD', 204.02)
prices_dict = {}
def take_all_prices(prices_list):
    global prices_dict
    for pairs in prices_list:
        joined_pair = ''.join(pairs.split('/'))
        prices_dict[pairs] = float(client.get_symbol_ticker(symbol=joined_pair)['price'])

    return prices_dict
prices_dict = take_all_prices(asset_pairs_list)
migration_objects = [mig_obj1, mig_obj2]
profit_percentage = 1.003
print('На ETH')
mig_obj1.take_new_quantites(mig_obj1.name, prices_dict)
print(mig_obj1.next_prices(mig_obj1.name, asset_pairs_list, profit_percentage))
print('На BUSD')
mig_obj2.take_new_quantites(mig_obj2.name, prices_dict)
print(mig_obj2.next_prices(mig_obj2.name, asset_pairs_list, profit_percentage))


transaction_count = 0

print(mig_obj1)
print(mig_obj2)

while True:
    prices_dict = take_all_prices(asset_pairs_list)
    for obj in migration_objects:
        if migration_objects.index(obj) == 0:
            other_obj = migration_objects[1]
        else:
            other_obj = migration_objects[0]

        is_profit, pair = obj.check_for_profit(obj, other_obj, profit_percentage, prices_dict)
        if is_profit:
            transaction_count+=1
            print(f'Поръчка номер: {transaction_count}')
            obj.execution(obj, pair, migration_objects.index(obj))
            # print(f'------Взимане на нови количества------')
            # obj.take_new_quantites(obj.name, prices_dict)
            print(obj.next_prices(obj.name, asset_pairs_list, profit_percentage))
            total_busd = 0
            for obj in migration_objects:
                if obj.name != 'BUSD':
                    pair = f'{obj.name}BUSD'
                    price = float(client.get_symbol_ticker(symbol=pair)['price'])
                    total_busd+=obj.quantity * price
                else:
                    total_busd += obj.quantity
            print(f'Тотална обща печалба BUSD: {(total_busd/407.79 -1)* 100:.2f}%')



    time.sleep(2)




