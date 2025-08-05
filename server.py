import asyncio
import websockets
import logging
from datetime import datetime

logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
PORT = 8000


client_list = []   
async def handler(websocket):
    #get all clients
    client_list.append(websocket)
    while True:
        try:
            message = await websocket.recv()
            logger.info(f'received trade: {message}')
            await broadcast(message)
        except Exception as e:
            print(e)
            client_list.remove(websocket)
            break

async def broadcast(message):
    logger.info(f'send trade: {message}')      
    for client in client_list:
        await client.send(message)

async def main():
    async with websockets.serve(handler, "localhost", PORT, ping_timeout=None):
        print('server running')
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

