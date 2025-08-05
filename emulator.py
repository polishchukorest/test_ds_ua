import pandas as pd
import asyncio
import websockets
import json
import logging
from datetime import datetime
import os 

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/emulator.log",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


PORT = 8000


async def client(df):
    """
    trades emulation using .parquet file
    """
    async with websockets.connect(f"ws://localhost:{PORT}", ping_interval=None, ping_timeout=None) as websocket:
        #needed to calculate time diff between trades
        last_time = df.iloc[0]['timestamp']
        num_sent = 0
        print('emulator running')
        #grouped by timestamp, df already sorted, so we sent chronologically trades, and, 
        #if they have the same timestamp send them asynchronically in one batch
        for timestamp, trades in df.groupby('timestamp'):
            trades['timestamp'] = trades['timestamp'].dt.strftime('%Y-%m-%d %X')
            trades = trades.to_dict('records')
            #print(trades)
            logger.info(f"grouped by trades from df: {trades}")
            await asyncio.gather(
                *[websocket.send(json.dumps(trade)) for trade in trades]
            )
            logger.info(f"sent trades: {trades}")

            time_to_wait = (timestamp - last_time).total_seconds()
            #time_to_wait = 0.1
            await asyncio.sleep(time_to_wait)
            last_time = timestamp
            logger.info(f'time to wait diff: {time_to_wait}')
            num_sent+=1
            #print(f"time to wait: {time_to_wait}")
        
        print('emulation finished')
        await websocket.close() 
            

if __name__ == "__main__":
    df = pd.read_parquet("trades_sample.parquet")
    #sort out trades so they are processed chronologically
    df.sort_values('timestamp', inplace=True)
    asyncio.run(client(df))
