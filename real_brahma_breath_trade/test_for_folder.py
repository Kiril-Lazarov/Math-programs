import time

from binance.client import Client
from binance.enums import *

from real_brahma_breath_trade.brahma_asset import Asset

api_key = 'zlQZ3S5PLL4W6rQ2AJEVlUpzFhPocWfhVFPiX0AYCwFi07uhnmmLMCyBtDHxpikh'
api_secret = 'hoevSXLi4CdhnFQRF3BWiv3JKeSDrP6QASFrDoz9TgkphNqgoKD9BEzlNmjREMkW'

client = Client(api_key, api_secret)

with open('brahma_data.txt') as file:
    # xrp, bnb, eth = file.readline().split(', ')
    a = file.read().split()
    print(len(a))

# xrp_qty = client.get_asset_balance('XRP')['free']
# bnb_qty = client.get_asset_balance('BNB')['free']
# eth_qty = client.get_asset_balance('ETH')['free']
# print(xrp, bnb, eth)
# print(xrp == xrp_qty)