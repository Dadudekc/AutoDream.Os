from src.utils.config_core import get_config

# MIGRATED: This file has been migrated to the centralized configuration system
"""Central configuration module providing SSOT for shared settings."""

from __future__ import annotations

import logging
import os

# Global logging level for the application
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)

# Standard timestamp format for task identifiers
TASK_ID_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S_%f"
