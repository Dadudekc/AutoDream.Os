"""
Strategic Oversight Factory Core
================================

Core factory methods for creating strategic oversight models.
V2 Compliance: < 150 lines, single responsibility, core factory methods.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .enums import (
    InsightType,
    ConfidenceLevel,
    ImpactLevel,
    MissionStatus,
    ReportType,
    PriorityLevel,
    AgentRole,
    EmergencyStatus,
)
from .core_models import (
    StrategicOversightReport,
    SwarmCoordinationInsight,
    StrategicRecommendation,
    AgentPerformanceMetrics,
    SwarmCoordinationStatus,
    StrategicMission,
    VectorDatabaseMetrics,
    SystemHealthMetrics,
)


class StrategicOversightFactoryCore:
    """Core factory methods for strategic oversight models."""

    @staticmethod
    def create_strategic_oversight_report(
        title: str,
        description: str,
        report_type: ReportType,
        insights: List[Any] = None,
        recommendations: List[Any] = None,
        metrics: Dict[str, Any] = None,
    ) -> StrategicOversightReport:
        """Create strategic oversight report."""
        return StrategicOversightReport(
            report_id=str(uuid.uuid4()),
            title=title,
            description=description,
            report_type=report_type,
            insights=insights or [],
            recommendations=recommendations or [],
            metrics=metrics or {},
            generated_at=datetime.now(),
            created_at=datetime.now(),
        )

    @staticmethod
    def create_swarm_coordination_insight(
        insight_type: InsightType,
        title: str,
        description: str,
        confidence: ConfidenceLevel = ConfidenceLevel.HIGH,
        impact: ImpactLevel = ImpactLevel.MEDIUM,
        evidence: List[str] = None,
        recommendations: List[str] = None,
    ) -> SwarmCoordinationInsight:
        """Create swarm coordination insight."""
        return SwarmCoordinationInsight(
            insight_id=str(uuid.uuid4()),
            insight_type=insight_type,
            title=title,
            description=description,
            confidence=confidence,
            impact=impact,
            evidence=evidence or [],
            recommendations=recommendations or [],
            created_at=datetime.now(),
        )

    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        impact: ImpactLevel = ImpactLevel.MEDIUM,
        implementation_effort: str = "medium",
        expected_benefits: List[str] = None,
        risks: List[str] = None,
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            impact=impact,
            implementation_effort=implementation_effort,
            expected_benefits=expected_benefits or [],
            risks=risks or [],
            created_at=datetime.now(),
        )

    @staticmethod
    def create_agent_performance_metrics(
        agent_id: str,
        agent_role: AgentRole,
        performance_score: float = 0.8,
        efficiency: float = 0.8,
        coordination_score: float = 0.8,
        task_completion_rate: float = 0.8,
        response_time: float = 0.1,
    ) -> AgentPerformanceMetrics:
        """Create agent performance metrics."""
        return AgentPerformanceMetrics(
            metrics_id=str(uuid.uuid4()),
            agent_id=agent_id,
            agent_role=agent_role,
            performance_score=performance_score,
            efficiency=efficiency,
            coordination_score=coordination_score,
            task_completion_rate=task_completion_rate,
            response_time=response_time,
            created_at=datetime.now(),
        )

    @staticmethod
    def create_swarm_coordination_status(
        status_name: str,
        description: str,
        active_agents: List[str] = None,
        coordination_level: str = "medium",
        efficiency_score: float = 0.8,
    ) -> SwarmCoordinationStatus:
        """Create swarm coordination status."""
        return SwarmCoordinationStatus(
            status_id=str(uuid.uuid4()),
            status_name=status_name,
            description=description,
            active_agents=active_agents or [],
            coordination_level=coordination_level,
            efficiency_score=efficiency_score,
            created_at=datetime.now(),
        )

    @staticmethod
    def create_strategic_mission(
        mission_name: str,
        description: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        status: MissionStatus = MissionStatus.PENDING,
        assigned_agents: List[str] = None,
        target_date: Optional[datetime] = None,
    ) -> StrategicMission:
        """Create strategic mission."""
        return StrategicMission(
            mission_id=str(uuid.uuid4()),
            mission_name=mission_name,
            description=description,
            priority=priority,
            status=status,
            assigned_agents=assigned_agents or [],
            target_date=target_date,
            created_at=datetime.now(),
        )
