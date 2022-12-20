from real_trading_carrusel_3.asset import Asset
from binance.client import Client

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )

asset_pairs_precision = {'XRPETH': (0, 4),
                             'XRPBTC': (0, 6), 'XRPBUSD': (0, 0),'ETHBTC': (4, 6), 'ETHBUSD': (4, 2), 'BTCBUSD': (5, 2)}


class Methods(Asset):
    @classmethod
    def get_precise_qty(cls, obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return float(result)

    @classmethod
    def calculate_result_quantities(self, pair, action, profit_percentage, obj, other_object, price):

        if action == 'multiply':
            relation = obj.total_quantity * price / other_object.total_quantity
            if relation >= profit_percentage and obj.number > 0:
                Methods.execution(obj, other_object, pair, 'sell')
                return True
        else:
            relation = obj.total_quantity / price / other_object.total_quantity
            if relation >= profit_percentage and obj.number > 0:
                Methods.execution(obj, other_object, pair, 'buy')
                return True
        return False

    @classmethod
    def check_for_profit(cls, obj, objects, profit_percentage, transaction_count):
        for other_obj in objects:
            if obj.name != other_obj.name:
                if objects.index(obj) < objects.index(other_obj):
                    pair = f'{obj.name}{other_obj.name}'
                    action = 'multiply'
                else:
                    pair = f'{other_obj.name}{obj.name}'
                    action = 'division'
                price = float(client.get_symbol_ticker(symbol=pair)['price'])
                if Methods.calculate_result_quantities(pair, action,
                                                       profit_percentage, obj, other_obj, price):
                    Methods.execution_report(obj, other_obj, pair, transaction_count, objects)
                    return True
        return False

    @classmethod
    def execution(cls, obj, other_obj, pair, direction):

        if direction == 'sell':
            precise_num = asset_pairs_precision[pair][0]
            trade_qty = obj.total_quantity
            trade_qty = Methods.get_precise_qty(trade_qty, precise_num)
            client.order_market_sell(symbol=pair, quantity=trade_qty)
            other_obj.total_quantity = float(client.get_asset_balance(other_obj.name)['free'])



        else:
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            precise_num = asset_pairs_precision[pair][0]
            transfer_obj_qty = obj.total_quantity / curr_price
            transfer_obj_qty = Methods.get_precise_qty(transfer_obj_qty, precise_num)
            client.order_market_buy(symbol=pair, quantity=transfer_obj_qty)
            other_obj.total_quantity = float(client.get_asset_balance(other_obj.name)['free'])

        other_obj.number += 1
        obj.number -= 1

    @classmethod
    def execution_report(cls, obj, other_object, pair, transaction_count, objects):
        first = obj.name
        second = other_object.name

        print('\n----------ИЗПЪЛНЕНИЕ----------')
        print(f'Поръчка номер: {transaction_count}')
        data = client.get_my_trades(symbol=pair)[-1]

        print(f'{obj.name} -> {other_object.name} на цена {data["price"]}')

        print(f'Тотално количество {other_object.name}: {other_object.total_quantity}')
        print(f'{other_object.name} печалба: {(other_object.total_quantity / other_object.init_qty - 1) * 100:.2f}%')
        print(f'Тотално количество {obj.name}: {obj.total_quantity}')
        print(f'{obj.name} печалба: {(obj.total_quantity / obj.init_qty - 1) * 100:.2f}%')

        asset = float(client.get_asset_balance(asset="BNB")["free"])
        busd_price = float(client.get_symbol_ticker(symbol="BNBBUSD")['price'])
        print(f'BNB за комисионни: {asset} = {asset * busd_price} BUSD')

        print(f'{obj.name} номер: {obj.number}')
        print(f'{other_object.name} номер: {other_object.number}')

    @classmethod
    def split(cls, obj, objects, transaction_count):
        is_first_split = True
        for other_obj in objects:
            if obj.name != other_obj.name:
                if objects.index(obj) < objects.index(other_obj):
                    pair = f'{obj.name}{other_obj.name}'
                    direction = 'sell'
                else:
                    pair = f'{other_obj.name}{obj.name}'
                    direction = 'buy'
                if is_first_split:
                    total_qty = float(client.get_asset_balance(obj.name)['free'])
                    obj.total_quantity = total_qty / 2
                    is_first_split = False

                Methods.execution(obj, other_obj, pair, direction)
                Methods.execution_report(obj, other_obj, pair, transaction_count, objects)
