"""
Discord Commander Bot Main
Main bot system with comprehensive Discord functionality
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv
    dotenv_path = Path(__file__).parent.parent.parent.parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
except ImportError:
    pass

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from .bot_core import BotConfiguration, BotCore
from .bot_commands import CommandManager


class DiscordCommanderBot:
    """Main Discord Commander Bot class"""
    
    def __init__(self, config: Optional[BotConfiguration] = None):
        self.config = config or BotConfiguration()
        self.bot_core = BotCore(self.config)
        self.command_manager = CommandManager(self.bot_core)
        self.bot: Optional[commands.Bot] = None
        self.logger = self.bot_core.logger
    
    async def initialize(self) -> None:
        """Initialize the bot"""
        if not DISCORD_AVAILABLE:
            self.logger.error("Discord.py is not available. Please install it.")
            return
        
        self.bot = self.bot_core.create_bot()
        self.command_manager.register_commands(self.bot)
        
        # Register event handlers
        self._register_event_handlers()
        
        self.logger.info("Discord Commander Bot initialized successfully")
    
    def _register_event_handlers(self) -> None:
        """Register Discord event handlers"""
        if not self.bot:
            return
        
        @self.bot.event
        async def on_ready():
            """Bot ready event handler"""
            await self._handle_ready()
        
        @self.bot.event
        async def on_command_error(ctx: commands.Context, error: Exception):
            """Command error event handler"""
            await self._handle_command_error(ctx, error)
        
        @self.bot.event
        async def on_message(message: discord.Message):
            """Message event handler"""
            await self._handle_message(message)
    
    async def _handle_ready(self) -> None:
        """Handle bot ready event"""
        self.bot_core.status.is_online = True
        self.bot_core.status.start_time = datetime.now()
        
        self.logger.info(f"Bot is online as {self.bot.user}")
        self.logger.info(f"Connected to {len(self.bot.guilds)} guilds")
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="WE ARE SWARM - Agent Coordination"
        )
        await self.bot.change_presence(activity=activity)
    
    async def _handle_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Handle command error event"""
        self.bot_core.status.errors_count += 1
        self.bot_core.status.last_error = str(error)
        
        self.logger.error(f"Command error in {ctx.command}: {error}")
        
        # Send error message to user
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
        embed = self.bot_core.command_manager.EmbedBuilder.create_error_embed(
            "Command Error",
            f"An error occurred: {str(error)}"
        )
        
        try:
            await ctx.send(embed=embed)
        except Exception as send_error:
            self.logger.error(f"Failed to send error message: {send_error}")
    
    async def _handle_message(self, message: discord.Message) -> None:
        """Handle message event"""
        # Process commands
        await self.bot.process_commands(message)
    
    async def start(self) -> None:
        """Start the bot"""
        if not self.bot:
            await self.initialize()
        
        if not self.bot:
            raise RuntimeError("Failed to initialize bot")
        
        try:
            await self.bot_core.start_bot()
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the bot"""
        await self.bot_core.stop_bot()
        self.logger.info("Bot stopped")
    
    def get_bot_info(self) -> Dict[str, Any]:
        """Get bot information"""
        return {
            "name": self.bot.user.name if self.bot and self.bot.user else "Unknown",
            "id": self.bot.user.id if self.bot and self.bot.user else None,
            "guilds": len(self.bot.guilds) if self.bot else 0,
            "users": len(self.bot.users) if self.bot else 0,
            "status": self.bot_core.get_status_info(),
            "commands": self.command_manager.get_command_stats()
        }
    
    def get_uptime(self) -> str:
        """Get bot uptime"""
        return self.bot_core.get_uptime()
    
    def is_online(self) -> bool:
        """Check if bot is online"""
        return self.bot_core.status.is_online


class BotManager:
    """Bot management system"""
    
    def __init__(self):
        self.bots: Dict[str, DiscordCommanderBot] = {}
        self.active_bot: Optional[str] = None
    
    def create_bot(self, bot_id: str, config: Optional[BotConfiguration] = None) -> DiscordCommanderBot:
        """Create a new bot instance"""
        bot = DiscordCommanderBot(config)
        self.bots[bot_id] = bot
        return bot
    
    def get_bot(self, bot_id: str) -> Optional[DiscordCommanderBot]:
        """Get bot by ID"""
        return self.bots.get(bot_id)
    
    def set_active_bot(self, bot_id: str) -> bool:
        """Set active bot"""
        if bot_id in self.bots:
            self.active_bot = bot_id
            return True
        return False
    
    def get_active_bot(self) -> Optional[DiscordCommanderBot]:
        """Get active bot"""
        if self.active_bot:
            return self.bots.get(self.active_bot)
        return None
    
    async def start_bot(self, bot_id: str) -> bool:
        """Start bot by ID"""
        bot = self.get_bot(bot_id)
        if bot:
            try:
                await bot.start()
                return True
            except Exception as e:
                logging.error(f"Failed to start bot {bot_id}: {e}")
                return False
        return False
    
    async def stop_bot(self, bot_id: str) -> bool:
        """Stop bot by ID"""
        bot = self.get_bot(bot_id)
        if bot:
            try:
                await bot.stop()
                return True
            except Exception as e:
                logging.error(f"Failed to stop bot {bot_id}: {e}")
                return False
        return False
    
    def list_bots(self) -> List[str]:
        """List all bot IDs"""
        return list(self.bots.keys())


def create_discord_bot(config: Optional[BotConfiguration] = None) -> DiscordCommanderBot:
    """Create a Discord bot instance"""
    return DiscordCommanderBot(config)


def create_bot_configuration(
    token: str,
    prefix: str = "!",
    description: str = "Discord Commander Bot",
    debug_mode: bool = False
) -> BotConfiguration:
    """Create bot configuration"""
    config = BotConfiguration()
    config.token = token
    config.prefix = prefix
    config.description = description
    config.debug_mode = debug_mode
    config.log_level = "DEBUG" if debug_mode else "INFO"
    return config


async def run_bot(token: str, prefix: str = "!") -> None:
    """Run Discord bot with given token"""
    config = create_bot_configuration(token, prefix)
    bot = create_discord_bot(config)
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        await bot.stop()
    except Exception as e:
        logging.error(f"Bot error: {e}")
        await bot.stop()
        raise
