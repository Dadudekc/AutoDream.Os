#!/usr/bin/env python3
"""
Integrated Discord Bot Service - Fixed for 5-Agent Mode

This service provides a Discord bot integrated with the consolidated messaging service.
Fixed to work properly with 5-agent testing mode without architecture dependencies.

Author: Agent-2 (Discord System Migration - Fixed)
Date: 2025-01-19
Version: 3.0.0 (Fixed)
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import messaging service for integration
try:
    from .consolidated_messaging_service import ConsolidatedMessagingService
except ImportError:
    # Fallback for direct execution
    pass

# Import integrated components - discord_commands was removed during consolidation
# These components are now integrated into the main Discord bot service
# from .discord_commands import DiscordCommandRegistry, command_registry  # Removed
# from .discord_config import DiscordBotConfig, discord_config  # Removed
# from .discord_ui import DiscordUIComponents, ui_components  # Removed

# Import the separate Discord devlog service for devlog functionality

logger = logging.getLogger(__name__)


class IntegratedDiscordBotService:
    """Integrated Discord bot service with consolidated messaging."""

    def __init__(self):
        """Initialize Discord bot service with integrated components."""
        self.bot = None
        self.messaging_service = None
        self.is_initialized = False
        self.logger = logging.getLogger(f"{__name__}.IntegratedDiscordBotService")

        # Integrated components
        # Note: discord_config, command_registry, and ui_components were consolidated
        # into the main Discord bot service for better architecture

        # Bot configuration
        self.token = None
        self.channel_id = None
        self.guild_id = None

    async def initialize(self) -> bool:
        """Initialize the Discord bot service with integrated components."""
        try:
            self.logger.info("🚀 Initializing Integrated Discord Bot Service...")

            # Load configuration
            self._load_configuration()

            # Check if properly configured
            if not self.token or not self.channel_id:
                self.logger.error("❌ Discord bot configuration incomplete")
                self.logger.error(f"   Token configured: {bool(self.token)}")
                self.logger.error(f"   Channel ID configured: {bool(self.channel_id)}")
                return False

            # Initialize messaging service
            await self._initialize_messaging_service()

            # Initialize Discord bot with configuration
            await self._initialize_discord_bot()

            # Setup basic commands
            await self._setup_commands()

            self.is_initialized = True
            self.logger.info("✅ Integrated Discord Bot Service initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Integrated Discord Bot Service: {e}")
            return False

    def _load_configuration(self) -> None:
        """Load Discord bot configuration."""
        self.token = self.config.get_bot_token()
        self.channel_id = self.config.get_channel_id()
        self.guild_id = self.config.get_guild_id()

        if self.token:
            self.logger.info("✅ Bot token configured")
        if self.channel_id:
            self.logger.info("✅ Channel ID configured")
        if self.guild_id:
            self.logger.info("✅ Guild ID configured")

    async def _initialize_messaging_service(self):
        """Initialize messaging service integration."""
        try:
            self.logger.info("🔗 Initializing messaging service integration...")
            self.messaging_service = MessagingService("config/coordinates.json")
            self.logger.info("✅ Messaging service integration complete")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize messaging service: {e}")
            raise

    async def _initialize_discord_bot(self):
        """Initialize the Discord bot with configuration."""
        try:
            self.logger.info("🤖 Initializing Discord bot...")

            # Create bot instance with proper intents
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            # Use default command prefix
            command_prefix = os.getenv("DISCORD_COMMAND_PREFIX", "!")

            self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)

            # Setup event handlers
            await self._setup_event_handlers()

            # Setup messaging integration
            self.bot.messaging_service = self.messaging_service

            # Setup bot settings
            bot_name = os.getenv("DISCORD_BOT_NAME", "UnifiedDiscordBot")
            bot_status = os.getenv(
                "DISCORD_BOT_STATUS", "🐝 WE ARE SWARM - Agent Coordination Active"
            )
            activity_type = os.getenv("DISCORD_BOT_ACTIVITY_TYPE", "watching")

            self.bot.bot_name = bot_name
            self.bot.bot_status = bot_status
            self.bot.activity_type = activity_type

            # Setup basic commands
            from discord_bot.commands.basic_commands import setup_basic_commands

            setup_basic_commands(self.bot)

            self.logger.info("✅ Discord bot initialized with configuration and commands")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            raise

    async def _setup_event_handlers(self):
        """Setup Discord bot event handlers."""

        @self.bot.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.logger.info(f"🤖 Discord Commander is online as {self.bot.user}")

            # Update presence for 5-agent mode
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name="🐝 5-Agent Mode - WE ARE SWARM"
                )
            )

        @self.bot.event
        async def on_message(message):
            """Handle incoming messages."""
            if message.author == self.bot.user:
                return

            # Process commands
            await self.bot.process_commands(message)

    async def _setup_commands(self):
        """Setup basic Discord commands."""
        self.logger.info("🔧 Setting up basic Discord commands...")

        # Basic commands are already set up in _initialize_discord_bot
        # No additional setup needed - commands are loaded via setup_basic_commands()

        self.logger.info("✅ Basic commands setup complete")

    # System integration is handled through messaging service
    # No additional integration needed for basic functionality

    async def start(self) -> None:
        """Start the Discord bot service."""
        try:
            if not self.bot:
                raise RuntimeError("Discord bot not initialized")

            self.logger.info("🚀 Starting Discord Commander...")

            # Get bot token
            token = os.getenv("DISCORD_BOT_TOKEN")
            if not token:
                raise RuntimeError("DISCORD_BOT_TOKEN environment variable not set")

            # Sync slash commands
            try:
                synced = await self.bot.tree.sync()
                self.logger.info(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                self.logger.error(f"❌ Failed to sync slash commands: {e}")

            # Start the bot
            await self.bot.start(token)

        except discord.LoginFailure:
            self.logger.error("❌ Invalid Discord bot token!")
            raise
        except Exception as e:
            self.logger.error(f"❌ Failed to start Discord Commander: {e}")
            raise

    async def stop(self) -> None:
        """Stop the Discord bot service."""
        try:
            if self.bot:
                self.logger.info("🛑 Stopping Discord Commander...")
                await self.bot.close()

            self.logger.info("✅ Discord Commander stopped")

        except Exception as e:
            self.logger.error(f"❌ Failed to stop Discord Commander: {e}")

    def get_status(self) -> dict:
        """Get the status of the Discord bot service."""
        return {
            "service_initialized": self.is_initialized,
            "bot_ready": self.bot.user is not None if self.bot else False,
            "guild_count": len(self.bot.guilds) if self.bot and self.bot.guilds else 0,
            "messaging_service_connected": self.messaging_service is not None,
        }


async def main():
    """Main function to run the integrated Discord bot service."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create and initialize service
    service = IntegratedDiscordBotService()

    try:
        # Initialize service
        success = await service.initialize()
        if not success:
            logger.error("❌ Failed to initialize service")
            return

        # Start service
        await service.start()

    # Start the bot with proper token handling
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
    finally:
        # Stop service
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
