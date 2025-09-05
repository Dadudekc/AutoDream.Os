#!/usr/bin/env python3
"""
Strategic Oversight Models Core - V2 Compliance Module
=====================================================

Core data models for vector strategic oversight operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import uuid


class InsightType(Enum):
    """Insight types."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    EMERGENCY = "emergency"


class ConfidenceLevel(Enum):
    """Confidence levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ImpactLevel(Enum):
    """Impact levels."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionStatus(Enum):
    """Mission status types."""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class StrategicInsight:
    """Strategic insight data."""
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    confidence_level: ConfidenceLevel
    impact_level: ImpactLevel
    created_at: datetime
    updated_at: datetime
    source_agent: str
    target_agents: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.target_agents is None:
            self.target_agents = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MissionContext:
    """Mission context data."""
    mission_id: str
    mission_name: str
    description: str
    status: MissionStatus
    priority: int
    created_at: datetime
    updated_at: datetime
    assigned_agents: List[str] = None
    success_criteria: List[str] = None
    risk_factors: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.assigned_agents is None:
            self.assigned_agents = []
        if self.success_criteria is None:
            self.success_criteria = []
        if self.risk_factors is None:
            self.risk_factors = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentCapability:
    """Agent capability data."""
    agent_id: str
    agent_name: str
    primary_role: str
    skills: List[str]
    experience_level: str
    availability_status: str
    current_workload: int
    max_workload: int
    success_rate: float
    last_active: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.skills is None:
            self.skills = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class PerformanceMetrics:
    """Performance metrics data."""
    metric_id: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    source_agent: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RiskAssessment:
    """Risk assessment data."""
    risk_id: str
    risk_type: str
    risk_level: str
    description: str
    probability: float
    impact: float
    mitigation_strategies: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.mitigation_strategies is None:
            self.mitigation_strategies = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation data."""
    recommendation_id: str
    category: str
    priority: str
    title: str
    description: str
    expected_impact: str
    implementation_effort: str
    estimated_improvement: float
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}
