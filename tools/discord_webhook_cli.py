#!/usr/bin/env python3
"""
Deprecation shim for tools/discord_webhook_cli.py

This module provides backward compatibility while redirecting to the
canonical implementation: src.services.discord_commander.discord_post_client

DEPRECATED: Use the canonical module directly.
"""

import warnings

from src.services.discord_commander.discord_post_client import *

# Symbol mappings for backward compatibility
# Import from canonical module: src.services.discord_commander.discord_post_client

# Deprecation warning
warnings.warn(
    "Module tools/discord_webhook_cli.py is deprecated. Use src.services.discord_commander.discord_post_client directly.",
    DeprecationWarning,
    stacklevel=2,
)
