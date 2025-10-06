#!/usr/bin/env python3
"""
Discord Commander Bot - Bot Manager
===================================

Bot management and initialization for Discord Commander Bot.
V2 Compliant: ≤400 lines, focused bot management.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import asyncio
import logging
import sys
from pathlib import Path

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

from src.services.discord_commander.command_definitions import create_command_definitions
from src.services.discord_commander.core import DiscordConfig, DiscordConnectionManager

logger = logging.getLogger(__name__)


class DiscordCommanderBot:
    """Main Discord Commander Bot class."""

    def __init__(self):
        """Initialize Discord Commander Bot."""
        self.bot: commands.Bot | None = None
        self.config: DiscordConfig | None = None
        self.connection_manager: DiscordConnectionManager | None = None
        self.command_definitions: object | None = None

    async def initialize(self) -> bool:
        """Initialize the bot."""
        try:
            if not DISCORD_AVAILABLE:
                logger.error("Discord.py not available")
                return False

            # Load configuration
            self.config = DiscordConfig()
            if not self.config.is_configured():
                logger.error("Discord configuration not found")
                return False

            # Create connection manager
            self.connection_manager = DiscordConnectionManager(self.config)

            # Create bot instance
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

            # Register commands
            self.command_definitions = create_command_definitions(self.bot)

            # Set up event handlers
            self._setup_event_handlers()

            logger.info("Discord Commander Bot initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Discord Commander Bot: {e}")
            return False

    def _setup_event_handlers(self) -> None:
        """Set up bot event handlers."""
        if not self.bot:
            return

        @self.bot.event
        async def on_ready():
            """Bot ready event."""
            logger.info(f"Discord Commander Bot logged in as {self.bot.user}")
            logger.info(f"Bot is in {len(self.bot.guilds)} guilds")

        @self.bot.event
        async def on_command_error(ctx, error):
            """Command error handler."""
            if isinstance(error, commands.CommandNotFound):
                await ctx.send("❌ Command not found. Use `!help` for available commands.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"❌ Missing required argument: {error.param}")
            elif isinstance(error, commands.BadArgument):
                await ctx.send(f"❌ Invalid argument: {error}")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send(f"❌ An error occurred: {error}")

        @self.bot.event
        async def on_message(message):
            """Message event handler."""
            if message.author == self.bot.user:
                return

            # Process commands
            await self.bot.process_commands(message)

    async def start(self) -> None:
        """Start the bot."""
        try:
            if not self.bot or not self.config:
                logger.error("Bot not initialized")
                return

            # Connect to Discord
            await self.bot.start(self.config.bot_token)

        except Exception as e:
            logger.error(f"Failed to start bot: {e}")

    async def stop(self) -> None:
        """Stop the bot."""
        try:
            if self.bot and not self.bot.is_closed():
                await self.bot.close()
                logger.info("Discord Commander Bot stopped")

        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

    def get_status(self) -> dict:
        """Get bot status."""
        return {
            "discord_available": DISCORD_AVAILABLE,
            "bot_initialized": self.bot is not None,
            "config_loaded": self.config is not None,
            "connection_manager_ready": self.connection_manager is not None,
            "commands_registered": self.command_definitions is not None,
            "is_running": self.bot is not None and not self.bot.is_closed() if self.bot else False,
        }

    def get_config_summary(self) -> dict:
        """Get configuration summary."""
        if self.config:
            return self.config.get_summary()
        return {"error": "Configuration not loaded"}


async def main():
    """Main function to run the Discord Commander Bot."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not installed! Please install: pip install discord.py")
        return

    # Create and start bot
    bot = DiscordCommanderBot()

    try:
        if await bot.initialize():
            await bot.start()
        else:
            print("❌ Failed to initialize Discord Commander Bot")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Discord Commander Bot...")
    except Exception as e:
        print(f"❌ Error running Discord Commander Bot: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
