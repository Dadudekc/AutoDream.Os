"""
Strategic Oversight Enums
========================

Enums for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, enum definitions.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from enum import Enum


class InsightType(Enum):
    """Insight type."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RESOURCE = "resource"
    TIMING = "timing"
    PATTERN = "pattern"


class ConfidenceLevel(Enum):
    """Confidence level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ImpactLevel(Enum):
    """Impact level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionStatus(Enum):
    """Mission status."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReportType(Enum):
    """Report type."""
    SUMMARY = "summary"
    DETAILED = "detailed"
    EXECUTIVE = "executive"
    TECHNICAL = "technical"


class PriorityLevel(Enum):
    """Priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class AgentRole(Enum):
    """Agent role."""
    COORDINATOR = "coordinator"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    OVERSIGHT = "oversight"


class EmergencyStatus(Enum):
    """Emergency status."""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"