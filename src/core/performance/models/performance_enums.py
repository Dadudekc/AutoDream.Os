import logging
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Performance Enums - V2 Compliant Module
======================================

Performance monitoring enumerations and types.
V2 COMPLIANT: Focused types under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from enum import Enum


class DashboardType(Enum):
    """Types of monitoring dashboards."""

    OPERATIONAL = "operational"
    CONSOLIDATION = "consolidation"
    PERFORMANCE = "performance"
    SLA_COMPLIANCE = "sla_compliance"
    ALERT_MANAGEMENT = "alert_management"


class MetricType(Enum):

EXAMPLE USAGE:
==============

# Import the core component
from src.core.performance.models.performance_enums import Performance_Enums

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Performance_Enums(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

    """Types of performance metrics."""

    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertSeverity(Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(Enum):
    """Alert status types."""

    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


# Export all enums for easy import
__all__ = [
    "DashboardType",
    "MetricType",
    "AlertSeverity",
    "AlertStatus",
]

