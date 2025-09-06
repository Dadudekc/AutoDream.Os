#!/usr/bin/env python3
"""
Discord Commander Configuration Manager
=======================================

Configuration management for the Discord commander system.
Handles config loading, channel initialization, and settings.
V2 COMPLIANT: Focused configuration management under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR CONFIGURATION MANAGER
@license MIT
"""

import logging
from typing import Dict, Any, List, Optional
import discord

from .discord_commander_models import (
    DiscordConfig,
    ChannelConfig,
    create_discord_config,
)


class DiscordConfigurationManager:
    """Configuration manager for Discord commander."""

    def __init__(self):
        """Initialize configuration manager."""
        self.logger = logging.getLogger(__name__)
        self._config: Optional[DiscordConfig] = None

    def load_config(self) -> DiscordConfig:
        """Load Discord commander configuration."""
        if self._config is None:
            self._config = self._load_discord_config()
        return self._config

    def _load_discord_config(self) -> DiscordConfig:
        """Load Discord configuration from unified config system."""
        try:
            # Import unified configuration utilities
            from ..core.unified_configuration_utility import get_unified_config
            from ..core.unified_utility import get_unified_utility

            config_manager = get_unified_config()
            discord_config = config_manager.get_discord_config()

            return create_discord_config(
                token=discord_config.token,
                guild_id=discord_config.guild_id,
                command_channel=discord_config.command_channel,
                status_channel=discord_config.status_channel,
                log_channel=discord_config.log_channel,
                admin_role=discord_config.admin_role,
                agent_roles=discord_config.agent_roles,
            )

        except Exception as e:
            self.logger.error(f"Failed to load Discord config: {e}")
            # Return default configuration
            return create_discord_config(
                token="",
                guild_id="",
                command_channel="swarm-commands",
                status_channel="swarm-status",
                log_channel="swarm-logs",
                admin_role="Captain",
                agent_roles=[f"Agent-{i}" for i in range(1, 9)],
            )

    def get_channel_configs(self) -> List[ChannelConfig]:
        """Get channel configurations."""
        config = self.load_config()

        return [
            ChannelConfig(
                name=config.command_channel,
                topic="Swarm command execution channel",
                channel_type="text",
            ),
            ChannelConfig(
                name=config.status_channel,
                topic="Swarm status and monitoring",
                channel_type="text",
            ),
            ChannelConfig(
                name=config.log_channel,
                topic="Swarm operation logs",
                channel_type="text",
            ),
        ]

    def get_guild_config(self) -> Dict[str, Any]:
        """Get guild configuration."""
        config = self.load_config()

        return {
            "guild_id": config.guild_id,
            "admin_role": config.admin_role,
            "agent_roles": config.agent_roles,
        }

    def get_bot_config(self) -> Dict[str, Any]:
        """Get bot configuration."""
        config = self.load_config()

        return {
            "token": config.token,
            "command_prefix": "!",
            "intents": self._get_default_intents(),
        }

    def _get_default_intents(self) -> discord.Intents:
        """Get default Discord intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.guild_messages = True
        intents.dm_messages = True
        return intents

    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues."""
        issues = []
        config = self.load_config()

        if not config.token:
            issues.append("Discord bot token is missing")

        if not config.guild_id:
            issues.append("Guild ID is missing")

        if not config.command_channel:
            issues.append("Command channel name is missing")

        if not config.status_channel:
            issues.append("Status channel name is missing")

        if not config.log_channel:
            issues.append("Log channel name is missing")

        if not config.admin_role:
            issues.append("Admin role is missing")

        if not config.agent_roles:
            issues.append("Agent roles are missing")

        return issues

    def update_config(self, **kwargs) -> None:
        """Update configuration values."""
        if self._config is None:
            self._config = self.load_config()

        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")

    def get_agent_validation_list(self) -> List[str]:
        """Get list of valid agent names."""
        return [f"Agent-{i}" for i in range(1, 9)]

    def is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid."""
        return agent in self.get_agent_validation_list()

    def get_channel_names(self) -> List[str]:
        """Get list of required channel names."""
        config = self.load_config()
        return [config.command_channel, config.status_channel, config.log_channel]

    def get_role_names(self) -> List[str]:
        """Get list of required role names."""
        config = self.load_config()
        roles = [config.admin_role]
        roles.extend(config.agent_roles)
        return roles


# Factory function for dependency injection
def create_discord_configuration_manager() -> DiscordConfigurationManager:
    """Factory function to create Discord configuration manager."""
    return DiscordConfigurationManager()


# Export for DI
__all__ = ["DiscordConfigurationManager", "create_discord_configuration_manager"]
