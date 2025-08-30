
# MIGRATED: This file has been migrated to the centralized configuration system
"""Shared agent configuration constants.

This module acts as a single source of truth (SSOT) for settings
used across manager components. Keeping these values in one place
helps maintain consistency and avoids magic numbers sprinkled
throughout the codebase.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    """Core configuration values for agent systems."""

    # Default lifecycle state when an agent is instantiated
    DEFAULT_LIFECYCLE_STATE: str = "initialized"

    # Coordination strategy used when distributing work
    DEFAULT_COORDINATION_STRATEGY: str = "round_robin"

    # Interval (in seconds) for metrics collection
    METRICS_POLL_INTERVAL: int = 60
