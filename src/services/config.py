# ✅ SINGLE SOURCE OF TRUTH: Consolidated Configuration System
"""Shared configuration options and constants for messaging services."""

from __future__ import annotations

from ..core.config_core import get_config

# Default messaging settings from SINGLE SOURCE OF TRUTH
DEFAULT_MODE: str = get_config("DEFAULT_MODE", "coordinated")
DEFAULT_COORDINATE_MODE: str = get_config("DEFAULT_COORDINATE_MODE", "swarm")
AGENT_COUNT: int = get_config("AGENT_COUNT", 8)
CAPTAIN_ID: str = get_config("CAPTAIN_ID", "captain-1")
