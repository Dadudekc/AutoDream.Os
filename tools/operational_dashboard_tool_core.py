#!/usr/bin/env python3
"""
Operational Dashboard Tool Core
==============================

Core classes and data structures for operational dashboard and analytics.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MetricType(Enum):
    """Types of operational metrics."""

    QUALITY_GATE = "quality_gate"
    AGENT_PERFORMANCE = "agent_performance"
    PROJECT_PROGRESS = "project_progress"
    RESOURCE_ALLOCATION = "resource_allocation"
    TEAM_COORDINATION = "team_coordination"


class AlertLevel(Enum):
    """Alert levels for operational issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class QualityGateResult:
    """Quality gate result data."""

    timestamp: str
    total_files: int
    compliant_files: int
    violations: int
    quality_score: float
    critical_issues: int
    recommendations: list[str]


@dataclass
class AgentPerformance:
    """Agent performance metrics."""

    agent_id: str
    tasks_completed: int
    tasks_failed: int
    average_cycle_time: float
    quality_score: float
    last_active: str
    current_status: str


@dataclass
class ProjectProgress:
    """Project progress tracking."""

    project_name: str
    completion_percentage: float
    tasks_completed: int
    tasks_total: int
    last_update: str
    status: str


@dataclass
class OperationalAlert:
    """Operational alert data."""

    alert_id: str
    level: AlertLevel
    message: str
    timestamp: str
    agent_id: str | None
    project_name: str | None
    resolved: bool
