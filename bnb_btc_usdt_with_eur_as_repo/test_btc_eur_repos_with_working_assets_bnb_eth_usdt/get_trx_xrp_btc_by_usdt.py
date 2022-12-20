from binance.client import Client

# from binance.enums import *

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

btc_usdt_price = float(client.get_symbol_ticker(symbol='BTCUSDT')['price'])
xrp_usdt_price = float(client.get_symbol_ticker(symbol='XRPUSDT')['price'])
trx_usdt_price = float(client.get_symbol_ticker(symbol='TRXUSDT')['price'])

usdt_qty = 1200

btc_qty = usdt_qty / btc_usdt_price
xrp_qty = usdt_qty/xrp_usdt_price
trx_qty = usdt_qty/trx_usdt_price

print(f'BTC: {btc_qty:.5f}\nXRP: {xrp_qty:.3f}\nTRX: {trx_qty:.2f}')