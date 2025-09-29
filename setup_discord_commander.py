#!/usr/bin/env python3
"""
Discord Commander Setup Script
==============================

This script helps you set up the Discord Commander environment variables.
It will guide you through the process of configuring your Discord bot.

🐝 WE ARE SWARM - Discord Commander Setup
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from discord_bot_config import config as discord_config
except ImportError:
    print("❌ Error: Cannot import discord_bot_config")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


class DiscordCommanderSetup:
    """Setup wizard for Discord Commander."""

    def __init__(self):
        """Initialize setup wizard."""
        self.env_file = Path(__file__).parent / ".env"
        self.template_file = Path(__file__).parent / ".env.template"
        self.env_vars = {}

    def welcome_message(self):
        """Display welcome message."""
        print("🐝 Discord Commander Setup Wizard - 5-Agent Mode")
        print("=" * 50)
        print("WE ARE SWARM - Discord Commander Configuration")
        print("5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
        print("=" * 50)
        print()
        print("This wizard will help you configure your Discord Commander.")
        print("You'll need to set up a Discord bot first:")
        print()
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a new application")
        print("3. Go to the 'Bot' section and create a bot")
        print("4. Copy the bot token")
        print("5. Go to OAuth2 -> URL Generator")
        print("6. Select 'bot' scope and required permissions")
        print("7. Copy the generated URL and visit it")
        print("8. Add the bot to your Discord server")
        print()
        print("💡 5-Agent Mode: Only Agent-4, Agent-5, Agent-6, Agent-7, Agent-8 are active")
        print()
        print("Press Enter to continue...")
        input()

    def get_discord_bot_token(self) -> str:
        """Get Discord bot token from user."""
        print("\n🤖 Discord Bot Token Setup")
        print("-" * 30)

        while True:
            token = input("Enter your Discord bot token (or press Enter to skip): ").strip()

            if not token:
                print("⚠️  Skipping Discord bot token setup")
                return ""

            if len(token) < 50:
                print("❌ Invalid token format. Discord bot tokens are usually 59 characters long.")
                continue

            # Basic validation - Discord bot tokens start with specific prefixes
            if not (token.startswith("M") or token.startswith("N") or token.startswith("Bot ")):
                print("❌ This doesn't look like a valid Discord bot token.")
                print("💡 Discord bot tokens usually start with 'M' or 'N', or 'Bot '")
                continue

            print("✅ Discord bot token accepted!")
            return token

    def get_channel_id(self, channel_name: str, required: bool = False) -> str:
        """Get Discord channel ID from user."""
        print(f"\n📺 {channel_name} Channel Setup")
        print("-" * 30)

        if required:
            print(f"💡 Right-click the {channel_name.lower()} channel in Discord")
            print("   Select 'Copy ID' (you may need to enable Developer Mode first)")
        else:
            print("   (Optional - press Enter to skip)")

        while True:
            channel_id = input(f"Enter {channel_name.lower()} channel ID: ").strip()

            if not channel_id:
                if required:
                    print(f"⚠️  {channel_name} channel ID is required!")
                    continue
                else:
                    print(f"⚠️  Skipping {channel_name.lower()} channel setup")
                    return ""

            if not channel_id.isdigit():
                print("❌ Channel ID must be a number (Discord snowflake ID)")
                continue

            if len(channel_id) < 15:
                print("❌ Invalid channel ID format")
                continue

            print(f"✅ {channel_name} channel ID accepted!")
            return channel_id

    def get_agent_channel_ids(self) -> dict[str, str]:
        """Get Discord channel IDs for each agent."""
        print("\n👥 Agent-Specific Channels Setup - 5-Agent Mode")
        print("-" * 30)
        print("💡 5-Agent Mode: Only Agent-4, Agent-5, Agent-6, Agent-7, Agent-8 are active")
        print("💡 You can create separate channels for each agent or use the same channel")
        print("   Press Enter to use the main channel for an agent")

        agent_channels = {}
        agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent in agents:
            channel_id = self.get_channel_id(f"{agent} Channel", required=False)
            if channel_id:
                agent_channels[agent] = channel_id

        return agent_channels

    def create_env_file(self):
        """Create .env file with configuration."""
        print("\n📝 Creating .env configuration file...")
        print("-" * 30)

        # Get all configuration values
        self.env_vars = {
            "DISCORD_BOT_TOKEN": self.get_discord_bot_token(),
            "DISCORD_CHANNEL_ID": self.get_channel_id("Main Channel", required=True),
            "DISCORD_GUILD_ID": self.get_channel_id("Server/Guild", required=False),
        }

        # Get agent channels
        agent_channels = self.get_agent_channel_ids()
        self.env_vars.update(
            {
                f"DISCORD_CHANNEL_{agent.upper().replace('-', '_')}": channel_id
                for agent, channel_id in agent_channels.items()
            }
        )

        # Add default configuration
        self.env_vars.update(
            {
                "DISCORD_COMMAND_PREFIX": "!",
                "DISCORD_BOT_STATUS": "🐝 WE ARE SWARM - Agent Coordination Active",
                "DISCORD_BOT_ACTIVITY_TYPE": "watching",
                "DISCORD_RATE_LIMIT_ENABLED": "true",
                "DISCORD_MAX_REQUESTS_PER_MINUTE": "60",
                "DISCORD_COMMANDER_LOG_LEVEL": "INFO",
                "DISCORD_COMMANDER_AUTO_START": "true",
                "DISCORD_COMMANDER_HEALTH_CHECK_INTERVAL": "30",
                "APP_NAME": "AgentCellphoneV2",
                "APP_ENV": "development",
                "LOG_LEVEL": "INFO",
                "DEBUG_MODE": "false",
            }
        )

        # Write .env file
        try:
            with open(self.env_file, "w") as f:
                f.write(
                    "# =============================================================================\n"
                )
                f.write("# Agent Cellphone V2 — Discord Commander Environment Configuration\n")
                f.write(
                    "# =============================================================================\n"
                )
                f.write("# Generated by setup_discord_commander.py\n")
                f.write("# Edit this file to modify your Discord Commander configuration\n")
                f.write("\n")

                for key, value in self.env_vars.items():
                    if value:  # Only write non-empty values
                        f.write(f"{key}={value}\n")

                f.write(
                    "\n# =============================================================================\n"
                )
                f.write("# Discord Commander is now configured!\n")
                f.write("# Run: python discord_commander.py\n")
                f.write(
                    "# =============================================================================\n"
                )

            print(f"✅ Configuration saved to {self.env_file}")
            print("🎉 Discord Commander setup completed!")

        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False

        return True

    def show_configuration_summary(self):
        """Show configuration summary."""
        print("\n📊 Configuration Summary")
        print("-" * 30)

        status = discord_config.get_config_status()

        print(
            f"Bot Token: {'✅ Configured' if status['bot_token_configured'] else '❌ Not configured'}"
        )
        print(
            f"Channel ID: {'✅ Configured' if status['channel_id_configured'] else '❌ Not configured'}"
        )

        print("\nAgent Channels:")
        for agent, configured in status["agent_channels_configured"].items():
            status_icon = "✅" if configured else "❌"
            print(f"  {agent}: {status_icon} {'Configured' if configured else 'Not configured'}")

    def show_next_steps(self):
        """Show next steps after setup."""
        print("\n🚀 Next Steps")
        print("-" * 30)
        print("1. Make sure your Discord bot is added to your server")
        print("2. Run the Discord Commander:")
        print("   python discord_commander.py")
        print("3. Check the Discord server - your bot should appear online!")
        print("4. Test the bot with: @DiscordCommander help")
        print()
        print("🐝 WE ARE SWARM - Discord Commander Ready!")


def main():
    """Main setup function."""
    print("Welcome to Discord Commander Setup!")
    print("=" * 50)

    # Check if already configured
    if discord_config.is_configured():
        print("✅ Discord Commander is already configured!")
        discord_config.print_config_status()
        print("\nWould you like to reconfigure? (y/n): ")
        if input().lower().startswith("n"):
            return

    # Run setup wizard
    setup = DiscordCommanderSetup()
    setup.welcome_message()
    success = setup.create_env_file()

    if success:
        setup.show_configuration_summary()
        setup.show_next_steps()

    print("\n👋 Setup complete! WE ARE SWARM!")


if __name__ == "__main__":
    main()
