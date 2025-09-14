#!/usr/bin/env python3
"""
Analytics Data Models - V2 Compliant Module
==========================================

Data models for unified analytics system with V2 compliance validation.
V2 COMPLIANT: Focused data models under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .analytics_enums import AnalyticsStatus, AnalyticsType, IntelligenceType, ProcessingMode


@dataclass
class AnalyticsInfo:
    """Analytics information model."""

    analytics_id: str
    name: str
    analytics_type: AnalyticsType
    status: AnalyticsStatus
    intelligence_type: IntelligenceType | None = None
    processing_mode: ProcessingMode = ProcessingMode.BATCH
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalyticsData:
    """Analytics data model."""

    data_id: str
    source: str
    data_type: str
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalyticsResult:
    """Analytics result model."""

    result_id: str
    analytics_id: str
    data_id: str
    result_type: str
    result_data: Any
    confidence: float = 0.0
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalyticsMetrics:
    """Analytics metrics model."""

    analytics_id: str
    total_processed: int = 0
    successful_processed: int = 0
    failed_processed: int = 0
    average_processing_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


# Export all models for easy import
__all__ = [
    "AnalyticsInfo",
    "AnalyticsData",
    "AnalyticsResult",
    "AnalyticsMetrics",
]
