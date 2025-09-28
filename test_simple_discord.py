#!/usr/bin/env python3
"""
Simple Discord Bot Test
=======================
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_simple():
    """Test simple Discord bot creation."""
    try:
        print("Testing simple Discord bot creation...")
        
        # Test basic imports
        print("1. Testing basic imports...")
        import discord
        print("   ✅ Discord import successful")
        
        # Test bot creation without custom class
        print("2. Testing basic bot creation...")
        from discord.ext import commands
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)
        print("   ✅ Basic bot created successfully")
        
        # Test custom bot import
        print("3. Testing custom bot import...")
        from services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot
        print("   ✅ Custom bot import successful")
        
        # Test custom bot creation
        print("4. Testing custom bot creation...")
        custom_bot = EnhancedDiscordAgentBot(command_prefix='!', intents=intents)
        print("   ✅ Custom bot created successfully")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple()
    sys.exit(0 if success else 1)