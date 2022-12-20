from binance.client import Client

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
initial_total_qty = 1299.46
usdt = float(client.get_asset_balance('USDT')['free'])
print(usdt)
busd = float(client.get_asset_balance('BUSD')['free'])
print(busd)
btc = float(client.get_asset_balance('BTC')['free'])
print(btc)
btc_usdt_price = float(client.get_symbol_ticker(symbol= 'BTCUSDT')['price'])
busd_usdt_price = float(client.get_symbol_ticker(symbol= 'BUSDUSDT')['price'])
total = usdt + btc*btc_usdt_price + busd*busd_usdt_price
print(total)
print(f'Price BTCUSDT: {btc_usdt_price:.2f}')
print(f'{((total/ initial_total_qty - 1)* 100)}%')

'binance.exceptions.BinanceAPIException:' \
' APIError(code=-1003): Too much request weight used; ' \
'current limit is 1200 request weight per 1 MINUTE. ' \
'Please use the websocket for live updates to avoid polling the API.'
