"""
Strategic Oversight Factory Methods - V2 Compliance Refactored
=============================================================

Factory methods for creating strategic oversight data models.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime

from .data_models import (
    AgentPerformanceMetrics,
    StrategicMission,
    StrategicOversightReport,
    StrategicRecommendation,
    SwarmCoordinationInsight,
    SwarmCoordinationStatus,
    SystemHealthMetrics,
    VectorDatabaseMetrics,
)
from .enums import AgentRole, ConfidenceLevel, ImpactLevel, PriorityLevel, ReportType
from .factories.metrics_factory import MetricsFactory
from .factories.mission_factory import MissionFactory

# Import modular factory components
from .factories.report_factory import ReportFactory


class StrategicOversightFactory:
    """Factory class for creating strategic oversight data models - V2 compliant."""

    def __init__(self):
        """Initialize factory with modular components."""
        self.report_factory = ReportFactory()
        self.metrics_factory = MetricsFactory()
        self.mission_factory = MissionFactory()

    # Delegate report creation to ReportFactory
    def create_oversight_report(
        self,
        report_type: ReportType,
        title: str,
        summary: str,
        insights: list[SwarmCoordinationInsight] = None,
        recommendations: list[StrategicRecommendation] = None,
        confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM,
        impact_level: ImpactLevel = ImpactLevel.MEDIUM,
    ) -> StrategicOversightReport:
        """Create strategic oversight report."""
        return self.report_factory.create_oversight_report(
            report_type,
            title,
            summary,
            insights,
            recommendations,
            confidence_level,
            impact_level,
        )

    def create_swarm_insight(
        self,
        insight_type: str,
        description: str,
        confidence_score: float,
        impact_score: float,
        source_agent: str = None,
        related_metrics: dict = None,
    ) -> SwarmCoordinationInsight:
        """Create swarm coordination insight."""
        return self.report_factory.create_swarm_insight(
            insight_type,
            description,
            confidence_score,
            impact_score,
            source_agent,
            related_metrics,
        )

    def create_strategic_recommendation(
        self,
        title: str,
        description: str,
        priority: str,
        implementation_steps: list[str],
        expected_impact: str,
        resource_requirements: str = None,
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return self.report_factory.create_strategic_recommendation(
            title,
            description,
            priority,
            implementation_steps,
            expected_impact,
            resource_requirements,
        )

    # Delegate metrics creation to MetricsFactory
    def create_agent_performance_metrics(
        self,
        agent_id: str,
        agent_name: str,
        role: AgentRole,
        performance_score: float,
        efficiency_rating: float,
        coordination_effectiveness: float,
        task_completion_rate: float,
        response_time_avg: float,
    ) -> AgentPerformanceMetrics:
        """Create agent performance metrics."""
        return self.metrics_factory.create_agent_performance_metrics(
            agent_id,
            agent_name,
            role,
            performance_score,
            efficiency_rating,
            coordination_effectiveness,
            task_completion_rate,
            response_time_avg,
        )

    def create_swarm_coordination_status(
        self,
        total_agents: int,
        active_agents: int,
        coordination_health: float,
        communication_efficiency: float,
        task_distribution_balance: float,
        overall_swarm_effectiveness: float,
        status_notes: str = None,
    ) -> SwarmCoordinationStatus:
        """Create swarm coordination status."""
        return self.metrics_factory.create_swarm_coordination_status(
            total_agents,
            active_agents,
            coordination_health,
            communication_efficiency,
            task_distribution_balance,
            overall_swarm_effectiveness,
            status_notes,
        )

    def create_vector_database_metrics(
        self,
        total_vectors: int,
        query_performance: float,
        index_efficiency: float,
        memory_usage: float,
        cache_hit_rate: float,
        search_accuracy: float,
    ) -> VectorDatabaseMetrics:
        """Create vector database metrics."""
        return self.metrics_factory.create_vector_database_metrics(
            total_vectors,
            query_performance,
            index_efficiency,
            memory_usage,
            cache_hit_rate,
            search_accuracy,
        )

    def create_system_health_metrics(
        self,
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
        network_latency: float,
        error_rate: float,
        uptime: float,
    ) -> SystemHealthMetrics:
        """Create system health metrics."""
        return self.metrics_factory.create_system_health_metrics(
            cpu_usage, memory_usage, disk_usage, network_latency, error_rate, uptime
        )

    # Delegate mission creation to MissionFactory
    def create_strategic_mission(
        self,
        title: str,
        description: str,
        priority: PriorityLevel,
        assigned_agents: list[str],
        objectives: list[str],
        success_criteria: list[str],
        deadline: datetime | None = None,
        dependencies: list[str] = None,
    ) -> StrategicMission:
        """Create strategic mission."""
        return self.mission_factory.create_strategic_mission(
            title,
            description,
            priority,
            assigned_agents,
            objectives,
            success_criteria,
            deadline,
            dependencies,
        )

    def create_quick_mission(
        self, title: str, description: str, assigned_agent: str, objective: str
    ) -> StrategicMission:
        """Create quick mission with minimal parameters."""
        return self.mission_factory.create_quick_mission(
            title, description, assigned_agent, objective
        )

    def create_emergency_mission(
        self,
        title: str,
        description: str,
        assigned_agents: list[str],
        objectives: list[str],
    ) -> StrategicMission:
        """Create emergency mission with high priority."""
        return self.mission_factory.create_emergency_mission(
            title, description, assigned_agents, objectives
        )


# Global factory instance for backward compatibility
_global_factory = None


def get_strategic_oversight_factory() -> StrategicOversightFactory:
    """Get global strategic oversight factory instance."""
    global _global_factory

    if _global_factory is None:
        _global_factory = StrategicOversightFactory()

    return _global_factory


# Backward compatibility functions
def create_oversight_report(*args, **kwargs) -> StrategicOversightReport:
    """Create strategic oversight report."""
    return get_strategic_oversight_factory().create_oversight_report(*args, **kwargs)


def create_swarm_insight(*args, **kwargs) -> SwarmCoordinationInsight:
    """Create swarm coordination insight."""
    return get_strategic_oversight_factory().create_swarm_insight(*args, **kwargs)


def create_strategic_recommendation(*args, **kwargs) -> StrategicRecommendation:
    """Create strategic recommendation."""
    return get_strategic_oversight_factory().create_strategic_recommendation(*args, **kwargs)


def create_agent_performance_metrics(*args, **kwargs) -> AgentPerformanceMetrics:
    """Create agent performance metrics."""
    return get_strategic_oversight_factory().create_agent_performance_metrics(*args, **kwargs)


def create_swarm_coordination_status(*args, **kwargs) -> SwarmCoordinationStatus:
    """Create swarm coordination status."""
    return get_strategic_oversight_factory().create_swarm_coordination_status(*args, **kwargs)


def create_strategic_mission(*args, **kwargs) -> StrategicMission:
    """Create strategic mission."""
    return get_strategic_oversight_factory().create_strategic_mission(*args, **kwargs)


def create_vector_database_metrics(*args, **kwargs) -> VectorDatabaseMetrics:
    """Create vector database metrics."""
    return get_strategic_oversight_factory().create_vector_database_metrics(*args, **kwargs)


def create_system_health_metrics(*args, **kwargs) -> SystemHealthMetrics:
    """Create system health metrics."""
    return get_strategic_oversight_factory().create_system_health_metrics(*args, **kwargs)
