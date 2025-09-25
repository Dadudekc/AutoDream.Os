#!/usr/bin/env python3
"""
Test Discord Commander System
=============================

Simple test script to verify Discord Commander functionality.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_discord_commander():
    """Test Discord Commander system."""
    print("🚀 Testing Discord Commander System...")
    print("=" * 50)

    # Check environment
    token = os.getenv("DISCORD_BOT_TOKEN", "")
    guild_id = os.getenv("DISCORD_GUILD_ID", "")

    print(f"Discord Token: {'✅ Set' if token else '❌ Not set'}")
    print(f"Discord Guild ID: {'✅ Set' if guild_id else '❌ Not set'}")

    # Check if we can import the components
    try:
        from src.services.discord_commander.bot import DiscordCommanderBot
        print("✅ Discord Commander Bot import successful")
    except Exception as e:
        print(f"❌ Discord Commander Bot import failed: {e}")
        return False

    try:
        from src.services.discord_commander.web_controller import DiscordCommanderController
        print("✅ Web Controller import successful")
    except Exception as e:
        print(f"❌ Web Controller import failed: {e}")
        return False

    # Try to create bot instance
    try:
        bot = DiscordCommanderBot()
        print("✅ Discord Commander Bot created successfully")

        # Test command registration
        commands = bot.command_manager.list_commands()
        print(f"✅ Commands registered: {len(commands)} commands")
        print(f"Available commands: {commands}")

    except Exception as e:
        print(f"❌ Discord Commander Bot creation failed: {e}")
        return False

    # Test web controller
    try:
        controller = DiscordCommanderController()
        print("✅ Web Controller created successfully")
    except Exception as e:
        print(f"❌ Web Controller creation failed: {e}")
        return False

    print("✅ Discord Commander system is working!")
    print("\n📋 To use the system:")
    print("1. Update .env with real Discord tokens for production")
    print("2. Run: python run_discord_commander.py")
    print("3. Open: http://localhost:8080")
    print("4. Use Discord commands: !help")

    return True

if __name__ == "__main__":
    success = asyncio.run(test_discord_commander())
    sys.exit(0 if success else 1)
