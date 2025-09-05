"""
Strategic Oversight Enums - V2 Compliance Module
===============================================

Enums for vector strategic oversight operations.

V2 Compliance: < 300 lines, single responsibility, enum definitions.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from enum import Enum


class InsightType(Enum):
    """Insight types."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    EMERGENCY = "emergency"


class ConfidenceLevel(Enum):
    """Confidence levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ImpactLevel(Enum):
    """Impact levels."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionStatus(Enum):
    """Mission status types."""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ReportType(Enum):
    """Report types."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    AD_HOC = "ad_hoc"
    EMERGENCY = "emergency"


class PriorityLevel(Enum):
    """Priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class AgentRole(Enum):
    """Agent roles."""
    CAPTAIN = "captain"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    EXECUTOR = "executor"
