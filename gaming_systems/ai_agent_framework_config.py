
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration utilities for the AI Agent Framework."""

import logging

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

__all__ = ["logger", "LOG_LEVEL"]
