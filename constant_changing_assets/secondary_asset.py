class SecondaryAsset:
    PRICE_LEVEL_PRCTG = 1.0022
    EXECUTION_STEP = 0.00005

    def __init__(self, name, qty, init_price):
        self.name = name
        self.qty = qty
        self.init_price = init_price
        self.increase_profit_level = self.PRICE_LEVEL_PRCTG
        self.execution_level = None
        self.step = self.EXECUTION_STEP

    def str(self):
        return f'{self.name}: {self.qty}\n{self.init_price}\n{self.increase_profit_level}\n' \
               f'{self.execution_level}'

