class SecondaryAsset:
    PRICE_LEVEL_PRCTG = 1.001
    EXECUTION_STEP = 0.0001

    def __init__(self, name, qty, init_price):
        self.name = name
        self.qty = qty
        self.init_price = init_price
        self.increase_profit_level = self.PRICE_LEVEL_PRCTG
        self.execution_level = None
        self.step = self.EXECUTION_STEP

