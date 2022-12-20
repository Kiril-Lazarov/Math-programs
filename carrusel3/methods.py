from carrusel3.asset import Asset
from binance.client import Client

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret, )





class Methods(Asset):
    @classmethod
    def calculate_result_quantities(self, pair, action, profit_percentage, obj, other_object, price):

        if action == 'multiply':
            relation = obj.real_quantity * price / other_object.real_quantity
            # print(f'\nОтношение количества {obj.name}/{other_object.name}: {relation}')
            if relation >= profit_percentage and obj.number >0:
                Methods.execution(obj, other_object, price, 'sell')
                return True
        else:
            relation = obj.real_quantity / price / other_object.real_quantity
            # print(f'\nОтношение количества {obj.name}/{other_object.name}: {relation}')
            if relation >= profit_percentage and obj.number > 0:
                Methods.execution(obj, other_object, price, 'buy')
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
                    Methods.execution_report(obj, other_obj, price,transaction_count)
                    return True
        return False

    @classmethod
    def execution(cls, obj, other_obj, price, direction):
        if direction == 'sell':
            other_obj.real_quantity = obj.real_quantity * price

        else:
            other_obj.real_quantity = obj.real_quantity / price
        other_obj.number += 1
        obj.number -= 1

    @classmethod
    def execution_report(cls, obj, other_object, price, transaction_count):

        print('\n----------ИЗПЪЛНЕНИЕ----------')
        print(f'Поръчка номер: {transaction_count}')
        print(f'{obj.real_quantity} {obj.name}-> {other_object.real_quantity} {other_object.name} на цена {price}')
        print(f'{obj.name} печалба: {(obj.real_quantity/obj.init_qty - 1) * 100:.2f}%')
        print(f'{other_object.name} печалба: {(other_object.real_quantity/other_object.init_qty - 1) * 100:.2f}%')
        print(f'{obj.name} номер: {obj.number}')
        print(f'{other_object.name} номер: {other_object.number}')

    @classmethod
    def split(cls, obj, objects, transaction_count):
        for other_obj in objects:
            if obj.name != other_obj.name:
                if objects.index(obj) < objects.index(other_obj):
                    pair = f'{obj.name}{other_obj.name}'
                    direction = 'sell'
                else:
                    pair = f'{other_obj.name}{obj.name}'
                    direction = 'buy'
                price = float(client.get_symbol_ticker(symbol=pair)['price'])
                Methods.execution(obj, other_obj, price, direction)
                Methods.execution_report(obj, other_obj, price, transaction_count)


