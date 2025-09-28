#!/usr/bin/env python3
"""
Test Discord Bot Creation
=========================
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_discord_bot():
    """Test Discord bot creation."""
    try:
        print("Testing Discord bot creation...")
        
        # Test imports
        print("1. Testing imports...")
        from services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot
        import discord
        print("   ✅ Imports successful")
        
        # Test bot creation
        print("2. Testing bot creation...")
        intents = discord.Intents.default()
        intents.message_content = True
        bot = EnhancedDiscordAgentBot(command_prefix='!', intents=intents)
        print("   ✅ Bot created successfully")
        
        # Test bot properties
        print("3. Testing bot properties...")
        print(f"   Agent coordinates: {len(bot.agent_coordinates)} agents")
        print(f"   Messaging service: {bot.messaging_service is not None}")
        print(f"   Command router: {bot.command_router is not None}")
        print(f"   Security manager: {bot.security_manager is not None}")
        print(f"   UI embeds: {bot.ui_embeds is not None}")
        
        # Test command registration
        print("4. Testing command registration...")
        print(f"   Commands registered: {len(bot.tree.get_commands())}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_discord_bot()
    sys.exit(0 if success else 1)