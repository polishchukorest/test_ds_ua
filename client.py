import asyncio
import websockets


PORT = 8000

async def client():
    async with websockets.connect(f"ws://localhost:{PORT}") as websocket:
        while True:
            try:
                trade = await websocket.recv()
                print(f"Received trade: {trade}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        #response = await websocket.recv()
        #print(f"Received trade from server: {response}")

if __name__ == "__main__":
    asyncio.run(client())