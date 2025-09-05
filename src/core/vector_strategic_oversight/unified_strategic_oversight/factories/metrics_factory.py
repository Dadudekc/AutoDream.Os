"""
Strategic Oversight Metrics Factory - V2 Compliance Module
=========================================================

Factory methods for creating strategic oversight metrics.

V2 Compliance: < 300 lines, single responsibility, metrics factory.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional
from datetime import datetime
import uuid

from ..enums import AgentRole
from ..data_models import (
    AgentPerformanceMetrics, SwarmCoordinationStatus, VectorDatabaseMetrics,
    SystemHealthMetrics
)


class MetricsFactory:
    """Factory class for creating strategic oversight metrics."""
    
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
    def create_vector_database_metrics(
        total_vectors: int,
        query_performance: float,
        index_efficiency: float,
        memory_usage: float,
        cache_hit_rate: float,
        search_accuracy: float
    ) -> VectorDatabaseMetrics:
        """Create vector database metrics."""
        return VectorDatabaseMetrics(
            metrics_id=str(uuid.uuid4()),
            total_vectors=total_vectors,
            query_performance=query_performance,
            index_efficiency=index_efficiency,
            memory_usage=memory_usage,
            cache_hit_rate=cache_hit_rate,
            search_accuracy=search_accuracy,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_system_health_metrics(
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
        network_latency: float,
        error_rate: float,
        uptime: float
    ) -> SystemHealthMetrics:
        """Create system health metrics."""
        return SystemHealthMetrics(
            health_id=str(uuid.uuid4()),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_latency=network_latency,
            error_rate=error_rate,
            uptime=uptime,
            last_updated=datetime.now()
        )
