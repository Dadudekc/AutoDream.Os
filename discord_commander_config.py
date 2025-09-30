#!/usr/bin/env python3
"""
Discord Commander Configuration Module
=====================================

Configuration management for the Discord Commander bot system.
Handles configuration validation and status reporting.

🐝 WE ARE SWARM - Discord Commander Configuration Active!
"""

import logging
from typing import Optional

from discord_bot_config import config as discord_config


class DiscordCommanderConfig:
    """Discord Commander configuration manager."""

    def __init__(self, logger: logging.Logger):
        """Initialize Discord Commander configuration."""
        self.logger = logger

    def check_configuration(self) -> bool:
        """Check Discord Commander configuration."""
        try:
            # Check Discord bot token
            if not discord_config.get_bot_token():
                self.logger.error("❌ Discord bot token not configured!")
                self.logger.error("   Set DISCORD_BOT_TOKEN environment variable")
                return False

            # Check Discord channel ID
            if not discord_config.get_channel_id():
                self.logger.warning("⚠️  Discord channel ID not configured!")
                self.logger.warning("   Set DISCORD_CHANNEL_ID environment variable")

            # Print configuration status
            discord_config.print_config_status()

            return True

        except Exception as e:
            self.logger.error(f"❌ Error checking configuration: {e}")
            return False

    def get_bot_token(self) -> Optional[str]:
        """Get Discord bot token."""
        return discord_config.get_bot_token()

    def get_channel_id(self) -> Optional[str]:
        """Get Discord channel ID."""
        return discord_config.get_channel_id()

    def is_configured(self) -> bool:
        """Check if configuration is valid."""
        return discord_config.is_configured()

    def get_config_status(self) -> dict:
        """Get configuration status."""
        return {
            "configuration_valid": self.is_configured(),
            "bot_token_configured": self.get_bot_token() is not None,
            "channel_configured": self.get_channel_id() is not None,
        }
