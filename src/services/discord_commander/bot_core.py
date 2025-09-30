"""
Discord Commander Bot Core
V2 Compliant main bot class
"""

import asyncio
import logging
from typing import Any

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from .bot_config import BotConfig
from .bot_events import BotEvents
from .bot_commands import BotCommands


class DiscordCommanderBot:
    """Main Discord Commander Bot - V2 Compliant"""
    
    def __init__(self):
        """Initialize bot"""
        self.config = BotConfig()
        self.events = BotEvents()
        self.commands = BotCommands()
        self.bot = None
        
    async def initialize(self):
        """Initialize bot components"""
        if not DISCORD_AVAILABLE:
            raise RuntimeError("Discord.py not available")
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        self.bot = commands.Bot(
            command_prefix=self.config.get_prefix(),
            intents=intents,
            help_command=None
        )
        
        # Setup events and commands
        await self.events.setup(self.bot)
        await self.commands.setup(self.bot)
        
    async def start_bot(self):
        """Start the bot"""
        if not self.bot:
            await self.initialize()
        
        token = self.config.get_token()
        if not token:
            raise ValueError("Discord token not found")
        
        await self.bot.start(token)
    
    async def close(self):
        """Close bot connections"""
        if self.bot:
            await self.bot.close()
    
    def get_status(self) -> dict[str, Any]:
        """Get bot status"""
        return {
            "status": "running" if self.bot else "stopped",
            "guilds": len(self.bot.guilds) if self.bot else 0,
            "users": len(self.bot.users) if self.bot else 0,
            "commands": len(self.bot.commands) if self.bot else 0
        }