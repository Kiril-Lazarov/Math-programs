from binance.client import Client

from binance.enums import *

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)


class Asset:
    PROFIT_PERCENTAGE = 1.0015

    def __init__(self, name, qty, on_charge=False):
        self.name = name
        self.qty = qty
        self.on_charge = on_charge
        self.init_qty = self.qty

        if self.name == 'BTC':
            self.precision_num = 5
        elif self.name == 'BUSD':
            self.precision_num = 2

    @staticmethod
    def get_qty(asset):
        return float(client.get_asset_balance(asset=asset)['free'])

    @staticmethod
    def take_curr_price(symbol):
        return float(client.get_symbol_ticker(symbol=symbol)['price'])

    @staticmethod
    def get_next_price(asset_obj, other_obj):
        if asset_obj.on_charge:
            if asset_obj.name == 'BTC':
                next_price = (other_obj.qty * Asset.PROFIT_PERCENTAGE) / asset_obj.qty
                return f'Следваща горна цена {next_price:.2f}'
            elif asset_obj.name == 'BUSD':
                next_price = asset_obj.qty / (other_obj.qty * Asset.PROFIT_PERCENTAGE)
                return f'Следваща долна цена: {next_price:.2f}'
        raise Exception('Объркан е редът на валутите за тази функция')

    def get_initial_qties(self):
        price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
        btc = Asset('BTC', Asset.get_qty('BTC'))
        busd = Asset('BUSD', Asset.get_qty('BUSD'))
        if btc.qty * price > 100:
            btc.on_charge = True
        elif busd.qty > 100:
            busd.on_charge = True

    @classmethod
    def execution(cls,asset_on_charge, btc, busd):
        if asset_on_charge == 'BTC':
            precise_qty = Asset.get_precise_qty(btc.qty, btc.precision_num)
            client.create_order(symbol='BTCBUSD', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=precise_qty)
            busd.qty = Asset.get_qty(busd.name)

            busd.on_charge = True
            btc.on_charge = False

            price = Asset.take_curr_price('BTCBUSD')
            return f'------ИЗПЪЛНЕНИЕ-------\n{precise_qty} BTC -> {busd.qty:.2f} BUSD на цена: {price:.2f}'

        elif asset_on_charge == 'BUSD':
            qty = busd.get_qty(busd.name)
            precise_qty_for_print = Asset.get_precise_qty(qty, busd.precision_num)
            qty /= 5
            price = Asset.take_curr_price('BTCBUSD')
            qty /= price
            precise_qty = Asset.get_precise_qty(qty, btc.precision_num)

            for i in range(5):
                if i == 4:
                    qty = busd.get_qty(busd.name)
                    price = Asset.take_curr_price('BTCBUSD')
                    qty /= (price * 1.001)
                    precise_qty = Asset.get_precise_qty(qty, btc.precision_num)
                    print(f'Ot BUSD precise qty posledno {precise_qty}')
                client.create_order(symbol='BTCBUSD', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                    quantity=precise_qty)
            btc.qty = btc.get_qty(btc.name)

            btc.on_charge = True
            busd.on_charge = False


            return f'------ИЗПЪЛНЕНИЕ-------\n{precise_qty_for_print} BUSD -> {btc.qty} BTC на цена: {price:.2f}'

    @staticmethod
    def check_for_profit(asset_on_charge, btc, busd):
        price = Asset.take_curr_price('BTCBUSD')
        if asset_on_charge == 'BTC':
            if btc.qty * price >= busd.qty * Asset.PROFIT_PERCENTAGE:
                return True
        elif asset_on_charge == 'BUSD':
            if busd.qty / price >= btc.qty * Asset.PROFIT_PERCENTAGE:
                return True
        return False


    @staticmethod
    def get_precise_qty(obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side

        return float(result)

    @classmethod
    def add_quantity(cls, add_count, btc, busd):
        add_count +=1
        symbol = 'BUSDUSDT' if busd.on_charge else 'BTCUSDT'
        price = Asset.take_curr_price(symbol)
        if symbol == 'BTCUSDT':
            qty = 11 / price
            precise_qty = Asset.get_precise_qty(qty, btc.precision_num)
            client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=precise_qty)
            btc.qty = Asset.get_qty('BTC')
            price_for_new_busd = Asset.take_curr_price('BTCBUSD')
            busd.qty = btc.qty * price_for_new_busd

            return f'-------ДОБАВЯНЕ-------\nНомер: {add_count}\n11 USDT -> {precise_qty:.5f} BTC\nНово количество BTC: {btc.qty}'
        else:
            qty = 11 / price
            precise_qty = Asset.get_precise_qty(qty, 0)
            client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=precise_qty)
            busd.qty = Asset.get_qty('BUSD')
            price_for_new_btc = Asset.take_curr_price('BTCBUSD')
            btc.qty = busd.qty / price_for_new_btc

            return f'-------ДОБАВЯНЕ-------\nНомер: {add_count}11 USDT -> {precise_qty:.2f} BTC\nНово количество BUSD: {busd.qty}'

    def __repr__(self):
        return f'{self.name}: {self.qty} , Init: {self.init_qty},' \
               f'On_charge: {self.on_charge}'
