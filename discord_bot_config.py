#!/usr/bin/env python3
"""
Discord Bot Configuration
========================

Centralized configuration for Discord bot to avoid environment parsing issues.
"""

import sys
from typing import Any
from discord_bot_config_core import DiscordBotConfigCore


class DiscordBotConfig:
    """Centralized Discord bot configuration."""

    def __init__(self):
        """Initialize Discord bot configuration."""
        self.core = DiscordBotConfigCore()

    def get_bot_token(self) -> str | None:
        """Get Discord bot token."""
        return self.core.get_bot_token()

    def get_channel_id(self) -> str | None:
        """Get main Discord channel ID."""
        return self.core.get_channel_id()

    def get_agent_channel_id(self, agent_id: str) -> str | None:
        """Get Discord channel ID for specific agent."""
        return self.core.get_agent_channel_id(agent_id)

    def is_configured(self) -> bool:
        """Check if Discord bot is properly configured."""
        return self.core.is_configured()

    def get_config_status(self) -> dict[str, Any]:
        """Get configuration status."""
        return self.core.get_config_status()

    def print_config_status(self):
        """Print configuration status."""
        return self.core.print_config_status()


# Global configuration instance
config = DiscordBotConfig()


def main():
    """Main function to test configuration."""
    print("🤖 Discord Bot Configuration Test")
    print("=" * 50)

    is_configured = config.print_config_status()

    if is_configured:
        print("\n✅ Discord bot is properly configured!")
        return 0
    else:
        print("\n❌ Discord bot configuration incomplete!")
        print("\n📝 To fix configuration issues:")
        print("1. Set DISCORD_BOT_TOKEN environment variable")
        print("2. Set DISCORD_CHANNEL_ID environment variable")
        print("3. Set agent-specific channel IDs if needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())