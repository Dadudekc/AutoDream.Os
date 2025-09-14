"""
Dashboard Metric Manager - V2 Compliance Module
==============================================

Metric management functionality for dashboard engine.

V2 Compliance: < 300 lines, single responsibility, metric management.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .models import MetricType, PerformanceMetric

logger = logging.getLogger(__name__)


class MetricManager:
    """Metric management functionality."""

    def __init__(self):
        """Initialize metric manager."""
        self.logger = logger
        self.metrics: dict[str, PerformanceMetric] = {}

    def add_metric(self, metric: PerformanceMetric) -> bool:
        """Add performance metric."""
        try:
            if not metric or not metric.metric_id:
                self.logger.error("Invalid metric provided")
                return False

            self.metrics[metric.metric_id] = metric
            self.logger.info(f"Added metric: {metric.metric_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add metric: {e}")
            return False

    def get_metric(self, metric_id: str) -> PerformanceMetric | None:
        """Get performance metric by ID."""
        return self.metrics.get(metric_id)

    def get_metrics_by_type(self, metric_type: MetricType) -> list[PerformanceMetric]:
        """Get metrics by type."""
        return [metric for metric in self.metrics.values() if metric.metric_type == metric_type]

    def update_metric(self, metric_id: str, updates: dict[str, Any]) -> bool:
        """Update performance metric."""
        try:
            if metric_id not in self.metrics:
                self.logger.error(f"Metric not found: {metric_id}")
                return False

            metric = self.metrics[metric_id]
            for key, value in updates.items():
                if hasattr(metric, key):
                    setattr(metric, key, value)

            metric.updated_at = datetime.now()
            self.logger.info(f"Updated metric: {metric_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update metric: {e}")
            return False

    def remove_metric(self, metric_id: str) -> bool:
        """Remove performance metric."""
        try:
            if metric_id in self.metrics:
                del self.metrics[metric_id]
                self.logger.info(f"Removed metric: {metric_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove metric: {e}")
            return False

    def get_all_metrics(self) -> list[PerformanceMetric]:
        """Get all metrics."""
        return list(self.metrics.values())

    def get_metrics_count(self) -> int:
        """Get total metrics count."""
        return len(self.metrics)

    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()
        self.logger.info("Cleared all metrics")

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get metrics summary."""
        return {
            "total_metrics": len(self.metrics),
            "metric_types": list({metric.metric_type.value for metric in self.metrics.values()}),
            "last_updated": max(
                (metric.updated_at for metric in self.metrics.values()), default=None
            ),
        }
