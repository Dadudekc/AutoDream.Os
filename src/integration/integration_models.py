#!/usr/bin/env python3
"""
Integration Models - Data models for Comprehensive Integration Assessment
=================================================================

Data models extracted from comprehensive_integration_assessment.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class AssessmentArea(Enum):
    """Assessment area enumeration"""

    CROSS_PLATFORM = "cross_platform"
    PERFORMANCE = "performance"
    REPOSITORY_AUTOMATION = "repository_automation"
    INTEGRATION_TESTING = "integration_testing"
    SECURITY = "security"
    SCALABILITY = "scalability"
    MAINTAINABILITY = "maintainability"
    RELIABILITY = "reliability"


class Priority(Enum):
    """Priority enumeration"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AssessmentStatus(Enum):
    """Assessment status enumeration"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class PlatformType(Enum):
    """Platform type enumeration"""

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"


@dataclass
class IntegrationAssessment:
    """Integration assessment structure"""

    area: AssessmentArea
    component: str
    assessment_score: float
    issues: list[str]
    recommendations: list[str]
    priority: Priority
    estimated_effort: int
    timestamp: str
    status: AssessmentStatus
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "area": self.area.value,
            "component": self.component,
            "assessment_score": self.assessment_score,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "priority": self.priority.value,
            "estimated_effort": self.estimated_effort,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "details": self.details,
        }

    def is_critical(self) -> bool:
        """Check if assessment is critical."""
        return self.priority == Priority.CRITICAL

    def get_health_score(self) -> str:
        """Get health score category."""
        if self.assessment_score >= 90:
            return "excellent"
        elif self.assessment_score >= 75:
            return "good"
        elif self.assessment_score >= 60:
            return "acceptable"
        else:
            return "poor"


@dataclass
class PlatformCompatibility:
    """Platform compatibility assessment"""

    platform: PlatformType
    compatibility_score: float
    tested_components: list[str]
    issues: list[str]
    recommendations: list[str]
    last_tested: datetime

    def is_compatible(self) -> bool:
        """Check if platform is compatible."""
        return self.compatibility_score >= 80.0

    def get_compatibility_level(self) -> str:
        """Get compatibility level."""
        if self.compatibility_score >= 95:
            return "fully_compatible"
        elif self.compatibility_score >= 80:
            return "mostly_compatible"
        elif self.compatibility_score >= 60:
            return "partially_compatible"
        else:
            return "incompatible"


@dataclass
class PerformanceMetrics:
    """Performance metrics assessment"""

    response_time: float
    throughput: float
    memory_usage: float
    cpu_usage: float
    error_rate: float
    uptime: float
    timestamp: datetime

    def get_performance_score(self) -> float:
        """Calculate overall performance score."""
        # Weighted scoring based on metrics
        weights = {
            "response_time": 0.25,
            "throughput": 0.25,
            "memory_usage": 0.15,
            "cpu_usage": 0.15,
            "error_rate": 0.10,
            "uptime": 0.10,
        }

        # Normalize and score each metric (0-100 scale)
        response_score = max(0, 100 - (self.response_time * 10))  # Lower is better
        throughput_score = min(100, self.throughput * 2)  # Higher is better
        memory_score = max(0, 100 - (self.memory_usage / 10))  # Lower is better
        cpu_score = max(0, 100 - (self.cpu_usage * 2))  # Lower is better
        error_score = max(0, 100 - (self.error_rate * 1000))  # Lower is better
        uptime_score = self.uptime  # Higher is better

        scores = [
            response_score,
            throughput_score,
            memory_score,
            cpu_score,
            error_score,
            uptime_score,
        ]
        weights_list = list(weights.values())

        return sum(score * weight for score, weight in zip(scores, weights_list, strict=False))


@dataclass
class IntegrationReport:
    """Comprehensive integration report"""

    report_id: str
    assessment_date: datetime
    overall_score: float
    total_components: int
    assessed_components: int
    critical_issues: int
    high_priority_issues: int
    recommendations_count: int
    platform_compatibility: dict[str, PlatformCompatibility]
    performance_metrics: PerformanceMetrics | None
    assessments: list[IntegrationAssessment]
    summary: str

    def get_completion_percentage(self) -> float:
        """Get assessment completion percentage."""
        return (
            (self.assessed_components / self.total_components * 100)
            if self.total_components > 0
            else 0.0
        )

    def get_overall_health(self) -> str:
        """Get overall system health."""
        if self.overall_score >= 90:
            return "excellent"
        elif self.overall_score >= 75:
            return "good"
        elif self.overall_score >= 60:
            return "acceptable"
        else:
            return "poor"

    def get_critical_issues_count(self) -> int:
        """Get count of critical issues."""
        return len([a for a in self.assessments if a.is_critical()])


@dataclass
class ComponentInfo:
    """Component information for assessment"""

    component_id: str
    name: str
    type: str
    version: str
    platform_requirements: list[PlatformType]
    dependencies: list[str]
    configuration: dict[str, Any]
    last_updated: datetime

    def is_multi_platform(self) -> bool:
        """Check if component supports multiple platforms."""
        return len(self.platform_requirements) > 1

    def get_dependency_count(self) -> int:
        """Get number of dependencies."""
        return len(self.dependencies)


@dataclass
class AssessmentConfiguration:
    """Assessment configuration settings"""

    max_concurrent_assessments: int
    timeout_seconds: float
    quality_threshold: float
    auto_retry: bool
    retry_attempts: int
    notification_enabled: bool
    detailed_logging: bool

    def is_valid(self) -> bool:
        """Validate configuration."""
        return (
            self.max_concurrent_assessments > 0
            and self.timeout_seconds > 0
            and 0 <= self.quality_threshold <= 1.0
            and self.retry_attempts >= 0
        )
