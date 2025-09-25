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

from discord_bot_config import config as discord_config

# Import Discord bot components
import sys
from pathlib import Path
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
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiscordCommander:
    """Main Discord Commander application."""

    def __init__(self):
        """Initialize Discord Commander."""
        self.bot = None
        self.logger = logging.getLogger(f"{__name__}.DiscordCommander")

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
            self.bot = self._create_discord_bot()

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

    def _create_discord_bot(self):
        """Create Discord bot instance."""
        if not discord or not EnhancedDiscordAgentBot:
            raise ImportError("Discord.py not installed or EnhancedDiscordAgentBot not found")

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        bot = EnhancedDiscordAgentBot(command_prefix="!", intents=intents)

        # Add agent interface and swarm coordinator
        from services.discord_bot.core.discord_bot import DiscordAgentInterface, DiscordSwarmCoordinator
        bot.agent_interface = DiscordAgentInterface(bot)
        bot.swarm_coordinator = DiscordSwarmCoordinator(bot)
        
        # Setup slash commands
        bot.setup_slash_commands()

        # Add on_ready event for slash command syncing
        @bot.event
        async def on_ready():
            """Called when bot is ready and connected."""
            self.logger.info(f"🤖 Discord Commander {bot.user} is online!")
            self.logger.info(f"📊 Connected to {len(bot.guilds)} servers")
            
            # Sync slash commands
            try:
                synced = await bot.tree.sync()
                self.logger.info(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                self.logger.warning(f"⚠️  Failed to sync slash commands: {e}")
            
            # Update presence
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="🐝 WE ARE SWARM - Agent Coordination Active"
                )
            )

            # Print startup message
            print("=" * 60)
            print("🐝 Discord Commander Successfully Started!")
            print("=" * 60)
            print(f"🤖 Bot: {bot.user}")
            print(f"📊 Servers: {len(bot.guilds)}")
            print(f"👥 Users: {len(bot.users)}")
            print(f"📡 Status: Online and Ready!")
            print(f"🎯 5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
            print("=" * 60)
            print("✅ All systems operational!")
            print("🚀 Ready for agent coordination!")
            print("=" * 60)

        return bot

    def _setup_additional_slash_commands(self):
        """Setup additional Discord slash commands that aren't already registered."""
        if not self.bot:
            return

        try:
            # Add only new commands that aren't already registered by the bot
            # The bot already has: agent_status, message_agent, swarm_status
            # So we only add: ping and help
            
            from discord import app_commands
            
            @app_commands.command(name="ping", description="Check bot latency")
            async def ping(interaction: discord.Interaction):
                latency = round(self.bot.latency * 1000)
                await interaction.response.send_message(
                    f"🏓 Pong! Latency: {latency}ms"
                )

            @app_commands.command(name="help", description="Show available commands")
            async def help_command(interaction: discord.Interaction):
                embed = discord.Embed(
                    title="🐝 Discord Commander Help",
                    description="Available Commands:",
                    color=0x0099ff
                )
                embed.add_field(
                    name="/ping",
                    value="Check bot latency",
                    inline=False
                )
                embed.add_field(
                    name="/agent_status",
                    value="Get status of a specific agent",
                    inline=False
                )
                embed.add_field(
                    name="/message_agent",
                    value="Send a message to a specific agent",
                    inline=False
                )
                embed.add_field(
                    name="/swarm_status",
                    value="Get current swarm status",
                    inline=False
                )
                embed.add_field(
                    name="/help",
                    value="Show this help message",
                    inline=False
                )
                await interaction.response.send_message(embed=embed)

            # Register commands with the bot using the same method as the bot
            self.bot.tree.add_command(ping)
            self.bot.tree.add_command(help_command)

            # Note: Slash commands will be synced when bot starts
            self.logger.info("✅ Additional slash commands (ping, help) registered")

        except Exception as e:
            self.logger.error(f"❌ Failed to setup additional slash commands: {e}")

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

            try:
                # Start the actual Discord bot with proper error handling
                await self.bot.start(token)

                self.logger.info("✅ Discord bot started successfully!")
                self.logger.info("📡 Ready to coordinate agents!")
                self.logger.info("🐝 WE ARE SWARM - Discord Commander Operational!")

                # Discord Commander successfully initialized!
                print("🐝 Discord Commander successfully initialized!")
                print("✅ All systems operational")
                print("🤖 5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
                print("📡 Ready for Discord bot token configuration")
                print("🚀 Use 'python setup_discord_commander.py' to configure")

                return True

            except discord.LoginFailure:
                self.logger.error("❌ Discord login failed - invalid token!")
                return False
            except discord.HTTPException as e:
                self.logger.error(f"❌ Discord HTTP error: {e}")
                return False
            except Exception as e:
                self.logger.error(f"❌ Error starting Discord bot: {e}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to start Discord Commander: {e}")
            return False

    async def stop(self):
        """Stop the Discord Commander."""
        try:
            self.logger.info("🛑 Stopping Discord Commander...")

            if self.bot:
                await self.bot.close()

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
            status.update(self.bot.get_swarm_status())

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
