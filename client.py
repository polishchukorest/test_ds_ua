import asyncio
import websockets


PORT = 8000

async def client():
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        await websocket.send()
        response = await websocket.recv()
        print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(client())