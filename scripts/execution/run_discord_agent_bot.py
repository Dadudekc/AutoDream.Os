#!/usr/bin/env python3
"""
Discord Agent Bot Runner - V2 Compliance Module
===============================================

Runner script for the V2_SWARM Discord Agent Bot.
Provides interactive agent prompting through Discord commands.

Usage:
    python run_discord_agent_bot.py [TOKEN]
    python run_discord_agent_bot.py --test
    python run_discord_agent_bot.py --config

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Environment variables must be set manually.")

# Add src and project root to path for better import handling
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

try:
    from src.discord_commander.discord_agent_bot import (
        get_discord_bot_manager,
        start_discord_agent_bot,
        test_discord_bot_connection,
    )
except ImportError as e:
    print(f"❌ Failed to import Discord bot modules: {e}")
    print("💡 Make sure you're running from the project root")
    sys.exit(1)


def print_banner():
    """Print V2_SWARM Discord Agent Bot banner."""
    banner = """
🐝 V2_SWARM Discord Agent Bot 🐝
================================

🤖 Interactive Agent Coordination System
📢 Real-time Agent Prompting via Discord
🎯 Swarm Intelligence Command Interface

Available Commands:
  🎯 Agent Commands: !agent1-8, !captain, !prompt @agent
  🐝 Swarm Commands: !swarm, !urgent, !broadcast
  📊 Status Commands: !status, !summary1-4, !agentsummary
  ⚡ Interactive: /agent (autocomplete), /summary_core
  🔧 Utilities: !help, !ping, !agents
  🔄 Aliases: From config/agent_aliases.json (!a1, !lead, etc.)

================================
    """
    print(banner)


def get_token_from_env() -> str:
    """Get Discord bot token from environment variables."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ Discord bot token not found!")
        print("💡 Set the DISCORD_BOT_TOKEN environment variable")
        print("   Example: export DISCORD_BOT_TOKEN='your_bot_token_here'")
        sys.exit(1)
    return token


def get_token_from_args() -> str:
    """Get Discord bot token from command line arguments."""
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        return sys.argv[1]
    return get_token_from_env()


async def test_bot(token: str):
    """Test Discord bot connection."""
    print("🧪 Testing Discord Bot Connection...")
    print("=" * 50)

    success = await test_discord_bot_connection(token)

    if success:
        print("✅ Bot connection test PASSED!")
        print("🎉 Bot is ready to connect to Discord")
    else:
        print("❌ Bot connection test FAILED!")
        print("💡 Check your bot token and internet connection")
        sys.exit(1)


def show_config():
    """Show current bot configuration."""
    print("📋 Discord Bot Configuration")
    print("=" * 50)

    manager = get_discord_bot_manager()
    config = manager.load_config()

    print(f"🤖 Command Prefix: {config.get('command_prefix', '!')}")
    print(f"⏱️  Command Timeout: {config.get('command_timeout', 300)}s")
    print(f"🔢 Max Concurrent Commands: {config.get('max_concurrent_commands', 10)}")
    print(f"📺 Allowed Channels: {len(config.get('allowed_channels', []))} configured")
    print(f"👥 Admin Users: {len(config.get('admin_users', []))} configured")

    print("\n🎯 Features:")
    features = config.get("features", {})
    for feature, enabled in features.items():
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"  {status} {feature.replace('_', ' ').title()}")

    print("\n🔧 Integrations:")
    integrations = config.get("integrations", {})
    for integration, enabled in integrations.items():
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"  {status} {integration.replace('_', ' ').title()}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="V2_SWARM Discord Agent Bot")
    parser.add_argument("token", nargs="?", help="Discord bot token")
    parser.add_argument("--test", action="store_true", help="Test bot connection only")
    parser.add_argument("--config", action="store_true", help="Show bot configuration")
    parser.add_argument("--setup", action="store_true", help="Show setup instructions")
    parser.add_argument("--diagnose", action="store_true", help="Run diagnostic checks for messaging issues")

    args = parser.parse_args()

    print_banner()

    if args.config:
        show_config()
        return

    if args.setup:
        show_setup_instructions()
        return

    if args.diagnose:
        asyncio.run(run_diagnostics())
        return

    # Get bot token
    if args.token:
        token = args.token
    else:
        token = get_token_from_env()

    if not token:
        print("❌ No Discord bot token provided!")
        print("💡 Use: python run_discord_agent_bot.py YOUR_TOKEN_HERE")
        print("   Or set: export DISCORD_BOT_TOKEN='your_token'")
        return

    # Test connection if requested
    if args.test:
        asyncio.run(test_bot(token))
        return

    # Start the bot
    print("🚀 Starting V2_SWARM Discord Agent Bot...")
    print(f"🤖 Token: {'***' + token[-10:] if len(token) > 10 else token}")
    print("=" * 60)

    try:
        asyncio.run(start_discord_agent_bot(token))
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        sys.exit(1)


