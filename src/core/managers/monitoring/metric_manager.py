#!/usr/bin/env python3
"""
Metric Manager - V2 Compliance Module
====================================

Metric management functionality.
Extracted from core_monitoring_manager.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import threading
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any

from ..contracts import ManagerContext, ManagerResult


class MetricType(Enum):
    """Metric types."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class MetricManager:
    """Manages metrics and metric history."""

    def __init__(self):
        """Initialize metric manager."""
        self.metrics: dict[str, dict[str, Any]] = {}
        self.metric_callbacks: dict[str, Callable] = {}
        self.metric_history: dict[str, list[dict[str, Any]]] = {}
        self._metric_lock = threading.Lock()
        self.max_history_size = 1000

    def record_metric(
        self, context: ManagerContext, metric_name: str, metric_value: Any
    ) -> ManagerResult:
        """Record a metric value."""
        try:
            with self._metric_lock:
                if metric_name not in self.metrics:
                    self.metrics[metric_name] = {
                        "metric_name": metric_name,
                        "type": MetricType.GAUGE.value,
                        "current_value": metric_value,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                        "count": 1,
                    }
                    self.metric_history[metric_name] = []
                else:
                    metric = self.metrics[metric_name]
                    metric["current_value"] = metric_value
                    metric["updated_at"] = datetime.now().isoformat()
                    metric["count"] += 1

                # Add to history
                history_entry = {
                    "value": metric_value,
                    "timestamp": datetime.now().isoformat(),
                }
                self.metric_history[metric_name].append(history_entry)

                # Trim history if too large
                if len(self.metric_history[metric_name]) > self.max_history_size:
                    self.metric_history[metric_name] = self.metric_history[metric_name][
                        -self.max_history_size :
                    ]

                # Call metric callbacks
                for callback in self.metric_callbacks.values():
                    try:
                        callback(metric_name, metric_value)
                    except Exception:
                        pass

                return ManagerResult(
                    success=True,
                    data={"metric_name": metric_name, "value": metric_value},
                    message=f"Metric recorded: {metric_name} = {metric_value}",
                    errors=[],
                )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to record metric: {e}",
                errors=[str(e)],
            )

    def get_metrics(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get metrics with optional filtering."""
        try:
            metric_name = payload.get("metric_name")
            if metric_name:
                if metric_name in self.metrics:
                    metric = self.metrics[metric_name]
                    history = self.metric_history.get(metric_name, [])
                    return ManagerResult(
                        success=True,
                        data={"metric": metric, "history": history},
                        message=f"Metric found: {metric_name}",
                        errors=[],
                    )
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        message=f"Metric not found: {metric_name}",
                        errors=[f"Metric not found: {metric_name}"],
                    )
            else:
                return ManagerResult(
                    success=True,
                    data={"metrics": list(self.metrics.values()), "count": len(self.metrics)},
                    message=f"Found {len(self.metrics)} metrics",
                    errors=[],
                )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to get metrics: {e}",
                errors=[str(e)],
            )
