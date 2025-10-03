#!/usr/bin/env python3
"""
Discord Bot Configuration
========================

Centralized configuration for Discord bot to avoid environment parsing issues.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

class DiscordBotConfig:
    """Centralized Discord bot configuration."""
    
    def __init__(self):
        """Initialize Discord bot configuration."""
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load Discord bot configuration."""
        return {
            # Discord Bot Configuration
            "discord_bot_token": os.getenv("DISCORD_BOT_TOKEN", "your_discord_bot_token_here"),
            "discord_channel_id": os.getenv("DISCORD_CHANNEL_ID", "your_discord_channel_id_here"),
            "discord_guild_id": os.getenv("DISCORD_GUILD_ID", "your_discord_guild_id_here"),
            
            # Agent-specific channels
            "agent_channels": {
                "Agent-1": os.getenv("DISCORD_CHANNEL_AGENT_1", "your_agent_1_channel_id"),
                "Agent-2": os.getenv("DISCORD_CHANNEL_AGENT_2", "your_agent_2_channel_id"),
                "Agent-3": os.getenv("DISCORD_CHANNEL_AGENT_3", "1387515009621430392"),
                "Agent-4": os.getenv("DISCORD_CHANNEL_AGENT_4", "your_agent_4_channel_id"),
                "Agent-5": os.getenv("DISCORD_CHANNEL_AGENT_5", "your_agent_5_channel_id"),
                "Agent-6": os.getenv("DISCORD_CHANNEL_AGENT_6", "your_agent_6_channel_id"),
                "Agent-7": os.getenv("DISCORD_CHANNEL_AGENT_7", "your_agent_7_channel_id"),
                "Agent-8": os.getenv("DISCORD_CHANNEL_AGENT_8", "your_agent_8_channel_id"),
            },
            
            # Webhook configuration
            "webhook_base_url": os.getenv("WEBHOOK_BASE_URL", ""),
            "webhook_secret": os.getenv("WEBHOOK_SECRET", ""),
            
            # Security configuration
            "security_enabled": os.getenv("SECURITY_ENABLED", "true").lower() == "true",
            "rate_limit_enabled": os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            "max_requests_per_minute": int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")),
            
            # App configuration
            "app_name": os.getenv("APP_NAME", "AgentCellphoneV2"),
            "app_env": os.getenv("APP_ENV", "development"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
        }
    
    def get_bot_token(self) -> Optional[str]:
        """Get Discord bot token."""
        token = self.config["discord_bot_token"]
        if token and token != "your_discord_bot_token_here":
            return token
        return None
    
    def get_channel_id(self) -> Optional[str]:
        """Get main Discord channel ID."""
        channel_id = self.config["discord_channel_id"]
        if channel_id and channel_id != "your_discord_channel_id_here":
            return channel_id
        return None
    
    def get_agent_channel_id(self, agent_id: str) -> Optional[str]:
        """Get Discord channel ID for specific agent."""
        return self.config["agent_channels"].get(agent_id)
    
    def get_guild_id(self) -> Optional[str]:
        """Get Discord guild (server) ID."""
        guild_id = self.config["discord_guild_id"]
        if guild_id and guild_id != "your_discord_guild_id_here":
            return guild_id
        return None
    
    def is_configured(self) -> bool:
        """Check if Discord bot is properly configured."""
        return (
            self.get_bot_token() is not None and
            self.get_channel_id() is not None and
            self.get_guild_id() is not None
        )
    
    def get_config_status(self) -> Dict[str, Any]:
        """Get configuration status."""
        return {
            "bot_token_configured": self.get_bot_token() is not None,
            "channel_id_configured": self.get_channel_id() is not None,
            "guild_id_configured": self.get_guild_id() is not None,
            "agent_channels_configured": {
                agent: self.get_agent_channel_id(agent) is not None
                for agent in self.config["agent_channels"]
            },
            "webhook_configured": bool(self.config["webhook_base_url"]),
            "security_enabled": self.config["security_enabled"],
            "rate_limit_enabled": self.config["rate_limit_enabled"],
        }
    
    def print_config_status(self):
        """Print configuration status."""
        print("🔧 Discord Bot Configuration Status")
        print("=" * 50)
        
        status = self.get_config_status()
        
        print(f"Bot Token: {'✅ Configured' if status['bot_token_configured'] else '❌ Not configured'}")
        print(f"Channel ID: {'✅ Configured' if status['channel_id_configured'] else '❌ Not configured'}")
        print(f"Guild ID: {'✅ Configured' if status['guild_id_configured'] else '❌ Not configured'}")
        print(f"Webhook: {'✅ Configured' if status['webhook_configured'] else '❌ Not configured'}")
        print(f"Security: {'✅ Enabled' if status['security_enabled'] else '❌ Disabled'}")
        print(f"Rate Limit: {'✅ Enabled' if status['rate_limit_enabled'] else '❌ Disabled'}")
        
        print("\nAgent Channels:")
        for agent, configured in status["agent_channels_configured"].items():
            status_icon = "✅" if configured else "❌"
            print(f"  {agent}: {status_icon} {'Configured' if configured else 'Not configured'}")
        
        if not self.is_configured():
            print("\n⚠️  Configuration Issues:")
            if not status['bot_token_configured']:
                print("  - Discord bot token not set (DISCORD_BOT_TOKEN)")
            if not status['channel_id_configured']:
                print("  - Discord channel ID not set (DISCORD_CHANNEL_ID)")
            if not status['guild_id_configured']:
                print("  - Discord guild ID not set (DISCORD_GUILD_ID)")
        
        return self.is_configured()

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
        print("3. Set DISCORD_GUILD_ID environment variable")
        print("4. Set agent-specific channel IDs if needed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