def show_setup_instructions():
    """Show setup instructions for the Discord bot."""
    instructions = """
📚 Discord Bot Setup Instructions
==================================

1. Create a Discord Application:
   • Go to https://discord.com/developers/applications
   • Click "New Application"
   • Give it a name (e.g., "V2_SWARM Agent Bot")

2. Create a Bot:
   • Go to the "Bot" section in the left sidebar
   • Click "Add Bot"
   • Copy the bot token

3. Set Environment Variable:
   • Windows: set DISCORD_BOT_TOKEN=your_bot_token_here
   • Linux/Mac: export DISCORD_BOT_TOKEN=your_bot_token_here
   • Or pass token as argument: python run_discord_agent_bot.py your_token

4. Invite Bot to Server:
   • Go to OAuth2 → URL Generator
   • Select scopes: bot, applications.commands
   • Select permissions: Send Messages, Read Messages, Embed Links
   • Use generated URL to invite bot to your server

5. Configure Bot (Optional):
   • Edit config/discord_bot_config.json
   • Set allowed_channels and admin_users if needed

6. Run the Bot:
   • python scripts/execution/run_discord_agent_bot.py
   • Or with token: python scripts/execution/run_discord_agent_bot.py your_token

🎯 Usage Examples:
• !prompt @Agent-4 Please analyze the current project status
• !status @Agent-1
• !swarm Emergency coordination meeting required
• !agents
• !help

🐝 WE ARE SWARM - Ready for Discord coordination!
    """
    print(instructions)


