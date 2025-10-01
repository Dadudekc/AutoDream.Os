"""
Discord Commander Bot Core - V2 Compliant
========================================

Core bot functionality for Discord Commander.
Manages bot instance, configuration, and agent integration.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import os

try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class DiscordCommanderBotCore:
    """Core Discord Commander bot functionality"""

    def __init__(self, token: str = None, guild_id: int = None):
        """Initialize Discord Commander bot core"""
        self.token = token or os.getenv("DISCORD_BOT_TOKEN")
        self.guild_id = guild_id or os.getenv("DISCORD_GUILD_ID")
        self.bot = None
        self.agent_interface = None
        self.swarm_coordinator = None

        if not DISCORD_AVAILABLE:
            logger.error("Discord.py not available")
            raise ImportError("Discord.py not installed")

        self._create_bot()

    def _create_bot(self):
        """Create Discord bot instance"""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Import and set up agent interface
        try:
            from src.services.discord_bot.core.discord_agent_interface import (
                DiscordAgentInterface,
                DiscordSwarmCoordinator,
            )

            self.agent_interface = DiscordAgentInterface(self.bot)
            self.swarm_coordinator = DiscordSwarmCoordinator(self.bot)
            logger.info("Agent interface and swarm coordinator initialized")
        except ImportError as e:
            logger.warning(f"Could not import agent interface: {e}")

    async def start(self):
        """Start the Discord bot"""
        if not self.token:
            raise ValueError("Discord bot token not configured")

        logger.info("Starting Discord Commander bot...")
        await self.bot.start(self.token)

    async def stop(self):
        """Stop the Discord bot"""
        if self.bot:
            await self.bot.close()
            logger.info("Discord Commander bot stopped")

    def get_bot(self):
        """Get the bot instance"""
        return self.bot

    def get_agent_interface(self):
        """Get the agent interface"""
        return self.agent_interface

    def get_swarm_coordinator(self):
        """Get the swarm coordinator"""
        return self.swarm_coordinator
