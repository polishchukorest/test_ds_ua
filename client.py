import asyncio
import websockets
import logging
from datetime import datetime
PORT = 8000

logging.basicConfig(
    filename="logs/client.log",
    level=logging.INFO
)

logger = logging.getLogger(__name__)



async def client():
    """
    Client that recieves the trades
    """
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        print("Cient connected")
        while True:
            try:
                trade = await websocket.recv()
                logger.info(f"Received trade: {trade}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed.")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    asyncio.run(client())