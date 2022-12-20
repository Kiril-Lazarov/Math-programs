from collections import deque


class Bitcoin:
    def __init__(self, quantity):
        self.quantity = quantity
        self.btc_trades_number = 0
        self.btc_waiting_profit = deque([])
        self.btc_price_list = deque([])
        self.btc_base_total_qty = 0

