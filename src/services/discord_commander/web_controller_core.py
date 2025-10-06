#!/usr/bin/env python3
"""
Discord Commander Web Controller - Core Logic
=============================================

Core web controller logic for Discord Commander system.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- Web controller initialization
- Bot integration
- Flask app management
- SocketIO event handling

Extracted from main web controller module for V2 compliance.
"""

import logging
import threading
from pathlib import Path

try:
    from flask import Flask, jsonify, render_template, request
    from flask_socketio import SocketIO, emit

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from .bot import DiscordCommanderBot

logger = logging.getLogger(__name__)


class DiscordCommanderController:
    """Web controller for Discord Commander system."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the web controller."""
        self.host = host
        self.port = port
        self.bot = None
        self.app = None
        self.socketio = None

        if not FLASK_AVAILABLE:
            logger.error(
                "Flask and Flask-SocketIO not available. Install: pip install flask flask-socketio"
            )
            return

        self._setup_flask_app()

    def _setup_flask_app(self):
        """Set up the Flask application."""
        self.app = Flask(
            __name__,
            template_folder=Path(__file__).parent / "templates",
            static_folder=Path(__file__).parent / "static",
        )
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        # Register routes
        self._register_routes()

        # Register socket events
        self._register_socket_events()

    def _register_routes(self):
        """Register Flask routes."""
        # Import routes from modular file
        from .web_controller_routes import register_routes

        register_routes(self.app, self.bot)

    def _register_socket_events(self):
        """Register SocketIO events."""
        # Import socket events from modular file
        from .web_controller_routes import register_socket_events

        register_socket_events(self.socketio, self.bot)

    def set_bot(self, bot: DiscordCommanderBot):
        """Set the Discord bot instance."""
        self.bot = bot

    def run(self):
        """Run the web controller."""
        if not FLASK_AVAILABLE:
            logger.error("Cannot run web controller: Flask not available")
            return

        if not self.app or not self.socketio:
            logger.error("Flask app not initialized")
            return

        logger.info(f"Starting Discord Commander Web Controller on {self.host}:{self.port}")
        logger.info("Open http://localhost:8080 in your browser to access the controller")

        # Start Flask app in a separate thread
        def run_app():
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False)

        thread = threading.Thread(target=run_app, daemon=True)
        thread.start()

    def stop(self):
        """Stop the web controller."""
        logger.info("Stopping Discord Commander Web Controller")
        if self.socketio:
            self.socketio.stop()
