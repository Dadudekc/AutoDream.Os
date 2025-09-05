"""
Strategic Oversight Factory Methods - V2 Compliance Module
=========================================================

Factory methods for creating strategic oversight data models.

V2 Compliance: < 300 lines, single responsibility, factory pattern.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from .enums import InsightType, ConfidenceLevel, ImpactLevel, ReportType, PriorityLevel, AgentRole
from .data_models import (
    SwarmCoordinationInsight, StrategicRecommendation, StrategicOversightReport,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics
)


class StrategicOversightFactory:
    """Factory class for creating strategic oversight data models."""
    
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
        insight_type: InsightType,
        description: str,
        confidence: float,
        impact_score: float,
        affected_agents: List[str] = None,
        recommendations: List[str] = None
    ) -> SwarmCoordinationInsight:
        """Create swarm coordination insight."""
        return SwarmCoordinationInsight(
            insight_id=str(uuid.uuid4()),
            insight_type=insight_type,
            description=description,
            confidence=confidence,
            impact_score=impact_score,
            affected_agents=affected_agents or [],
            recommendations=recommendations or [],
            generated_at=datetime.now()
        )
    
    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        priority: int,
        expected_impact: ImpactLevel,
        implementation_effort: str,
        success_probability: float,
        dependencies: List[str] = None
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            expected_impact=expected_impact,
            implementation_effort=implementation_effort,
            success_probability=success_probability,
            dependencies=dependencies or [],
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_agent_performance_metrics(
        agent_id: str,
        agent_name: str,
        role: AgentRole,
        performance_score: float,
        efficiency_rating: float,
        coordination_effectiveness: float,
        task_completion_rate: float,
        response_time_avg: float
    ) -> AgentPerformanceMetrics:
        """Create agent performance metrics."""
        return AgentPerformanceMetrics(
            agent_id=agent_id,
            agent_name=agent_name,
            role=role,
            performance_score=performance_score,
            efficiency_rating=efficiency_rating,
            coordination_effectiveness=coordination_effectiveness,
            task_completion_rate=task_completion_rate,
            response_time_avg=response_time_avg,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_swarm_coordination_status(
        total_agents: int,
        active_agents: int,
        coordination_health: float,
        communication_efficiency: float,
        task_distribution_balance: float,
        overall_swarm_effectiveness: float,
        status_notes: str = None
    ) -> SwarmCoordinationStatus:
        """Create swarm coordination status."""
        return SwarmCoordinationStatus(
            status_id=str(uuid.uuid4()),
            total_agents=total_agents,
            active_agents=active_agents,
            coordination_health=coordination_health,
            communication_efficiency=communication_efficiency,
            task_distribution_balance=task_distribution_balance,
            overall_swarm_effectiveness=overall_swarm_effectiveness,
            last_updated=datetime.now(),
            status_notes=status_notes
        )
    
    @staticmethod
    def create_strategic_mission(
        title: str,
        description: str,
        priority: PriorityLevel,
        assigned_agents: List[str],
        objectives: List[str],
        success_criteria: List[str]
    ) -> StrategicMission:
        """Create strategic mission."""
        return StrategicMission(
            mission_id=str(uuid.uuid4()),
            title=title,
            description=description,
            status=MissionStatus.PLANNING,
            priority=priority,
            assigned_agents=assigned_agents,
            objectives=objectives,
            success_criteria=success_criteria,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_vector_database_metrics(
        total_vectors: int,
        query_performance: float,
        indexing_efficiency: float,
        search_accuracy: float,
        memory_usage: float,
        optimization_recommendations: List[str] = None
    ) -> VectorDatabaseMetrics:
        """Create vector database metrics."""
        return VectorDatabaseMetrics(
            metrics_id=str(uuid.uuid4()),
            total_vectors=total_vectors,
            query_performance=query_performance,
            indexing_efficiency=indexing_efficiency,
            search_accuracy=search_accuracy,
            memory_usage=memory_usage,
            last_optimization=datetime.now(),
            optimization_recommendations=optimization_recommendations or []
        )
    
    @staticmethod
    def create_system_health_metrics(
        overall_health_score: float,
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
        network_latency: float,
        error_rate: float,
        uptime_percentage: float
    ) -> SystemHealthMetrics:
        """Create system health metrics."""
        return SystemHealthMetrics(
            health_id=str(uuid.uuid4()),
            overall_health_score=overall_health_score,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_latency=network_latency,
            error_rate=error_rate,
            uptime_percentage=uptime_percentage,
            last_updated=datetime.now()
        )
