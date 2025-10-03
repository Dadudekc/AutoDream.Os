"""
Discord Commander Bot Models
============================

Core data models and classes for Discord Commander.
Created to resolve circular import issues and missing classes.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class BotConfiguration:
    """Bot configuration data"""

    token: str | None = None
    guild_id: int | None = None
    command_prefix: str = "!"
    status_message: str = "Ready"
    max_retries: int = 3
    timeout_seconds: int = 30
    log_level: str = "INFO"
    enable_commands: bool = True
    enable_events: bool = True


@dataclass
class CommandContext:
    """Command execution context"""

    command_name: str
    user_id: str
    channel_id: str
    guild_id: str
    args: list[str] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class BotCore:
    """Bot core functionality"""

    def __init__(self, config: BotConfiguration | None = None):
        """Initialize bot core"""
        self.config = config or BotConfiguration()
        self.is_ready = False
        self.error_count = 0
        self.logger = logger
        logger.info("BotCore initialized")

    def start_bot(self) -> bool:
        """Start bot"""
        try:
            self.is_ready = True
            logger.info("Bot core started")
            return True
        except Exception as e:
            logger.error(f"Error starting bot core: {e}")
            return False

    def stop_bot(self) -> bool:
        """Stop bot"""
        try:
            self.is_ready = False
            logger.info("Bot core stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping bot core: {e}")
            return False

    def record_error(self) -> None:
        """Record error"""
        self.error_count += 1
        logger.warning(f"Error recorded. Total errors: {self.error_count}")

    def create_bot(self):
        """Create Discord bot instance"""
        try:
            import discord
            from discord.ext import commands

            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            bot = commands.Bot(
                command_prefix=self.config.command_prefix, intents=intents, help_command=None
            )

            self.logger.info("Discord bot created successfully")
            return bot

        except ImportError:
            self.logger.error("Discord.py not available")
            return None
        except Exception as e:
            self.logger.error(f"Error creating bot: {e}")
            return None

    def get_status(self) -> dict[str, Any]:
        """Get bot status"""
        return {
            "is_ready": self.is_ready,
            "error_count": self.error_count,
            "config": self.config.__dict__ if self.config else {},
        }


class EmbedBuilder:
    """Discord embed builder utility"""

    def __init__(self):
        """Initialize embed builder"""
        self.embeds = []

    def create_embed(self, title: str, description: str, color: int = 0x00FF00) -> dict[str, Any]:
        """Create Discord embed"""
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.now().isoformat(),
            "fields": [],
        }
        return embed

    def add_field(self, embed: dict, name: str, value: str, inline: bool = False) -> dict:
        """Add field to embed"""
        embed["fields"].append({"name": name, "value": value, "inline": inline})
        return embed

    def build(self, embed: dict) -> dict:
        """Build final embed"""
        return embed
