#!/usr/bin/env python3
"""
Discord Commander Test Tool
===========================

Simple CLI tool to test Discord Commander functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

async def test_discord_commander():
    """Test Discord Commander functionality."""
    try:
        from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2
        
        # Check environment variables
        token = os.getenv("DISCORD_BOT_TOKEN")
        guild_id = os.getenv("DISCORD_GUILD_ID")
        
        if not token:
            print("❌ DISCORD_BOT_TOKEN not set")
            return False
            
        if not guild_id:
            print("❌ DISCORD_GUILD_ID not set")
            return False
            
        print("✅ Environment variables configured")
        
        # Create bot instance
        bot = DiscordCommanderBotV2(token, int(guild_id))
        print("✅ Bot instance created")
        
        # Test bot status
        status = bot.get_bot_status()
        print(f"✅ Bot status: {status}")
        
        # Test quality metrics
        metrics = bot.get_quality_metrics()
        print(f"✅ Quality metrics: {metrics}")
        
        # Test integration status
        integration = bot.get_integration_status()
        print(f"✅ Integration status: {integration}")
        
        print("🎉 Discord Commander test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Discord Commander test failed: {e}")
        return False

def main():
    """Main function."""
    print("🧪 Testing Discord Commander...")
    success = asyncio.run(test_discord_commander())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
