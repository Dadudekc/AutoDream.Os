"""
Emergency Intervention Unified Models Enums - KISS Simplified
============================================================

Enums for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency enums.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from enum import Enum


class EmergencySeverity(Enum):
    """Emergency severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyType(Enum):
    """Types of emergencies."""
    SYSTEM_FAILURE = "system_failure"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SECURITY_BREACH = "security_breach"
    DATA_CORRUPTION = "data_corruption"
    NETWORK_OUTAGE = "network_outage"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


class EmergencyStatus(Enum):
    """Emergency status states."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    INTERVENING = "intervening"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    FAILED = "failed"


class InterventionAction(Enum):
    """Types of intervention actions."""
    RESTART_SERVICE = "restart_service"
    SCALE_RESOURCES = "scale_resources"
    ISOLATE_SYSTEM = "isolate_system"
    NOTIFY_ADMIN = "notify_admin"
    ROLLBACK_CHANGES = "rollback_changes"
    ACTIVATE_BACKUP = "activate_backup"
    ESCALATE_ISSUE = "escalate_issue"
    MONITOR_SYSTEM = "monitor_system"


class InterventionPriority(Enum):
    """Intervention priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
