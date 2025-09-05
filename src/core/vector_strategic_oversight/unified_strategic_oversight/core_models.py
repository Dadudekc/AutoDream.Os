"""
Strategic Oversight Core Models
==============================

Core data models for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, core data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole, EmergencyStatus
)


@dataclass
class StrategicOversightReport:
    """Strategic oversight report data."""
    report_id: str
    title: str
    description: str
    report_type: ReportType
    insights: List[Any]
    recommendations: List[Any]
    metrics: Dict[str, Any]
    generated_at: datetime
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.generated_at is None:
            self.generated_at = datetime.now()


@dataclass
class SwarmCoordinationInsight:
    """Swarm coordination insight data."""
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    confidence: ConfidenceLevel
    impact: ImpactLevel
    evidence: List[str]
    recommendations: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data."""
    recommendation_id: str
    title: str
    description: str
    priority: PriorityLevel
    impact: ImpactLevel
    implementation_effort: str
    expected_benefits: List[str]
    risks: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class AgentPerformanceMetrics:
    """Agent performance metrics data."""
    metrics_id: str
    agent_id: str
    agent_role: AgentRole
    performance_score: float
    efficiency: float
    coordination_score: float
    task_completion_rate: float
    response_time: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class SwarmCoordinationStatus:
    """Swarm coordination status data."""
    status_id: str
    swarm_id: str
    coordination_level: float
    communication_efficiency: float
    task_distribution: Dict[str, Any]
    bottlenecks: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class StrategicMission:
    """Strategic mission data."""
    mission_id: str
    title: str
    description: str
    status: MissionStatus
    priority: PriorityLevel
    assigned_agents: List[str]
    objectives: List[str]
    success_criteria: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class VectorDatabaseMetrics:
    """Vector database metrics data."""
    metrics_id: str
    database_name: str
    total_vectors: int
    query_performance: float
    storage_usage: float
    indexing_efficiency: float
    search_accuracy: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class SystemHealthMetrics:
    """System health metrics data."""
    metrics_id: str
    system_component: str
    health_score: float
    performance_metrics: Dict[str, Any]
    alerts: List[str]
    recommendations: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
