import asyncio
from binance.client import Client
import pandas as pd
from binance import BinanceSocketManager

api_key = "Api key"
api_secret = "Api secret"

def create_frame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ["s", "E", "p"]]
    df.columns = ["Symbol", "Time", "Price"]
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit="ms")
    return df

async def main():
    # client = Client(API_KEY, API_SECRET)
    client = Client()

    bsm = BinanceSocketManager(client)

    socket = bsm.trade_socket('BTCUSDT')

    async with socket as ts:
        while True:
            await socket.__aenter__()
            msg = await ts.recv()
            frame = create_frame(msg)
            print(frame)


msg = asyncio.run(main())





# print(asyncio.run(create_frame(msg)))
