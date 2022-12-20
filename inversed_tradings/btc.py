from trade_methods import TradeMethods


class Bitcoin(TradeMethods):
    def __init__(self, quantity):
        self.quantity = quantity
        self.btc_trades_number = 0
        self.btc_base_total_qty = 0
        self.btc_profit_percentage = 0
        self.btc_reached_profit = 0
