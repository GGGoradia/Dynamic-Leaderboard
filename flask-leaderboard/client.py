import asyncio
import websockets
import json
import sys

# Set a compatible event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def listen():
    url = "ws://127.0.0.1:5000/ws/leaderboard"
    while True:
        try:
            async with websockets.connect(url) as websocket:
                print("Connected to the WebSocket server")

                while True:
                    message = await websocket.recv()
                    print("Received update from server:")
                    leaderboard = json.loads(message)
                    for player in leaderboard:
                        print(f"{player['name']}: {player['score']}")
        
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting...")
            await asyncio.sleep(2)  # Wait before reconnecting
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(2)  # Wait before retrying

# Run the WebSocket client
asyncio.run(listen())
