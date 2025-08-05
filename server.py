import asyncio
import websockets
import logging
import os
import pandas as pd
import json

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
PORT = 8000

async def process_trade(websocket):
    print("server running")
    
    df = pd.read_parquet("trades_sample.parquet")
    df.sort_values('timestamp', inplace=True)

    last_time = df.iloc[0]['timestamp']
    for timestamp, trades in df.groupby('timestamp'):
        trades['timestamp'] = trades['timestamp'].dt.strftime('%Y-%m-%d %X')
        trades = trades.to_dict('records')
        print(trades)
        await asyncio.gather(
            *[websocket.send(json.dumps(trade)) for trade in trades]
        )
        logger.info(f"sent trades: {trades}")
        time_to_wait = (timestamp - last_time).total_seconds()
        await asyncio.sleep(time_to_wait)
        logger.info(f'time to wait diff: {time_to_wait}')
        last_time = timestamp

async def main():

    async with websockets.serve(process_trade, "localhost", PORT):
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())

