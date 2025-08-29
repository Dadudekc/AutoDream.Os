#!/usr/bin/env python3
"""
Flask Portal App - V2 Core Web Integration

Flask-based web application for the unified portal.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging

from typing import Optional
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from src.settings import SECRET_KEY
from .portal_core import UnifiedPortal
from .data_models import PortalConfig
from .routes import register_routes


class FlaskPortalApp:
    """
    Flask-based portal web application

    Single responsibility: Flask web interface for portal.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self, portal: UnifiedPortal, config: Optional[PortalConfig] = None):
        """Initialize Flask portal app"""
        self.portal = portal
        self.config = config or portal.config

        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.secret_key = SECRET_KEY

        # Initialize SocketIO for real-time features
        if self.config.enable_websockets:
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        else:
            self.socketio = None

        self.logger = logging.getLogger(f"{__name__}.FlaskPortalApp")
        register_routes(self.app, self.portal)
        self.logger.info("Flask portal app initialized")

    def _setup_socketio_events(self):
        """Setup SocketIO event handlers"""
        if not self.socketio:
            return

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection"""
            connection_id = request.sid
            self.portal.add_connection(connection_id)
            self.logger.info(f"Client connected: {connection_id}")
            emit("connected", {"status": "connected", "connection_id": connection_id})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection"""
            connection_id = request.sid
            self.portal.remove_connection(connection_id)
            self.logger.info(f"Client disconnected: {connection_id}")

        @self.socketio.on("join_room")
        def handle_join_room(data):
            """Handle room joining"""
            room = data.get("room")
            if room:
                join_room(room)
                emit("room_joined", {"room": room}, room=room)

        @self.socketio.on("leave_room")
        def handle_leave_room(data):
            """Handle room leaving"""
            room = data.get("room")
            if room:
                leave_room(room)
                emit("room_left", {"room": room}, room=room)

        @self.socketio.on("portal_update")
        def handle_portal_update(data):
            """Handle portal update requests"""
            update_type = data.get("type")
            if update_type == "status":
                emit("portal_status", self.portal.get_portal_status())
            elif update_type == "agents":
                agents = [agent.to_dict() for agent in self.portal.agents.values()]
                emit("agents_update", {"agents": agents})

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = None):
        """Run the Flask portal app"""
        debug_mode = debug if debug is not None else self.config.debug_mode

        if self.config.enable_websockets:
            self._setup_socketio_events()
            self.socketio.run(self.app, host=host, port=port, debug=debug_mode)
        else:
            self.app.run(host=host, port=port, debug=debug_mode)

    def get_app(self) -> Flask:
        """Get the Flask app instance"""
        return self.app

    def get_socketio(self) -> Optional[SocketIO]:
        """Get the SocketIO instance if available"""
        return self.socketio
