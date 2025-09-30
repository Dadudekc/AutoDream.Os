#!/usr/bin/env python3
"""
Discord Commander Web Controller Core
=====================================

Core functionality for the Discord Commander web controller.
Handles basic initialization and Flask app setup.
"""

import logging
from pathlib import Path

try:
    from flask import Flask, jsonify, render_template, request
    from flask_socketio import SocketIO, emit

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from .bot import DiscordCommanderBot

logger = logging.getLogger(__name__)


class DiscordCommanderControllerCore:
    """Core web controller functionality."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the web controller core."""
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
        if not FLASK_AVAILABLE:
            return

        self.app = Flask(
            __name__,
            template_folder=str(Path(__file__).parent / "templates"),
            static_folder=str(Path(__file__).parent / "static"),
        )

        self.app.config["SECRET_KEY"] = "discord-commander-secret-key"

        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self._register_routes()

    def _register_routes(self):
        """Register Flask routes."""
        if not self.app:
            return

        @self.app.route("/")
        def index():
            """Main dashboard page."""
            return render_template("dashboard.html")

        @self.app.route("/api/status")
        def api_status():
            """API status endpoint."""
            return jsonify(
                {
                    "status": "active",
                    "bot_connected": self.bot is not None,
                    "agents": self._get_agent_status(),
                }
            )

        @self.app.route("/api/agents")
        def api_agents():
            """Get agent status."""
            return jsonify(self._get_agent_status())

        @self.app.route("/api/send-message", methods=["POST"])
        def api_send_message():
            """Send message to Discord."""
            try:
                data = request.get_json()
                message = data.get("message", "")
                channel = data.get("channel", "general")

                if not message:
                    return jsonify({"error": "Message is required"}), 400

                # This would be handled by the messaging service
                result = {"success": True, "message": "Message sent successfully"}
                return jsonify(result)

            except Exception as e:
                logger.error(f"Error sending message: {e}")
                return jsonify({"error": str(e)}), 500

    def _get_agent_status(self):
        """Get current agent status."""
        # This would integrate with the actual agent system
        return {
            "Agent-1": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
            "Agent-2": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
            "Agent-3": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
            "Agent-4": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
            "Agent-5": {"status": "active", "last_seen": "2025-09-20T19:11:00Z"},
        }

    def set_bot(self, bot: DiscordCommanderBot):
        """Set the Discord bot instance."""
        self.bot = bot

    def run(self):
        """Run the web controller."""
        if not self.app or not self.socketio:
            logger.error("Flask app not initialized")
            return

        logger.info(f"Starting Discord Commander Web Controller on {self.host}:{self.port}")
        self.socketio.run(self.app, host=self.host, port=self.port, debug=False)

    def stop(self):
        """Stop the web controller."""
        logger.info("Stopping Discord Commander Web Controller")
        # Add cleanup logic here if needed
