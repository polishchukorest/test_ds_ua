import pandas as pd
import asyncio
import websockets
import json
import time

PORT = 8000

async def client(df):
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        for timestamp, trades in df.groupby('timestamp'):
            trades['timestamp'] = trades['timestamp'].dt.strftime('%Y-%m-%d %X')
            trades = trades.to_dict('records')
            #print(trades)
            message = {
                "trades": trades
            }
            #print(message)
            await websocket.send(json.dumps(message))
            await asyncio.sleep(2)
            print(f"sent trades: {message}")

async def client_test():
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        trade = {
            "timestamp": "2025-08-02",
            "trade": {
                "price": 1,
                "vol":20
            }
        }
        await websocket.send(json.dumps(trade))
        #response = await websocket.recv()
        print(f"sent to server: {json.dumps(trade)}")


if __name__ == "__main__":
    df = pd.read_parquet("trades_sample.parquet")
    df.sort_values('timestamp', inplace=True)
    #asyncio.run(client_test())
    asyncio.run(client(df))
