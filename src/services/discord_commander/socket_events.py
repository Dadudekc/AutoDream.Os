#!/usr/bin/env python3
"""
Discord Commander SocketIO Events
=================================

Handles SocketIO events for real-time communication.
"""

import logging
from datetime import datetime
from typing import Any

try:
    from flask_socketio import emit

    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False

logger = logging.getLogger(__name__)


class SocketEventHandler:
    """Handles SocketIO events for real-time communication."""

    def __init__(self, socketio=None):
        """Initialize the socket event handler."""
        self.socketio = socketio
        self.connected_clients = set()
        self.message_history = []

    def register_events(self):
        """Register SocketIO events."""
        if not SOCKETIO_AVAILABLE or not self.socketio:
            logger.warning("SocketIO not available, skipping event registration")
            return

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection."""
            logger.info(f"Client connected: {request.sid}")
            self.connected_clients.add(request.sid)
            emit(
                "status",
                {
                    "message": "Connected to Discord Commander",
                    "timestamp": datetime.now().isoformat(),
                },
            )

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info(f"Client disconnected: {request.sid}")
            self.connected_clients.discard(request.sid)

        @self.socketio.on("join_room")
        def handle_join_room(data):
            """Handle joining a room."""
            room = data.get("room", "general")
            join_room(room)
            emit(
                "status",
                {"message": f"Joined room: {room}", "timestamp": datetime.now().isoformat()},
            )

        @self.socketio.on("leave_room")
        def handle_leave_room(data):
            """Handle leaving a room."""
            room = data.get("room", "general")
            leave_room(room)
            emit(
                "status", {"message": f"Left room: {room}", "timestamp": datetime.now().isoformat()}
            )

        @self.socketio.on("send_message")
        def handle_send_message(data):
            """Handle sending a message."""
            try:
                message = data.get("message", "")
                room = data.get("room", "general")

                if not message:
                    emit("error", {"message": "Message cannot be empty"})
                    return

                # Store message in history
                message_data = {
                    "id": len(self.message_history) + 1,
                    "message": message,
                    "room": room,
                    "timestamp": datetime.now().isoformat(),
                    "sender": request.sid,
                }
                self.message_history.append(message_data)

                # Broadcast to room
                emit("message_received", message_data, room=room)

            except Exception as e:
                logger.error(f"Error handling message: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("get_message_history")
        def handle_get_message_history(data):
            """Handle getting message history."""
            try:
                room = data.get("room", "general")
                limit = data.get("limit", 50)

                # Filter messages by room and limit
                room_messages = [msg for msg in self.message_history if msg["room"] == room][
                    -limit:
                ]

                emit(
                    "message_history",
                    {"room": room, "messages": room_messages, "count": len(room_messages)},
                )

            except Exception as e:
                logger.error(f"Error getting message history: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("agent_status_request")
        def handle_agent_status_request():
            """Handle agent status request."""
            try:
                # This would integrate with the actual agent system
                agent_status = {
                    "Agent-1": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
                    "Agent-2": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
                    "Agent-3": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
                    "Agent-4": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
                    "Agent-5": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
                }

                emit(
                    "agent_status_response",
                    {"agents": agent_status, "timestamp": datetime.now().isoformat()},
                )

            except Exception as e:
                logger.error(f"Error getting agent status: {e}")
                emit("error", {"message": str(e)})

    def broadcast_agent_update(self, agent_data: dict[str, Any]):
        """Broadcast agent status update to all connected clients."""
        if not SOCKETIO_AVAILABLE or not self.socketio:
            return

        self.socketio.emit(
            "agent_update", {"agent": agent_data, "timestamp": datetime.now().isoformat()}
        )

    def broadcast_system_message(self, message: str, level: str = "info"):
        """Broadcast system message to all connected clients."""
        if not SOCKETIO_AVAILABLE or not self.socketio:
            return

        self.socketio.emit(
            "system_message",
            {"message": message, "level": level, "timestamp": datetime.now().isoformat()},
        )

    def get_connection_count(self) -> int:
        """Get number of connected clients."""
        return len(self.connected_clients)

    def get_message_count(self) -> int:
        """Get total number of messages in history."""
        return len(self.message_history)
