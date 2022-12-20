
from binance.client import Client
api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)
xrp = float(client.get_asset_balance('XRP')['free'])
eth = float(client.get_asset_balance('ETH')['free'])
bnb = float(client.get_asset_balance('BNB')['free'])

total_usdt = xrp * float(client.get_symbol_ticker(symbol='XRPUSDT')['price']) +\
    eth * float(client.get_symbol_ticker(symbol='ETHUSDT')['price']) +\
    bnb * float(client.get_symbol_ticker(symbol='BNBUSDT')['price']) +\
    float(client.get_asset_balance('USDT')['free'])

total_btc =  xrp * float(client.get_symbol_ticker(symbol='XRPBTC')['price']) +\
    eth * float(client.get_symbol_ticker(symbol='ETHBTC')['price']) +\
    bnb * float(client.get_symbol_ticker(symbol='BNBBTC')['price'])

print(total_usdt)
print(total_btc)