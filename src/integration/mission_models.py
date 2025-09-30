#!/usr/bin/env python3
"""
Mission Models - Data models for Dual Role Comprehensive Mission System
=================================================================

Data models extracted from dual_role_comprehensive_mission.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class MissionTask(Enum):
    """Mission task enumeration"""

    TEST_AGENT7_INTERFACE = "test_agent7_interface"
    VALIDATE_AGENT6_VSCODE = "validate_agent6_vscode"
    DEVELOP_TESTING_FRAMEWORK = "develop_testing_framework"
    ENSURE_CROSS_PLATFORM = "ensure_cross_platform"
    OPTIMIZE_PERFORMANCE = "optimize_performance"
    INTEGRATION_VALIDATION = "integration_validation"
    QUALITY_ASSURANCE = "quality_assurance"
    DOCUMENTATION_REVIEW = "documentation_review"


class TaskStatus(Enum):
    """Task status enumeration"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Task priority enumeration"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class MissionAssessment:
    """Mission assessment structure"""

    task: MissionTask
    status: TaskStatus
    score: float
    progress: float
    issues: list[str]
    recommendations: list[str]
    execution_time: float
    priority: Priority
    timestamp: datetime
    agent_id: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task": self.task.value,
            "status": self.status.value,
            "score": self.score,
            "progress": self.progress,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "execution_time": self.execution_time,
            "priority": self.priority.value,
            "timestamp": self.timestamp.isoformat(),
            "agent_id": self.agent_id,
            "details": self.details,
        }


@dataclass
class MissionProgress:
    """Mission progress tracking"""

    mission_id: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    in_progress_tasks: int
    overall_progress: float
    overall_score: float
    start_time: datetime
    last_update: datetime
    estimated_completion: datetime | None

    def get_completion_percentage(self) -> float:
        """Get completion percentage."""
        return (self.completed_tasks / self.total_tasks * 100) if self.total_tasks > 0 else 0.0

    def get_success_rate(self) -> float:
        """Get success rate."""
        total_finished = self.completed_tasks + self.failed_tasks
        return (self.completed_tasks / total_finished * 100) if total_finished > 0 else 0.0


@dataclass
class AgentCapability:
    """Agent capability assessment"""

    agent_id: str
    role: str
    capabilities: list[str]
    expertise_level: float
    availability: bool
    current_workload: float
    performance_score: float
    last_assessment: datetime

    def is_available(self) -> bool:
        """Check if agent is available."""
        return self.availability and self.current_workload < 0.8

    def get_capability_score(self) -> float:
        """Get overall capability score."""
        return (self.expertise_level + self.performance_score) / 2


@dataclass
class SystemRequirement:
    """System requirement specification"""

    requirement_id: str
    description: str
    priority: Priority
    complexity: str
    estimated_effort: float
    dependencies: list[str]
    acceptance_criteria: list[str]
    validation_method: str
    assigned_agent: str | None

    def is_high_priority(self) -> bool:
        """Check if requirement is high priority."""
        return self.priority in [Priority.CRITICAL, Priority.HIGH]

    def get_effort_category(self) -> str:
        """Get effort category."""
        if self.estimated_effort <= 2.0:
            return "low"
        elif self.estimated_effort <= 5.0:
            return "medium"
        else:
            return "high"


@dataclass
class QualityMetric:
    """Quality metric tracking"""

    metric_name: str
    current_value: float
    target_value: float
    unit: str
    measurement_date: datetime
    trend: str
    status: str

    def get_achievement_rate(self) -> float:
        """Get achievement rate."""
        return (self.current_value / self.target_value * 100) if self.target_value > 0 else 0.0

    def is_target_met(self) -> bool:
        """Check if target is met."""
        return self.current_value >= self.target_value


@dataclass
class IntegrationReport:
    """Integration assessment report"""

    report_id: str
    assessment_date: datetime
    overall_status: str
    total_components: int
    integrated_components: int
    failed_integrations: int
    pending_integrations: int
    critical_issues: list[str]
    recommendations: list[str]
    next_steps: list[str]
    success_rate: float

    def get_integration_percentage(self) -> float:
        """Get integration percentage."""
        return (
            (self.integrated_components / self.total_components * 100)
            if self.total_components > 0
            else 0.0
        )

    def get_health_score(self) -> float:
        """Get integration health score."""
        if self.success_rate >= 0.9:
            return 100.0
        elif self.success_rate >= 0.7:
            return 75.0
        elif self.success_rate >= 0.5:
            return 50.0
        else:
            return 25.0


@dataclass
class MissionConfiguration:
    """Mission configuration settings"""

    mission_name: str
    version: str
    max_concurrent_tasks: int
    timeout_seconds: float
    retry_attempts: int
    quality_threshold: float
    auto_escalation: bool
    notification_enabled: bool
    log_level: str

    def is_valid(self) -> bool:
        """Validate configuration."""
        return (
            self.max_concurrent_tasks > 0
            and self.timeout_seconds > 0
            and self.retry_attempts >= 0
            and 0 <= self.quality_threshold <= 1.0
        )
