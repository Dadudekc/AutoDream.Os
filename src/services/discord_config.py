#!/usr/bin/env python3
"""
Discord Bot Configuration - V2 Compliant
=========================================

Centralized configuration for the unified Discord bot.
Handles environment variables, channel mappings, and bot settings.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

# V2 Compliance: File under 400 lines, functions under 30 lines


class DiscordBotConfig:
    """Centralized Discord bot configuration."""

    def __init__(self):
        """Initialize Discord bot configuration."""
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Load Discord bot configuration."""
        return {
            # Discord Bot Configuration
            'discord_bot_token': os.getenv('DISCORD_BOT_TOKEN', ''),
            'discord_channel_id': os.getenv('DISCORD_CHANNEL_ID', ''),
            'discord_guild_id': os.getenv('DISCORD_GUILD_ID', ''),

            # Agent-specific channels
            'agent_channels': {
                'Agent-1': os.getenv('DISCORD_CHANNEL_AGENT_1', ''),
                'Agent-2': os.getenv('DISCORD_CHANNEL_AGENT_2', ''),
                'Agent-3': os.getenv('DISCORD_CHANNEL_AGENT_3', '1387515009621430392'),
                'Agent-4': os.getenv('DISCORD_CHANNEL_AGENT_4', ''),
                'Agent-5': os.getenv('DISCORD_CHANNEL_AGENT_5', ''),
                'Agent-6': os.getenv('DISCORD_CHANNEL_AGENT_6', ''),
                'Agent-7': os.getenv('DISCORD_CHANNEL_AGENT_7', ''),
                'Agent-8': os.getenv('DISCORD_CHANNEL_AGENT_8', ''),
            },

            # Bot settings
            'command_prefix': os.getenv('DISCORD_COMMAND_PREFIX', '!'),
            'bot_name': os.getenv('DISCORD_BOT_NAME', 'UnifiedDiscordBot'),
            'bot_status': os.getenv('DISCORD_BOT_STATUS', 'Online'),
            'activity_type': os.getenv('DISCORD_ACTIVITY_TYPE', 'watching'),
            'activity_text': os.getenv('DISCORD_ACTIVITY_TEXT', 'Swarm Operations'),

            # Security configuration
            'security_enabled': os.getenv('SECURITY_ENABLED', 'true').lower() == 'true',
            'rate_limit_enabled': os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true',
            'max_requests_per_minute': int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60')),

            # Performance configuration
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
            'performance_monitoring': os.getenv('PERFORMANCE_MONITORING', 'true').lower() == 'true',

            # Feature flags
            'enable_slash_commands': os.getenv('ENABLE_SLASH_COMMANDS', 'true').lower() == 'true',
            'enable_prefix_commands': os.getenv('ENABLE_PREFIX_COMMANDS', 'true').lower() == 'true',
            'enable_agent_commands': os.getenv('ENABLE_AGENT_COMMANDS', 'true').lower() == 'true',
            'enable_messaging_commands': os.getenv('ENABLE_MESSAGING_COMMANDS', 'true').lower() == 'true',
            'enable_system_commands': os.getenv('ENABLE_SYSTEM_COMMANDS', 'true').lower() == 'true',

            # Timeout configurations
            'command_timeout': int(os.getenv('COMMAND_TIMEOUT', '30')),
            'response_timeout': int(os.getenv('RESPONSE_TIMEOUT', '60')),
            'connection_timeout': int(os.getenv('CONNECTION_TIMEOUT', '30')),
        }

    def get_bot_token(self) -> Optional[str]:
        """Get Discord bot token."""
        token = self.config['discord_bot_token']
        return token if token else None

    def get_channel_id(self) -> Optional[str]:
        """Get main Discord channel ID."""
        channel_id = self.config['discord_channel_id']
        return channel_id if channel_id else None

    def get_guild_id(self) -> Optional[str]:
        """Get Discord guild ID."""
        guild_id = self.config['discord_guild_id']
        return guild_id if guild_id else None

    def get_agent_channel_id(self, agent_id: str) -> Optional[str]:
        """Get Discord channel ID for specific agent."""
        return self.config['agent_channels'].get(agent_id)

    def get_command_prefix(self) -> str:
        """Get command prefix."""
        return self.config['command_prefix']

    def get_bot_settings(self) -> Dict[str, str]:
        """Get bot settings."""
        return {
            'name': self.config['bot_name'],
            'status': self.config['bot_status'],
            'activity_type': self.config['activity_type'],
            'activity_text': self.config['activity_text'],
        }

    def is_configured(self) -> bool:
        """Check if Discord bot is properly configured."""
        return (
            self.get_bot_token() is not None and
            self.get_channel_id() is not None
        )

    def get_config_status(self) -> Dict[str, Any]:
        """Get configuration status."""
        return {
            'bot_token_configured': self.get_bot_token() is not None,
            'channel_id_configured': self.get_channel_id() is not None,
            'guild_id_configured': self.get_guild_id() is not None,
            'agent_channels_configured': {
                agent: self.get_agent_channel_id(agent) is not None
                for agent in self.config['agent_channels']
            },
            'features_enabled': {
                'slash_commands': self.config['enable_slash_commands'],
                'prefix_commands': self.config['enable_prefix_commands'],
                'agent_commands': self.config['enable_agent_commands'],
                'messaging_commands': self.config['enable_messaging_commands'],
                'system_commands': self.config['enable_system_commands'],
            },
            'security_enabled': self.config['security_enabled'],
            'rate_limit_enabled': self.config['rate_limit_enabled'],
            'debug_mode': self.config['debug_mode'],
        }

    def print_config_status(self) -> bool:
        """Print configuration status."""
        print("🔧 Unified Discord Bot Configuration Status")
        print("=" * 50)

        status = self.get_config_status()

        print(f"Bot Token: {'✅ Configured' if status['bot_token_configured'] else '❌ Not configured'}")
        print(f"Channel ID: {'✅ Configured' if status['channel_id_configured'] else '❌ Not configured'}")
        print(f"Guild ID: {'✅ Configured' if status['guild_id_configured'] else '❌ Not configured'}")
        print(f"Security: {'✅ Enabled' if status['security_enabled'] else '❌ Disabled'}")
        print(f"Rate Limit: {'✅ Enabled' if status['rate_limit_enabled'] else '❌ Disabled'}")
        print(f"Debug Mode: {'✅ Enabled' if status['debug_mode'] else '❌ Disabled'}")

        print("\nFeatures:")
        for feature, enabled in status['features_enabled'].items():
            status_icon = "✅" if enabled else "❌"
            print(f"  {feature.replace('_', ' ').title()}: {status_icon}")

        print("\nAgent Channels:")
        for agent, configured in status['agent_channels_configured'].items():
            status_icon = "✅" if configured else "❌"
            print(f"  {agent}: {status_icon} {'Configured' if configured else 'Not configured'}")

        if not self.is_configured():
            print("\n⚠️ Configuration Issues:")
            if not status['bot_token_configured']:
                print("  - Discord bot token not set (DISCORD_BOT_TOKEN)")
            if not status['channel_id_configured']:
                print("  - Discord channel ID not set (DISCORD_CHANNEL_ID)")

        return self.is_configured()

    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance settings."""
        return {
            'log_level': self.config['log_level'],
            'performance_monitoring': self.config['performance_monitoring'],
            'command_timeout': self.config['command_timeout'],
            'response_timeout': self.config['response_timeout'],
            'connection_timeout': self.config['connection_timeout'],
        }

    def get_security_settings(self) -> Dict[str, Any]:
        """Get security settings."""
        return {
            'security_enabled': self.config['security_enabled'],
            'rate_limit_enabled': self.config['rate_limit_enabled'],
            'max_requests_per_minute': self.config['max_requests_per_minute'],
        }

    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues."""
        issues = []

        if not self.get_bot_token():
            issues.append("Discord bot token not configured")

        if not self.get_channel_id():
            issues.append("Discord channel ID not configured")

        if not self.get_guild_id():
            issues.append("Discord guild ID not configured")

        if not any(self.config['agent_channels'].values()):
            issues.append("No agent channels configured")

        return issues

    def get_all_agent_channels(self) -> Dict[str, str]:
        """Get all agent channel mappings."""
        return {k: v for k, v in self.config['agent_channels'].items() if v}


# Global configuration instance
discord_config = DiscordBotConfig()


def main():
    """Main function to test configuration."""
    print("🤖 Unified Discord Bot Configuration Test")
    print("=" * 50)

    is_configured = discord_config.print_config_status()

    if is_configured:
        print("\n✅ Discord bot is properly configured!")
        return 0
    else:
        print("\n❌ Discord bot configuration incomplete!")
        print("\n📝 To fix configuration issues:")
        print("1. Set DISCORD_BOT_TOKEN environment variable")
        print("2. Set DISCORD_CHANNEL_ID environment variable")
        print("3. Set DISCORD_GUILD_ID environment variable")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())


