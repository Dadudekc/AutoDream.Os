#!/usr/bin/env python3
"""
Discord Commander Core Configuration
====================================

Core configuration for Discord bot operations.

V2 Compliance: ≤400 lines, single responsibility
"""

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DiscordConfig:
    """Discord bot configuration."""

    bot_token: str | None = None
    command_prefix: str = "!"
    channel_id: str | None = None

    def __post_init__(self):
        """Load configuration from environment variables."""
        if self.bot_token is None:
            self.bot_token = os.getenv("DISCORD_BOT_TOKEN")

        if self.channel_id is None:
            self.channel_id = os.getenv("DISCORD_CHANNEL_ID")

    def validate(self) -> list[str]:
        """
        Validate configuration.

        Returns:
            List of validation error messages (empty if valid)
        """
        issues = []

        if not self.bot_token:
            issues.append("DISCORD_BOT_TOKEN environment variable not set")

        if not self.channel_id:
            logger.warning("DISCORD_CHANNEL_ID not set - bot will respond in all channels")

        return issues

    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return len(self.validate()) == 0
