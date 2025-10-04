#!/usr/bin/env python3
"""
Deprecation shim for src/services/messaging/providers/discord_provider_operations.py

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
    "Module src/services/messaging/providers/discord_provider_operations.py is deprecated. Use src.services.discord_commander.discord_post_client directly.",
    DeprecationWarning,
    stacklevel=2,
)
