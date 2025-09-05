"""
Vector Integration Enums - V2 Compliant Module
==============================================

Enums for vector integration analytics system.
Extracted from vector_integration_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from enum import Enum


class AnalyticsMode(Enum):
    """Analytics modes."""
    REAL_TIME = "real_time"
    BATCH = "batch"
    HYBRID = "hybrid"
    SCHEDULED = "scheduled"


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TrendDirection(Enum):
    """Trend direction indicators."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


class RecommendationCategory(Enum):
    """Optimization recommendation categories."""
    PERFORMANCE = "performance"
    RESOURCE = "resource"
    CONFIGURATION = "configuration"
    ARCHITECTURE = "architecture"


class RecommendationPriority(Enum):
    """Recommendation priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImplementationEffort(Enum):
    """Implementation effort levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
