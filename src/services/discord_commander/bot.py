#!/usr/bin/env python3
"""
Discord Commander Bot - Main Interface
======================================

Main interface for Discord Commander Bot.
V2 Compliant: ≤100 lines, imports from modular components.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.discord_commander.bot_manager import DiscordCommanderBot

logger = logging.getLogger(__name__)


async def main():
    """Main function to run the Discord Commander Bot."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

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
