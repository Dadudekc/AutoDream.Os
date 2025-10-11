"""
Configuration Defaults and Validation Rules
===========================================
Default configurations and validation rules for core configuration manager.
Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-3's core_configuration_manager.py)
License: MIT
"""

from typing import Any


def get_default_discord_config(env_vars: dict[str, str]) -> dict[str, Any]:
    """Get default Discord configuration."""
    return {
        "type": "discord",
        "token": env_vars.get("DISCORD_TOKEN", ""),
        "guild_id": env_vars.get("DISCORD_GUILD_ID", ""),
        "command_channel": env_vars.get("DISCORD_COMMAND_CHANNEL", ""),
        "status_channel": env_vars.get("DISCORD_STATUS_CHANNEL", ""),
        "log_channel": env_vars.get("DISCORD_LOG_CHANNEL", ""),
        "enable_discord": (env_vars.get("DISCORD_ENABLE", "false").lower() == "true"),
    }


def get_default_app_config(env_vars: dict[str, str]) -> dict[str, Any]:
    """Get default application configuration."""
    return {
        "type": "application",
        "debug": env_vars.get("DEBUG", "false").lower() == "true",
        "log_level": env_vars.get("LOG_LEVEL", "INFO"),
        "max_workers": int(env_vars.get("MAX_WORKERS", "4")),
        "timeout": int(env_vars.get("TIMEOUT", "30")),
    }


def get_default_db_config(env_vars: dict[str, str]) -> dict[str, Any]:
    """Get default database configuration."""
    return {
        "type": "database",
        "host": env_vars.get("DB_HOST", "localhost"),
        "port": int(env_vars.get("DB_PORT", "5432")),
        "name": env_vars.get("DB_NAME", "agent_cellphone"),
        "user": env_vars.get("DB_USER", "postgres"),
        "password": env_vars.get("DB_PASSWORD", ""),
    }


def get_validation_rules() -> dict[str, dict[str, Any]]:
    """Get configuration validation rules."""
    return {
        "discord": {
            "token": {"required": True, "type": str, "min_length": 1},
            "guild_id": {"required": True, "type": str, "min_length": 1},
            "command_channel": {"required": True, "type": str, "min_length": 1},
            "enable_discord": {"required": True, "type": bool},
        },
        "application": {
            "debug": {"required": True, "type": bool},
            "log_level": {"required": True, "type": str, "min_length": 1},
            "max_workers": {"required": True, "type": int, "min_value": 1},
            "timeout": {"required": True, "type": int, "min_value": 1},
        },
        "database": {
            "host": {"required": True, "type": str, "min_length": 1},
            "port": {
                "required": True,
                "type": int,
                "min_value": 1,
                "max_value": 65535,
            },
            "name": {"required": True, "type": str, "min_length": 1},
            "user": {"required": True, "type": str, "min_length": 1},
        },
    }
