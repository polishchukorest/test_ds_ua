import asyncio
import websockets

PORT = 8000

async def process_trade(websocket):
    async for message in websocket:
        trade = await websocket.recv()
        print(f'trade:{trade}')

async def main():

    async with websockets.serve(process_trade, "localhost", PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    #df = pd.read_parquet("trades_sample.parquet")
    #df.sort_values('timestamp', inplace=True)
    asyncio.run(main())

