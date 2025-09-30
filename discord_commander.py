#!/usr/bin/env python3
"""
Discord Commander - Main Entry Point
====================================

Main entry point for the Discord Commander bot system.
Handles initialization, configuration, and startup of the Discord bot.

🐝 WE ARE SWARM - Discord Commander Active!
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Discord imports for error handling
try:
    import discord
except ImportError:
    discord = None

# Load environment variables from .env or .env.template file
try:
    from dotenv import load_dotenv

    # Try to load from .env file first
    dotenv_path = Path(__file__).parent / ".env"
    template_path = Path(__file__).parent / ".env.template"

    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print("✅ Loaded environment variables from .env file")
    elif template_path.exists():
        load_dotenv(template_path)
        print("✅ Loaded environment variables from .env.template file")
        print("💡 Consider copying .env.template to .env and filling in your actual values")
    else:
        print("⚠️  No .env or .env.template file found, using system environment variables")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables only")
    print("💡 Consider installing python-dotenv: pip install python-dotenv")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import Discord bot components
import sys
from pathlib import Path

from discord_bot_config import config as discord_config
from discord_commander_core import DiscordCommanderCore

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import discord
    from discord.ext import commands
    from services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot
except ImportError:
    discord = None
    commands = None
    EnhancedDiscordAgentBot = None

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DiscordCommander:
    """Main Discord Commander application."""

    def __init__(self):
        """Initialize Discord Commander."""
        self.bot = None
        self.logger = logging.getLogger(f"{__name__}.DiscordCommander")
        self.core = DiscordCommanderCore(self.logger)

    async def initialize(self) -> bool:
        """Initialize the Discord Commander system."""
        try:
            self.logger.info("🚀 Initializing Discord Commander...")
            self.logger.info("🐝 WE ARE SWARM - Discord Commander Starting!")

            # Check configuration
            if not self._check_configuration():
                self.logger.error("❌ Discord Commander configuration incomplete!")
                return False

            # Create Discord bot
            self.bot = self.core.create_discord_bot()

            # Slash commands are set up in the bot's setup_slash_commands method

            self.logger.info("✅ Discord Commander initialized successfully!")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord Commander: {e}")
            return False

    def _check_configuration(self) -> bool:
        """Check Discord Commander configuration."""
        try:
            # Check Discord bot token
            if not discord_config.get_bot_token():
                self.logger.error("❌ Discord bot token not configured!")
                self.logger.error("   Set DISCORD_BOT_TOKEN environment variable")
                return False

            # Check Discord channel ID
            if not discord_config.get_channel_id():
                self.logger.warning("⚠️  Discord channel ID not configured!")
                self.logger.warning("   Set DISCORD_CHANNEL_ID environment variable")

            # Print configuration status
            discord_config.print_config_status()

            return True

        except Exception as e:
            self.logger.error(f"❌ Error checking configuration: {e}")
            return False

    async def start(self) -> bool:
        """Start the Discord Commander."""
        try:
            if not self.bot:
                self.logger.error("❌ Discord Commander not initialized!")
                return False

            self.logger.info("🚀 Starting Discord Commander...")
            self.logger.info("🐝 WE ARE SWARM - 5-Agent Mode Active!")

            # Get bot token
            token = discord_config.get_bot_token()
            if not token:
                self.logger.error("❌ No Discord bot token available!")
                self.logger.error("💡 Please set DISCORD_BOT_TOKEN environment variable")
                self.logger.error("💡 Run: python setup_discord_commander.py to configure")
                return False

            # Start the Discord bot
            self.logger.info("🤖 Starting Discord bot...")
            self.logger.info(f"🔑 Token: {token[:10]}...{token[-4:]}")

            # Use core to start the bot
            self.core.bot = self.bot
            success = await self.core.start_bot(token)

            if success:
                self.logger.info("✅ Discord Commander started successfully!")
                return True
            else:
                self.logger.error("❌ Failed to start Discord Commander!")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to start Discord Commander: {e}")
            return False

    async def stop(self):
        """Stop the Discord Commander."""
        try:
            self.logger.info("🛑 Stopping Discord Commander...")

            if self.bot:
                await self.core.stop_bot()

            self.logger.info("✅ Discord Commander stopped successfully!")

        except Exception as e:
            self.logger.error(f"❌ Error stopping Discord Commander: {e}")

    def get_status(self) -> dict:
        """Get Discord Commander status."""
        status = {
            "commander_status": "Active" if self.bot else "Stopped",
            "bot_initialized": self.bot is not None,
            "configuration_valid": discord_config.is_configured(),
            "bot_token_configured": discord_config.get_bot_token() is not None,
            "channel_configured": discord_config.get_channel_id() is not None,
        }

        if self.bot:
            status.update(self.core.get_bot_status())

        return status


async def main():
    """Main function to run Discord Commander."""
    # Create Discord Commander instance
    commander = DiscordCommander()

    try:
        # Initialize
        success = await commander.initialize()
        if not success:
            logger.error("❌ Discord Commander initialization failed!")
            return 1

        # Print status
        status = commander.get_status()
        logger.info("📊 Discord Commander Status:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")

        # Start the commander
        success = await commander.start()
        if not success:
            logger.error("❌ Discord Commander start failed!")
            return 1

        # Keep running until interrupted
        logger.info("🐝 WE ARE SWARM - Discord Commander Operational!")
        logger.info("Press Ctrl+C to stop...")

        # Wait for bot to run
        while not commander.bot.is_closed():
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("🛑 Received keyboard interrupt - shutting down...")
    except Exception as e:
        logger.error(f"❌ Discord Commander error: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1
    finally:
        # Stop the commander
        await commander.stop()

    logger.info("👋 Discord Commander shutdown complete!")
    return 0


def setup_environment():
    """Setup environment for Discord Commander."""
    # Set default environment variables if not set
    if not os.getenv("DISCORD_BOT_TOKEN"):
        logger.warning("⚠️  DISCORD_BOT_TOKEN not set - Discord bot will not function!")

    if not os.getenv("DISCORD_CHANNEL_ID"):
        logger.warning("⚠️  DISCORD_CHANNEL_ID not set - Using default channel!")

    # Set app environment
    if not os.getenv("APP_ENV"):
        os.environ["APP_ENV"] = "production"

    if not os.getenv("LOG_LEVEL"):
        os.environ["LOG_LEVEL"] = "INFO"


if __name__ == "__main__":
    # Setup environment
    setup_environment()

    # Print header
    print("🐝 Discord Commander - Agent Cellphone V2")
    print("=" * 50)
    print("WE ARE SWARM - 5-Agent Mode Active")
    print("Agent Coordination Hub (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)")
    print("=" * 50)

    # Run main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)