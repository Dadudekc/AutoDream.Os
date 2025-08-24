"""Metric sink implementations."""

from __future__ import annotations

from typing import Dict, List

from .interfaces import MetricSink


class InMemoryMetricSink(MetricSink):
    """Store persisted summaries in memory for inspection in tests."""

    def __init__(self) -> None:
        self.persisted: List[Dict[str, float]] = []

    def persist(self, data: Dict[str, float]) -> None:
        self.persisted.append(dict(data))

