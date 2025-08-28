"""Simple metrics visualization helpers."""
from __future__ import annotations

import time
from datetime import datetime
from typing import Dict, List

from .metrics_definitions import MetricData


class MetricsVisualizer:
    """Minimal in-memory dashboard for metrics visualization."""

    def __init__(self) -> None:
        self.metrics: Dict[str, List[Dict[str, float]]] = {}
        self.agent_metrics: Dict[str, Dict[str, List[Dict[str, float]]]] = {}

    def record_metric(self, name: str, value: float) -> None:
        """Record a metric value by name."""

        self.metrics.setdefault(name, []).append(
            {"timestamp": time.time(), "value": value}
        )

    def record_agent_metric(self, agent: str, name: str, value: float) -> None:
        """Record a metric for a specific agent."""

        agent_data = self.agent_metrics.setdefault(agent, {})
        agent_data.setdefault(name, []).append(
            {"timestamp": time.time(), "value": value}
        )

    def record_metric_data(self, metric: MetricData) -> None:
        """Record a :class:`MetricData` instance."""

        self.record_metric(metric.metric_name, float(metric.value))

    def get_summary(self) -> Dict[str, object]:
        """Return a summary of stored metrics."""

        return {
            "total_metrics": sum(len(v) for v in self.metrics.values()),
            "metrics_tracked": len(self.metrics),
            "timestamp": datetime.now().isoformat(),
        }

    def get_performance_summary(self) -> Dict[str, float]:
        """Return a naive system health score for demonstration purposes."""

        total = sum(
            value["value"]
            for values in self.metrics.values()
            for value in values
        )
        count = sum(len(values) for values in self.metrics.values())
        avg = (total / count) if count else 0.0
        # In a real system this would be more sophisticated.
        return {"system_health_score": max(0.0, 100.0 - avg)}


# Backwards compatibility alias
MetricsDashboardService = MetricsVisualizer


__all__ = ["MetricsVisualizer", "MetricsDashboardService"]

