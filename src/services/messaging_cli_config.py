#!/usr/bin/env python3
"""
Configuration Management for Messaging CLI - Agent Cellphone V2
=============================================================

Configuration loading and management for the messaging CLI service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from typing import Any, Dict
from pathlib import Path
import yaml

import os


def load_config_with_precedence() -> Dict[str, Any]:
    """Load configuration with precedence: CLI → ENV → YAML → defaults."""
    config = {}
    config.update(
        {
            "sender": "Captain Agent-4",
            "mode": "pyautogui",
            "new_tab_method": "ctrl_t",
            "priority": "regular",
            "paste": True,
            "onboarding_style": "friendly",
        }
    )

    # Load from YAML config file (lowest precedence)
    config_file = Path("config/messaging.yml")
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config and "defaults" in yaml_config:
                    config.update(yaml_config["defaults"])
        except Exception:
            # Silently ignore YAML errors
            pass

    # Override with environment variables (medium precedence)
    env_mappings = {
        "AC_SENDER": "sender",
        "AC_MODE": "mode",
        "AC_NEW_TAB_METHOD": "new_tab_method",
        "AC_PRIORITY": "priority",
        "AC_ONBOARDING_STYLE": "onboarding_style",
    }

    for env_var, config_key in env_mappings.items():
        env_value = os.getenv(env_var)
        if env_value:
            config[config_key] = env_value

    return config


def get_default_config() -> Dict[str, Any]:
    """Get default configuration values."""
    return {
        "sender": "Captain Agent-4",
        "mode": "pyautogui",
        "new_tab_method": "ctrl_t",
        "priority": "regular",
        "paste": True,
        "onboarding_style": "friendly",
    }
