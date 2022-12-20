from binance.client import Client
from binance.enums import *

from real_usdt_trade.secondary_asset import SecondaryAsset
api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

class MainAsset(SecondaryAsset):
    MAX_TRADES_NUM = 30
    def __init__(self, name, qty, price= None):
        super().__init__(name, qty, price)
        self.obj_list = []
        self.prices_list = []
        self.max_trades_num = self.MAX_TRADES_NUM
        self.executed_orders = 0

    @classmethod
    def create_object(cls, quantity, price):
        client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                            quantity=quantity)
        print(f'------ИЗПЪЛНЕНИЕ-------\n{quantity*price:.2f} USDT -> {quantity} BTC на цена: {price:.2f}')
        return cls('BTC', quantity, price)

    def append_left_obj(self, obj):
        self.obj_list.insert(0,obj)
        return f'Добавен {obj.qty:.5f} {obj.name}' \
               f' на цена {obj.init_price:.2f}'

    def append_right_obj(self, obj):
        self.obj_list.append(obj)
        return f'Добавен {obj.qty:.5f} {obj.name}' \
               f' на цена {obj.init_price:.2f}'

    def add_price(self, price):
        if price >= self.prices_list[-1] * self.PRICE_LEVEL_PRCTG:
            self.prices_list.append(float(f'{price:.2f}'))
            return 'Right'
        elif price <= self.prices_list[0] / self.PRICE_LEVEL_PRCTG:
            self.prices_list.insert(0, float(f'{price:.2f}'))
            return 'Left'
        return ''

    def check_for_execution(self, price):
        for index in range(len(self.obj_list)):
            obj = self.obj_list[index]
            if price >= obj.init_price * obj.increase_profit_level:
                obj.increase_profit_level += obj.step
                obj.execution_level = obj.increase_profit_level - 4 * obj.step
                print(f'{obj.name} на индекс {index} увеличава нивото си на {obj.increase_profit_level:.4f}%\n'
                      f'сигурната печалба на {obj.execution_level:.4f}%')
                print(f'Price list execution levels: {[obj.execution_level for obj in self.obj_list]}')
                print(f'Цени за печалба:'
                      f'{[float(f"{o.init_price * o.execution_level:.2f}") for o in self.obj_list if o.execution_level is not None]}')
            if obj.execution_level is not None:
                if price <= float(f'{obj.init_price* obj.execution_level:.2f}'):
                    client.create_order(symbol='BTCUSDT', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                            quantity=obj.qty)
                    print(f'-------ЕКЗЕКУЦИЯ-------\n{obj.name} на индекс {index}:\n'
                          f'{obj.qty} {obj.name} -> {obj.qty * price:.2f} {self.name} на цена: {price:.2f}')
                    del self.obj_list[0]
                    del self.prices_list[0]
                    self.executed_orders-= 1
                    self.qty = float(client.get_asset_balance('USDT')['free'])
                    print(f'{self.name}: {self.qty} executed orders: {self.executed_orders}')
                    return True
        return False

    def get_trade_quantity(self):
        return self.qty / (self.max_trades_num - self.executed_orders)

# usdt = MainAsset('USDT', 1000)
# btc = usdt.create_object(500)
# btc1 = usdt.create_object(400)
# print(btc.name)
# usdt.append_left_obj(btc)
# print(usdt.obj_list)
# print(usdt.append_right_obj(btc1))
# print(usdt.obj_list)
# usdt.prices_list.append(100)
# usdt.add_price(100.1)
# print(usdt.prices_list)
# print(usdt.add_price(100.3))
# print(usdt.prices_list)
# print(usdt.add_price(99.9))
# print(usdt.prices_list)
# print(usdt.add_price(99.81))
# print(usdt.prices_list)
