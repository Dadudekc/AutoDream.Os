"""Compatibility layer for metric definitions.

The actual data structures live in :mod:`src.services.metrics_definitions` to
provide a single source of truth for metric schemas.  This module simply
re-exports those definitions for backwards compatibility with existing
imports throughout the code base.
"""
from src.services.metrics_definitions import MetricData, MetricType


__all__ = ["MetricType", "MetricData"]
