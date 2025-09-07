
# MIGRATED: This file has been migrated to the centralized configuration system
"""Shared configuration and definitions for the metrics pipeline.

This module centralizes metric-related constants and simple data
structures so they can be reused across the data collection,
transformation and export modules.  Keeping these definitions in one
place reduces coupling and makes the pipeline easier to maintain.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# General constants
# ---------------------------------------------------------------------------

# Default path used when exporting metrics to disk.  Individual callers may
# override this value if a custom destination is required.
DEFAULT_EXPORT_PATH = "metrics_export.json"

# Keys used in summary dictionaries returned by the transformer.  Using
# constants avoids hard-coded strings being scattered through the codebase.
SUMMARY_TOTAL_METRICS = "total_metrics"
SUMMARY_METRICS_TRACKED = "metrics_tracked"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class MetricRecord:
    """Represents a single recorded metric value."""

    timestamp: float
    value: float


__all__ = [
    "DEFAULT_EXPORT_PATH",
    "SUMMARY_METRICS_TRACKED",
    "SUMMARY_TOTAL_METRICS",
    "MetricRecord",
]
