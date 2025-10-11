#!/usr/bin/env python3
"""
Discord Messaging Bot Launcher
===============================

Easy launcher for the enhanced Discord messaging bot.
Provides seamless agent communication through Discord interface.

Usage:
    python run_discord_messaging.py

Features:
- Interactive agent messaging with Discord views
- Real-time swarm status monitoring
- Broadcast messaging capabilities
- Easy agent selection and communication
"""

import asyncio
import logging
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # dotenv not available, try loading manually
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        import os

        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.discord_commander.enhanced_bot import EnhancedBotManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("discord_messaging.log")],
)

logger = logging.getLogger(__name__)


async def main():
    """Main launcher function."""
    print("🤖 Enhanced Discord Messaging Bot Launcher")
    print("=" * 50)
    print("Starting Discord bot with messaging controller...")
    print("Features:")
    print("• Interactive agent messaging with Discord views")
    print("• Real-time swarm status monitoring")
    print("• Broadcast messaging capabilities")
    print("• Easy agent selection and communication")
    print("=" * 50)

    manager = EnhancedBotManager()

    try:
        # Start the bot
        logger.info("Starting Enhanced Discord Messaging Bot...")
        await manager.start_bot()

    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user (Ctrl+C)")
        logger.info("Bot stopped by user")

    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        logger.error(f"Bot crashed: {e}")

    finally:
        print("🔄 Shutting down bot...")
        await manager.stop_bot()
        print("✅ Bot shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
