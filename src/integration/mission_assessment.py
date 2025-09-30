#!/usr/bin/env python3
"""
Mission Assessment - Assessment logic for Dual Role Comprehensive Mission System
====================================================================

Assessment logic extracted from dual_role_comprehensive_mission.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Any

from .mission_models import (
    AgentCapability,
    MissionAssessment,
    MissionTask,
    Priority,
    QualityMetric,
    TaskStatus,
)

logger = logging.getLogger(__name__)


class MissionAssessmentEngine:
    """Mission assessment engine for comprehensive evaluation."""

    def __init__(self):
        """Initialize mission assessment engine."""
        self.assessments: list[MissionAssessment] = []
        self.capabilities: dict[str, AgentCapability] = {}
        self.quality_metrics: dict[str, QualityMetric] = {}
        logger.info("Mission assessment engine initialized")

    def assess_task(
        self, task: MissionTask, agent_id: str, details: dict[str, Any] = None
    ) -> MissionAssessment:
        """Assess a specific mission task."""
        start_time = time.time()

        try:
            # Perform assessment based on task type
            if task == MissionTask.TEST_AGENT7_INTERFACE:
                assessment = self._assess_agent7_interface(agent_id, details)
            elif task == MissionTask.VALIDATE_AGENT6_VSCODE:
                assessment = self._assess_agent6_vscode(agent_id, details)
            elif task == MissionTask.DEVELOP_TESTING_FRAMEWORK:
                assessment = self._assess_testing_framework(agent_id, details)
            elif task == MissionTask.ENSURE_CROSS_PLATFORM:
                assessment = self._assess_cross_platform(agent_id, details)
            elif task == MissionTask.OPTIMIZE_PERFORMANCE:
                assessment = self._assess_performance_optimization(agent_id, details)
            else:
                assessment = self._assess_generic_task(task, agent_id, details)

            assessment.execution_time = time.time() - start_time
            assessment.timestamp = datetime.now()
            assessment.agent_id = agent_id
            assessment.details = details or {}

            self.assessments.append(assessment)
            logger.info(f"Task assessment completed: {task.value}")

            return assessment

        except Exception as e:
            logger.error(f"Error assessing task {task.value}: {e}")
            return self._create_failed_assessment(task, agent_id, str(e))

    def _assess_agent7_interface(self, agent_id: str, details: dict[str, Any]) -> MissionAssessment:
        """Assess Agent-7 interface functionality."""
        issues = []
        recommendations = []
        score = 85.0  # Base score

        # Check interface components
        if details and "components_tested" in details:
            components = details["components_tested"]
            if len(components) < 5:
                issues.append("Insufficient component coverage")
                score -= 10
            else:
                recommendations.append("Good component coverage achieved")

        # Check response time
        if details and "response_time" in details:
            response_time = details["response_time"]
            if response_time > 2.0:
                issues.append("Slow response time detected")
                score -= 15
            else:
                recommendations.append("Response time within acceptable limits")

        return MissionAssessment(
            task=MissionTask.TEST_AGENT7_INTERFACE,
            status=TaskStatus.COMPLETED if score >= 70 else TaskStatus.FAILED,
            score=score,
            progress=100.0,
            issues=issues,
            recommendations=recommendations,
            execution_time=0.0,
            priority=Priority.HIGH,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _assess_agent6_vscode(self, agent_id: str, details: dict[str, Any]) -> MissionAssessment:
        """Assess Agent-6 VSCode validation."""
        issues = []
        recommendations = []
        score = 90.0  # Base score

        # Check VSCode integration
        if details and "vscode_integration" in details:
            integration_status = details["vscode_integration"]
            if not integration_status:
                issues.append("VSCode integration not working")
                score -= 25
            else:
                recommendations.append("VSCode integration validated")

        # Check extension compatibility
        if details and "extensions_tested" in details:
            extensions = details["extensions_tested"]
            if len(extensions) < 3:
                issues.append("Limited extension testing")
                score -= 10

        return MissionAssessment(
            task=MissionTask.VALIDATE_AGENT6_VSCODE,
            status=TaskStatus.COMPLETED if score >= 70 else TaskStatus.FAILED,
            score=score,
            progress=100.0,
            issues=issues,
            recommendations=recommendations,
            execution_time=0.0,
            priority=Priority.HIGH,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _assess_testing_framework(
        self, agent_id: str, details: dict[str, Any]
    ) -> MissionAssessment:
        """Assess testing framework development."""
        issues = []
        recommendations = []
        score = 80.0  # Base score

        # Check test coverage
        if details and "test_coverage" in details:
            coverage = details["test_coverage"]
            if coverage < 0.8:
                issues.append("Low test coverage")
                score -= 15
            else:
                recommendations.append("Good test coverage achieved")

        # Check framework completeness
        if details and "framework_components" in details:
            components = details["framework_components"]
            required_components = ["test_runner", "assertions", "mocking", "reporting"]
            missing = [comp for comp in required_components if comp not in components]
            if missing:
                issues.append(f"Missing framework components: {missing}")
                score -= len(missing) * 5

        return MissionAssessment(
            task=MissionTask.DEVELOP_TESTING_FRAMEWORK,
            status=TaskStatus.COMPLETED if score >= 70 else TaskStatus.FAILED,
            score=score,
            progress=100.0,
            issues=issues,
            recommendations=recommendations,
            execution_time=0.0,
            priority=Priority.MEDIUM,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _assess_cross_platform(self, agent_id: str, details: dict[str, Any]) -> MissionAssessment:
        """Assess cross-platform compatibility."""
        issues = []
        recommendations = []
        score = 75.0  # Base score

        # Check platform support
        if details and "platforms_tested" in details:
            platforms = details["platforms_tested"]
            required_platforms = ["Windows", "Linux", "macOS"]
            missing = [p for p in required_platforms if p not in platforms]
            if missing:
                issues.append(f"Missing platform support: {missing}")
                score -= len(missing) * 10
            else:
                recommendations.append("Full cross-platform support confirmed")

        return MissionAssessment(
            task=MissionTask.ENSURE_CROSS_PLATFORM,
            status=TaskStatus.COMPLETED if score >= 70 else TaskStatus.FAILED,
            score=score,
            progress=100.0,
            issues=issues,
            recommendations=recommendations,
            execution_time=0.0,
            priority=Priority.MEDIUM,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _assess_performance_optimization(
        self, agent_id: str, details: dict[str, Any]
    ) -> MissionAssessment:
        """Assess performance optimization."""
        issues = []
        recommendations = []
        score = 85.0  # Base score

        # Check performance metrics
        if details and "performance_improvement" in details:
            improvement = details["performance_improvement"]
            if improvement < 0.1:  # Less than 10% improvement
                issues.append("Minimal performance improvement")
                score -= 15
            else:
                recommendations.append(f"Significant performance improvement: {improvement:.1%}")

        return MissionAssessment(
            task=MissionTask.OPTIMIZE_PERFORMANCE,
            status=TaskStatus.COMPLETED if score >= 70 else TaskStatus.FAILED,
            score=score,
            progress=100.0,
            issues=issues,
            recommendations=recommendations,
            execution_time=0.0,
            priority=Priority.HIGH,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _assess_generic_task(
        self, task: MissionTask, agent_id: str, details: dict[str, Any]
    ) -> MissionAssessment:
        """Assess generic task."""
        return MissionAssessment(
            task=task,
            status=TaskStatus.COMPLETED,
            score=75.0,
            progress=100.0,
            issues=[],
            recommendations=["Generic assessment completed"],
            execution_time=0.0,
            priority=Priority.MEDIUM,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details=details or {},
        )

    def _create_failed_assessment(
        self, task: MissionTask, agent_id: str, error: str
    ) -> MissionAssessment:
        """Create a failed assessment."""
        return MissionAssessment(
            task=task,
            status=TaskStatus.FAILED,
            score=0.0,
            progress=0.0,
            issues=[f"Assessment failed: {error}"],
            recommendations=["Review error and retry assessment"],
            execution_time=0.0,
            priority=Priority.HIGH,
            timestamp=datetime.now(),
            agent_id=agent_id,
            details={"error": error},
        )

    def get_assessment_summary(self) -> dict[str, Any]:
        """Get assessment summary."""
        if not self.assessments:
            return {"total_assessments": 0}

        total_assessments = len(self.assessments)
        completed = len([a for a in self.assessments if a.status == TaskStatus.COMPLETED])
        failed = len([a for a in self.assessments if a.status == TaskStatus.FAILED])
        avg_score = sum(a.score for a in self.assessments) / total_assessments

        return {
            "total_assessments": total_assessments,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total_assessments * 100) if total_assessments > 0 else 0,
            "average_score": avg_score,
            "latest_assessment": self.assessments[-1].to_dict() if self.assessments else None,
        }
