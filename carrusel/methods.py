from carrusel.asset import Asset
from binance.client import Client

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )



class Methods(Asset):
    asset_pairs_precision = {'ETHEUR': (4, 2),
                             'EURBUSD': (1, 3),
                             'ETHBUSD': (4, 2)}


    @classmethod
    def get_precise_qty(cls,obj_qty, precise_num):
        # result = float("{:0.0{}f}".format(obj_qty, precise_num))
        qty = str(obj_qty)
        # print(f'Вътре в присайза')
        # print(obj_qty)
        qty = qty.split('.')
        # print(obj_qty)
        # print(obj_qty[0])
        # print(obj_qty[-1])
        right_side = qty[-1][:precise_num]
        # print(f'Right_side: {right_side}')

        result = qty[0] + '.' + right_side
        # print(f'Форматирано количество')
        if precise_num == 0:
            result = qty[0]

        return float(result)
    @classmethod
    def check_for_profit(cls, asset_on_charge_qty, other_qty, price, profit_percentage, operation):
        if operation == 'mltp':
            relation = (asset_on_charge_qty * price) /other_qty
            # print(f'Relation {asset_on_charge_qty}/{other_qty}: {relation:.5f}')
            if relation >= profit_percentage:
                return True
        else:
            relation = (asset_on_charge_qty / price)/other_qty
            # print(f'Relation {other_qty}/{asset_on_charge_qty}: {relation:.5f}')
            if relation >= profit_percentage:
                return True
        return False

    @classmethod
    def execution(cls, obj_on_charge, other_obj, operation, objects, transactions_count):
        print(f'\n-------ИЗПЪЛНЕНИЕ-------')
        print(f'Двойка: активна - {obj_on_charge.name}  неактивна - {other_obj.name}')
        print(f'Поръчка номер: {transactions_count}')
        if operation == 'mltp':
            pair = f'{obj_on_charge.name}{other_obj.name}'
            precise_num =  Methods.asset_pairs_precision[pair][0]
            trade_quantity = Methods.get_precise_qty(obj_on_charge.real_quantity, precise_num)
            curr_price = float(client.get_symbol_ticker(symbol=pair )['price'])
            # order = client.order_market_sell(symbol= pair,quantity=trade_quantity)
            # other_obj.real_quantity = float(client.get_asset_balance(other_obj.name)['free'])
            other_obj.on_charge = True
            obj_on_charge.on_charge = False
            # new_qty = trade_quantity * curr_price
            other_obj.real_quantity = trade_quantity * curr_price
            print(f'{trade_quantity} {obj_on_charge.name} на цена {curr_price} -> {other_obj.real_quantity}')

        else:
            pair = f'{other_obj.name}{obj_on_charge.name}'
            precise_num = Methods.asset_pairs_precision[pair][1]
            trade_quantity = Methods.get_precise_qty(obj_on_charge.real_quantity, precise_num)
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price']) * 1.0001
            trade_quantity /= curr_price
            # trade_quantity *= 0.995
            print(f'Трансферирано количество: {trade_quantity}')
            precise_num = Methods.asset_pairs_precision[pair][0]
            trade_quantity = Methods.get_precise_qty(trade_quantity, precise_num)
            print(f'Прецизно количество: {trade_quantity}')
            # order = client.order_market_buy(symbol=pair, quantity=trade_quantity)
            # other_obj.real_quantity = float(client.get_asset_balance(other_obj.name)['free'])
            other_obj.on_charge = True
            obj_on_charge.on_charge = False
            curr_price = float(client.get_symbol_ticker(symbol=pair)['price'])
            other_obj.real_quantity = trade_quantity
            print(f'{trade_quantity * curr_price} {obj_on_charge.name} на цена {curr_price} -> {trade_quantity}')
        print(f'Актвни валути:')
        for obj in objects:
            if obj.on_charge:
                print(f'{obj.name} печалба {(obj.real_quantity/ obj.init_qty - 1)*100:.2f}%')





