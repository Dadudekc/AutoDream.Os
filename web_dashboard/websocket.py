"""
Enhanced WebSocket Server for Real-time Dashboard Updates
=======================================================

Provides real-time updates for the Dream.OS Captain Dashboard including:
- Devlog analytics and trends
- Agent activity monitoring
- System health metrics
- Live log streaming
"""

import asyncio
import datetime
import json
import logging

import websockets

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardWebSocketServer:
    """Enhanced WebSocket server for real-time dashboard updates."""

    def __init__(self, host: str = "localhost", port: int = 8001):
        """Initialize the WebSocket server."""
        self.host = host
        self.port = port
        self.connected_clients: set = set()
        self.devlogs_cache = []
        self.last_devlog_update = datetime.datetime.now()

        # Start background tasks
        self.running = True
        logger.info(f"DashboardWebSocketServer initialized on {host}:{port}")

    async def handle_client(self, websocket, path: str):
        """Handle individual client connections."""
        client_address = websocket.remote_address
        logger.info(f"Client connected: {client_address}")

        # Add client to connected set
        self.connected_clients.add(websocket)

        try:
            # Send initial data
            await self.send_initial_data(websocket)

            # Keep connection alive and send updates
            while self.running:
                try:
                    # Check for client messages
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)

                    # Handle client messages (if needed)
                    if message == "ping":
                        await websocket.send(json.dumps({"type": "pong"}))

                except TimeoutError:
                    # No message from client, continue
                    pass
                except websockets.exceptions.ConnectionClosed:
                    break

                # Send periodic updates
                await self.send_periodic_updates(websocket)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_address}")
        finally:
            # Remove client from connected set
            self.connected_clients.discard(websocket)

    async def send_initial_data(self, websocket):
        """Send initial dashboard data to newly connected client."""
        try:
            # System metrics
            system_metrics = {
                "type": "system_metrics",
                "data": {
                    "active_agents": 8,
                    "completed_contracts": 12,
                    "system_uptime": self._get_uptime(),
                    "cpu_usage": 45,
                    "memory_usage": 67,
                    "disk_usage": 23,
                },
                "timestamp": datetime.datetime.now().isoformat(),
            }
            await websocket.send(json.dumps(system_metrics))

            # Devlog analytics summary
            devlog_summary = await self._get_devlog_summary()
            if devlog_summary:
                await websocket.send(json.dumps(devlog_summary))

            # Agent status
            agent_status = {
                "type": "agent_status",
                "data": await self._get_agent_status(),
                "timestamp": datetime.datetime.now().isoformat(),
            }
            await websocket.send(json.dumps(agent_status))

        except Exception as e:
            logger.error(f"Error sending initial data: {e}")

    async def send_periodic_updates(self, websocket):
        """Send periodic updates to connected clients."""
        try:
            # Send system metrics every 10 seconds
            if int(datetime.datetime.now().timestamp()) % 10 == 0:
                system_metrics = {
                    "type": "system_metrics",
                    "data": {
                        "cpu_usage": 40
                        + (datetime.datetime.now().second % 20),  # Simulated variation
                        "memory_usage": 60 + (datetime.datetime.now().second % 15),
                        "disk_usage": 20 + (datetime.datetime.now().second % 10),
                        "active_connections": len(self.connected_clients),
                    },
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                await websocket.send(json.dumps(system_metrics))

            # Send devlog updates every 30 seconds
            if int(datetime.datetime.now().timestamp()) % 30 == 0:
                devlog_summary = await self._get_devlog_summary()
                if devlog_summary:
                    await websocket.send(json.dumps(devlog_summary))

            # Send live log message every 5 seconds
            if int(datetime.datetime.now().timestamp()) % 5 == 0:
                log_message = {
                    "type": "log",
                    "data": {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "level": "INFO",
                        "message": f"Dashboard update - {len(self.connected_clients)} active connections",
                        "source": "websocket_server",
                    },
                }
                await websocket.send(json.dumps(log_message))

            await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error sending periodic updates: {e}")

    async def _get_devlog_summary(self) -> dict:
        """Get summary of recent devlog activity."""
        try:
            # This would normally query the vector database
            # For now, return simulated data
            return {
                "type": "devlog_summary",
                "data": {
                    "total_devlogs": 156,
                    "today_devlogs": 12,
                    "active_agents": 6,
                    "completion_rate": 87.5,
                    "top_agent": "Agent-4",
                    "recent_activity": [
                        {
                            "agent": "Agent-4",
                            "action": "Enhanced Devlog System Implementation",
                            "status": "completed",
                            "timestamp": datetime.datetime.now().isoformat(),
                        },
                        {
                            "agent": "Agent-2",
                            "action": "Architecture review completed",
                            "status": "completed",
                            "timestamp": (
                                datetime.datetime.now() - datetime.timedelta(minutes=5)
                            ).isoformat(),
                        },
                    ],
                },
                "timestamp": datetime.datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting devlog summary: {e}")
            return None

    async def _get_agent_status(self) -> list[dict]:
        """Get current status of all agents."""
        try:
            # Simulated agent status data
            agents = [
                {
                    "id": "Agent-1",
                    "status": "ACTIVE",
                    "current_task": "V3-010",
                    "efficiency": 9.5,
                    "last_activity": datetime.datetime.now().isoformat(),
                },
                {
                    "id": "Agent-2",
                    "status": "ACTIVE",
                    "current_task": "V3-008",
                    "efficiency": 8.8,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=2)
                    ).isoformat(),
                },
                {
                    "id": "Agent-3",
                    "status": "ACTIVE",
                    "current_task": "V3-003",
                    "efficiency": 8.2,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=1)
                    ).isoformat(),
                },
                {
                    "id": "Agent-4",
                    "status": "ACTIVE",
                    "current_task": "V3-COORDINATION-001",
                    "efficiency": 9.8,
                    "last_activity": datetime.datetime.now().isoformat(),
                },
                {
                    "id": "Agent-5",
                    "status": "ACTIVE",
                    "current_task": "AUTONOMOUS_OPERATION",
                    "efficiency": 8.0,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=3)
                    ).isoformat(),
                },
                {
                    "id": "Agent-6",
                    "status": "ACTIVE",
                    "current_task": "AUTONOMOUS_OPERATION",
                    "efficiency": 8.3,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=1)
                    ).isoformat(),
                },
                {
                    "id": "Agent-7",
                    "status": "ACTIVE",
                    "current_task": "AUTONOMOUS_OPERATION",
                    "efficiency": 7.9,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=4)
                    ).isoformat(),
                },
                {
                    "id": "Agent-8",
                    "status": "ACTIVE",
                    "current_task": "AUTONOMOUS_OPERATION",
                    "efficiency": 8.1,
                    "last_activity": (
                        datetime.datetime.now() - datetime.timedelta(minutes=2)
                    ).isoformat(),
                },
            ]
            return agents
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return []

    def _get_uptime(self) -> str:
        """Get system uptime as formatted string."""
        try:
            # Calculate uptime since server start
            uptime_seconds = int(
                (datetime.datetime.now() - self._server_start_time).total_seconds()
            )
            hours, remainder = divmod(uptime_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours}h {minutes}m {seconds}s"
        except:
            return "Unknown"

    async def broadcast_message(self, message: dict):
        """Broadcast a message to all connected clients."""
        if not self.connected_clients:
            return

        message_json = json.dumps(message)
        disconnected_clients = []

        for websocket in self.connected_clients.copy():
            try:
                await websocket.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(websocket)

        # Remove disconnected clients
        for websocket in disconnected_clients:
            self.connected_clients.discard(websocket)

    async def start(self):
        """Start the WebSocket server."""
        self._server_start_time = datetime.datetime.now()
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")

        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever

    async def stop(self):
        """Stop the WebSocket server."""
        logger.info("Stopping WebSocket server...")
        self.running = False

        # Close all connections
        for websocket in self.connected_clients.copy():
            try:
                await websocket.close()
            except:
                pass

        self.connected_clients.clear()


# Global server instance
websocket_server = DashboardWebSocketServer()


async def main():
    """Main function to run the WebSocket server."""
    try:
        await websocket_server.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        await websocket_server.stop()


if __name__ == "__main__":
    asyncio.run(main())
