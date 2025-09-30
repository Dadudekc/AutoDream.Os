"""
Discord Bot Core Engine
V2 Compliant Discord bot core functionality
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import discord
from discord.ext import commands

from .discord_bot_models import BotConfiguration, BotMetrics, BotStatus, CommandContext


class DiscordBotCore:
    """Discord bot core engine - V2 Compliant"""
    
    def __init__(self, config: BotConfiguration):
        """Initialize Discord bot core"""
        self.config = config
        self.bot: Optional[commands.Bot] = None
        self.metrics = BotMetrics(
            uptime=0.0,
            commands_executed=0,
            messages_sent=0,
            errors_count=0,
            guilds_count=0,
            users_count=0
        )
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self):
        """Initialize the bot"""
        intents = discord.Intents.default()
        intents.message_content = self.config.intents.get("message_content", True)
        intents.members = self.config.intents.get("members", True)
        intents.guilds = self.config.intents.get("guilds", True)
        
        self.bot = commands.Bot(
            command_prefix=self.config.command_prefix,
            intents=intents,
            help_command=None
        )
        
        # Setup event handlers
        self._setup_event_handlers()
        
    def _setup_event_handlers(self):
        """Setup Discord event handlers"""
        if not self.bot:
            return
            
        @self.bot.event
        async def on_ready():
            """Bot ready event"""
            self.logger.info(f"Bot logged in as {self.bot.user}")
            self.metrics.guilds_count = len(self.bot.guilds)
            self.metrics.users_count = len(self.bot.users)
            
        @self.bot.event
        async def on_command_error(ctx, error):
            """Command error handler"""
            self.metrics.errors_count += 1
            self.logger.error(f"Command error: {error}")
            
        @self.bot.event
        async def on_message(message):
            """Message event handler"""
            if message.author == self.bot.user:
                self.metrics.messages_sent += 1
            await self.bot.process_commands(message)
            
    async def start_bot(self, token: str):
        """Start the bot"""
        if not self.bot:
            await self.initialize()
            
        try:
            await self.bot.start(token)
        except Exception as e:
            self.logger.error(f"Bot start error: {e}")
            raise
            
    async def stop_bot(self):
        """Stop the bot"""
        if self.bot:
            await self.bot.close()
            
    def get_status(self) -> BotStatus:
        """Get bot status"""
        if not self.bot:
            return BotStatus.OFFLINE
            
        if self.bot.is_ready():
            return BotStatus.ONLINE
        else:
            return BotStatus.OFFLINE
            
    def get_metrics(self) -> BotMetrics:
        """Get bot metrics"""
        return self.metrics
        
    def increment_command_count(self):
        """Increment command execution count"""
        self.metrics.commands_executed += 1
        
    def create_command_context(self, ctx: commands.Context) -> CommandContext:
        """Create command context"""
        return CommandContext(
            command_name=ctx.command.name if ctx.command else "unknown",
            user_id=ctx.author.id,
            guild_id=ctx.guild.id if ctx.guild else None,
            channel_id=ctx.channel.id,
            timestamp=datetime.now(),
            parameters={}
        )
