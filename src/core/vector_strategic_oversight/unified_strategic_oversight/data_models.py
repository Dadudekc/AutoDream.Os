"""
Strategic Oversight Data Models - V2 Compliance Module
=====================================================

Core data models for vector strategic oversight operations.

V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus,
    ReportType, PriorityLevel, AgentRole
)


@dataclass
class SwarmCoordinationInsight:
    """Swarm coordination insight data model."""
    insight_id: str
    insight_type: InsightType
    description: str
    confidence: float
    impact_score: float
    affected_agents: List[str]
    recommendations: List[str]
    generated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data model."""
    recommendation_id: str
    title: str
    description: str
    priority: int
    expected_impact: ImpactLevel
    implementation_effort: str
    success_probability: float
    dependencies: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str = "pending"


@dataclass
class StrategicOversightReport:
    """Strategic oversight report data model."""
    report_id: str
    report_type: ReportType
    title: str
    summary: str
    insights: List[SwarmCoordinationInsight]
    recommendations: List[StrategicRecommendation]
    confidence_level: ConfidenceLevel
    impact_level: ImpactLevel
    generated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentPerformanceMetrics:
    """Agent performance metrics data model."""
    agent_id: str
    agent_name: str
    role: AgentRole
    performance_score: float
    efficiency_rating: float
    coordination_effectiveness: float
    task_completion_rate: float
    response_time_avg: float
    last_updated: datetime
    metrics_period: str = "daily"


@dataclass
class SwarmCoordinationStatus:
    """Swarm coordination status data model."""
    status_id: str
    total_agents: int
    active_agents: int
    coordination_health: float
    communication_efficiency: float
    task_distribution_balance: float
    overall_swarm_effectiveness: float
    last_updated: datetime
    status_notes: Optional[str] = None


@dataclass
class StrategicMission:
    """Strategic mission data model."""
    mission_id: str
    title: str
    description: str
    status: MissionStatus
    priority: PriorityLevel
    assigned_agents: List[str]
    objectives: List[str]
    success_criteria: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: float = 0.0


@dataclass
class VectorDatabaseMetrics:
    """Vector database metrics data model."""
    metrics_id: str
    total_vectors: int
    query_performance: float
    indexing_efficiency: float
    search_accuracy: float
    memory_usage: float
    last_optimization: datetime
    optimization_recommendations: List[str]
    performance_trend: str = "stable"


@dataclass
class SystemHealthMetrics:
    """System health metrics data model."""
    health_id: str
    overall_health_score: float
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_latency: float
    error_rate: float
    uptime_percentage: float
    last_updated: datetime
    health_status: str = "healthy"
