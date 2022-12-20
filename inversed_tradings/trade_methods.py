class TradeMethods:

    def multipl(self, x, y):
        return x * y

    def sumation(self, x, y):
        return x + y

    def next_execution_prices(self, curr_price, btc_total, btc_qty, busd_total, busd_qty, btc_profit_percentage,
                              busd_profit_percentage):
        # curr_total_btc, curr_total_busd = self.get_total_quantities(curr_price, btc_qty, busd_qty)
        up_price = (busd_total * busd_profit_percentage - busd_qty) / btc_qty
        down_price = busd_qty / (btc_total * btc_profit_percentage - btc_qty)
        print(f'Следваща горна цена изпълнение: {up_price:.2f}')
        print(f'Разлика с текущата цена: {up_price - curr_price:.2f}')
        print(f'Следваща долна цена изпълнение: {down_price:.2f}')
        print(f'Разлика с текущата цена: {curr_price - down_price:.2f}')


    def factor(self, trade_number, number_trades):
        # return 1 / (trade_number - number_trades)
        # qty = 1 / (10 - abs(number_trades) * 0.5)
        # print(f'Делител: {(10 - abs(number_trades) * 0.5)}')
        return 1/5

    def get_total_quantities(self, curr_price, btc, busd):
        total_btc = btc + busd / curr_price
        total_busd = busd + btc * curr_price
        return total_btc, total_busd

    def execution(self, curr_price, btc_qty, btc_trades_number, busd_qty, busd_trades_number, trade_number, asset):
        print(f'\n-------ИЗПЪЛНЕНИЕ-------\n')
        if asset == 'BTC':
            qty = btc_qty * self.factor(trade_number, btc_trades_number)
            result_qty = qty * curr_price
            busd_qty = self.sumation(busd_qty, result_qty)
            btc_qty = self.sumation(btc_qty, -qty)
            print(f'{qty:.8f} BTC -> {result_qty:.2f} BUSD на цена: {curr_price:.2f}\n')
            return btc_qty, busd_qty

        else:
            qty = busd_qty * self.factor(trade_number, busd_trades_number)
            result_qty = qty / curr_price
            btc_qty = self.sumation(btc_qty, result_qty)
            busd_qty = self.sumation(busd_qty, -qty)
            print(f'{qty:.2f} BUSD -> {result_qty:.8f} BTC на цена: {curr_price:.2f}\n')
            return btc_qty, busd_qty

    def change_profit_percentage(self, btc_trades_number, busd_trades_number, profit_percentage, profit_step, curr_price):
        btc_factor, busd_factor = 0, 0
        new_btc_profit_percentage,new_busd_profit_percentage = 0,0
        if btc_trades_number > 0:
            new_btc_profit_percentage = profit_percentage - btc_trades_number * profit_step
            down_price = curr_price/new_btc_profit_percentage
            diff = curr_price - down_price
            up_price = curr_price + 2.5 * btc_trades_number *  diff
            new_busd_profit_percentage =   up_price / curr_price
        elif busd_trades_number > 0:
            new_busd_profit_percentage = profit_percentage -  busd_trades_number * profit_step
            up_price = curr_price * new_busd_profit_percentage
            diff = up_price - curr_price
            down_price = curr_price -  2.5 * diff *busd_trades_number
            new_btc_profit_percentage =  curr_price / down_price
        elif btc_trades_number == 0 and busd_trades_number == 0:
            new_btc_profit_percentage = profit_percentage
            new_busd_profit_percentage = profit_percentage
        return new_btc_profit_percentage, new_busd_profit_percentage

    def check_for_split(self, btc_total_init, btc_qty, btc_reached_profit, busd_total_init, busd_qty,
                        busd_reached_profit,
                        curr_price, profit_level):

        curr_btc_overall, curr_busd_overall = self.get_total_quantities(curr_price, btc_qty, busd_qty)
        if ((curr_btc_overall / btc_total_init - 1) * 100 >= btc_reached_profit + profit_level) \
                and ((curr_busd_overall / busd_total_init - 1) * 100 >= busd_reached_profit + profit_level):
            btc_reached_profit = (curr_btc_overall / btc_total_init - 1) * 100
            busd_reached_profit = (curr_busd_overall / busd_total_init - 1) * 100
            return True, btc_reached_profit, busd_reached_profit
        return False,

    def split(self, curr_price, btc_quantity, busd_quantity):
        print(f'\n-------РАЗДЕЛЯНЕ-------')
        print(f'\nТекуща цена: {curr_price:.2f}')
        # if asset == 'BUSD':
        #     btc_quantity += (busd_quantity / 3) / curr_price
        #     busd_quantity *= 2/3
        # else:
        #     busd_quantity += (btc_quantity / 3) * curr_price
        #     btc_quantity *= 2/3
        busd_quantity += btc_quantity * curr_price
        busd_quantity /= 2
        btc_quantity = busd_quantity / curr_price
        return btc_quantity, busd_quantity
