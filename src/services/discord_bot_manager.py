#!/usr/bin/env python3
"""
Discord Devlog Service - Bot Connection Manager
===============================================

Manages Discord bot connections and channel access.
V2 Compliant: ≤400 lines, focused bot connection management.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import asyncio
import logging
from typing import Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from .discord_devlog_config import DiscordDevlogConfig

logger = logging.getLogger(__name__)


class DiscordBotManager:
    """Manages Discord bot connections and operations."""

    def __init__(self, config: DiscordDevlogConfig):
        """Initialize Discord bot manager."""
        self.config = config
        self.bot: Optional[commands.Bot] = None
        self.is_connected = False

    async def connect(self) -> bool:
        """Connect to Discord bot."""
        if not DISCORD_AVAILABLE:
            logger.error("Discord.py not available")
            return False

        if not self.config.bot_token:
            logger.error("No Discord bot token configured")
            return False

        try:
            # Create bot instance
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix='!', intents=intents)

            # Connect to Discord
            await self.bot.start(self.config.bot_token)
            self.is_connected = True
            logger.info("Discord bot connected successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect Discord bot: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect Discord bot."""
        try:
            if self.bot and self.is_connected:
                await self.bot.close()
                self.is_connected = False
                logger.info("Discord bot disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting Discord bot: {e}")

    async def get_channel(self, agent_id: Optional[str] = None):
        """Get Discord channel for posting."""
        try:
            if not self.bot or not self.is_connected:
                return None

            # Determine target channel ID
            target_channel_id = None
            if agent_id and agent_id in self.config.agent_channels:
                target_channel_id = self.config.agent_channels[agent_id]
                logger.info(f"Using agent-specific channel: {agent_id} -> {target_channel_id}")
            elif self.config.channel_id:
                target_channel_id = self.config.channel_id
                logger.info(f"Using default channel: {target_channel_id}")
            else:
                logger.warning("No Discord channel ID configured")
                return None

            channel = self.bot.get_channel(target_channel_id)
            if not channel:
                logger.error(f"Discord channel {target_channel_id} not found")
                return None

            return channel

        except Exception as e:
            logger.error(f"Failed to get Discord channel: {e}")
            return None

    async def test_connection(self) -> dict:
        """Test Discord bot connection."""
        try:
            result = {
                "bot_token_configured": bool(self.config.bot_token),
                "channel_id_configured": bool(self.config.channel_id),
                "guild_id_configured": bool(self.config.guild_id),
                "bot_connected": False,
                "channel_accessible": False,
                "error": None,
            }

            if not self.config.bot_token:
                result["error"] = "No Discord bot token configured"
                return result

            if not self.config.channel_id:
                result["error"] = "No Discord channel ID configured"
                return result

            # Test bot connection
            if await self.connect():
                result["bot_connected"] = True

                # Test channel access
                channel = await self.get_channel()
                if channel:
                    result["channel_accessible"] = True
                else:
                    result["error"] = "Channel not accessible"
            else:
                result["error"] = "Failed to connect Discord bot"

            return result

        except Exception as e:
            return {
                "bot_token_configured": bool(self.config.bot_token),
                "channel_id_configured": bool(self.config.channel_id),
                "guild_id_configured": bool(self.config.guild_id),
                "bot_connected": False,
                "channel_accessible": False,
                "error": str(e),
            }

    async def post_message(self, content: str, agent_id: Optional[str] = None) -> bool:
        """Post message to Discord channel."""
        try:
            if not self.bot or not self.is_connected:
                return False

            channel = await self.get_channel(agent_id)
            if not channel:
                return False

            await channel.send(content)
            logger.info(f"Message posted to Discord channel {channel.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to post message to Discord: {e}")
            return False

    def is_available(self) -> bool:
        """Check if bot is available."""
        return DISCORD_AVAILABLE and self.config.bot_token is not None

    def get_status(self) -> dict:
        """Get bot status."""
        return {
            "discord_available": DISCORD_AVAILABLE,
            "bot_token_configured": bool(self.config.bot_token),
            "is_connected": self.is_connected,
            "is_available": self.is_available()
        }


def create_discord_bot_manager(config: DiscordDevlogConfig) -> DiscordBotManager:
    """Create Discord bot manager."""
    return DiscordBotManager(config)

