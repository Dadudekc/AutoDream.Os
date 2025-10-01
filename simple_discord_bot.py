#!/usr/bin/env python3
"""
Simple Discord Bot - V2_SWARM Agent Control
===========================================

Simple, working Discord bot for agent control.
Uses Agent-7's proven agent_control.py commands.

Author: Agent-5 (Coordinator)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import discord
    from discord import app_commands

    DISCORD_AVAILABLE = True
except ImportError:
    print("❌ Discord.py not installed. Run: pip install discord.py")
    DISCORD_AVAILABLE = False
    sys.exit(1)

from src.services.discord_commander.commands.agent_control import AgentControlCommands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleDiscordBot:
    """Simple Discord bot for V2_SWARM agent control"""

    def __init__(self, token: str, guild_id: int):
        """Initialize simple Discord bot"""
        self.token = token
        self.guild_id = guild_id

        # Create bot with intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        self.bot = discord.Client(intents=intents)
        self.tree = app_commands.CommandTree(self.bot)

        # Initialize agent control commands
        self.agent_commands = AgentControlCommands(self.bot, None)

        # Register event handlers
        self._register_events()

        logger.info("Simple Discord Bot initialized")

    def _register_events(self):
        """Register Discord event handlers"""

        @self.bot.event
        async def on_ready():
            """Handle bot ready event"""
            logger.info(f"Bot logged in as {self.bot.user}")

            # Register slash commands
            self.agent_commands.register_commands(self.tree)

            # Sync commands to guild
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

            logger.info(f"Commands synced to guild {self.guild_id}")
            print(f"✅ Simple Discord Bot ready! Logged in as {self.bot.user}")
            print("📡 Commands available:")
            print("   /send_message - Send custom message to agent")
            print("   /agent_status - Check agent status")
            print("   /run_scan - Run project scanner")
            print("   /custom_task - Assign custom task")

        @self.bot.event
        async def on_error(event, *args, **kwargs):
            """Handle bot errors"""
            logger.error(f"Bot error in {event}: {args} {kwargs}")

    async def start(self):
        """Start the bot"""
        try:
            logger.info("Starting Simple Discord Bot...")
            await self.bot.start(self.token)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

    async def stop(self):
        """Stop the bot"""
        await self.bot.close()
        logger.info("Simple Discord Bot stopped")


def validate_environment() -> tuple[str, int]:
    """Validate environment and get credentials"""
    token = os.getenv("DISCORD_BOT_TOKEN")
    guild_id = os.getenv("DISCORD_GUILD_ID")

    if not token:
        print("❌ DISCORD_BOT_TOKEN not set!")
        print("💡 Set it with: $env:DISCORD_BOT_TOKEN='your_token'")
        sys.exit(1)

    if not guild_id:
        print("❌ DISCORD_GUILD_ID not set!")
        print("💡 Set it with: $env:DISCORD_GUILD_ID='your_guild_id'")
        sys.exit(1)

    try:
        guild_id = int(guild_id)
    except ValueError:
        print(f"❌ Invalid DISCORD_GUILD_ID: {guild_id}")
        sys.exit(1)

    print("✅ Environment validation passed!")
    return token, guild_id


async def main():
    """Main entry point"""
    print("🚀 Starting Simple Discord Bot for V2_SWARM Agent Control...")
    print("=" * 60)

    # Validate environment
    token, guild_id = validate_environment()

    # Create and start bot
    bot = SimpleDiscordBot(token, guild_id)

    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
        await bot.stop()
    except Exception as e:
        print(f"❌ Bot error: {e}")
        await bot.stop()
        sys.exit(1)


if __name__ == "__main__":
    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not available")
        sys.exit(1)

    asyncio.run(main())
