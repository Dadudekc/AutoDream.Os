#!/usr/bin/env python3
"""
Deprecation shim for src.services.discord_commander.discord_post_client

This module provides backward compatibility while redirecting to the
canonical implementation.

DEPRECATED: Use the canonical module directly.
"""

import warnings

from src.services.discord_commander.discord_post_client import *

# Deprecation warning
warnings.warn(
    "Module src.services.discord_commander.discord_post_client is deprecated. Use canonical module directly.",
    DeprecationWarning,
    stacklevel=2,
)