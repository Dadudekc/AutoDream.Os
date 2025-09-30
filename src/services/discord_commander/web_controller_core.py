"""
Web Controller Core - V2 Compliant
==================================

Core web controller functionality separated for V2 compliance.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import logging

logger = logging.getLogger(__name__)


class WebControllerCore:
    """Core web controller functionality."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the web controller core."""
        self.host = host
        self.port = port
        self.bot = None
        self.app = None
        self.socketio = None
        self.is_running = False

    def set_bot(self, bot) -> None:
        """Set the Discord bot instance."""
        self.bot = bot
        logger.info("Discord bot instance set")

    def get_status(self) -> dict:
        """Get controller status."""
        return {
            "host": self.host,
            "port": self.port,
            "is_running": self.is_running,
            "bot_connected": self.bot is not None,
        }

    def start(self) -> None:
        """Start the web controller."""
        if not self.is_running:
            self.is_running = True
            logger.info(f"Web controller started on {self.host}:{self.port}")

    def stop(self) -> None:
        """Stop the web controller."""
        if self.is_running:
            self.is_running = False
            logger.info("Web controller stopped")

    def get_agent_status(self) -> dict:
        """Get agent status information."""
        if self.bot:
            return self.bot.get_agent_status()
        return {"error": "Bot not connected"}

    def send_message(self, agent_id: str, message: str) -> dict:
        """Send message to agent."""
        if self.bot:
            return self.bot.send_message_to_agent(agent_id, message)
        return {"error": "Bot not connected"}

    def get_system_health(self) -> dict:
        """Get system health information."""
        return {
            "controller_status": "healthy" if self.is_running else "stopped",
            "bot_status": "connected" if self.bot else "disconnected",
            "timestamp": self._get_timestamp(),
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()
