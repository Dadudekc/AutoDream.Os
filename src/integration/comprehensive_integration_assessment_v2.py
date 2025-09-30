#!/usr/bin/env python3
"""
Comprehensive Integration Assessment V2 - V2 Compliant
==================================================

V2 compliant version of Comprehensive Integration Assessment using modular architecture.
Maintains all functionality while achieving V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .integration_assessment_engine import IntegrationAssessmentEngine
from .integration_models import (
    AssessmentArea,
    AssessmentConfiguration,
    ComponentInfo,
    IntegrationAssessment,
    IntegrationReport,
    Priority,
)

logger = logging.getLogger(__name__)


class ComprehensiveIntegrationAssessmentV2:
    """V2 compliant Comprehensive Integration Assessment System."""

    def __init__(self, config: AssessmentConfiguration = None):
        """Initialize V2 integration assessment system."""
        self.config = config or AssessmentConfiguration(
            max_concurrent_assessments=5,
            timeout_seconds=300.0,
            quality_threshold=0.8,
            auto_retry=True,
            retry_attempts=3,
            notification_enabled=True,
            detailed_logging=True,
        )

        self.assessment_engine = IntegrationAssessmentEngine()
        self.assessments: list[IntegrationAssessment] = []
        self.components: dict[str, ComponentInfo] = {}
        self.current_report: IntegrationReport | None = None

        logger.info("Comprehensive Integration Assessment V2 initialized")

    def register_component(self, component: ComponentInfo):
        """Register a component for assessment."""
        self.assessment_engine.register_component(component)
        self.components[component.component_id] = component
        logger.info(f"Component registered: {component.component_id}")

    def assess_all_components(self, areas: list[AssessmentArea] = None) -> dict[str, Any]:
        """Assess all registered components in specified areas."""
        if areas is None:
            areas = list(AssessmentArea)

        try:
            assessments = []
            for component_id in self.components.keys():
                for area in areas:
                    assessment = self.assessment_engine.assess_component(component_id, area)
                    assessments.append(assessment)
                    self.assessments.append(assessment)

            # Generate comprehensive report
            report = self._generate_integration_report()
            self.current_report = report

            logger.info(f"Assessment completed: {len(assessments)} assessments generated")

            return {
                "success": True,
                "total_assessments": len(assessments),
                "components_assessed": len(self.components),
                "areas_assessed": len(areas),
                "report": report.__dict__,
                "summary": self._get_assessment_summary(),
            }

        except Exception as e:
            logger.error(f"Error in comprehensive assessment: {e}")
            return {"success": False, "error": str(e)}

    def assess_component_area(self, component_id: str, area: AssessmentArea) -> dict[str, Any]:
        """Assess a specific component in a specific area."""
        try:
            if component_id not in self.components:
                return {"success": False, "error": f"Component {component_id} not registered"}

            assessment = self.assessment_engine.assess_component(component_id, area)
            self.assessments.append(assessment)

            logger.info(f"Component assessment completed: {component_id} - {area.value}")

            return {
                "success": True,
                "assessment": assessment.to_dict(),
                "component_id": component_id,
                "area": area.value,
            }

        except Exception as e:
            logger.error(f"Error assessing component {component_id}: {e}")
            return {"success": False, "error": str(e)}

    def get_assessment_report(self) -> dict[str, Any]:
        """Get comprehensive assessment report."""
        if not self.current_report:
            return {
                "success": False,
                "error": "No assessment report available. Run assessment first.",
            }

        return {
            "success": True,
            "report": self.current_report.__dict__,
            "summary": self._get_assessment_summary(),
            "recommendations": self._get_top_recommendations(),
        }

    def get_component_status(self, component_id: str) -> dict[str, Any]:
        """Get status for a specific component."""
        if component_id not in self.components:
            return {"success": False, "error": f"Component {component_id} not registered"}

        component_assessments = [
            a for a in self.assessments if a.details.get("component_id") == component_id
        ]

        if not component_assessments:
            return {"success": False, "error": f"No assessments found for component {component_id}"}

        avg_score = sum(a.assessment_score for a in component_assessments) / len(
            component_assessments
        )
        critical_issues = len([a for a in component_assessments if a.priority == Priority.CRITICAL])

        return {
            "success": True,
            "component_id": component_id,
            "total_assessments": len(component_assessments),
            "average_score": avg_score,
            "critical_issues": critical_issues,
            "assessments": [a.to_dict() for a in component_assessments],
            "overall_health": self._get_health_status(avg_score),
        }

    def _generate_integration_report(self) -> IntegrationReport:
        """Generate comprehensive integration report."""
        total_components = len(self.components)
        assessed_components = len(set(a.details.get("component_id") for a in self.assessments))

        # Calculate overall score
        overall_score = (
            sum(a.assessment_score for a in self.assessments) / len(self.assessments)
            if self.assessments
            else 0.0
        )

        # Count issues by priority
        critical_issues = len([a for a in self.assessments if a.priority == Priority.CRITICAL])
        high_priority_issues = len([a for a in self.assessments if a.priority == Priority.HIGH])

        # Collect all recommendations
        all_recommendations = []
        for assessment in self.assessments:
            all_recommendations.extend(assessment.recommendations)

        # Generate summary
        summary = self._generate_report_summary(
            overall_score, critical_issues, high_priority_issues
        )

        return IntegrationReport(
            report_id=f"integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            assessment_date=datetime.now(),
            overall_score=overall_score,
            total_components=total_components,
            assessed_components=assessed_components,
            critical_issues=critical_issues,
            high_priority_issues=high_priority_issues,
            recommendations_count=len(all_recommendations),
            platform_compatibility={},  # TODO: Implement platform compatibility assessment
            performance_metrics=None,  # TODO: Implement performance metrics collection
            assessments=self.assessments,
            summary=summary,
        )

    def _generate_report_summary(
        self, overall_score: float, critical_issues: int, high_priority_issues: int
    ) -> str:
        """Generate report summary."""
        if overall_score >= 90:
            health_status = "excellent"
        elif overall_score >= 75:
            health_status = "good"
        elif overall_score >= 60:
            health_status = "acceptable"
        else:
            health_status = "poor"

        summary = f"Integration Assessment Summary: Overall health is {health_status} "
        summary += f"(score: {overall_score:.1f}/100). "

        if critical_issues > 0:
            summary += f"CRITICAL: {critical_issues} critical issues require immediate attention. "

        if high_priority_issues > 0:
            summary += f"HIGH: {high_priority_issues} high priority issues need resolution. "

        summary += f"Total components assessed: {len(self.components)}. "
        summary += "See detailed recommendations for improvement steps."

        return summary

    def _get_assessment_summary(self) -> dict[str, Any]:
        """Get assessment summary."""
        return self.assessment_engine.get_assessment_summary()

    def _get_top_recommendations(self, limit: int = 5) -> list[str]:
        """Get top recommendations."""
        all_recommendations = []
        for assessment in self.assessments:
            all_recommendations.extend(assessment.recommendations)

        # Remove duplicates and return top recommendations
        unique_recommendations = list(set(all_recommendations))
        return unique_recommendations[:limit]

    def _get_health_status(self, score: float) -> str:
        """Get health status based on score."""
        if score >= 90:
            return "excellent"
        elif score >= 75:
            return "good"
        elif score >= 60:
            return "acceptable"
        else:
            return "poor"

    def validate_system_integrity(self) -> dict[str, Any]:
        """Validate system integrity."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "components_checked": len(self.components),
        }

        # Validate configuration
        if not self.config.is_valid():
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid assessment configuration")

        # Check registered components
        if not self.components:
            validation_result["warnings"].append("No components registered for assessment")

        # Check assessment engine
        summary = self.assessment_engine.get_assessment_summary()
        if summary["total_assessments"] == 0:
            validation_result["warnings"].append("No assessments performed yet")

        return validation_result
