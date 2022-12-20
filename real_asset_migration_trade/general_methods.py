import time

from real_asset_migration_trade.asset import Asset
from binance.client import Client
from binance.enums import *

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )


class GeneralMethods(Asset):
    # asset_pairs_precision = {'LTCEUR': (3, 3), 'ETHEUR  ': (4, 2), 'BTCEUR': (5, 2), 'EURBUSD': (1, 3), 'LTCETH': (3, 5),
    #                          'LTCBTC': (3, 7), 'LTCBUSD': (3, 2), 'ETHBTC': (4, 6),
    #                          'ETHBUSD': (4, 2), 'BTCBUSD': (5, 2)}

    # asset_pairs_precision = {'XRPEUR': (0, 2), 'ETHEUR': (4, 2), 'BTCEUR': (5, 2), 'EURBUSD': (1, 3),
    #                          'XRPETH': (0, 4),
    #                          'XRPBTC': (0, 6), 'XRPBUSD': (0, 2), 'ETHBTC': (4, 6),
    #                          'ETHBUSD': (4, 2), 'BTCBUSD': (5, 2)}
    asset_pairs_precision = {'TRXUSDT': (1, 3), 'TRXETH': (0, 5),'TRXEUR':(0,2),'TRXBTC': (0,6), 'TRXBUSD' : (1,2), 'ETHEUR': (4, 2), 'BTCEUR': (5, 2), 'EURBUSD': (1, 3),

                             'ETHBTC': (4, 6),
                             'ETHBUSD': (4, 2),'ETHUSDT': (4,1), 'BTCUSDT': (5,2), 'BTCBUSD': (5, 2),'EURUSDT': (1,3),'BUSDUSDT': (0,2)}

    price_precision = { 'ETHEUR': 2, 'BTCEUR': 2, 'EURBUSD': 4,
                         'ETHBTC': 6,
                       'ETHBUSD': 2, 'BTCBUSD': 2}

    def __init__(self, init_qty, name):
        super().__init__(init_qty, name)

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def summation(x, y):
        return x + y

    @staticmethod
    def first_char(asset, pair):
        if asset[0] != pair[0]:
            return -1
        return 1

    @staticmethod
    def cycling_objects(obj_list, asset_on_charge):
        for obj in obj_list:
            if obj.name == asset_on_charge:
                return obj

    @staticmethod
    def get_price_precision(prices_dict, pair, coef):
        result = 0
        for asset, price in prices_dict.items():
            if asset == pair:
                price = float(price)
                price *= coef
                num = GeneralMethods.price_precision[pair]

                result = GeneralMethods.get_precise_qty(price, num)
                print(f'Форматирана цена за :{pair}: {result}')
                return str(result)

    @staticmethod
    def get_precise_qty(obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return result

    @staticmethod
    def get_accuracy_num(asset_pair):
        return GeneralMethods.asset_pairs_precision[asset_pair]

    @staticmethod
    def check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage, asset_pairs_list):
        max_profits_list = []

        for pair, price in prices_dict.items():
            if asset_on_charge == pair.split('/')[0]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[1])

                trade_qty = GeneralMethods.multiply(object1.total_quantity, price)
                possible_profit = object2.total_quantity * profit_percentage
                if trade_qty > possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

            elif asset_on_charge == pair.split('/')[1]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[0])

                trade_qty = GeneralMethods.multiply(object1.total_quantity, 1 / price)
                possible_profit = object2.total_quantity * profit_percentage
                if trade_qty > possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

        if not max_profits_list:
            return asset_on_charge, 0, ''
        object2, final_trade_qty, price, object2_name = sorted(max_profits_list, key=lambda x: x[1], reverse=True)[0]
        pair = f'{asset_on_charge}/{object2_name}'
        if pair in asset_pairs_list:
            pair = f'{asset_on_charge}{object2_name}'
            print(pair)
            object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
            obj1_accuracy, obj2_accuracy = GeneralMethods.get_accuracy_num(pair)

            object1_quantity = float(GeneralMethods.get_precise_qty(object1.total_quantity, obj1_accuracy))
            # print(f'Tова ще се търгува за SELL: {object1_quantity}')

            # print(f'object1_qty след точност: {object1_quantity}')
            # price = GeneralMethods.get_price_precision( prices_dict, pair, 1.0014)
            client.create_order(symbol=pair, side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=object1_quantity)
            # curr_price = client.get_my_trades(symbol=pair)
            object2.total_quantity = client.get_asset_balance(object2_name)['free']
            # client.order_limit_sell(
            #     symbol=pair,
            #     quantity=object1_quantity,
            #     price=price)


        else:
            pair = f'{object2_name}{asset_on_charge}'
            print(pair)
            object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
            obj2_accuracy, obj1_accuracy = GeneralMethods.get_accuracy_num(pair)
            # print(f'obj1_accuracy: {obj1_accuracy}')
            # print(f'obj2_accuracy: {obj2_accuracy}')
            # print(f'object1_qty преди точност: {object1.quantity}')

            # object1_quantity = GeneralMethods.get_precise_qty(object1.fict_quantity, obj1_accuracy)
            # print(f'object1_qty след точност: {object1_quantity}')

            # curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            # print(f'curr_price: {curr_price}')
            # curr_price *= 1.0015
            # print(f'curr_price  с увеличението: {curr_price}')


            # object2_quantity = object1_quantity / (prices_dict[f'{object2_name}/{asset_on_charge}'])
            # # object2_quantity = object1_quantity /
            # # print(f'Обект2  равностойно количество: {object2_quantity}')
            # object2_quantity = GeneralMethods.get_precise_qty(object2_quantity, obj2_accuracy)
            # print(f'object2_qty след точност: {object2_quantity}')
            # # print(f'PRice: {price}')
            # # price = GeneralMethods.get_price_precision( prices_dict, pair, 1/1.0014)
            # print(f'Tова ще се търгува за BUY: {object1_quantity}')
            # print(f'Това е еквивалентът: {object2_quantity}')

            trade_qty = float(client.get_asset_balance(asset=object1.name)["free"])
            trade_qty /= 6
            trade_qty = float(GeneralMethods.get_precise_qty(trade_qty, obj1_accuracy))
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            trade_qty /= curr_price
            trade_qty = float(GeneralMethods.get_precise_qty(trade_qty, obj2_accuracy))

            print(f'trade_qty: {trade_qty}')

            print(f'trade_qty след деленето: {trade_qty}')
            print(f'trade_qty след форматирането: {trade_qty}')
            for i in range(6):

                if i == 5:
                    trade_qty = float(client.get_asset_balance(asset=object1.name)["free"])
                    trade_qty = float(GeneralMethods.get_precise_qty(trade_qty, obj1_accuracy))
                    curr_price = float(client.get_symbol_ticker(symbol=pair)['price']) * 1.0015
                    trade_qty /= curr_price
                    trade_qty = float(GeneralMethods.get_precise_qty(trade_qty, obj2_accuracy))
                    if 'TRX' in pair:
                        if trade_qty * curr_price > float(client.get_asset_balance(asset=object1.name)["free"]):
                            if 'BUSD' not in pair:
                                trade_qty -= 1
                            else:
                                trade_qty -= 0.1
                client.create_order(symbol=pair, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                    quantity=trade_qty)

        object2.total_quantity = float(client.get_asset_balance(asset=object2_name)['free'])
        curr_price = client.get_my_trades(symbol=pair)

        return object2.name, curr_price, pair


    @staticmethod
    def execution_report(previous_asset, asset_on_charge, price, transaction_count, pair, obj_list):
        object_ = GeneralMethods.cycling_objects(obj_list, previous_asset)
        price = client.get_my_trades(symbol=pair)[-1]['price']

        traded_qty = float(client.get_asset_balance(asset=previous_asset)['free'])

        return f'--------ИЗПЪЛНЕНИЕ--------\n' \
               f'Поредна поръчка: {transaction_count}\n' \
               f'{object_.total_quantity} {previous_asset} -> {asset_on_charge} на цена: {price}'


    @staticmethod
    def next_prices(asset_on_charge, asset_dict, asset_pairs_list, profit_percentage):
        asset_on_charge_qty = asset_dict[asset_on_charge]
        # print(f'Asset on charge qty преди точност: {asset_on_charge_qty}')

        result = ''
        for asset, quantity in asset_dict.items():
            if asset != asset_on_charge:

                if f'{asset_on_charge}/{asset}' in asset_pairs_list:
                    # pair = f'{asset_on_charge}{asset}'
                    #     asset_chrg_accuracy, quantity_accuracy = GeneralMethods.get_accuracy_num(pair)
                    #     asset_on_charge_qty = GeneralMethods.get_precise_qty(asset_on_charge_qty, asset_chrg_accuracy)
                    #     quantity = GeneralMethods.get_precise_qty(quantity, quantity_accuracy)
                    #     price = quantity * profit_percentage / asset_on_charge_qty
                    #
                    #     result += f'{asset} Следваща горна цена: {price}\n'
                    # else:
                    #     pair = f'{asset}{asset_on_charge}'
                    #     quantity_accuracy,asset_chrg_accuracy = GeneralMethods.get_accuracy_num(pair)
                    #     asset_on_charge_qty = GeneralMethods.get_precise_qty(asset_on_charge_qty, asset_chrg_accuracy)
                    #     quantity = GeneralMethods.get_precise_qty(quantity, quantity_accuracy)
                    #
                    #     price = asset_on_charge_qty / (quantity * profit_percentage)
                    #
                    #     result += f'{asset} Следваща долна цена: {price}\n'
                    price = quantity * profit_percentage / asset_on_charge_qty
                    result += f'{asset} Следваща горна цена: {price}\n'
                else:
                    price = asset_on_charge_qty / (quantity * profit_percentage)
                    result += f'{asset} Следваща долна цена: {price}\n'
        return result.strip()


    @classmethod
    def normalize_quantities(cls, asset_on_charge, obj_list, prices_dict):
        object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
        result = '\n--------РЕНОРМИРАНЕ---------\n'
        for object in obj_list:
            if obj_list.index(object) < obj_list.index(object1):
                object.total_quantity = GeneralMethods.multiply(object1.total_quantity,
                                                                1 / prices_dict[f'{object.name}/{object1.name}'])
            elif obj_list.index(object) > obj_list.index(object1):
                object.total_quantity = GeneralMethods.multiply(object1.total_quantity,
                                                                prices_dict[f'{object1.name}/{object.name}'])
        for object in obj_list:
            result += f'{object.name}: {object.total_quantity} Печалба: {(object.total_quantity / object.init_qty - 1) * 100:.2f}%\n'
        return result.strip()

    @staticmethod
    def check_for_bnb_commission():
        price = float(client.get_symbol_ticker(symbol="BNBUSDT")['price'])
        bnb_qty = float(client.get_asset_balance(asset= 'BNB')['free'])
        qty = 11
        if bnb_qty*price <= 0.30:
            client.create_order(symbol='BNBUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=qty)
            bnb_qty = float(client.get_asset_balance(asset='BNB')['free'])
            usdt_qty = float(client.get_asset_balance(asset='USDT')['free'])
            print('------ДОБАВКА ЗА КОМИСИОННА------')
            print(f'{qty} USDT -> {bnb_qty} BNB')
            print(f'USDT: {usdt_qty}')

    @classmethod
    def initialize_objects(cls, asset_on_charge,asset_qty,asset,primary_object_list, prices_dict, asset_order_list):
        name_primary_list = []
        if primary_object_list:
            for obj in primary_object_list:
                name_primary_list.append(obj.name)


        for asset in asset_order_list:
            if asset == asset_on_charge and asset not in name_primary_list:
                name_primary_list.append(asset)
                return Asset(asset_qty, asset_on_charge)
            if asset != asset_on_charge and asset not in name_primary_list:
                for asset_pair, price in prices_dict.items():
                    if asset_on_charge in asset_pair and asset in asset_pair:
                        if asset_order_list.index(asset_on_charge) < asset_order_list.index(asset):
                            qty = asset_qty * price
                        else:
                            qty = asset_qty / price


                        return Asset(qty, asset)

    @classmethod
    def get_asset_on_charge(cls):
        trx = client.get_asset_balance(asset='TRX')
        eth = client.get_asset_balance(asset='ETH')
        btc = client.get_asset_balance(asset='BTC')
        eur = client.get_asset_balance(asset='EUR')
        busd = client.get_asset_balance(asset='BUSD')

        for asset_info in [trx,eth,btc,eur,busd]:
            if asset_info['asset'] == 'BUSD':
                return asset_info['asset'], float(asset_info['free'])
            symbol = f"{asset_info['asset']}BUSD"
            qty = float(asset_info['free'])
            curr_price = float(client.get_symbol_ticker(symbol= symbol)['price'])
            if qty * curr_price >100:
                return asset_info['asset'], float(asset_info['free'])

