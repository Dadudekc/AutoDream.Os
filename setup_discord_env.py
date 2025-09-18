#!/usr/bin/env python3
"""
Setup Discord Environment Configuration
======================================

Simple script to set up Discord bot environment variables.
"""

import os
import sys

def setup_discord_environment():
    """Set up Discord bot environment variables."""
    
    # Discord Bot Configuration
    discord_config = {
        "DISCORD_BOT_TOKEN": "your_discord_bot_token_here",
        "DISCORD_CHANNEL_ID": "your_discord_channel_id_here", 
        "DISCORD_GUILD_ID": "your_discord_guild_id_here",
        
        # Agent-specific channels
        "DISCORD_CHANNEL_AGENT_1": "your_agent_1_channel_id",
        "DISCORD_CHANNEL_AGENT_2": "your_agent_2_channel_id", 
        "DISCORD_CHANNEL_AGENT_3": "1387515009621430392",  # From the error message
        "DISCORD_CHANNEL_AGENT_4": "your_agent_4_channel_id",
        "DISCORD_CHANNEL_AGENT_5": "your_agent_5_channel_id",
        "DISCORD_CHANNEL_AGENT_6": "your_agent_6_channel_id",
        "DISCORD_CHANNEL_AGENT_7": "your_agent_7_channel_id",
        "DISCORD_CHANNEL_AGENT_8": "your_agent_8_channel_id",
        
        # Webhook configuration
        "WEBHOOK_BASE_URL": "",
        "WEBHOOK_SECRET": "",
        
        # Security configuration
        "SECURITY_ENABLED": "true",
        "RATE_LIMIT_ENABLED": "true",
        "MAX_REQUESTS_PER_MINUTE": "60"
    }
    
    # Set environment variables
    for key, value in discord_config.items():
        os.environ[key] = value
        print(f"Set {key} = {value}")
    
    print("\n✅ Discord environment variables configured!")
    print("⚠️  Remember to replace placeholder values with actual Discord bot tokens and channel IDs")
    
    return True

if __name__ == "__main__":
    setup_discord_environment()
