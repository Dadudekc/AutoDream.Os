"""
Strategic Oversight Report Factory - V2 Compliance Module
========================================================

Factory methods for creating strategic oversight reports.

V2 Compliance: < 300 lines, single responsibility, report factory.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional
from datetime import datetime
import uuid

from ..enums import ReportType, ConfidenceLevel, ImpactLevel
from ..data_models import (
    SwarmCoordinationInsight, StrategicRecommendation, StrategicOversightReport
)


class ReportFactory:
    """Factory class for creating strategic oversight reports."""
    
    @staticmethod
    def create_oversight_report(
        report_type: ReportType,
        title: str,
        summary: str,
        insights: List[SwarmCoordinationInsight] = None,
        recommendations: List[StrategicRecommendation] = None,
        confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM,
        impact_level: ImpactLevel = ImpactLevel.MEDIUM
    ) -> StrategicOversightReport:
        """Create strategic oversight report."""
        return StrategicOversightReport(
            report_id=str(uuid.uuid4()),
            report_type=report_type,
            title=title,
            summary=summary,
            insights=insights or [],
            recommendations=recommendations or [],
            confidence_level=confidence_level,
            impact_level=impact_level,
            generated_at=datetime.now()
        )
    
    @staticmethod
    def create_swarm_insight(
        insight_type: str,
        description: str,
        confidence_score: float,
        impact_score: float,
        source_agent: str = None,
        related_metrics: dict = None
    ) -> SwarmCoordinationInsight:
        """Create swarm coordination insight."""
        return SwarmCoordinationInsight(
            insight_id=str(uuid.uuid4()),
            insight_type=insight_type,
            description=description,
            confidence_score=confidence_score,
            impact_score=impact_score,
            source_agent=source_agent,
            related_metrics=related_metrics or {},
            generated_at=datetime.now()
        )
    
    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        priority: str,
        implementation_steps: List[str],
        expected_impact: str,
        resource_requirements: str = None
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            implementation_steps=implementation_steps,
            expected_impact=expected_impact,
            resource_requirements=resource_requirements,
            created_at=datetime.now()
        )
