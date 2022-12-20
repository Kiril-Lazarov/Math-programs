class PompAsset:
    INCREASE_PROFIT_PECENTAGE = 1.003
    TRADE_STEP = 1.001
    MAX_TRADES_NUM = 10
    def __init__(self, name, qty, base_price):
        self.name = name
        self.qty = qty
        self.base_price = base_price
        self.base_qty = self.qty
        self.increase_profit = self.INCREASE_PROFIT_PECENTAGE
        self.step = 0.0001
        self.execution_level = None
        self.executed_orders = 0
        self.opposite_obj_qty = 0
        self.prices_list = []

    def get_trade_quantity(self):
        return self.qty / (self.MAX_TRADES_NUM - self.executed_orders)


    def execute_trade(self, price, other_object_name):
        qty = self.get_trade_quantity()
        if self.name == 'BTC':
            traded_qty = qty * price
            self.opposite_obj_qty +=  traded_qty
        else:
            traded_qty = qty / price
            self.opposite_obj_qty += traded_qty
        self.qty -= qty
        return f'------ИЗПЪЛНЕНИЕ------\n{qty} {self.name} -> ' \
               f'{traded_qty} {other_object_name} на цена {price:.2f}'

    def check_for_execution(self, price):
        pass




