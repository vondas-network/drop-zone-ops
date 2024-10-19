import asyncio
import websockets
import json
import uuid

# OBS WebSocket connection details
host = 'localhost'
port = 4455

async def listen_for_events():
    uri = f"ws://{host}:{port}"
    async with websockets.connect(uri) as websocket:
        print("Connected to OBS WebSocket.")

        # Send identify message to OBS WebSocket server
        identify_message = {
            "op": 1,  # Identify operation
            "d": {
                "rpcVersion": 1
            }
        }
        await websocket.send(json.dumps(identify_message))
        print("Identified with the WebSocket server.")

        # Subscribe to all events
        subscribe_message = {
            "op": 6,  # Subscribe operation
            "d": {
                "eventSubscriptions": ["*"],  # Subscribe to all events
                "requestId": str(uuid.uuid4()),  # Generate a unique request ID
                "requestType": "subscribe"  # Specify the request type
            }
        }
        await websocket.send(json.dumps(subscribe_message))
        print("Subscribed to all events.")

        # Listen for events
        while True:
            try:
                message = await websocket.recv()
                event_data = json.loads(message)

                # Print all incoming messages
                print("Received message:", event_data)

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

async def main():
    try:
        await listen_for_events()
    except Exception as e:
        print(f"Failed to connect to OBS WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(main())