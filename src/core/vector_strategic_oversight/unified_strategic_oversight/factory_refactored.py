"""
Strategic Oversight Factory - Refactored Entry Point
====================================================

Unified entry point for strategic oversight factory with backward compatibility.
V2 Compliance: < 100 lines, single responsibility, unified interface.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .factory_core import StrategicOversightFactoryCore
from .factory_extended import StrategicOversightFactoryExtended
from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole, EmergencyStatus
)
from .core_models import (
    StrategicOversightReport, SwarmCoordinationInsight, StrategicRecommendation,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics
)


class StrategicOversightFactory:
    """Unified strategic oversight factory with modular architecture."""
    
    # Core factory methods
    @staticmethod
    def create_strategic_oversight_report(
        title: str,
        description: str,
        report_type: ReportType,
        insights: List[Any] = None,
        recommendations: List[Any] = None,
        metrics: Dict[str, Any] = None
    ) -> StrategicOversightReport:
        """Create strategic oversight report."""
        return StrategicOversightFactoryCore.create_strategic_oversight_report(
            title, description, report_type, insights, recommendations, metrics
        )
    
    @staticmethod
    def create_swarm_coordination_insight(
        insight_type: InsightType,
        description: str,
        confidence: float = 0.8,
        impact_score: float = 0.5,
        affected_agents: List[str] = None,
        recommendations: List[str] = None
    ) -> SwarmCoordinationInsight:
        """Create swarm coordination insight."""
        return StrategicOversightFactoryCore.create_swarm_coordination_insight(
            insight_type, description, confidence, impact_score, affected_agents, recommendations
        )
    
    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        priority: int = 1,
        expected_impact: ImpactLevel = ImpactLevel.MEDIUM,
        implementation_effort: str = "medium",
        success_probability: float = 0.8,
        dependencies: List[str] = None
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicOversightFactoryCore.create_strategic_recommendation(
            title, description, priority, expected_impact, implementation_effort, success_probability, dependencies
        )
    
    @staticmethod
    def create_agent_performance_metrics(
        agent_id: str,
        mission_id: str,
        cpu_usage: float = 0.0,
        memory_usage: float = 0.0,
        execution_time: float = 0.0,
        success_rate: float = 1.0,
        error_count: int = 0
    ) -> AgentPerformanceMetrics:
        """Create agent performance metrics."""
        return StrategicOversightFactoryCore.create_agent_performance_metrics(
            agent_id, mission_id, cpu_usage, memory_usage, execution_time, success_rate, error_count
        )
    
    @staticmethod
    def create_swarm_coordination_status(
        status_name: str,
        description: str,
        active_agents: List[str] = None,
        coordination_level: str = "medium",
        efficiency_score: float = 0.8
    ) -> SwarmCoordinationStatus:
        """Create swarm coordination status."""
        return StrategicOversightFactoryCore.create_swarm_coordination_status(
            status_name, description, active_agents, coordination_level, efficiency_score
        )
    
    @staticmethod
    def create_strategic_mission(
        mission_name: str,
        description: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        status: MissionStatus = MissionStatus.PENDING,
        assigned_agents: List[str] = None,
        target_date: Optional[datetime] = None
    ) -> StrategicMission:
        """Create strategic mission."""
        return StrategicOversightFactoryCore.create_strategic_mission(
            mission_name, description, priority, status, assigned_agents, target_date
        )
    
    # Extended factory methods
    @staticmethod
    def create_vector_database_metrics(
        database_id: str,
        query_count: int = 0,
        response_time: float = 0.0,
        accuracy: float = 1.0,
        memory_usage: float = 0.0,
        index_size: int = 0
    ) -> VectorDatabaseMetrics:
        """Create vector database metrics."""
        return StrategicOversightFactoryExtended.create_vector_database_metrics(
            database_id, query_count, response_time, accuracy, memory_usage, index_size
        )
    
    @staticmethod
    def create_system_health_metrics(
        system_id: str,
        cpu_usage: float = 0.0,
        memory_usage: float = 0.0,
        disk_usage: float = 0.0,
        network_latency: float = 0.0,
        error_rate: float = 0.0,
        uptime: float = 0.0
    ) -> SystemHealthMetrics:
        """Create system health metrics."""
        return StrategicOversightFactoryExtended.create_system_health_metrics(
            system_id, cpu_usage, memory_usage, disk_usage, network_latency, error_rate, uptime
        )
    
    @staticmethod
    def create_comprehensive_report(
        title: str,
        description: str,
        insights: List[SwarmCoordinationInsight] = None,
        recommendations: List[StrategicRecommendation] = None,
        performance_metrics: List[AgentPerformanceMetrics] = None,
        system_metrics: List[SystemHealthMetrics] = None
    ) -> StrategicOversightReport:
        """Create comprehensive strategic oversight report."""
        return StrategicOversightFactoryExtended.create_comprehensive_report(
            title, description, insights, recommendations, performance_metrics, system_metrics
        )
