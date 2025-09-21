
import asyncio
import websockets
import json
import datetime

async def handle_client(websocket, path):
    print(f"Client connected: {websocket.remote_address}")
    
    try:
        while True:
            # Send live metrics
            metrics = {
                "type": "metric",
                "metrics": {
                    "active_agents": 4,
                    "completed_contracts": 3,
                    "system_uptime": "2h 15m"
                }
            }
            await websocket.send(json.dumps(metrics))
            
            # Send sample log
            log = {
                "type": "log",
                "log": {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "level": "INFO",
                    "message": "System running normally"
                }
            }
            await websocket.send(json.dumps(log))
            
            await asyncio.sleep(5)
            
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

start_server = websockets.serve(handle_client, "localhost", 8001)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
