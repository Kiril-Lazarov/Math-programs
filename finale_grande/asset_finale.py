from binance.client import Client
from binance.enums import *

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)


class Asset:
    TRADE_LEVEL_STEP = 1.0003
    EXECUTION_STEP = 0.00005
    PROFIT_PERCENTAGE = 1.001

    def __init__(self, name, qty, initial_qty):
        self.name = name
        self.qty = qty
        self.base_qty = qty
        self.base_price = 0
        self.initial_qty = initial_qty
        self.prices_list = []
        self.profit_percentage = self.PROFIT_PERCENTAGE
        self.execution_level = None
        self.max_trades_num = 30
        self.executed_orders = 0

    def get_total_qty(self, other_obj, price):
        if self.name == 'BTC':
            return self.qty + other_obj.qty / price
        else:
            return self.qty + other_obj.qty * price

    def get_precise_qty(self, obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return result

    def add_price(self, price):
        if not self.prices_list:
            if price >= self.base_price * self.TRADE_LEVEL_STEP:
                self.prices_list.append(float(f'{price:.2f}'))
                return True
            elif price <= self.base_price / self.TRADE_LEVEL_STEP:
                self.prices_list.insert(0, float(f'{price:.2f}'))
                return True
            return False
        else:
            if price >= self.prices_list[-1] * self.TRADE_LEVEL_STEP:
                self.prices_list.append(float(f'{price:.2f}'))
                return True
            elif price <= self.prices_list[0] / self.TRADE_LEVEL_STEP:
                self.prices_list.insert(0, float(f'{price:.2f}'))
                return True
            return False

    def get_trade_quantity(self):
        return self.qty / (self.max_trades_num - self.executed_orders)

    def trade_execution(self, price, other_object, btc, usdt):
        trade_qty = self.get_trade_quantity()
        other_name = other_object.name
        if self.name == 'BTC':
            # print(f'От trade_execution self.name: {self.name}')
            trade_qty = float(self.get_precise_qty(trade_qty, 5))
            result_qty = trade_qty * price
            other_object.qty += result_qty
            self.qty -= trade_qty

        else:
            # print(f'От trade_execution self.name: {self.name}')
            trade_qty = float(self.get_precise_qty(trade_qty, 2))
            result_qty = trade_qty / price
            other_object.qty += result_qty
            self.qty -= trade_qty
        self.executed_orders += 1
        info = Asset.get_info(btc, usdt, price)
        return f'------ИЗПЪЛНЕНИЕ-------\n{trade_qty} {self.name} -> {result_qty} {other_name} на цена {price:.2f}\n' \
               f'BTC: {btc.qty}\nUSDT: {usdt.qty}\n{info}'

    def check_for_execution(self, price, btc, usdt, level, is_execution_level):

        if self.name == 'BTC':
            total_btc = self.get_total_qty(usdt, price)
            if is_execution_level:
                if total_btc <= self.base_qty * level:
                    return True
            else:
                if total_btc >= self.base_qty * level:
                    return True
        else:
            total_usdt = self.get_total_qty(btc, price)
            if is_execution_level:
                if total_usdt <= self.base_qty * level:
                    return True
            else:
                if total_usdt >= self.base_qty * level:
                    return True
        return False

    def profit_execution(self, price, btc, usdt, other_obj):
        print('Method profit_execution')
        if self.name == 'BTC':
            other_name = other_obj.name
            trade_qty = other_obj.qty
            result = trade_qty / price
            self.qty += result
            other_obj.qty = 0
        else:
            other_name = other_obj.name
            trade_qty = other_obj.qty
            result = trade_qty * price
            self.qty += result
            other_obj.qty = 0
        self.base_price = price
        self.base_qty = self.qty
        other_obj.base_qty = other_obj.get_total_qty(self, price)
        self.null_the_properties(self)
        info = Asset.get_info(btc, usdt, price)
        return f'-------ПЕЧАЛБА-------\n{trade_qty} {other_name} -> {result} {self.name}\n' \
               f'BTC base: {btc.base_qty}\nUSDT base: {usdt.base_qty}\n{info}'

    def profit_execution_other_obj(self, price, btc, usdt, main_object):
        print('Method profit_execution_other_obj')
        trade_qty = main_object.qty
        if self.name == 'BTC':
            other_name = main_object.name
            result = trade_qty / price

        else:
            other_name = main_object.name
            result = trade_qty * price
        self.qty += result
        main_object.qty -= trade_qty
        self.base_qty = self.qty
        self.base_price = price
        self.null_the_properties(self)
        info = Asset.get_info(btc, usdt, price)
        return f'-------ПЕЧАЛБА-------\n{trade_qty} {other_name} -> {result} {self.name}\n' \
               f'BTC base: {btc.base_qty}\nUSDT base: {usdt.base_qty}\n{info}'

    def check_for_increase(self, price, other_object):
        total_qty = self.get_total_qty(other_object, price)
        if total_qty >= self.base_qty * self.profit_percentage:
            self.profit_percentage += self.EXECUTION_STEP
            self.execution_level = self.profit_percentage - 4 * self.EXECUTION_STEP
            print(f'Покачване: процент {self.profit_percentage} сигурна печалба {self.execution_level}')

    def next_prices(self, other_object):
        level = self.profit_percentage if self.execution_level is None else self.execution_level
        if self.name == 'BTC':
            result = other_object.qty / ((self.base_qty * level) - self.qty)
            return f'Следваща долна цена за печалба на BTC: {result:.2f}'
        else:
            result = ((self.base_qty * level) - self.qty) / other_object.qty
            return f'Следваща горна цена за печалба на USDT: {result:.2f}'
    @staticmethod
    def null_the_properties(obj):
        obj.prices_list = []
        obj.execution_level = None
        obj.executed_orders = 0
        obj.profit_percentage = Asset.PROFIT_PERCENTAGE
    @staticmethod
    def change_asset_on_charge(obj_on_charge, other_object, btc, usdt, price):
        print('Method change_asset_on_charge')
        if obj_on_charge.name == 'BTC':
            obj_on_charge = usdt
            other_object = btc
        else:
            obj_on_charge = btc
            other_object = usdt
        obj_on_charge.null_the_properties(obj_on_charge)
        obj_on_charge.base_qty = obj_on_charge.get_total_qty(other_object, price)
        other_object.null_the_properties(other_object)
        other_object.base_qty = other_object.get_total_qty(obj_on_charge, price)

        # print(
        #     f'Change_asset_on_charge: Obj_on_charge: {obj_on_charge.name}, {obj_on_charge.qty}, {obj_on_charge.base_qty}'
        #     f'{obj_on_charge.prices_list},{obj_on_charge.executed_orders}'
        #     f'{obj_on_charge.execution_level}'
        #     f'Other_obj: {other_object.name}, {other_object.qty}, {other_object.base_qty}, {other_object.prices_list}'
        #     f'{other_object.executed_orders}, {other_object.execution_level}')
        print(f'------СМЯНА ПОД ВЪПРОС-------\nГлавна валута: {obj_on_charge.name}\nВтора валута: {other_object.name}')
        return obj_on_charge, other_object

    @staticmethod
    def get_info(btc, usdt, price):
        btc_curr_total = btc.get_total_qty(usdt, price)
        usdt_curr_total = usdt.get_total_qty(btc, price)
        btc_total_profit = ((btc_curr_total / btc.initial_qty - 1) * 100)
        btc_base_profit = ((btc_curr_total / btc.base_qty - 1) * 100)
        usdt_total_profit = ((usdt_curr_total / usdt.initial_qty - 1) * 100)
        usdt_base_profit = ((usdt_curr_total / usdt.base_qty - 1) * 100)
        return f'BTC тотална печалба: {btc_total_profit:.2f}%\nUSDT тотална печалба: {usdt_total_profit:.2f}%\n' \
               f'BTC спрямо база: {btc_base_profit:.2f}%\nUSDT спрямо база: {usdt_base_profit:.2f}%'

    def convert_all_qty(self, price, other_obj):
        print('Method convert_all_qty')
        trade_qty = self.qty
        self.executed_orders = self.max_trades_num
        if self.name == 'BTC':
            other_name = other_obj.name

            result = trade_qty * price
            other_obj.qty += result
            self.qty = 0
        else:
            other_name = other_obj.name

            result = trade_qty / price
            other_obj.qty += result
            self.qty = 0
        return f'------ПРЕХВЪРЛЯНЕ-------\n{trade_qty} {self.name} -> {result} {other_name}' \
               f'на цена {price:.2f}\n{self.name}: {self.qty}\n{other_name} {other_obj.qty}'


