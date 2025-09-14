#!/usr/bin/env python3
"""
Analytics Enums and Types - V2 Compliant Module
==============================================

Analytics enumerations and type definitions for unified analytics system.
V2 COMPLIANT: Focused types and enums under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from enum import Enum


class AnalyticsStatus(Enum):
    """Analytics status enumeration."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AnalyticsType(Enum):
    """Analytics type enumeration."""

    INTELLIGENCE = "intelligence"
    PROCESSING = "processing"
    COORDINATION = "coordination"
    ORCHESTRATION = "orchestration"
    PREDICTION = "prediction"
    CACHING = "caching"
    REALTIME = "realtime"
    BATCH = "batch"
    METRICS = "metrics"
    INTEGRATION = "integration"


class IntelligenceType(Enum):
    """Intelligence type enumeration."""

    PATTERN_RECOGNITION = "pattern_recognition"
    ANOMALY_DETECTION = "anomaly_detection"
    PREDICTIVE_ANALYTICS = "predictive_analytics"
    BEHAVIORAL_ANALYSIS = "behavioral_analysis"
    OPTIMIZATION = "optimization"


class ProcessingMode(Enum):
    """Processing mode enumeration."""

    REALTIME = "realtime"
    BATCH = "batch"
    STREAMING = "streaming"
    MICRO_BATCH = "micro_batch"


# Export all enums for easy import
__all__ = [
    "AnalyticsStatus",
    "AnalyticsType",
    "IntelligenceType",
    "ProcessingMode",
]