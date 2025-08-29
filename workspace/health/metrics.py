"""Simple metrics collection utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class Metric:
    """Representation of a single metric value."""
    name: str
    value: float


class MetricsCollector:
    """Store and retrieve metric values in-memory."""

    def __init__(self) -> None:
        self._metrics: Dict[str, float] = {}

    def record(self, name: str, value: float) -> None:
        """Record a metric value."""
        self._metrics[name] = float(value)

    def get(self, name: str) -> float | None:
        """Return the latest value for *name* if available."""
        return self._metrics.get(name)

    def all(self) -> Dict[str, float]:
        """Return a copy of all metrics."""
        return dict(self._metrics)
