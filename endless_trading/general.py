class General:
    def multipl(self, x, y):
        return x * y

    def sumation(self, x, y):
        return x + y

    def change_asset(self, asset, new_asset):
        previous_asset = asset
        asset = new_asset
        return f'\n------СМЯНА НА ВАЛУТА------\n      {previous_asset} -> {asset}'

    def check_number_trades(self, asset, curr_number_trades, number_trades):
        if asset == 'BTC':
            if curr_number_trades == number_trades:
                print(General.change_asset(self, 'BTC', 'BUSD'))
                return 'BUSD', True
            return 'BTC', False
        else:
            if asset == 'BUSD':
                if curr_number_trades == number_trades:
                    print(General.change_asset(self, 'BUSD', 'BTC'))
                    return 'BTC', True
            return 'BUSD', False

    def check_for_trade(self, curr_price, price_list, price_percentage):
        if curr_price >= price_list[-1] * price_percentage or curr_price <= price_list[0]/price_percentage:
            return True
        return False

    def factor(self, trade_number, number_trades):
        return 1 / (number_trades - trade_number)
