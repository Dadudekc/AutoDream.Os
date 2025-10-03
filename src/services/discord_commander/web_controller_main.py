"""
Discord Commander Web Controller Main
V2 Compliant main web controller
"""

import logging

from flask import Flask
from flask_socketio import SocketIO

from .web_controller_models import WebControllerConfig
from .web_routes import WebRoutes

logger = logging.getLogger(__name__)


class DiscordCommanderController:
    """Web controller for Discord Commander system"""

    def __init__(self, config: WebControllerConfig):
        """Initialize the web controller"""
        self.config = config
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.routes = WebRoutes(self.app)
        self._setup_app()

    def _setup_app(self):
        """Setup Flask application"""
        self.app.config["SECRET_KEY"] = "discord-commander-secret"
        self.app.config["DEBUG"] = self.config.debug_mode

        # Register socket events
        self._register_socket_events()

    def _register_socket_events(self):
        """Register socket events"""

        @self.socketio.on("connect")
        def handle_connect():
            logger.info("Client connected")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            logger.info("Client disconnected")

        @self.socketio.on("agent_status_request")
        def handle_agent_status_request():
            # Emit agent status updates
            self.socketio.emit(
                "agent_status_update",
                {
                    "agents": [
                        {"id": "Agent-1", "status": "active"},
                        {"id": "Agent-2", "status": "idle"},
                    ]
                },
            )

    def run(self):
        """Run the web controller"""
        try:
            logger.info(
                f"Starting Discord Commander Web Controller on {self.config.host}:{self.config.port}"
            )
            self.socketio.run(
                self.app, host=self.config.host, port=self.config.port, debug=self.config.debug_mode
            )
        except Exception as e:
            logger.error(f"Error running web controller: {e}")
            raise

    def get_app(self):
        """Get Flask app instance"""
        return self.app

    def get_socketio(self):
        """Get SocketIO instance"""
        return self.socketio

    def set_bot(self, bot):
        """Set the Discord bot instance"""
        self.bot = bot
        logger.info("Discord bot instance set in web controller")