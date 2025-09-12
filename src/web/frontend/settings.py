# MIGRATED: This file has been migrated to the centralized configuration system
"""Shared configuration for frontend modules.

This module centralizes configuration values used across the frontend
application to provide a single source of truth (SSOT).
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FrontendSettings:
    """Configuration values for the frontend layer."""

    secret_key: str = field(default_factory=lambda: secrets.token_hex(32))
    debug: bool = False
    title: str = "Agent_Cellphone_V2 Frontend API"
    description: str = "Modern Frontend API with WebSocket Support"
    version: str = "2.0.0"


def get_settings() -> FrontendSettings:
    """Return application settings."""
    return FrontendSettings()
