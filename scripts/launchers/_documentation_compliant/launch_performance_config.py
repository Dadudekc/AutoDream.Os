"""
launch_performance_config.py
Module: launch_performance_config.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:52
"""


# MIGRATED: This file has been migrated to the centralized configuration system
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def _expand_env_vars(obj):
    """Recursively expand environment variables in configuration."""
    if isinstance(obj, dict):
        return {k: _expand_env_vars(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand_env_vars(i) for i in obj]
    if isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
        env_var = obj[2:-1]
        return os.getenv(env_var, obj)
    return obj


def load_config(config_file: str):
        """
        load_config
        
        Purpose: Automated function documentation
        """
    """Load configuration from file and expand environment variables.

    Returns the configuration dict or None if loading fails.
    """
    try:
        config_path = Path(config_file)
        if not config_path.exists():
            logger.error("Configuration file not found: %s", config_file)
            return None

        with open(config_path, "r") as f:
            config = json.load(f)

        config = _expand_env_vars(config)
        logger.info("Configuration loaded from %s", config_file)
        return config
    except Exception as e:
        logger.error("Failed to load configuration: %s", e)
        return None

