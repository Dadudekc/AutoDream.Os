#!/usr/bin/env python3
"""
Discord Commander Web Controller (Refactored)
=============================================

Refactored web controller using modular design.
V2 compliant with proper separation of concerns.
"""

import logging

from .bot import DiscordCommanderBot
from .social_media_poster import SocialMediaPoster
from .socket_events import SocketEventHandler
from .web_controller_core import DiscordCommanderControllerCore

logger = logging.getLogger(__name__)


class DiscordCommanderController:
    """Refactored web controller for Discord Commander system."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the refactored web controller."""
        self.host = host
        self.port = port

        # Initialize core components
        self.core = DiscordCommanderControllerCore(host, port)
        self.social_poster = SocialMediaPoster()
        self.socket_handler = None

        # Set up socket events if available
        if self.core.socketio:
            self.socket_handler = SocketEventHandler(self.core.socketio)
            self.socket_handler.register_events()

        # Set up additional routes
        self._register_additional_routes()

    def _register_additional_routes(self):
        """Register additional routes for social media posting."""
        if not self.core.app:
            return

        @self.core.app.route("/api/post-social", methods=["POST"])
        def api_post_social():
            """Post message to social media platforms."""
            try:
                data = self.core.app.request.get_json()
                platform = data.get("platform", "discord")
                message = data.get("message", "")

                if not message:
                    return self.core.app.jsonify({"error": "Message is required"}), 400

                # This would be handled asynchronously in a real implementation
                result = {"success": True, "message": f"Message posted to {platform}"}
                return self.core.app.jsonify(result)

            except Exception as e:
                logger.error(f"Error posting to social media: {e}")
                return self.core.app.jsonify({"error": str(e)}), 500

        @self.core.app.route("/api/platforms")
        def api_platforms():
            """Get supported social media platforms."""
            platforms = self.social_poster.get_supported_platforms()
            return self.core.app.jsonify({"platforms": platforms})

    def set_bot(self, bot: DiscordCommanderBot):
        """Set the Discord bot instance."""
        self.core.set_bot(bot)

    def run(self):
        """Run the web controller."""
        self.core.run()

    def stop(self):
        """Stop the web controller."""
        self.core.stop()

    def get_status(self) -> dict:
        """Get controller status."""
        return {
            "host": self.host,
            "port": self.port,
            "core_active": self.core.app is not None,
            "socketio_active": self.core.socketio is not None,
            "connected_clients": self.socket_handler.get_connection_count()
            if self.socket_handler
            else 0,
            "message_count": self.socket_handler.get_message_count() if self.socket_handler else 0,
            "supported_platforms": self.social_poster.get_supported_platforms(),
        }

    def broadcast_agent_update(self, agent_data: dict):
        """Broadcast agent status update."""
        if self.socket_handler:
            self.socket_handler.broadcast_agent_update(agent_data)

    def broadcast_system_message(self, message: str, level: str = "info"):
        """Broadcast system message."""
        if self.socket_handler:
            self.socket_handler.broadcast_system_message(message, level)