async def run_diagnostics():
    """Run diagnostic checks for Discord bot messaging issues."""
    print("🔍 DISCORD BOT DIAGNOSTICS")
    print("=" * 50)

    # Check environment variables
    print("📋 Environment Variables:")
    discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
    allowed_channel_ids = os.getenv("ALLOWED_CHANNEL_IDS")
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

    print(f"  DISCORD_CHANNEL_ID: {'✅ Set' if discord_channel_id else '❌ Not set'}")
    print(f"  ALLOWED_CHANNEL_IDS: {'✅ Set' if allowed_channel_ids else '❌ Not set'}")
    print(f"  DISCORD_BOT_TOKEN: {'✅ Set' if discord_bot_token else '❌ Not set'}")

    # Auto-fix: If DISCORD_CHANNEL_ID is set but ALLOWED_CHANNEL_IDS is not, suggest setting it
    if discord_channel_id and not allowed_channel_ids:
        print()
        print("⚠️  POTENTIAL FIX FOUND:")
        print("  ALLOWED_CHANNEL_IDS is not set, but DISCORD_CHANNEL_ID is set.")
        print("  This may cause the bot to reject commands in the intended channel.")
        print()
        print("  Quick fix - Run this command to set ALLOWED_CHANNEL_IDS:")
        print(f"  $env:ALLOWED_CHANNEL_IDS = '{discord_channel_id}'")
        print("  Or add to your .env file: ALLOWED_CHANNEL_IDS=" + discord_channel_id)

    # Check bot configuration
    print("\n⚙️ Bot Configuration:")
    config_path = Path("config/discord_bot_config.json")
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            allowed_channels = config.get("permissions", {}).get("allowed_channels", [])
            print(f"  Config file: ✅ Found at {config_path}")
            print(f"  Allowed channels in config: {len(allowed_channels)} configured")
            if allowed_channels:
                print(f"    Channel IDs: {allowed_channels}")
        except Exception as e:
            print(f"  Config file: ❌ Error reading: {e}")
    else:
        print(f"  Config file: ❌ Not found at {config_path}")

    # Test bot connection
    print("\n🤖 Bot Connection Test:")
    token = discord_bot_token or get_token_from_args()
    if token:
        success = await test_discord_bot_connection(token)
        if success:
            print("  Connection: ✅ Bot can connect to Discord")

            # Try to start bot briefly to check channel access
            print("\n📺 Channel Access Test:")
            try:
                manager = get_discord_bot_manager()
                bot = manager.create_bot(token)

                @bot.event
                async def on_ready():
                    print(f"  Bot logged in as: {bot.user}")
                    print(f"  Connected to {len(bot.guilds)} guild(s)")

                    for guild in bot.guilds:
                        print(f"    Guild: {guild.name} (ID: {guild.id})")
                        text_channels = [c for c in guild.text_channels if c.permissions_for(guild.me).send_messages]
                        print(f"      Sendable text channels: {len(text_channels)}")

                        if text_channels:
                            # Try to send a test message
                            test_channel = text_channels[0]
                            try:
                                test_msg = await test_channel.send("🧪 **DIAGNOSTIC TEST MESSAGE**\n\nThis is a test message from the diagnostic tool. If you see this, Discord messaging is working!")
                                await test_msg.delete()  # Clean up the test message
                                print(f"      ✅ Can send messages in: #{test_channel.name}")
                            except Exception as e:
                                print(f"      ❌ Cannot send messages in #{test_channel.name}: {e}")

                    await bot.close()

                await bot.start(token)

            except Exception as e:
                print(f"  ❌ Channel access test failed: {e}")
        else:
            print("  Connection: ❌ Bot cannot connect to Discord")
    else:
        print("  Connection: ❌ No bot token available")

    # Check agent inboxes
    print("\n📨 Agent Inbox Status:")
    agent_workspaces = Path("agent_workspaces")
    if agent_workspaces.exists():
        agent_dirs = [d for d in agent_workspaces.iterdir() if d.is_dir()]
        print(f"  Agent workspaces found: {len(agent_dirs)}")

        for agent_dir in agent_dirs:
            inbox_dir = agent_dir / "inbox"
            if inbox_dir.exists():
                inbox_files = list(inbox_dir.glob("*.md"))
                print(f"    {agent_dir.name}: {len(inbox_files)} messages in inbox")
            else:
                print(f"    {agent_dir.name}: ❌ No inbox directory")
    else:
        print("  ❌ Agent workspaces directory not found")

    print("\n📋 DIAGNOSTIC SUMMARY:")
    print("=" * 50)
    print("🔍 Issue Analysis:")
    print("  - Bot reports 'sending' messages → This refers to agent inbox delivery")
    print("  - Discord channel messages may be failing due to permissions/restrictions")
    print()
    print("💡 Possible Solutions:")
    print("  1. Check bot permissions in Discord server (Send Messages, Embed Links)")
    print("  2. Verify ALLOWED_CHANNEL_IDS environment variable is set correctly")
    print("  3. Ensure bot has access to the channel you're testing in")
    print("  4. Check if channel restrictions are too strict in config")
    print("  5. Try the --test flag to verify basic Discord connectivity")
    print()
    print("🧪 Test Commands:")
    print("  python run_discord_agent_bot.py --test          # Test Discord connection")
    print("  python run_discord_agent_bot.py --diagnose      # Run this diagnostic")
    print("  !ping                                          # Test bot responsiveness in Discord")
    print("  !test                                          # Send test message to current channel")
    print()
    print("🔧 Quick Fix - Set ALLOWED_CHANNEL_IDS:")
    print("  If messages aren't appearing, set this environment variable:")
    print("  ALLOWED_CHANNEL_IDS=<your_channel_id>")
    print("  Example: ALLOWED_CHANNEL_IDS=1412461118970138714")
    print()
    if discord_channel_id:
        print("💡 Auto-fix suggestion:")
        print(f"  Set ALLOWED_CHANNEL_IDS={discord_channel_id}")
        print("  This will restrict the bot to only respond in your specified channel.")


if __name__ == "__main__":
    main()
