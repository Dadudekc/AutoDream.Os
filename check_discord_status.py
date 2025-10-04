#!/usr/bin/env python3
"""
Discord Commander Status Check
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


async def check_discord_commander():
    """Check Discord Commander status."""
    print("🔍 Checking Discord Commander Status...")
    print("=" * 50)

    try:
        from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2

        print("✅ Discord Commander V2 imported successfully")

        # Initialize bot
        bot = DiscordCommanderBotV2()
        print("✅ Bot initialized")

        # Check if bot has health check
        if hasattr(bot, "is_healthy"):
            health_status = bot.is_healthy()
            print(f"🏥 Bot health status: {'✅ Healthy' if health_status else '❌ Unhealthy'}")
        else:
            print("⚠️ No health check method available")

        # Try to start the bot briefly
        print("🚀 Attempting to start bot...")
        try:
            await bot.start()
            print("✅ Bot started successfully")

            # Wait a moment
            await asyncio.sleep(3)

            # Check health again
            if hasattr(bot, "is_healthy"):
                health_status = bot.is_healthy()
                print(
                    f"🏥 Bot health after start: {'✅ Healthy' if health_status else '❌ Unhealthy'}"
                )

            # Stop the bot
            await bot.stop()
            print("🛑 Bot stopped")

        except Exception as e:
            print(f"❌ Error starting bot: {e}")

    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(check_discord_commander())
