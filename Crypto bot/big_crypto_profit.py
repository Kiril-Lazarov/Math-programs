import asyncio
from binance.client import Client
import pandas as pd
from binance import BinanceSocketManager

api_key = "api key"
api_secret = "api secret"


async def main():
    # client = Client(API_KEY, API_SECRET)
    client = Client()

    bsm = BinanceSocketManager(client)

    socket = bsm.trade_socket('BTCUSDT')

    async with socket as ts:
        msg = await ts.recv()

    return msg
msg = asyncio.run(main())



def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,["s", "E", "p"]]
    df.columns = ["Symbol", "Time", "Price"]
    df.Price = df.Price.astype(float)
    # df.Time = df.Time("ms")
    return df

print(createframe(msg))