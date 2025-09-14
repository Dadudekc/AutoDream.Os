#!/usr/bin/env python3
"""
Dashboard WebSocket Handlers - V2 Compliant Module
================================================

WebSocket handlers for real-time dashboard updates.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Dashboard Modularization
License: MIT
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set

from fastapi import WebSocket, WebSocketDisconnect

from .dashboard_models import WebSocketMessage
from .dashboard_routes import dashboard_routes

# Setup logging
logger = logging.getLogger(__name__)


class WebSocketManager:
    """WebSocket connection manager."""

    def __init__(self):
        """Initialize WebSocket manager."""
        self.active_connections: List[WebSocket] = []
        self.logger = logger

    async def connect(self, websocket: WebSocket) -> None:
        """Accept WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """Send message to specific WebSocket."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            self.logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: str) -> None:
        """Broadcast message to all connected WebSockets."""
        if not self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                self.logger.error(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)

        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_data(self, data_type: str, data: Dict) -> None:
        """Broadcast structured data to all connections."""
        message = WebSocketMessage(
            type=data_type,
            data=data,
            timestamp=datetime.now()
        )
        await self.broadcast(message.json())


class DashboardWebSocketHandlers:
    """Dashboard WebSocket handlers."""

    def __init__(self):
        """Initialize WebSocket handlers."""
        self.manager = WebSocketManager()
        self.logger = logger
        self._broadcast_task = None

    async def websocket_endpoint(self, websocket: WebSocket) -> None:
        """Handle WebSocket connections."""
        await self.manager.connect(websocket)
        
        try:
            while True:
                # Wait for client messages
                data = await websocket.receive_text()
                
                try:
                    message_data = json.loads(data)
                    await self._handle_client_message(websocket, message_data)
                except json.JSONDecodeError:
                    await self._send_error(websocket, "Invalid JSON format")
                except Exception as e:
                    self.logger.error(f"Error handling client message: {e}")
                    await self._send_error(websocket, f"Error: {str(e)}")
                    
        except WebSocketDisconnect:
            self.manager.disconnect(websocket)
        except Exception as e:
            self.logger.error(f"WebSocket error: {e}")
            self.manager.disconnect(websocket)

    async def _handle_client_message(self, websocket: WebSocket, message_data: Dict) -> None:
        """Handle client messages."""
        message_type = message_data.get("type", "")
        
        if message_type == "ping":
            await self._handle_ping(websocket)
        elif message_type == "subscribe":
            await self._handle_subscribe(websocket, message_data)
        elif message_type == "unsubscribe":
            await self._handle_unsubscribe(websocket, message_data)
        elif message_type == "request_data":
            await self._handle_data_request(websocket, message_data)
        else:
            await self._send_error(websocket, f"Unknown message type: {message_type}")

    async def _handle_ping(self, websocket: WebSocket) -> None:
        """Handle ping message."""
        pong_message = WebSocketMessage(
            type="pong",
            data={"timestamp": datetime.now().isoformat()},
            timestamp=datetime.now()
        )
        await self.manager.send_personal_message(pong_message.json(), websocket)

    async def _handle_subscribe(self, websocket: WebSocket, message_data: Dict) -> None:
        """Handle subscription request."""
        subscription_type = message_data.get("data", {}).get("type", "")
        
        if subscription_type in ["all", "agents", "metrics", "consolidation", "alerts"]:
            await self._send_success(websocket, f"Subscribed to {subscription_type}")
        else:
            await self._send_error(websocket, f"Invalid subscription type: {subscription_type}")

    async def _handle_unsubscribe(self, websocket: WebSocket, message_data: Dict) -> None:
        """Handle unsubscription request."""
        subscription_type = message_data.get("data", {}).get("type", "")
        await self._send_success(websocket, f"Unsubscribed from {subscription_type}")

    async def _handle_data_request(self, websocket: WebSocket, message_data: Dict) -> None:
        """Handle data request."""
        data_type = message_data.get("data", {}).get("type", "")
        
        try:
            if data_type == "agents":
                agents = dashboard_routes.get_agent_statuses()
                await self.manager.send_personal_message(
                    json.dumps([agent.dict() for agent in agents]), websocket
                )
            elif data_type == "metrics":
                metrics = dashboard_routes.get_swarm_metrics()
                await self.manager.send_personal_message(metrics.json(), websocket)
            elif data_type == "consolidation":
                progress = dashboard_routes.get_consolidation_progress()
                await self.manager.send_personal_message(progress.json(), websocket)
            elif data_type == "alerts":
                alerts = dashboard_routes.get_alerts()
                await self.manager.send_personal_message(
                    json.dumps([alert.dict() for alert in alerts]), websocket
                )
            else:
                await self._send_error(websocket, f"Unknown data type: {data_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling data request: {e}")
            await self._send_error(websocket, f"Error getting {data_type} data")

    async def _send_success(self, websocket: WebSocket, message: str) -> None:
        """Send success message."""
        success_message = WebSocketMessage(
            type="success",
            data={"message": message},
            timestamp=datetime.now()
        )
        await self.manager.send_personal_message(success_message.json(), websocket)

    async def _send_error(self, websocket: WebSocket, error_message: str) -> None:
        """Send error message."""
        error_response = WebSocketMessage(
            type="error",
            data={"error": error_message},
            timestamp=datetime.now()
        )
        await self.manager.send_personal_message(error_response.json(), websocket)

    async def start_broadcast_updates(self) -> None:
        """Start broadcasting updates to all connected clients."""
        if self._broadcast_task is None:
            self._broadcast_task = asyncio.create_task(self._broadcast_loop())

    async def stop_broadcast_updates(self) -> None:
        """Stop broadcasting updates."""
        if self._broadcast_task:
            self._broadcast_task.cancel()
            self._broadcast_task = None

    async def _broadcast_loop(self) -> None:
        """Broadcast loop for real-time updates."""
        while True:
            try:
                if self.manager.active_connections:
                    # Broadcast agent statuses
                    agents = dashboard_routes.get_agent_statuses()
                    await self.manager.broadcast_data(
                        "agents_update",
                        {"agents": [agent.dict() for agent in agents]}
                    )
                    
                    # Broadcast metrics
                    metrics = dashboard_routes.get_swarm_metrics()
                    await self.manager.broadcast_data(
                        "metrics_update",
                        {"metrics": metrics.dict()}
                    )
                    
                    # Broadcast consolidation progress
                    progress = dashboard_routes.get_consolidation_progress()
                    await self.manager.broadcast_data(
                        "consolidation_update",
                        {"progress": progress.dict()}
                    )
                
                # Wait before next broadcast
                await asyncio.sleep(5)  # 5 second intervals
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.manager.active_connections)


# Create WebSocket handlers instance
dashboard_websocket = DashboardWebSocketHandlers()


# Export for use by main dashboard
__all__ = ["dashboard_websocket", "DashboardWebSocketHandlers", "WebSocketManager"]
