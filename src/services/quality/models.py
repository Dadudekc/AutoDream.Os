#!/usr/bin/env python3
"""Shared data models for quality monitoring services."""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class QualityAlert:
    """Unified quality alert model used across monitoring systems."""

    alert_id: str
    severity: str
    message: str
    threshold: Any
    timestamp: float
    service_id: Optional[str] = None
    alert_type: Optional[str] = None
    file_path: Optional[str] = None
    quality_score: Optional[float] = None
    metric_value: Optional[Any] = None
    recommendations: Optional[List[str]] = None
    resolved: bool = False
