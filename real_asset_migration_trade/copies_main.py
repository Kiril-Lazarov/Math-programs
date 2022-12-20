from asset_migration.asset import Asset
from binance.client import Client

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )


class GeneralMethods(Asset):
    precisions_dict = {'TRX': 1, 'XRP': 0, 'ETH': 4, 'BTC': 5, 'BUSD': 0}

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
    def get_precise_qty(obj_qty, precise_num):
        result = float("{:0.0{}f}".format(obj_qty, precise_num))


        return result



    @staticmethod
    def check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage, asset_pairs_list):
        max_profits_list = []

        for pair, price in prices_dict.items():
            if asset_on_charge == pair.split('/')[0]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[1])
                trade_qty = GeneralMethods.multiply(object1.quantity, price)
                possible_profit = object2.quantity * profit_percentage
                if trade_qty >= possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

            elif asset_on_charge == pair.split('/')[1]:
                object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
                object2 = GeneralMethods.cycling_objects(obj_list, pair.split('/')[0])
                trade_qty = GeneralMethods.multiply(object1.quantity, 1 / price)
                possible_profit = object2.quantity * profit_percentage
                if trade_qty >= possible_profit:
                    max_profits_list.append((object2, trade_qty, price, object2.name))

        if not max_profits_list:
            return asset_on_charge, 0
        object2, final_trade_qty, price, object2_name = \
            sorted(max_profits_list, key=lambda x: x[1], reverse=True)[0]
        pair = f'{asset_on_charge}/{object2_name}'
        if pair in asset_pairs_list:
            pair = f'{asset_on_charge}{object2_name}'
            object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)
            final_trade_qty = GeneralMethods.get_precise_qty(final_trade_qty,
                                                             GeneralMethods.precisions_dict[object1.name])
            client.order_market_sell(symbol=pair, quantity=final_trade_qty)
        else:
            pair = f'{object2_name}{asset_on_charge}'
            object1 = GeneralMethods.cycling_objects(obj_list, asset_on_charge)

            final_trade_qty = GeneralMethods.get_precise_qty(final_trade_qty,
                                                                     GeneralMethods.precisions_dict[object1.name])
            final_trade_qty /= prices_dict[f'{object2_name}/{asset_on_charge}']
            client.order_market_buy(symbol=pair, quantity=final_trade_qty)
        print(f'Цена {pair}: {price}')
        object2.quantity = float(client.get_asset_balance(asset=object2_name)['free'])
        print(f'Новото обжект2 количество: {object2.quantity}')
        print(f'Новият асет он чрдж: {object2.name}')

        return object2.name, price

    @staticmethod
    def execution_report(previous_asset, asset_on_charge, price, transaction_count):

        return f'--------ИЗПЪЛНЕНИЕ--------\n' \
               f'Поредна поръчка: {transaction_count}\n' \
               f'{previous_asset} -> {asset_on_charge} на цена: {price}'

    @staticmethod
    def next_prices(asset_on_charge, asset_dict, asset_pairs_list, profit_percentage):
        asset_on_charge_qty = asset_dict[asset_on_charge]
        result = ''
        for asset, quantity in asset_dict.items():
            if asset != asset_on_charge:
                if f'{asset_on_charge}/{asset}' in asset_pairs_list:
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
                object.quantity = GeneralMethods.multiply(object1.quantity,
                                                          1 / prices_dict[f'{object.name}/{object1.name}'])
            elif obj_list.index(object) > obj_list.index(object1):
                object.quantity = GeneralMethods.multiply(object1.quantity,
                                                          prices_dict[f'{object1.name}/{object.name}'])
        for object in obj_list:
            result += f'{object.name}: {object.quantity} Печалба: {(object.quantity / object.init_qty - 1) * 100:.2f}%\n'
        return result.strip()
