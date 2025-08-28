"""Shared constants for baseline measurement modules."""

from __future__ import annotations

DEFAULT_METRICS = [
    "code_complexity",
    "maintainability_index",
    "duplication_percentage",
    "refactoring_duration",
    "performance_improvement",
    "memory_usage",
    "cpu_utilization",
    "lines_of_code",
    "test_coverage",
    "bug_density",
]

DEFAULT_BASELINE_CONFIG = {
    "auto_calibration_enabled": True,
    "calibration_threshold": 0.8,
    "max_baselines_per_type": 5,
    "baseline_retention_days": 90,
    "trend_analysis_enabled": True,
    "forecast_horizon_days": 30,
    "validation_interval_hours": 24,
    "default_metrics": DEFAULT_METRICS,
}

__all__ = ["DEFAULT_BASELINE_CONFIG", "DEFAULT_METRICS"]
