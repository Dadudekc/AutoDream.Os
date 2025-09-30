#!/usr/bin/env python3
"""
Integration Assessment Engine - Assessment logic for Comprehensive Integration Assessment
==================================================================================

Assessment logic extracted from comprehensive_integration_assessment.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import platform
from datetime import datetime
from typing import Any

from .integration_models import (
    AssessmentArea,
    AssessmentStatus,
    ComponentInfo,
    IntegrationAssessment,
    PlatformCompatibility,
    PlatformType,
    Priority,
)

logger = logging.getLogger(__name__)


class IntegrationAssessmentEngine:
    """Integration assessment engine for comprehensive evaluation."""

    def __init__(self):
        """Initialize integration assessment engine."""
        self.assessments: list[IntegrationAssessment] = []
        self.platform_compatibilities: dict[str, PlatformCompatibility] = {}
        self.components: dict[str, ComponentInfo] = {}
        self.current_platform = self._detect_platform()
        logger.info("Integration assessment engine initialized")

    def _detect_platform(self) -> PlatformType:
        """Detect current platform."""
        system = platform.system().lower()
        if system == "windows":
            return PlatformType.WINDOWS
        elif system == "linux":
            return PlatformType.LINUX
        elif system == "darwin":
            return PlatformType.MACOS
        else:
            return PlatformType.UNKNOWN

    def register_component(self, component: ComponentInfo):
        """Register a component for assessment."""
        self.components[component.component_id] = component
        logger.info(f"Component registered: {component.component_id}")

    def assess_component(self, component_id: str, area: AssessmentArea) -> IntegrationAssessment:
        """Assess a specific component in a specific area."""
        if component_id not in self.components:
            return self._create_failed_assessment(component_id, area, "Component not registered")

        component = self.components[component_id]

        try:
            if area == AssessmentArea.CROSS_PLATFORM:
                return self._assess_cross_platform(component)
            elif area == AssessmentArea.PERFORMANCE:
                return self._assess_performance(component)
            elif area == AssessmentArea.REPOSITORY_AUTOMATION:
                return self._assess_repository_automation(component)
            elif area == AssessmentArea.INTEGRATION_TESTING:
                return self._assess_integration_testing(component)
            else:
                return self._assess_generic_area(component, area)

        except Exception as e:
            logger.error(f"Error assessing component {component_id} in area {area.value}: {e}")
            return self._create_failed_assessment(component_id, area, str(e))

    def _assess_cross_platform(self, component: ComponentInfo) -> IntegrationAssessment:
        """Assess cross-platform compatibility."""
        issues = []
        recommendations = []
        score = 85.0  # Base score

        # Check platform requirements
        if not component.is_multi_platform():
            issues.append("Component not designed for multi-platform support")
            score -= 20
        else:
            recommendations.append("Good multi-platform design")

        # Check current platform compatibility
        if self.current_platform not in component.platform_requirements:
            issues.append(f"Current platform {self.current_platform.value} not supported")
            score -= 25
        else:
            recommendations.append(f"Current platform {self.current_platform.value} supported")

        # Check platform-specific dependencies
        platform_deps = component.configuration.get("platform_dependencies", {})
        if platform_deps:
            current_deps = platform_deps.get(self.current_platform.value, [])
            if not current_deps:
                issues.append("No platform-specific dependencies configured")
                score -= 10

        return IntegrationAssessment(
            area=AssessmentArea.CROSS_PLATFORM,
            component=component.name,
            assessment_score=score,
            issues=issues,
            recommendations=recommendations,
            priority=Priority.HIGH if score < 70 else Priority.MEDIUM,
            estimated_effort=3 if score < 70 else 1,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.COMPLETED,
            details={
                "component_id": component.component_id,
                "platform": self.current_platform.value,
            },
        )

    def _assess_performance(self, component: ComponentInfo) -> IntegrationAssessment:
        """Assess performance characteristics."""
        issues = []
        recommendations = []
        score = 80.0  # Base score

        # Check performance configuration
        perf_config = component.configuration.get("performance", {})
        if not perf_config:
            issues.append("No performance configuration found")
            score -= 15
        else:
            recommendations.append("Performance configuration present")

        # Check resource requirements
        memory_req = component.configuration.get("memory_requirements", 0)
        if memory_req > 1000:  # More than 1GB
            issues.append("High memory requirements detected")
            score -= 10

        # Check caching configuration
        cache_config = component.configuration.get("caching", {})
        if not cache_config.get("enabled", False):
            issues.append("Caching not enabled")
            score -= 5
        else:
            recommendations.append("Caching enabled")

        return IntegrationAssessment(
            area=AssessmentArea.PERFORMANCE,
            component=component.name,
            assessment_score=score,
            issues=issues,
            recommendations=recommendations,
            priority=Priority.HIGH if score < 70 else Priority.MEDIUM,
            estimated_effort=2 if score < 70 else 1,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.COMPLETED,
            details={"component_id": component.component_id, "performance_config": perf_config},
        )

    def _assess_repository_automation(self, component: ComponentInfo) -> IntegrationAssessment:
        """Assess repository automation capabilities."""
        issues = []
        recommendations = []
        score = 75.0  # Base score

        # Check automation configuration
        automation_config = component.configuration.get("automation", {})
        if not automation_config:
            issues.append("No automation configuration found")
            score -= 20
        else:
            recommendations.append("Automation configuration present")

        # Check CI/CD integration
        ci_config = automation_config.get("ci_cd", {})
        if not ci_config.get("enabled", False):
            issues.append("CI/CD integration not enabled")
            score -= 15
        else:
            recommendations.append("CI/CD integration enabled")

        # Check automated testing
        test_config = automation_config.get("testing", {})
        if not test_config.get("automated", False):
            issues.append("Automated testing not configured")
            score -= 10
        else:
            recommendations.append("Automated testing configured")

        return IntegrationAssessment(
            area=AssessmentArea.REPOSITORY_AUTOMATION,
            component=component.name,
            assessment_score=score,
            issues=issues,
            recommendations=recommendations,
            priority=Priority.HIGH if score < 70 else Priority.MEDIUM,
            estimated_effort=4 if score < 70 else 2,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.COMPLETED,
            details={
                "component_id": component.component_id,
                "automation_config": automation_config,
            },
        )

    def _assess_integration_testing(self, component: ComponentInfo) -> IntegrationAssessment:
        """Assess integration testing capabilities."""
        issues = []
        recommendations = []
        score = 70.0  # Base score

        # Check test configuration
        test_config = component.configuration.get("testing", {})
        if not test_config:
            issues.append("No testing configuration found")
            score -= 25
        else:
            recommendations.append("Testing configuration present")

        # Check integration test coverage
        integration_tests = test_config.get("integration_tests", [])
        if not integration_tests:
            issues.append("No integration tests configured")
            score -= 20
        else:
            recommendations.append(f"{len(integration_tests)} integration tests configured")

        # Check test automation
        if not test_config.get("automated", False):
            issues.append("Integration tests not automated")
            score -= 10
        else:
            recommendations.append("Integration tests automated")

        return IntegrationAssessment(
            area=AssessmentArea.INTEGRATION_TESTING,
            component=component.name,
            assessment_score=score,
            issues=issues,
            recommendations=recommendations,
            priority=Priority.HIGH if score < 70 else Priority.MEDIUM,
            estimated_effort=3 if score < 70 else 1,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.COMPLETED,
            details={"component_id": component.component_id, "test_config": test_config},
        )

    def _assess_generic_area(
        self, component: ComponentInfo, area: AssessmentArea
    ) -> IntegrationAssessment:
        """Assess generic area."""
        return IntegrationAssessment(
            area=area,
            component=component.name,
            assessment_score=75.0,
            issues=[],
            recommendations=["Generic assessment completed"],
            priority=Priority.MEDIUM,
            estimated_effort=1,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.COMPLETED,
            details={"component_id": component.component_id, "area": area.value},
        )

    def _create_failed_assessment(
        self, component_id: str, area: AssessmentArea, error: str
    ) -> IntegrationAssessment:
        """Create a failed assessment."""
        return IntegrationAssessment(
            area=area,
            component=component_id,
            assessment_score=0.0,
            issues=[f"Assessment failed: {error}"],
            recommendations=["Review error and retry assessment"],
            priority=Priority.CRITICAL,
            estimated_effort=5,
            timestamp=datetime.now().isoformat(),
            status=AssessmentStatus.FAILED,
            details={"error": error},
        )

    def get_assessment_summary(self) -> dict[str, Any]:
        """Get assessment summary."""
        if not self.assessments:
            return {"total_assessments": 0}

        total_assessments = len(self.assessments)
        completed = len([a for a in self.assessments if a.status == AssessmentStatus.COMPLETED])
        failed = len([a for a in self.assessments if a.status == AssessmentStatus.FAILED])
        critical = len([a for a in self.assessments if a.priority == Priority.CRITICAL])
        avg_score = sum(a.assessment_score for a in self.assessments) / total_assessments

        return {
            "total_assessments": total_assessments,
            "completed": completed,
            "failed": failed,
            "critical_issues": critical,
            "success_rate": (completed / total_assessments * 100) if total_assessments > 0 else 0,
            "average_score": avg_score,
            "components_assessed": len(set(a.component for a in self.assessments)),
            "platform": self.current_platform.value,
        }
