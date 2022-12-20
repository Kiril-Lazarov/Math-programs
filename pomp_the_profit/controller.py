from binance.client import Client

from pomp_the_profit.pomp_asset import PompAsset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])

btc = PompAsset('BTC', 0.1,price)
usdt = PompAsset('USDT', btc.qty * price, price)

object_on_charge = btc
other_object = usdt

while True:
    price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
    if not object_on_charge.prices_list:
        object_on_charge.prices_list.append(price)
        print(object_on_charge.execute_trade(price, other_object.name))
    object_on_charge.check_for_execution(price)


