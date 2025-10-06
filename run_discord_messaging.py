#!/usr/bin/env python3
"""
Launcher script for the Enhanced Discord Commander Bot.
This script initializes and starts the Discord bot, integrating it
with the Consolidated Messaging Service for agent interaction.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import after path setup
from src.services.discord_commander.enhanced_bot import EnhancedBotManager  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to initialize and run the bot."""
    print("🤖 Enhanced Discord Messaging Bot Launcher")
    print("=" * 50)
    print("Starting Discord bot with messaging controller...")
    print("Features:")
    print("• Interactive agent messaging with Discord views")
    print("• Real-time swarm status monitoring")
    print("• Broadcast messaging capabilities")
    print("• Easy agent selection and communication")
    print("=" * 50)

    logger.info("Starting Enhanced Discord Messaging Bot...")

    # Use EnhancedBotManager which handles configuration properly
    manager = EnhancedBotManager()

    # Check configuration before starting
    config_issues = manager.config.validate()
    if config_issues:
        print("\n❌ Configuration Issues Found:")
        for issue in config_issues:
            print(f"  • {issue}")
        print("\n📋 Setup Instructions:")
        print("1. Create a .env file in the project root")
        print("2. Add the following environment variables:")
        print("   DISCORD_BOT_TOKEN=your_bot_token_here")
        print("   DISCORD_GUILD_ID=your_guild_id_here")
        print("3. Get your Discord bot token from: https://discord.com/developers/applications")
        print(
            "4. Get your Guild ID by enabling Developer Mode in Discord and "
            "right-clicking your server"
        )
        print("\n💡 Example .env file:")
        print("DISCORD_BOT_TOKEN=your_actual_bot_token_here")
        print("DISCORD_GUILD_ID=123456789012345678")
        print("DISCORD_COMMAND_PREFIX=!")
        return

    await manager.start_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Discord bot stopped by user.")
    except Exception as e:
        logger.error(f"An unhandled error occurred: {e}")
        sys.exit(1)
