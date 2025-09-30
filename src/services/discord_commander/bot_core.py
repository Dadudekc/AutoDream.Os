#!/usr/bin/env python3
"""
Discord Commander Bot Core - Core bot functionality
=================================================

Core bot functionality extracted from bot.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class DiscordCommanderBotCore:
    """Core Discord Commander bot functionality."""

    def __init__(self, token: str = None, guild_id: int = None):
        """Initialize Discord Commander bot core."""
        self.token = token
        self.guild_id = guild_id
        self.start_time = datetime.now()
        self.is_running = False
        self.is_healthy = True

        # Bot state
        self.command_prefix = "!"
        self.status_message = "Discord Commander Active"
        self.last_activity = datetime.now()

        # Performance tracking
        self.commands_executed = 0
        self.messages_processed = 0
        self.errors_count = 0

        logger.info("Discord Commander Bot Core initialized")

    def get_bot_info(self) -> dict[str, Any]:
        """Get bot information."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "bot_name": "Discord Commander",
            "version": "2.0",
            "uptime_seconds": uptime,
            "uptime_hours": uptime / 3600,
            "is_running": self.is_running,
            "is_healthy": self.is_healthy,
            "command_prefix": self.command_prefix,
            "status_message": self.status_message,
            "last_activity": self.last_activity.isoformat(),
            "start_time": self.start_time.isoformat(),
        }

    def get_performance_stats(self) -> dict[str, Any]:
        """Get bot performance statistics."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "commands_executed": self.commands_executed,
            "messages_processed": self.messages_processed,
            "errors_count": self.errors_count,
            "uptime_seconds": uptime,
            "commands_per_hour": (self.commands_executed / (uptime / 3600)) if uptime > 0 else 0,
            "messages_per_hour": (self.messages_processed / (uptime / 3600)) if uptime > 0 else 0,
            "error_rate": (self.errors_count / max(self.messages_processed, 1)) * 100,
        }

    def record_command_execution(self):
        """Record a command execution."""
        self.commands_executed += 1
        self.last_activity = datetime.now()

    def record_message_processed(self):
        """Record a message processed."""
        self.messages_processed += 1
        self.last_activity = datetime.now()

    def record_error(self):
        """Record an error."""
        self.errors_count += 1
        self.is_healthy = False

    def set_healthy(self, healthy: bool = True):
        """Set bot health status."""
        self.is_healthy = healthy

    def set_status_message(self, message: str):
        """Set bot status message."""
        self.status_message = message
        self.last_activity = datetime.now()

    def get_health_status(self) -> dict[str, Any]:
        """Get bot health status."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        error_rate = (self.errors_count / max(self.messages_processed, 1)) * 100

        health_score = 100
        if error_rate > 5:
            health_score -= 20
        if not self.is_running:
            health_score -= 30
        if uptime < 60:  # Less than 1 minute uptime
            health_score -= 10

        return {
            "is_healthy": self.is_healthy,
            "is_running": self.is_running,
            "health_score": max(health_score, 0),
            "error_rate": error_rate,
            "uptime_seconds": uptime,
            "last_activity": self.last_activity.isoformat(),
            "status_message": self.status_message,
        }

    def start_bot(self):
        """Start the bot."""
        self.is_running = True
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        logger.info("Discord Commander Bot started")

    def stop_bot(self):
        """Stop the bot."""
        self.is_running = False
        logger.info("Discord Commander Bot stopped")

    def restart_bot(self):
        """Restart the bot."""
        self.stop_bot()
        asyncio.sleep(1)  # Brief pause
        self.start_bot()
        logger.info("Discord Commander Bot restarted")

    def get_system_info(self) -> dict[str, Any]:
        """Get system information."""
        return {
            "python_version": "3.9+",
            "platform": "Windows/Linux/Mac",
            "bot_version": "2.0",
            "core_version": "1.0",
            "features": [
                "Agent Coordination",
                "Quality Monitoring",
                "Performance Tracking",
                "Web Dashboard",
                "Social Media Integration",
            ],
        }

    def validate_configuration(self) -> dict[str, Any]:
        """Validate bot configuration."""
        validation_result = {"valid": True, "errors": [], "warnings": []}

        if not self.token:
            validation_result["valid"] = False
            validation_result["errors"].append("Bot token not configured")

        if not self.guild_id:
            validation_result["warnings"].append("Guild ID not configured")

        if not self.command_prefix:
            validation_result["warnings"].append("Command prefix not set")

        return validation_result

    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()

    def get_uptime_string(self) -> str:
        """Get formatted uptime string."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def is_bot_ready(self) -> bool:
        """Check if bot is ready for operations."""
        return self.is_running and self.is_healthy and self.token is not None
