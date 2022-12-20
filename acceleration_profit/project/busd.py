from project.trade_methods import TradeMethods


class Busd(TradeMethods):
    def __init__(self, quantity):
        self.quantity = quantity
        self.busd_trades_number = 0
        self.busd_base_total_qty = 0
        self.busd_profit_percentage = 0
        self.busd_reached_profit = 0