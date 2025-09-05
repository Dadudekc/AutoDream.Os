"""
Emergency Intervention Enums - V2 Compliance Module
==================================================

Enums for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
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
    """Types of emergencies that can occur."""
    AGENT_FAILURE = "agent_failure"
    MISSION_BLOCKED = "mission_blocked"
    RESOURCE_SHORTAGE = "resource_shortage"
    DEADLINE_PRESSURE = "deadline_pressure"
    COMMUNICATION_BREAKDOWN = "communication_breakdown"
    QUALITY_DEGRADATION = "quality_degradation"
    SYSTEM_OVERLOAD = "system_overload"
    SECURITY_INCIDENT = "security_incident"


class EmergencyStatus(Enum):
    """Emergency status enumeration."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    RESPONDING = "responding"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    MONITORING = "monitoring"


class InterventionType(Enum):
    """Types of intervention actions."""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    ESCALATION = "escalation"
    RESOURCE_ALLOCATION = "resource_allocation"
    MISSION_REDIRECTION = "mission_redirection"
    COMMUNICATION_RESTORATION = "communication_restoration"


class InterventionPriority(Enum):
    """Intervention priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"
