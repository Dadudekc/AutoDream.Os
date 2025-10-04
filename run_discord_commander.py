#!/usr/bin/env python3
"""
Discord Commander Launcher
==========================

Comprehensive launcher for the Discord Commander system.
Starts both the Discord bot and the web controller interface.

Usage:
    python run_discord_commander.py

Features:
- Automatic Discord bot startup with configuration validation
- Web-based controller interface on port 8080
- Real-time monitoring and control
- Comprehensive logging and error handling
- Environment validation and setup guidance
"""

import asyncio
import logging
import os
import sys
import threading
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.services.discord_commander.bot import DiscordCommanderBot
    from src.services.discord_commander.web_controller import DiscordCommanderController, create_default_templates
    BOT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing Discord Commander: {e}")
    BOT_AVAILABLE = False

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DiscordCommanderLauncher:
    """Launcher for the Discord Commander system."""

    def __init__(self):
        """Initialize the launcher."""
        self.bot = None
        self.controller = None
        self.running = False

    def validate_environment(self) -> bool:
        """Validate the environment and provide guidance."""
        print("🔍 Validating Discord Commander environment...")

        issues = []

        # Check for Discord token
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            issues.append("DISCORD_BOT_TOKEN not set")
        else:
            print("✅ Discord Bot Token configured")

        # Check for Guild ID
        guild_id = os.getenv("DISCORD_GUILD_ID")
        if not guild_id:
            issues.append("DISCORD_GUILD_ID not set")
        else:
            print("✅ Discord Guild ID configured")

        # Check for required packages
        try:
            import discord
            import flask
            import flask_socketio
            print("✅ Required packages installed")
        except ImportError as e:
            issues.append(f"Missing packages: {e}")

        if issues:
            print("❌ Environment validation failed:")
            for issue in issues:
                print(f"   • {issue}")

            print("\n💡 Setup instructions:")
            print("1. Install required packages:")
            print("   pip install discord.py flask flask-socketio")
            print("\n2. Set up your Discord bot:")
            print("   • Go to https://discord.com/developers/applications")
            print("   • Create a new application")
            print("   • Go to 'Bot' section and create a bot")
            print("   • Copy the bot token")
            print("   • Set environment variables:")
            print("     export DISCORD_BOT_TOKEN='your_bot_token'")
            print("     export DISCORD_GUILD_ID='your_guild_id'")
            print("\n3. Invite the bot to your server:")
            print("   • Go to OAuth2 section")
            print("   • Select 'bot' scope")
            print("   • Copy the generated URL and visit it")

            return False

        print("✅ Environment validation passed!")
        return True

    def create_default_templates(self):
        """Create default web templates."""
        try:
            create_default_templates()
            print("✅ Web interface templates created")
        except Exception as e:
            print(f"❌ Error creating templates: {e}")

    async def start_bot(self):
        """Start the Discord bot."""
        if not BOT_AVAILABLE:
            print("❌ Discord Commander not available")
            return False

        try:
            print("🤖 Starting Discord Commander Bot...")
            self.bot = DiscordCommanderBot()

            if await self.bot.initialize():
                print("✅ Discord bot initialized successfully")

                # Start bot in a separate thread
                def run_bot():
                    asyncio.run(self.bot.start())

                bot_thread = threading.Thread(target=run_bot, daemon=True)
                bot_thread.start()

                # Give the bot a moment to connect
                await asyncio.sleep(3)

                if self.bot.is_healthy():
                    print("✅ Discord bot connected and healthy")
                    return True
                else:
                    print("❌ Discord bot failed to connect properly")
                    return False
            else:
                print("❌ Failed to initialize Discord bot")
                return False

        except Exception as e:
            print(f"❌ Error starting Discord bot: {e}")
            return False

    def start_controller(self):
        """Start the web controller."""
        try:
            print("🖥️ Starting Web Controller...")
            self.controller = DiscordCommanderController()

            if self.bot:
                self.controller.set_bot(self.bot)

            # Start controller in a separate thread
            def run_controller():
                self.controller.run()

            controller_thread = threading.Thread(target=run_controller, daemon=True)
            controller_thread.start()

            print("✅ Web controller started on http://localhost:8080")
            return True

        except Exception as e:
            print(f"❌ Error starting web controller: {e}")
            return False

    def show_status(self):
        """Show current system status."""
        print("\n" + "="*50)
        print("🐝 DISCORD COMMANDER STATUS")
        print("="*50)

        if self.bot:
            status = self.bot.get_status()
            print(f"🤖 Bot Status: {'🟢 Connected' if status.get('status') == 'healthy' else '🔴 Disconnected'}")
            print(f"⏱️ Uptime: {status.get('uptime_formatted', 'Unknown')}")
            print(f"📊 Commands Available: {status.get('command_count', 0)}")
            print(f"📈 Messages Received: {status.get('messages_received', 0)}")
        else:
            print("🤖 Bot Status: 🔴 Not running")

        if self.controller:
            print("🖥️ Web Controller: 🟢 Running on http://localhost:8080")
        else:
            print("🖥️ Web Controller: 🔴 Not running")

        print("\n📋 Available Commands:")
        print("• !agent_status [agent_id] - Get agent status")
        print("• !send_message <agent_id> <message> - Send message to agent")
        print("• !agent_coordinates [agent_id] - Get agent coordinates")
        print("• !system_status - Get system status")
        print("• !project_info - Get project information")
        print("• !swarm_status - Get swarm status")
        print("• !swarm_coordinate <message> - Coordinate all agents")
        print("• !help - Show help")

        print("\n🎯 Web Interface Features:")
        print("• Real-time agent status monitoring")
        print("• Interactive message sending")
        print("• Swarm coordination tools")
        print("• System health monitoring")
        print("• Live activity logs")

        print("\n" + "="*50)

    def run(self):
        """Run the Discord Commander system."""
        print("🚀 Starting Discord Commander System...")
        print("="*50)

        # Validate environment
        if not self.validate_environment():
            print("❌ Cannot start: Environment validation failed")
            return False

        # Create templates
        self.create_default_templates()

        # Start bot
        bot_success = asyncio.run(self.start_bot())

        # Start controller
        controller_success = self.start_controller()

        if not bot_success:
            print("❌ Discord bot failed to start")
            return False

        if not controller_success:
            print("⚠️ Web controller failed to start, but bot is running")

        # Show status
        self.show_status()

        # Keep running
        try:
            self.running = True
            print("\n✅ Discord Commander System is running!")
            print("📱 Use !help in Discord for bot commands")
            print("🖥️ Open http://localhost:8080 for web interface")
            print("🛑 Press Ctrl+C to stop")

            while self.running:
                import time
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Shutting down Discord Commander System...")
            self.stop()

        return True

    def stop(self):
        """Stop the Discord Commander system."""
        self.running = False

        if self.controller:
            self.controller.stop()

        if self.bot:
            asyncio.run(self.bot.stop())

        print("✅ Discord Commander System stopped")


def main():
    """Main function."""
    launcher = DiscordCommanderLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
