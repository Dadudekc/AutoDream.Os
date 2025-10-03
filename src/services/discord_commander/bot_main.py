"""
Discord Commander Bot Main
Main bot system with comprehensive Discord functionality
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

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

from .bot_models import BotConfiguration, BotCore


# Utility functions for Discord bot creation and management
def create_bot_configuration(token: str = None, guild_id: int = None) -> BotConfiguration:
    """Create bot configuration."""
    return BotConfiguration(token=token, guild_id=guild_id)


def create_discord_bot(config: BotConfiguration = None) -> "DiscordCommanderBot":
    """Create Discord bot instance."""
    return DiscordCommanderBot(config)


async def run_bot(bot: "DiscordCommanderBot") -> None:
    """Run the Discord bot."""
    await bot.start()


class BotManager:
    """Bot management utility."""

    def __init__(self):
        self.bots = {}

    def create_bot(self, name: str, config: BotConfiguration) -> "DiscordCommanderBot":
        """Create a named bot instance."""
        bot = DiscordCommanderBot(config)
        self.bots[name] = bot
        return bot

    async def start_bot(self, name: str) -> None:
        """Start a named bot."""
        if name in self.bots:
            await self.bots[name].start()


class DiscordCommanderBot:
    """Main Discord Commander Bot class"""

    def __init__(self, config: BotConfiguration | None = None):
        self.config = config or BotConfiguration()
        self.bot_core = BotCore(self.config)
        self.command_manager = None  # Will be initialized after bot is created
        self.bot: commands.Bot | None = None
        self.logger = self.bot_core.logger

    async def initialize(self) -> None:
        """Initialize the bot"""
        if not DISCORD_AVAILABLE:
            self.logger.error("Discord.py is not available. Please install it.")
            return

        self.bot = self.bot_core.create_bot()
        if not self.bot:
            self.logger.error("Failed to create Discord bot")
            return

        # Initialize command manager with bot_core
        from .commands import CommandManager

        self.command_manager = CommandManager(self.bot, None)
        self.command_manager.register_commands(self.bot.tree)
        self.command_manager.register_regular_commands(self.bot)

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
            type=discord.ActivityType.watching, name="WE ARE SWARM - Agent Coordination"
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

        from .bot_models import EmbedBuilder

        embed = EmbedBuilder.create_error_embed("Command Error", f"An error occurred: {str(error)}")

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
            await self.bot.start(self.config.token)
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            raise

    async def stop(self) -> None:
        """Stop the bot"""
        if self.bot:
            await self.bot.close()
        self.logger.info("Bot stopped")

    def get_bot_info(self) -> dict[str, Any]:
        """Get bot information"""
        return {
            "name": self.bot.user.name if self.bot and self.bot.user else "Unknown",
            "id": self.bot.user.id if self.bot and self.bot.user else None,
            "guilds": len(self.bot.guilds) if self.bot else 0,
            "users": len(self.bot.users) if self.bot else 0,
            "status": self.bot_core.get_status_info(),
            "commands": self.command_manager.get_command_stats(),
        }

    # Uptime and online status accessed via bot_core directly


# Original BotManager class removed - using simplified version above


# Utility functions moved to separate module to maintain V2 compliance
