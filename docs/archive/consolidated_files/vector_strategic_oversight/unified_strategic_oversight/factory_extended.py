"""
Strategic Oversight Factory Extended
===================================

Extended factory methods for creating complex strategic oversight models.
V2 Compliance: < 150 lines, single responsibility, extended factory methods.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

import uuid
from datetime import datetime

from .core_models import (
    AgentPerformanceMetrics,
    StrategicMission,
    StrategicOversightReport,
    StrategicRecommendation,
    SwarmCoordinationInsight,
    SystemHealthMetrics,
    VectorDatabaseMetrics,
)
from .enums import (
    EmergencyStatus,
    ImpactLevel,
    InsightType,
    MissionStatus,
    PriorityLevel,
    ReportType,
)


class StrategicOversightFactoryExtended:
    """Extended factory methods for strategic oversight models."""

    @staticmethod
    def create_vector_database_metrics(
        database_id: str,
        query_count: int = 0,
        response_time: float = 0.0,
        accuracy: float = 1.0,
        memory_usage: float = 0.0,
        index_size: int = 0,
    ) -> VectorDatabaseMetrics:
        """Create vector database metrics."""
        return VectorDatabaseMetrics(
            metrics_id=str(uuid.uuid4()),
            database_id=database_id,
            query_count=query_count,
            response_time=response_time,
            accuracy=accuracy,
            memory_usage=memory_usage,
            index_size=index_size,
            timestamp=datetime.now(),
        )

    @staticmethod
    def create_system_health_metrics(
        system_id: str,
        cpu_usage: float = 0.0,
        memory_usage: float = 0.0,
        disk_usage: float = 0.0,
        network_latency: float = 0.0,
        error_rate: float = 0.0,
        uptime: float = 0.0,
    ) -> SystemHealthMetrics:
        """Create system health metrics."""
        return SystemHealthMetrics(
            metrics_id=str(uuid.uuid4()),
            system_id=system_id,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_latency=network_latency,
            error_rate=error_rate,
            uptime=uptime,
            timestamp=datetime.now(),
        )

    @staticmethod
    def create_comprehensive_report(
        title: str,
        description: str,
        insights: list[SwarmCoordinationInsight] = None,
        recommendations: list[StrategicRecommendation] = None,
        performance_metrics: list[AgentPerformanceMetrics] = None,
        system_metrics: list[SystemHealthMetrics] = None,
    ) -> StrategicOversightReport:
        """Create comprehensive strategic oversight report."""
        return StrategicOversightReport(
            report_id=str(uuid.uuid4()),
            title=title,
            description=description,
            report_type=ReportType.COMPREHENSIVE,
            insights=insights or [],
            recommendations=recommendations or [],
            metrics={
                "performance_metrics": performance_metrics or [],
                "system_metrics": system_metrics or [],
                "total_insights": len(insights or []),
                "total_recommendations": len(recommendations or []),
            },
            created_at=datetime.now(),
            status=MissionStatus.ACTIVE,
        )

    @staticmethod
    def create_emergency_insight(
        description: str,
        affected_agents: list[str] = None,
        emergency_level: EmergencyStatus = EmergencyStatus.WARNING,
        immediate_actions: list[str] = None,
    ) -> SwarmCoordinationInsight:
        """Create emergency coordination insight."""
        return SwarmCoordinationInsight(
            insight_id=str(uuid.uuid4()),
            insight_type=InsightType.COORDINATION,
            description=description,
            confidence=0.9,  # High confidence for emergencies
            impact_score=0.8,  # High impact for emergencies
            affected_agents=affected_agents or [],
            recommendations=immediate_actions or [],
            generated_at=datetime.now(),
        )

    @staticmethod
    def create_high_priority_recommendation(
        title: str,
        description: str,
        expected_impact: ImpactLevel = ImpactLevel.HIGH,
        implementation_effort: str = "high",
        success_probability: float = 0.9,
        dependencies: list[str] = None,
    ) -> StrategicRecommendation:
        """Create high priority strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=1,  # Highest priority
            expected_impact=expected_impact,
            implementation_effort=implementation_effort,
            success_probability=success_probability,
            dependencies=dependencies or [],
            created_at=datetime.now(),
        )

    @staticmethod
    def create_mission_batch(
        mission_names: list[str],
        descriptions: list[str],
        priorities: list[PriorityLevel] = None,
        assigned_agents: list[list[str]] = None,
    ) -> list[StrategicMission]:
        """Create batch of strategic missions."""
        missions = []
        for i, name in enumerate(mission_names):
            mission = StrategicMission(
                mission_id=str(uuid.uuid4()),
                mission_name=name,
                description=descriptions[i] if i < len(descriptions) else "",
                priority=(
                    priorities[i] if priorities and i < len(priorities) else PriorityLevel.MEDIUM
                ),
                status=MissionStatus.PENDING,
                assigned_agents=(
                    assigned_agents[i] if assigned_agents and i < len(assigned_agents) else []
                ),
                created_at=datetime.now(),
            )
            missions.append(mission)
        return missions
