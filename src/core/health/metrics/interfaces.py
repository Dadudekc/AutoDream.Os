"""Common metric interfaces and data structures.

This module defines the core protocol based interfaces used by the
metrics collection pipeline.  ``MetricSource`` implementations provide
metric samples while ``MetricSink`` implementations persist aggregated
results.  The lightweight :class:`Metric` dataclass is shared across the
pipeline.

The interfaces are intentionally minimal which makes it easy to unit
test components in isolation and to plug new sources or sinks into the
pipeline without modifying the collector itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Protocol


@dataclass
class Metric:
    """Simple representation of a collected metric sample."""

    source: str
    name: str
    value: float
    timestamp: float


class MetricSource(Protocol):
    """Interface for objects capable of producing metrics."""

    interval: float

    def collect(self) -> Iterable[Metric]:
        """Return an iterable of metric samples."""


class MetricSink(Protocol):
    """Interface for persisting aggregated metric data."""

    def persist(self, data: Dict[str, float]) -> None:
        """Persist an aggregated metrics summary."""

