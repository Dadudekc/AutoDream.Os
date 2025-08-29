"""Legacy module for metric adapters.

The actual implementations now live in ``refactoring.metrics.adapters``.
This module re-exports them for backward compatibility.
"""

from __future__ import annotations

from refactoring.metrics.aggregator import Metric
from refactoring.metrics.adapters import MetricAdapter as MetricSourceAdapter, SystemMetricsAdapter

__all__ = ["Metric", "MetricSourceAdapter", "SystemMetricsAdapter"]
