"""Collect simple in-memory metrics for agents."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict

from ..agent_config import AgentConfig


class AgentMetricsManager:
    """Tracks counters and durations for agents.

    Metrics collection is intentionally lightweight. Values are stored in
    dictionaries to avoid introducing external dependencies while still
    giving developers insight into system behaviour.
    """

    def __init__(self) -> None:
        self.interval = AgentConfig.METRICS_POLL_INTERVAL
        self.counters: Dict[str, int] = defaultdict(int)

    def increment(self, name: str, amount: int = 1) -> None:
        """Increment a named counter."""

        self.counters[name] += amount

    def get(self, name: str) -> int:
        """Retrieve a counter value (defaults to 0)."""

        return self.counters.get(name, 0)
