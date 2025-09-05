"""
Pattern Analysis Extended Models
================================

Extended data structures and complex business logic for pattern analysis operations.
V2 Compliance: < 150 lines, single responsibility, extended data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid

from .models_core import (
    MissionPattern, PatternCorrelation, MissionContext,
    PatternType, RecommendationType, ImpactLevel
)


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data."""
    recommendation_id: str
    title: str
    description: str
    recommendation_type: RecommendationType
    impact_level: ImpactLevel
    priority: int
    implementation_effort: str
    expected_benefits: List[str]
    risks: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PatternAnalysisResult:
    """Pattern analysis result data."""
    result_id: str
    analysis_type: str
    patterns_found: List[MissionPattern]
    correlations: List[PatternCorrelation]
    recommendations: List[StrategicRecommendation]
    confidence_score: float
    analysis_metadata: Dict[str, Any]
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
class ResourceUtilization:
    """Resource utilization data."""
    utilization_id: str
    resource_type: str
    current_usage: float
    max_capacity: float
    utilization_percentage: float
    efficiency_score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class TimingPattern:
    """Timing pattern data."""
    timing_id: str
    pattern_name: str
    start_time: datetime
    end_time: datetime
    duration: float
    frequency: float
    consistency_score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CoordinationPattern:
    """Coordination pattern data."""
    coordination_id: str
    pattern_name: str
    agents_involved: List[str]
    coordination_type: str
    success_rate: float
    efficiency_score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()