#!/usr/bin/env python3
"""
Discord Commander Bot - Remote Swarm Control Center
Text commands + Interactive UI + Detailed agent status
Author: Agent-8 | Enhanced: 2025-10-13
Refactored: Agent-7 (Lean Excellence) | 2025-10-14
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Discord imports
try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ discord.py not installed!")
    print("   Install with: pip install discord.py")
    sys.exit(1)

# Import our systems
from src.discord_commander.messaging_controller import DiscordMessagingController
from src.discord_commander.status_reader import StatusReader
from src.services.messaging_service import ConsolidatedMessagingService

# Import command handlers (Lean Excellence refactor)
from discord_command_handlers import DiscordCommandHandlers, register_commands

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("discord_unified_bot.log")],
)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Initialize messaging systems
messaging_service = ConsolidatedMessagingService()
messaging_controller = DiscordMessagingController(messaging_service)
status_reader = StatusReader()

# Initialize command handlers (Lean Excellence refactor)
handlers = DiscordCommandHandlers(bot, messaging_controller, status_reader)


@bot.event
async def on_ready():
    """Bot startup event."""
    logger.info(f"✅ Discord Commander connected as {bot.user}")
    print("\n🚀 DISCORD COMMANDER ONLINE! Remote swarm control ready!\n")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="the swarm 🤖")
    )

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🤖 DISCORD COMMANDER",
                    description="Remote Swarm Control Center",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="📝 Quick Commands",
                    value="`!message <agent> <text>`\n`!broadcast <text>`\n`!status`",
                    inline=True,
                )
                embed.add_field(
                    name="🎮 Interactive UI",
                    value="`!agent_interact`\n`!swarm_status`\n`!agents`",
                    inline=True,
                )
                embed.add_field(name="ℹ️ Info", value="`!help`", inline=True)
                embed.set_footer(text="🐝 Remote Coordination Enabled!")
                await channel.send(embed=embed)
                logger.info(f"📢 Commander online in {guild.name}")
                break
        break


# Register all command handlers (Lean Excellence refactor)
register_commands(bot, handlers)


async def main():
    """Main entry point."""
    token = os.getenv("DISCORD_BOT_TOKEN")

    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not found!")
        print("\n❌ SETUP: Set DISCORD_BOT_TOKEN in .env file")
        return

    try:
        logger.info("🚀 Starting Discord Commander - Remote Swarm Control...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord bot token!")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot shutdown complete")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
