#!/usr/bin/env python3
"""
Test Discord Environment Loading
===============================
Test if Discord Commander can load configuration from .env and config files.
"""

import os
import sys
import yaml
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_env_file_loading():
    """Test loading from .env file."""
    print("🔍 Testing .env file loading...")
    
    # Check if .env exists
    env_file = project_root / ".env"
    if env_file.exists():
        print("✅ .env file exists")
        
        # Load .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        discord_vars = {}
        for line in lines:
            line = line.strip()
            if line.startswith('DISCORD_') and '=' in line:
                key, value = line.split('=', 1)
                discord_vars[key] = value
                print(f"   • {key}: {'Set' if value else 'Empty'}")
        
        if discord_vars:
            print(f"✅ Found {len(discord_vars)} Discord variables in .env")
            return discord_vars
        else:
            print("⚠️ No Discord variables found in .env")
            return {}
    else:
        print("❌ .env file does not exist")
        return {}

def test_config_file_loading():
    """Test loading from config files."""
    print("\n🔍 Testing config file loading...")
    
    # Test unified_config.yaml
    config_file = project_root / "config" / "unified_config.yaml"
    if config_file.exists():
        print("✅ unified_config.yaml exists")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        discord_config = config.get('discord', {})
        if discord_config:
            print("✅ Discord config found in unified_config.yaml:")
            for key, value in discord_config.items():
                print(f"   • {key}: {'Set' if value else 'Empty'}")
            return discord_config
        else:
            print("⚠️ No Discord config found in unified_config.yaml")
    else:
        print("❌ unified_config.yaml does not exist")
    
    return {}

def test_discord_commander_config_loading():
    """Test if Discord Commander can load its own config."""
    print("\n🔍 Testing Discord Commander config loading...")
    
    try:
        from src.services.discord_commander.bot_config import BotConfiguration
        
        # Test BotConfiguration
        config = BotConfiguration()
        print("✅ BotConfiguration class imported and instantiated")
        
        # Test getting Discord token
        token = config.get_discord_token()
        print(f"   • Discord token: {'Set' if token else 'Not set'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Discord Commander config loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variable_loading():
    """Test loading from environment variables."""
    print("\n🔍 Testing environment variable loading...")
    
    discord_vars = {}
    env_vars_to_check = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_GUILD_ID', 
        'DISCORD_CHANNEL_ID',
        'DISCORD_CHANNEL_AGENT_4',
        'DISCORD_CHANNEL_AGENT_5',
        'DISCORD_CHANNEL_AGENT_6',
        'DISCORD_CHANNEL_AGENT_7',
        'DISCORD_CHANNEL_AGENT_8'
    ]
    
    for var in env_vars_to_check:
        value = os.getenv(var)
        if value:
            discord_vars[var] = value
            print(f"   • {var}: Set")
        else:
            print(f"   • {var}: Not set")
    
    if discord_vars:
        print(f"✅ Found {len(discord_vars)} Discord environment variables")
        return discord_vars
    else:
        print("⚠️ No Discord environment variables found")
        return {}

def create_sample_env_file():
    """Create a sample .env file for testing."""
    print("\n📝 Creating sample .env file...")
    
    env_file = project_root / ".env"
    
    # Read template
    template_file = project_root / "config" / "discord_bot_config.template"
    if template_file.exists():
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        # Write to .env
        with open(env_file, 'w') as f:
            f.write(template_content)
        
        print("✅ Sample .env file created from template")
        print("💡 Edit .env file with your real Discord credentials")
        return True
    else:
        print("❌ Template file not found")
        return False

def test_discord_commander_with_config():
    """Test Discord Commander with loaded configuration."""
    print("\n🤖 Testing Discord Commander with loaded config...")
    
    try:
        from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2
        
        # Get token from environment
        token = os.getenv("DISCORD_BOT_TOKEN")
        guild_id = os.getenv("DISCORD_GUILD_ID")
        
        if not token:
            print("⚠️ No DISCORD_BOT_TOKEN found, using placeholder")
            token = "test_token_placeholder"
        
        if not guild_id:
            print("⚠️ No DISCORD_GUILD_ID found, using placeholder")
            guild_id = "123456789"
        
        try:
            guild_id_int = int(guild_id)
        except ValueError:
            guild_id_int = 123456789
        
        # Create bot with loaded config
        bot = DiscordCommanderBotV2(token, guild_id_int)
        print("✅ Discord Commander created with loaded configuration")
        
        # Test status
        status = bot.get_bot_status()
        print(f"📊 Bot status: {status.get('system_info', {}).get('status', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Discord Commander config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🐝 Discord Environment Loading Test")
    print("=" * 50)
    
    # Test 1: .env file loading
    env_vars = test_env_file_loading()
    
    # Test 2: Config file loading
    config_vars = test_config_file_loading()
    
    # Test 3: Environment variables
    env_env_vars = test_environment_variable_loading()
    
    # Test 4: Discord Commander config
    commander_ok = test_discord_commander_config_loading()
    
    # Test 5: Discord Commander with config
    bot_ok = test_discord_commander_with_config()
    
    # Create sample .env if needed
    if not env_vars:
        create_sample_env_file()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 CONFIGURATION LOADING SUMMARY")
    print("=" * 50)
    
    print(f"• .env file: {'✅ Found' if env_vars else '❌ Not found'}")
    print(f"• Config file: {'✅ Found' if config_vars else '❌ Not found'}")
    print(f"• Environment vars: {'✅ Found' if env_env_vars else '❌ Not found'}")
    print(f"• Discord Commander config: {'✅ Working' if commander_ok else '❌ Failed'}")
    print(f"• Bot with config: {'✅ Working' if bot_ok else '❌ Failed'}")
    
    if not any([env_vars, config_vars, env_env_vars]):
        print("\n💡 RECOMMENDATION:")
        print("   Create a .env file with your Discord credentials:")
        print("   DISCORD_BOT_TOKEN=your_real_bot_token")
        print("   DISCORD_GUILD_ID=your_real_guild_id")
        print("   DISCORD_CHANNEL_ID=your_main_channel_id")
    
    print("\n" + "=" * 50)
    
    return all([commander_ok, bot_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
