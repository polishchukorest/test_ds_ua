import pandas as pd
import asyncio
import websockets
import json
import time

PORT = 8000

async def client(df):
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        #time delay emulation
        last_time = df.iloc[0]['timestamp']
        for timestamp, trades in df.groupby('timestamp'):
            trades['timestamp'] = trades['timestamp'].dt.strftime('%Y-%m-%d %X')
            trades = trades.to_dict('records')
            print(trades)
            #print(trades)
            message = {
                "trades": trades
            }
            #print(message)
            await asyncio.gather(
                *[websocket.send(json.dumps(trade)) for trade in trades]
            )
            #await websocket.send(trades)
            #await websocket.send(json.dumps(message))
            time_to_wait = (timestamp - last_time).microseconds/(10**6)
            await asyncio.sleep(time_to_wait)
            last_time = timestamp
            print(f'time to wait diff: {time_to_wait}')
            print(f"sent trades: {message}")

if __name__ == "__main__":
    df = pd.read_parquet("trades_sample.parquet")
    df.sort_values('timestamp', inplace=True)
    #asyncio.run(client_test())
    asyncio.run(client(df))
