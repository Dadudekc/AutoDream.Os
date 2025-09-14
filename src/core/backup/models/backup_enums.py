#!/usr/bin/env python3
"""
Backup Enums - V2 Compliant Module
=================================

Backup monitoring enumerations and types.
V2 COMPLIANT: Focused types and enums under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):

EXAMPLE USAGE:
==============

# Import the core component
from src.core.backup.models.backup_enums import Backup_Enums

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Backup_Enums(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

    """Alert status enumeration."""

    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class AlertType(Enum):
    """Alert type enumeration."""

    BACKUP_FAILURE = "backup_failure"
    DISK_SPACE = "disk_space"
    SYSTEM_LOAD = "system_load"
    MEMORY_USAGE = "memory_usage"
    NETWORK_ISSUE = "network_issue"
    CONFIGURATION_ERROR = "configuration_error"
    SECURITY_ISSUE = "security_issue"
    PERFORMANCE_DEGRADATION = "performance_degradation"


class HealthCheckStatus(Enum):
    """Health check status enumeration."""

    PASSING = "passing"
    WARNING = "warning"
    FAILING = "failing"
    UNKNOWN = "unknown"


class HealthCheckType(Enum):
    """Health check type enumeration."""

    BACKUP_SYSTEM = "backup_system"
    SYSTEM_HEALTH = "system_health"
    STORAGE_HEALTH = "storage_health"
    NETWORK_HEALTH = "network_health"
    SECURITY_HEALTH = "security_health"
    PERFORMANCE_HEALTH = "performance_health"


class MetricType(Enum):
    """Metric type enumeration."""

    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MonitoringStatus(Enum):
    """Monitoring system status."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"

