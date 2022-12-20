from binance.client import Client
from binance.enums import *

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)


class Asset:
    PROFIT_PERCENTAGE = 1.001
    INCREASE_STEP = 0.0001
    FACTOR = 1 / 12

    def __init__(self, name, qty):
        self.name = name
        self.qty = qty
        self.init_qty = self.qty
        self.base_qty = self.init_qty
        self.total_init = None
        self.total_base = None
        self.profit_percentage = Asset.PROFIT_PERCENTAGE
        self.execution_percentage = None
        self.number_trades = 0

    def __str__(self):
        return f'{self.name} Количество: {self.qty}\nНачално количество: {self.total_init}\n' \
               f'Базово количество {self.total_base}'

    @staticmethod
    def take_total_qty(asset, other_asset):
        if asset.name == 'BTC':
            return asset.qty + other_asset.qty / asset.take_price('BTCBUSD')

        return asset.qty + other_asset.qty * asset.take_price('BTCBUSD')

    @staticmethod
    def take_price(pair):
        return float(client.get_symbol_ticker(symbol=pair)['price'])

    def check_for_increase(self, asset, other_asset):
        asset.total = asset.take_total_qty(asset, other_asset)
        if asset.total >= asset.total_base * self.profit_percentage:
            return True
        return False

    @staticmethod
    def get_precise_qty(obj_qty, precise_num):
        obj_qty = str(obj_qty)
        obj_qty = obj_qty.split('.')
        right_side = obj_qty[-1][:precise_num]
        result = obj_qty[0] + '.' + right_side
        if precise_num == 0:
            result = obj_qty[0]
        return result

    @staticmethod
    def execution(asset, other_asset, transactions_count):
        price = float(asset.take_price('BTCBUSD'))
        if asset.name == 'BTC':
            trade_qty = asset.qty * Asset.FACTOR
            trade_qty = float(Asset.get_precise_qty(trade_qty, 5))
            client.create_order(symbol='BTCBUSD', side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
            result_qty = trade_qty * price
            asset.qty = float(client.get_asset_balance(asset.name)['free'])
            other_asset.qty = float(client.get_asset_balance(other_asset.name)['free'])
            # asset.total_base = asset.take_total_qty(asset, other_asset)
            other_asset.total_base = other_asset.take_total_qty(other_asset, asset)

        else:
            trade_qty = asset.qty * Asset.FACTOR
            result_qty = trade_qty / price
            trade_qty /= price
            trade_qty = float(Asset.get_precise_qty(trade_qty, 5))
            client.create_order(symbol='BTCBUSD', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=trade_qty)
            trade_qty *= price
            asset.qty = float(client.get_asset_balance(asset.name)['free'])
            other_asset.qty = float(client.get_asset_balance(other_asset.name)['free'])
            # asset.total_base = asset.take_total_qty(asset, other_asset)
            other_asset.total_base = other_asset.take_total_qty(other_asset, asset)

        other_asset.execution_percentage = None

        asset.number_trades += 1
        other_asset.number_trades -= 1
        print(f'{asset.name} asset num trades: {asset.number_trades}')
        print(f'{other_asset.name} asset num trades: {other_asset.number_trades}')
        if asset.number_trades == 4:
            asset.number_trades = other_asset.number_trades = 0
            asset.profit_percentage = other_asset.profit_percentage = Asset.PROFIT_PERCENTAGE
            asset.execution_percentage = other_asset.execution_percentage = None
            print(asset.add_usdt(asset, other_asset))
            print(asset.next_prices(asset, other_asset, asset.profit_percentage))
            print(other_asset.next_prices(other_asset, asset, other_asset.profit_percentage))
            return f'{asset.name} количество: {asset.qty}\n' \
                   f'{other_asset.name} количество: {other_asset.qty}'

        return f'-------ИЗПЪЛНЕНИЕ-------\nПоръчка номер: {transactions_count}\n' \
               f'{trade_qty} {asset.name} -> {result_qty} на цена {price:.2f}'

    def increase_level(self, asset):
        print(float(client.get_symbol_ticker(symbol="BTCBUSD")['price']))
        asset.profit_percentage += Asset.INCREASE_STEP
        asset.execution_percentage = asset.profit_percentage - 4 * Asset.INCREASE_STEP
        # print(f'{asset.name} increase profit percentage: {asset.profit_percentage}')
        # print(f'{asset.name} execution profit percentage: {asset.execution_percentage}')

    @staticmethod
    def check_for_execution(asset, other_asset):
        if asset.execution_percentage is not None:
            if asset.take_total_qty(asset, other_asset) <= asset.total_base * asset.execution_percentage:
                return True
        return False

    def add_usdt(self, asset, other_asset):
        if asset.name == 'BTC':
            price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            addition_qty = 11 / price
            addition_qty = Asset.get_precise_qty(addition_qty, 5)
            client.create_order(symbol='BTCUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=addition_qty)
            asset.qty = float(client.get_asset_balance(asset.name)['free'])


        else:
            price = float(client.get_symbol_ticker(symbol='BUSDUSDT')['price'])
            addition_qty = 11 / price
            addition_qty = Asset.get_precise_qty(addition_qty, 0)
            client.create_order(symbol='BUSDUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                quantity=addition_qty)
            asset.qty = float(client.get_asset_balance(asset.name)['free'])
        other_asset.total_base =  other_asset.take_total_qty(other_asset, asset)
        asset.total_base = asset.take_total_qty(asset, other_asset)
        return f'-------ДОБАВЯНЕ-------\n{addition_qty} {asset.name} -> {asset.qty}'

    @staticmethod
    def next_prices(asset, other_asset, percentage):
        if percentage is not None:
            if asset.name == 'BTC':
                price = other_asset.qty / (asset.total_base * percentage - asset.qty)

            else:
                price = (asset.total_base * percentage - asset.qty) / other_asset.qty
            string_exp = ''
            if percentage == asset.profit_percentage:
                string_exp = f'Следваща цена покачване: {asset.name}'
            elif percentage == asset.execution_percentage:
                string_exp = f'Следваща цена изпълнение: {asset.name}'
            return f'{string_exp} {price}'
        return 'Execution Percentage is None'

    @staticmethod
    def profit_info(asset, other_asset):
        btc_profit = (asset.total_base / asset.total_init - 1) * 100
        busd_profit = (other_asset.total_base / other_asset.total_init - 1) * 100
        return f'Печалба BTC: {btc_profit:.2f}%\nПечалба BUSD: {busd_profit:.2f}%'
