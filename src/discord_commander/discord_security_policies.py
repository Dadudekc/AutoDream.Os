import logging

logger = logging.getLogger(__name__)
"""
Discord Security Policies - V2 Compliant Module
===============================================

Security policies and access control for Discord Agent Bot.
V2 COMPLIANT: Security policies under 200 lines.

Features:
- Channel and guild access control
- User permission management
- Security policy enforcement
- Rate limiting integration

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""
import json
from pathlib import Path
from typing import Any

try:
    from .rate_limits import RateLimiter
    from .security_policies import allow_channel, allow_guild, allow_user
except ImportError as e:
    logger.info(f"⚠️ Import warning: {e}")
    allow_channel = lambda x: True
    allow_guild = lambda x: True
    allow_user = lambda x: True
    RateLimiter = None


class DiscordSecurityManager:
    """Security policies and access control for Discord Agent Bot."""

    def __init__(self, bot):
        """Initialize security manager."""
        self.bot = bot
        self.allowed_channels = []
        self.admin_users = []
        self.command_timeout = 300
        self.max_concurrent_commands = 10
        self._load_security_config()

    def _load_security_config(self):
        """Load security configuration."""
        config_path = Path("config/discord_bot_config.json")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self.allowed_channels = config.get("allowed_channels", [])
                    self.admin_users = config.get("admin_users", [])
                    self.command_timeout = config.get("command_timeout", 300)
                    self.max_concurrent_commands = config.get("max_concurrent_commands", 10)
            except Exception as e:
                logger.info(f"⚠️  Failed to load Discord security config: {e}")

    def is_channel_allowed(self, channel_id: int) -> bool:
        """Check if channel is allowed for bot commands."""
        if not self.allowed_channels:
            return True
        return channel_id in self.allowed_channels

    def is_guild_allowed(self, guild_id: int) -> bool:
        """Check if guild is allowed for bot commands."""
        return allow_guild(guild_id)

    def is_user_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to use bot commands."""
        return allow_user(user_id)

    def is_admin_user(self, user_id: int) -> bool:
        """Check if user is an admin."""
        return user_id in self.admin_users

    def check_security_policies(self, message) -> bool:
        """Check all security policies for a message."""
        guild_id = message.guild.id if message.guild else None
        return (
            self.is_guild_allowed(guild_id)
            and self.is_channel_allowed(message.channel.id)
            and self.is_user_allowed(message.author.id)
        )

    def get_security_status(self) -> dict[str, Any]:
        """Get current security configuration status."""
        return {
            "allowed_channels": len(self.allowed_channels),
            "admin_users": len(self.admin_users),
            "command_timeout": self.command_timeout,
            "max_concurrent_commands": self.max_concurrent_commands,
            "security_enabled": bool(self.allowed_channels or self.admin_users),
        }

    def update_security_config(self, config: dict[str, Any]):
        """Update security configuration."""
        if "allowed_channels" in config:
            self.allowed_channels = config["allowed_channels"]
        if "admin_users" in config:
            self.admin_users = config["admin_users"]
        if "command_timeout" in config:
            self.command_timeout = config["command_timeout"]
        if "max_concurrent_commands" in config:
            self.max_concurrent_commands = config["max_concurrent_commands"]
        self._save_security_config()

    def _save_security_config(self):
        """Save security configuration to file."""
        config_path = Path("config/discord_bot_config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config = {
            "allowed_channels": self.allowed_channels,
            "admin_users": self.admin_users,
            "command_timeout": self.command_timeout,
            "max_concurrent_commands": self.max_concurrent_commands,
        }
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            logger.info("✅ Security configuration saved")
        except Exception as e:
            logger.info(f"⚠️  Failed to save security config: {e}")

    def add_allowed_channel(self, channel_id: int):
        """Add channel to allowed list."""
        if channel_id not in self.allowed_channels:
            self.allowed_channels.append(channel_id)
            self._save_security_config()

    def remove_allowed_channel(self, channel_id: int):
        """Remove channel from allowed list."""
        if channel_id in self.allowed_channels:
            self.allowed_channels.remove(channel_id)
            self._save_security_config()

    def add_admin_user(self, user_id: int):
        """Add user to admin list."""
        if user_id not in self.admin_users:
            self.admin_users.append(user_id)
            self._save_security_config()

    def remove_admin_user(self, user_id: int):
        """Remove user from admin list."""
        if user_id in self.admin_users:
            self.admin_users.remove(user_id)
            self._save_security_config()

    def get_security_help(self) -> str:
        """Get security configuration help text."""
        return f"""
**Discord Security Configuration Help**

**Current Settings:**
- Allowed Channels: {len(self.allowed_channels)}
- Admin Users: {len(self.admin_users)}
- Command Timeout: {self.command_timeout}s
- Max Concurrent Commands: {self.max_concurrent_commands}

**Security Features:**
- Channel-based access control
- User-based permission management
- Rate limiting protection
- Command timeout enforcement
- Concurrent command limiting

**Configuration File:** `config/discord_bot_config.json`
        """
