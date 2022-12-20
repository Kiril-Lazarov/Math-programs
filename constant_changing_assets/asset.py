from binance.client import Client
from binance.enums import *

from constant_changing_assets.secondary_asset import SecondaryAsset
import pickle

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)


class Asset:
    MAX_TRADES_NUM = 12
    TRADE_LEVEL_STEP = 1.001

    def __init__(self, name, qty, price=None):
        self.name = name
        self.qty = qty
        self.price = price
        self.obj_list = []
        self.prices_list = []
        self.max_trades_num = self.MAX_TRADES_NUM
        self.executed_orders = 0

    def create_object(self, quantity, price):
        if self.name == 'BTC':
            quantity = float(self.get_precise_qty(quantity, 5))
            client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=quantity)
            print(f'------ИЗПЪЛНЕНИЕ-------\n{quantity} BTC -> {quantity * price:.2f} USDT на цена: {price:.2f}')
            qty_to_new_obj = float(f'{quantity * price:.2f}')
            new_obj = SecondaryAsset('USDT', qty_to_new_obj, price)
        else:
            quantity_to_new_obj = quantity
            price_to_divide = price if (self.MAX_TRADES_NUM - self.executed_orders) > 2 else price * 1.001
            quantity /= price_to_divide
            quantity = float(self.get_precise_qty(quantity, 5))
            client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=quantity)
            print(f'------ИЗПЪЛНЕНИЕ-------\n{quantity_to_new_obj:.2f} USDT -> {quantity:.5f} BTC на цена: {price:.2f}')
            new_obj = SecondaryAsset('BTC', quantity, price)
        return new_obj

    def append_left_obj(self, obj):
        self.obj_list.insert(0, obj)
        return f'Добавен {obj.qty} {obj.name}' \
               f' на цена {obj.init_price:.2f}'

    def append_right_obj(self, obj):
        self.obj_list.append(obj)
        return f'Добавен {obj.qty} {obj.name}' \
               f' на цена {obj.init_price:.2f}'

    def add_price(self, price):
        if price >= self.prices_list[-1] * self.TRADE_LEVEL_STEP:
            self.prices_list.append(float(f'{price:.2f}'))
            return 'Right'
        elif price <= self.prices_list[0] / self.TRADE_LEVEL_STEP:
            self.prices_list.insert(0, float(f'{price:.2f}'))
            return 'Left'
        return ''

    def get_trade_quantity(self):
        return self.qty / (self.max_trades_num - self.executed_orders)

    def get_precise_qty(self, obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return result

    def check_for_execution(self, price):
        if self.name == 'USDT':
            for index in range(len(self.obj_list)):
                obj = self.obj_list[index]
                if price >= obj.init_price * obj.increase_profit_level:
                    obj.increase_profit_level += obj.step
                    obj.execution_level = obj.increase_profit_level - 14 * obj.step
                    print(f'{obj.name} на индекс {index} увеличава нивото си на {obj.increase_profit_level:.4f}%\n'
                          f'сигурната печалба на {obj.execution_level:.4f}% текуща цена: {price:.2f}')
                    print(f'Price list execution levels: {[obj.execution_level for obj in self.obj_list]}')
                    print(f'Цени за печалба:'
                          f'{[float(f"{o.init_price * o.execution_level:.2f}") for o in self.obj_list if o.execution_level is not None]}')
                if obj.execution_level is not None:
                    if price <= float(f'{obj.init_price * obj.execution_level:.2f}'):
                        client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                            quantity=obj.qty)
                        print(f'-------ЕКЗЕКУЦИЯ-------\n{obj.name} на индекс {index}:\n'
                              f'{obj.qty} {obj.name} -> {obj.qty * price:.2f} {self.name} на цена: {price:.2f}')
                        print(f'Преди екзекуция: {self.prices_list}')
                        del self.obj_list[0]
                        del self.prices_list[0]
                        print(f'След екзекуция: {self.prices_list}')
                        self.executed_orders -= 1
                        self.qty = float(client.get_asset_balance('USDT')['free'])
                        print(f'{self.name}: {self.qty} executed orders: {self.executed_orders}')
                        return True
            return False
        else:
            for index in range(len(self.obj_list) - 1, -1, -1):
                obj = self.obj_list[index]
                if price <= obj.init_price / obj.increase_profit_level:
                    obj.increase_profit_level += obj.step
                    obj.execution_level = obj.increase_profit_level - 14 * obj.step
                    print(f'{obj.name} на индекс {index} увеличава нивото си на {obj.increase_profit_level:.4f}%\n'
                          f'сигурната печалба на {obj.execution_level:.4f}% текуща цена: {price:.2f}')
                    print(f'Price list execution levels: {[obj.execution_level for obj in self.obj_list]}')
                    print(f'Цени за печалба:'
                          f'{[float(f"{o.init_price / o.execution_level:.2f}") for o in self.obj_list if o.execution_level is not None]}')
                if obj.execution_level is not None:
                    if price >= float(f'{obj.init_price / obj.execution_level:.2f}'):
                        if len(self.obj_list) == 1:
                            trade_qty = float(client.get_asset_balance('USDT')['free'])
                            trade_qty /= (price * 1.001)
                            trade_qty = float(self.get_precise_qty(trade_qty, 5))
                        else:
                            trade_qty = obj.qty / price
                            trade_qty = float(self.get_precise_qty(trade_qty, 5))
                        client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                            quantity=trade_qty)
                        print(f'-------ЕКЗЕКУЦИЯ-------\n{obj.name} на индекс {index}:\n'
                              f'{obj.qty} {obj.name} -> {trade_qty} {self.name} на цена: {price:.2f}')
                        print(f'Преди екзекуция: {self.prices_list}')
                        del self.obj_list[-1]
                        del self.prices_list[-1]
                        print(f'След екзекуция: {self.prices_list}')
                        self.executed_orders -= 1
                        self.qty = float(client.get_asset_balance('BTC')['free'])
                        print(f'{self.name}: {self.qty} executed orders: {self.executed_orders}')
                        return True
            return False

    def change_object_on_charge(self,price):
        if self.name == 'USDT':
            btc = Asset('BTC', float(client.get_asset_balance('BTC')['free']))
            btc.prices_list.append(price)
            print(f'-------ПРОМЯНА НА ГЛАВНА ВАЛУТА-------\nUSDT -> BTC')
            return btc
        usdt = Asset('USDT', float(client.get_asset_balance('USDT')['free']))
        usdt.prices_list.append(price)
        print(f'-------ПРОМЯНА НА ГЛАВНА ВАЛУТА-------\nBTC -> USDT')
        return usdt

    @staticmethod
    def update_data(obj_on_charge):
        with open('data.txt', 'wb') as file:
            pickle.dump(obj_on_charge, file)

