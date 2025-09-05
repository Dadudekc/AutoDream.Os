"""
Strategic Oversight Extended Models
===================================

Extended data structures and complex business logic for strategic oversight operations.
V2 Compliance: < 200 lines, single responsibility, extended data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .models_core import (
    StrategicInsight, MissionObjective, ResourceAllocation,
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, PriorityLevel
)


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data."""
    recommendation_id: str
    title: str
    description: str
    insight_id: str
    priority: PriorityLevel
    impact_level: ImpactLevel
    implementation_effort: str
    expected_benefits: List[str]
    risks: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class OversightReport:
    """Oversight report data."""
    report_id: str
    title: str
    report_type: str
    insights: List[StrategicInsight]
    recommendations: List[StrategicRecommendation]
    objectives: List[MissionObjective]
    resource_allocations: List[ResourceAllocation]
    summary: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PerformanceMetrics:
    """Performance metrics data."""
    metrics_id: str
    mission_id: str
    agent_id: str
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    execution_time: float
    success_rate: float
    error_count: int
    throughput: float
    latency: float
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class CoordinationPattern:
    """Coordination pattern data."""
    pattern_id: str
    pattern_name: str
    agents_involved: List[str]
    coordination_type: str
    success_rate: float
    efficiency_score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class StrategicContext:
    """Strategic context data."""
    context_id: str
    mission_id: str
    phase: str
    priority: PriorityLevel
    resources: Dict[str, Any]
    constraints: List[str]
    objectives: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class OversightConfig:
    """Oversight configuration data."""
    config_id: str
    analysis_interval: float
    confidence_threshold: float
    impact_threshold: float
    max_insights: int
    report_frequency: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()