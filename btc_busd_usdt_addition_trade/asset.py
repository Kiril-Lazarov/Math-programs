from binance.client import Client

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)


class Asset:
    PROFIT_PERCENTAGE = 1.0005
    INCREASE_STEP = 0.00013
    FACTOR = 0.2

    def __init__(self, name, qty):
        self.name = name
        self.qty = qty
        self.init_qty = self.qty
        self.base_qty = self.init_qty
        self.profit_percentage = Asset.PROFIT_PERCENTAGE
        self.execution_percentage = None
        self.number_trades = 0

    def __str__(self):
        return f'{self.name} Количество: {self.qty}\nНачално количество: {self.init_qty}\n' \
               f'Базово количество {self.base_qty}'
    @staticmethod
    def take_total_qty(asset, other_asset):
        if asset.name == 'BTC':
            return asset.qty + other_asset.qty / asset.take_price('BTCBUSD')

        return asset.qty + other_asset.qty * asset.take_price('BTCBUSD')

    @staticmethod
    def take_price(pair):
        return float(client.get_symbol_ticker(symbol=pair)['price'])

    @staticmethod
    def check_for_increase(asset, other_asset):
        asset_total = asset.take_total_qty(asset, other_asset)
        # asset_for_profit = asset.base_qty * asset.profit_percentage
        if  asset_total >= asset.base_qty * asset.profit_percentage:

            return True

        return False

    @staticmethod
    def execution(asset, other_asset, transactions_count):
        price = asset.take_price('BTCBUSD')
        if asset.name == 'BTC':
            trade_qty = asset.qty * Asset.FACTOR
            asset.qty -= trade_qty
            result_qty = trade_qty * price
            other_asset.qty += result_qty


        else:
            trade_qty = asset.qty * Asset.FACTOR
            asset.qty -= trade_qty
            result_qty = trade_qty / price
            other_asset.qty += result_qty
        other_asset.base_qty = other_asset.take_total_qty(other_asset, asset)
        other_asset.execution_percentage = None

        asset.number_trades += 1
        other_asset.number_trades -= 1
        print(f'{asset.name} asset num trades: {asset.number_trades}')
        print(f'{other_asset.name} asset num trades: {other_asset.number_trades}')
        if asset.number_trades == 3:
            asset.number_trades = 0
            other_asset.number_trades = 0
            asset.profit_percentage = Asset.PROFIT_PERCENTAGE
            other_asset.profit_percentage = Asset.PROFIT_PERCENTAGE
            asset.execution_percentage = None
            other_asset.execution_percentage = None
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
        asset.execution_percentage = asset.profit_percentage - 3 * Asset.INCREASE_STEP
        print(f'{asset.name} increase profit percentage: {asset.profit_percentage}')
        print(f'{asset.name} execution profit percentage: {asset.execution_percentage}')

    @staticmethod
    def check_for_execution(asset, other_asset):
        if asset.execution_percentage is not None:
            if asset.take_total_qty(asset, other_asset) <= asset.base_qty * asset.execution_percentage:
                return True
        return False

    def add_usdt(self, asset, other_asset):
        if asset.name == 'BTC':
            price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            addition_qty = 11 / price
            asset.qty += addition_qty
            # asset.base_qty = asset.take_total_qty(asset, other_asset)
            # other_asset.base_qty = other_asset.take_total_qty(other_asset,asset)

        else:
            price = float(client.get_symbol_ticker(symbol='BUSDUSDT')['price'])
            addition_qty = 11 / price
            asset.qty += addition_qty
            # asset.base_qty = asset.take_total_qty(asset, other_asset)
            # other_asset.base_qty = other_asset.take_total_qty(other_asset, asset)
        return f'-------ДОБАВЯНЕ-------\n{addition_qty} {asset.name} -> {asset.qty}'

    @staticmethod
    def next_prices(asset, other_asset, percentage):
        if percentage is not None:
            if asset.name == 'BTC':
                price = other_asset.qty/ (asset.base_qty * percentage - asset.qty)

            else:
                price = (asset.base_qty * percentage - asset.qty) / other_asset.qty
            string_exp = ''
            if percentage == asset.profit_percentage:
                string_exp = f'Следваща цена покачване: {asset.name}'
            elif percentage == asset.execution_percentage:
                string_exp = f'Следваща цена изпълнение: {asset.name}'
            return f'{string_exp} {price}'
        return 'Execution Percentage is None'

    @staticmethod
    def profit_info(asset, other_asset):
        btc_profit = (asset.base_qty / asset.init_qty - 1) * 100
        busd_profit = (other_asset.base_qty / other_asset.init_qty - 1) * 100
        return f'Печалба BTC: {btc_profit:.2f}%\nПечалба BUSD: {busd_profit:.2f}%'
