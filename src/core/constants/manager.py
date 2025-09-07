from pathlib import Path
import yaml
from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Manager Constants - Manager Module Definitions

This module provides manager-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "messaging.yml"
with _CONFIG_PATH.open() as f:
    _messaging_config = yaml.safe_load(f) or {}

COMPLETION_SIGNAL = _messaging_config.get(
    "defaults", {}
).get("completion_signal", "<TASK_COMPLETED>")


def get_completion_signal() -> str:
    """Return the task completion signal."""
    return COMPLETION_SIGNAL


# Manager module constants
DEFAULT_HEALTH_CHECK_INTERVAL = get_config('DEFAULT_HEALTH_CHECK_INTERVAL', 30)
DEFAULT_MAX_STATUS_HISTORY = get_config('DEFAULT_MAX_STATUS_HISTORY', 1000)
DEFAULT_AUTO_RESOLVE_TIMEOUT = get_config('DEFAULT_AUTO_RESOLVE_TIMEOUT', 3600)
STATUS_CONFIG_PATH = "config/status_manager.json"
