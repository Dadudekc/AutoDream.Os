"""Compatibility wrapper for portfolio tracking components.

The original monolithic tracking module has been split into
three focused modules:

* :mod:`tracking_logic` - core tracking calculations
* :mod:`data_management` - persistence of snapshots and reports
* :mod:`reporting` - generation of performance reports

This file re-exports the primary classes for backward
compatibility.
"""

from .tracking_logic import (
    PerformanceMetric,
    PortfolioAllocation,
    PerformanceSnapshot,
    PerformanceReport,
    PortfolioPerformanceTracker,
)
from .data_management import PerformanceDataManager
from .reporting import PerformanceReporter

__all__ = [
    "PerformanceMetric",
    "PortfolioAllocation",
    "PerformanceSnapshot",
    "PerformanceReport",
    "PortfolioPerformanceTracker",
    "PerformanceDataManager",
    "PerformanceReporter",
]
