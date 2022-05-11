import asyncio
from binance.client import Client
import pandas as pd
from binance import BinanceSocketManager

api_key = "CDC4VCJASc0ZBHe1ZrXGM6BFUbGqp7nUAe3cbIkFUKfbjitPsLKOocvbGWyM6i78"
api_secret = "oJkghtV3LZFCCeJ8Vj7TA9TCdVVQzY9ezcZpygCiQPMwY5pzv2gCIT2UwYOJDhEd"

# def create_frame(msg):
#     df = pd.DataFrame([msg])
#     df = df.loc[:, ["s", "E", "p"]]
#     df.columns = ["Symbol", "Time", "Price"]
#     df.Price = df.Price.astype(float)
#     df.Time = pd.to_datetime(df.Time, unit="ms")
#     return df
initial_price = 30000
upper_limit = initial_price * 1.01
lower_limit = initial_price * 0.99
price_dict = {"Init": initial_price, "Low": lower_limit, "Up": upper_limit}

quantities_dict = {"USDT": 1000, "BTC": 0.034482}

commission = 0.995

last_bitcoin_trades = []
last_usdt_trades = []


# Defines quantities to trade
def define_quantity(crypto, price):
    initial_percentage = 1
    if crypto == "USDT":
        if quantities_dict['USDT'] * 0.75 >= 316:
            initial_percentage = 0.25
        else:
            initial_percentage = 0.2
        quantities_dict['USDT'] *= (1 - initial_percentage)
        quantities_dict['BTC'] += (quantities_dict['USDT'] * initial_percentage) / price * commission
        last_bitcoin_trades.append((quantities_dict['USDT'] * initial_percentage) / price * commission)
    elif crypto == "BTC":
        if quantities_dict['BTC'] * 0.75 >= 0.010910:
            initial_percentage = 0.25
        else:
            initial_percentage = 0.2
        quantities_dict["BTC"] *= (1 - initial_percentage)
        quantities_dict["USDT"] += (quantities_dict['BTC'] * initial_percentage) * price * commission
        


# Execute orders
def order_execution(price, side):
    if side == "Buy":
        quantity = define_quantity("USDT", price)
    else:
        pass


def check_price(price):
    price = float(price)
    if price >= price_dict["Up"]:
        order_execution(price, "Sell")
    elif price <= price_dict["Low"]:
        order_execution(price, "Buy")


async def main():
    # client = Client(API_KEY, API_SECRET)
    client = Client()

    bsm = BinanceSocketManager(client)

    socket = bsm.trade_socket('BTCUSDT')

    async with socket as ts:
        while True:
            await socket.__aenter__()
            msg = await ts.recv()
            # frame = create_frame(msg)

            check_price(msg["p"])


msg = asyncio.run(main())

# print(asyncio.run(create_frame(msg)))
