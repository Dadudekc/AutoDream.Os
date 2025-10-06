#!/usr/bin/env python3
"""
Discord Devlog Service - Configuration
=====================================

Configuration and initialization for Discord devlog service.
V2 Compliant: ≤400 lines, focused configuration management.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import logging
import os
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DiscordDevlogConfig:
    """Configuration management for Discord devlog service."""

    def __init__(self):
        """Initialize Discord devlog configuration."""
        self.bot_token: Optional[str] = None
        self.channel_id: Optional[int] = None
        self.guild_id: Optional[int] = None
        self.webhook_url: Optional[str] = None
        self.agent_channels: Dict[str, int] = {}
        self.agent_webhooks: Dict[str, str] = {}
        
        # Load configuration
        self._load_config()

    def _load_config(self) -> None:
        """Load Discord configuration from environment variables."""
        try:
            # Load from .env file if available
            env_path = Path(__file__).parent.parent.parent.parent / ".env"
            if env_path.exists():
                from dotenv import load_dotenv
                load_dotenv(env_path)

            # Load Discord configuration
            self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
            self.channel_id = self._parse_int(os.getenv("DISCORD_CHANNEL_ID"))
            self.guild_id = self._parse_int(os.getenv("DISCORD_GUILD_ID"))
            self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

            # Load agent-specific channels
            self._load_agent_channels()
            
            # Load agent-specific webhooks
            self._load_agent_webhooks()

            logger.info("Discord configuration loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load Discord configuration: {e}")

    def _parse_int(self, value: Optional[str]) -> Optional[int]:
        """Parse string to integer safely."""
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Invalid integer value: {value}")
            return None

    def _load_agent_channels(self) -> None:
        """Load agent-specific channel mappings."""
        try:
            # Agent-1: Infrastructure Specialist
            if os.getenv("DISCORD_AGENT1_CHANNEL_ID"):
                self.agent_channels["Agent-1"] = int(os.getenv("DISCORD_AGENT1_CHANNEL_ID"))
            
            # Agent-2: Data Processing Expert
            if os.getenv("DISCORD_AGENT2_CHANNEL_ID"):
                self.agent_channels["Agent-2"] = int(os.getenv("DISCORD_AGENT2_CHANNEL_ID"))
            
            # Agent-3: Quality Assurance Lead
            if os.getenv("DISCORD_AGENT3_CHANNEL_ID"):
                self.agent_channels["Agent-3"] = int(os.getenv("DISCORD_AGENT3_CHANNEL_ID"))
            
            # Agent-4: Captain (Strategic Oversight)
            if os.getenv("DISCORD_AGENT4_CHANNEL_ID"):
                self.agent_channels["Agent-4"] = int(os.getenv("DISCORD_AGENT4_CHANNEL_ID"))
            
            # Agent-5: Coordinator
            if os.getenv("DISCORD_AGENT5_CHANNEL_ID"):
                self.agent_channels["Agent-5"] = int(os.getenv("DISCORD_AGENT5_CHANNEL_ID"))
            
            # Agent-6: Quality Assurance
            if os.getenv("DISCORD_AGENT6_CHANNEL_ID"):
                self.agent_channels["Agent-6"] = int(os.getenv("DISCORD_AGENT6_CHANNEL_ID"))
            
            # Agent-7: Implementation Specialist
            if os.getenv("DISCORD_AGENT7_CHANNEL_ID"):
                self.agent_channels["Agent-7"] = int(os.getenv("DISCORD_AGENT7_CHANNEL_ID"))
            
            # Agent-8: Integration Specialist
            if os.getenv("DISCORD_AGENT8_CHANNEL_ID"):
                self.agent_channels["Agent-8"] = int(os.getenv("DISCORD_AGENT8_CHANNEL_ID"))

            logger.info(f"Loaded {len(self.agent_channels)} agent-specific channels")

        except Exception as e:
            logger.error(f"Failed to load agent channels: {e}")

    def _load_agent_webhooks(self) -> None:
        """Load agent-specific webhook URLs."""
        try:
            # Agent-1: Infrastructure Specialist
            if os.getenv("DISCORD_AGENT1_WEBHOOK_URL"):
                self.agent_webhooks["Agent-1"] = os.getenv("DISCORD_AGENT1_WEBHOOK_URL")
            
            # Agent-2: Data Processing Expert
            if os.getenv("DISCORD_AGENT2_WEBHOOK_URL"):
                self.agent_webhooks["Agent-2"] = os.getenv("DISCORD_AGENT2_WEBHOOK_URL")
            
            # Agent-3: Quality Assurance Lead
            if os.getenv("DISCORD_AGENT3_WEBHOOK_URL"):
                self.agent_webhooks["Agent-3"] = os.getenv("DISCORD_AGENT3_WEBHOOK_URL")
            
            # Agent-4: Captain (Strategic Oversight)
            if os.getenv("DISCORD_AGENT4_WEBHOOK_URL"):
                self.agent_webhooks["Agent-4"] = os.getenv("DISCORD_AGENT4_WEBHOOK_URL")
            
            # Agent-5: Coordinator
            if os.getenv("DISCORD_AGENT5_WEBHOOK_URL"):
                self.agent_webhooks["Agent-5"] = os.getenv("DISCORD_AGENT5_WEBHOOK_URL")
            
            # Agent-6: Quality Assurance
            if os.getenv("DISCORD_AGENT6_WEBHOOK_URL"):
                self.agent_webhooks["Agent-6"] = os.getenv("DISCORD_AGENT6_WEBHOOK_URL")
            
            # Agent-7: Implementation Specialist
            if os.getenv("DISCORD_AGENT7_WEBHOOK_URL"):
                self.agent_webhooks["Agent-7"] = os.getenv("DISCORD_AGENT7_WEBHOOK_URL")
            
            # Agent-8: Integration Specialist
            if os.getenv("DISCORD_AGENT8_WEBHOOK_URL"):
                self.agent_webhooks["Agent-8"] = os.getenv("DISCORD_AGENT8_WEBHOOK_URL")

            logger.info(f"Loaded {len(self.agent_webhooks)} agent-specific webhooks")

        except Exception as e:
            logger.error(f"Failed to load agent webhooks: {e}")

    def is_configured(self) -> bool:
        """Check if Discord is properly configured."""
        return bool(self.bot_token or self.webhook_url)

    def get_config_summary(self) -> Dict[str, any]:
        """Get configuration summary."""
        return {
            "bot_token_configured": bool(self.bot_token),
            "channel_id_configured": bool(self.channel_id),
            "guild_id_configured": bool(self.guild_id),
            "webhook_url_configured": bool(self.webhook_url),
            "agent_channels_count": len(self.agent_channels),
            "agent_webhooks_count": len(self.agent_webhooks),
            "is_configured": self.is_configured()
        }


def create_discord_config() -> DiscordDevlogConfig:
    """Create Discord devlog configuration."""
    return DiscordDevlogConfig()

