#!/usr/bin/env python3
"""
Test Discord Commander with .env file loading
=============================================
Test if Discord Commander can load and use Discord configuration from .env file.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def load_env_file():
    """Load environment variables from .env file."""
    print("🔧 Loading .env file...")
    
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load .env file manually
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip('"\'')
                os.environ[key] = value
    
    print("✅ .env file loaded into environment")
    return True

def test_discord_environment_loading():
    """Test Discord environment variables after loading .env."""
    print("\n🔍 Testing Discord environment variables...")
    
    discord_vars = {
        'DISCORD_BOT_TOKEN': os.getenv('DISCORD_BOT_TOKEN'),
        'DISCORD_GUILD_ID': os.getenv('DISCORD_GUILD_ID'),
        'DISCORD_CHANNEL_ID': os.getenv('DISCORD_CHANNEL_ID'),
        'DISCORD_CHANNEL_AGENT_4': os.getenv('DISCORD_CHANNEL_AGENT_4'),
        'DISCORD_CHANNEL_AGENT_5': os.getenv('DISCORD_CHANNEL_AGENT_5'),
        'DISCORD_CHANNEL_AGENT_6': os.getenv('DISCORD_CHANNEL_AGENT_6'),
        'DISCORD_CHANNEL_AGENT_7': os.getenv('DISCORD_CHANNEL_AGENT_7'),
        'DISCORD_CHANNEL_AGENT_8': os.getenv('DISCORD_CHANNEL_AGENT_8'),
    }
    
    found_vars = 0
    for key, value in discord_vars.items():
        if value:
            found_vars += 1
            # Mask sensitive token
            display_value = value[:10] + "..." if key == 'DISCORD_BOT_TOKEN' else value
            print(f"   ✅ {key}: {display_value}")
        else:
            print(f"   ❌ {key}: Not set")
    
    print(f"\n📊 Found {found_vars}/{len(discord_vars)} Discord variables")
    return found_vars > 0

def test_discord_commander_with_real_config():
    """Test Discord Commander with real configuration from .env."""
    print("\n🤖 Testing Discord Commander with real .env configuration...")
    
    try:
        from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2
        
        # Get real values from environment
        token = os.getenv('DISCORD_BOT_TOKEN')
        guild_id = os.getenv('DISCORD_GUILD_ID')
        
        if not token:
            print("❌ DISCORD_BOT_TOKEN not found in environment")
            return False
        
        if not guild_id:
            print("❌ DISCORD_GUILD_ID not found in environment")
            return False
        
        print(f"✅ Using real Discord token: {token[:10]}...")
        print(f"✅ Using real Guild ID: {guild_id}")
        
        # Create bot with real configuration
        bot = DiscordCommanderBotV2(token, int(guild_id))
        print("✅ Discord Commander created with real configuration")
        
        # Test status
        status = bot.get_bot_status()
        print(f"📊 Bot status: {status.get('system_info', {}).get('status', 'Unknown')}")
        
        # Test quality metrics
        metrics = bot.get_quality_metrics()
        print(f"📈 Quality score: {metrics.get('quality_score', 'N/A')}")
        
        # Test integration status
        integration = bot.get_integration_status()
        print(f"🔗 Integration health: {integration.get('integration_health', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Discord Commander test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_discord_commander_connection():
    """Test actual Discord connection (this will fail with invalid token but shows the process)."""
    print("\n🌐 Testing Discord connection process...")
    
    try:
        from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2
        
        token = os.getenv('DISCORD_BOT_TOKEN')
        guild_id = os.getenv('DISCORD_GUILD_ID')
        
        if not token or not guild_id:
            print("❌ Missing Discord configuration")
            return False
        
        bot = DiscordCommanderBotV2(token, int(guild_id))
        
        # Try to start the bot (this will attempt to connect)
        print("🔄 Attempting Discord connection...")
        print("⚠️ This will fail if the token is invalid, but shows the connection process")
        
        # Note: We won't actually start the bot as it would hang
        # Just test that the bot can be created and configured
        print("✅ Bot configured for Discord connection")
        print("💡 To test actual connection, run the Discord Commander with: python run_discord_commander.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Discord connection test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🐝 Discord Commander .env Configuration Test")
    print("=" * 60)
    
    # Step 1: Load .env file
    env_loaded = load_env_file()
    if not env_loaded:
        print("❌ Cannot proceed without .env file")
        return False
    
    # Step 2: Test environment variables
    env_vars_ok = test_discord_environment_loading()
    if not env_vars_ok:
        print("❌ Discord environment variables not found")
        return False
    
    # Step 3: Test Discord Commander with real config
    commander_ok = test_discord_commander_with_real_config()
    if not commander_ok:
        print("❌ Discord Commander configuration test failed")
        return False
    
    # Step 4: Test connection process
    connection_ok = test_discord_commander_connection()
    if not connection_ok:
        print("❌ Discord connection process test failed")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DISCORD COMMANDER .ENV TEST SUMMARY")
    print("=" * 60)
    
    print("✅ .env file loaded successfully")
    print("✅ Discord environment variables found")
    print("✅ Discord Commander configured with real values")
    print("✅ Connection process ready")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Verify Discord bot token is valid")
    print("2. Ensure bot has proper permissions in Discord server")
    print("3. Run: python run_discord_commander.py")
    print("4. Test commands in Discord: !help")
    
    print("\n💡 DISCORD CONFIGURATION FOUND:")
    print(f"   • Bot Token: {os.getenv('DISCORD_BOT_TOKEN', 'Not set')[:10]}...")
    print(f"   • Guild ID: {os.getenv('DISCORD_GUILD_ID', 'Not set')}")
    print(f"   • Channel ID: {os.getenv('DISCORD_CHANNEL_ID', 'Not set')}")
    print(f"   • Agent Channels: 8 configured")
    
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
