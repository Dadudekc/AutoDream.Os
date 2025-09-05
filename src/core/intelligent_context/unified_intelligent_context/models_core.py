#!/usr/bin/env python3
"""
Intelligent Context Models Core - V2 Compliance Module
=====================================================

Core data models for intelligent context operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class ContextType(Enum):
    """Context types."""
    MISSION = "mission"
    AGENT_CAPABILITY = "agent_capability"
    EMERGENCY = "emergency"
    INTERVENTION = "intervention"
    RISK_ASSESSMENT = "risk_assessment"
    SUCCESS_PREDICTION = "success_prediction"


class Priority(Enum):
    """Priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    """Status types."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MissionContext:
    """Mission context data."""
    mission_id: str
    mission_name: str
    description: str
    mission_type: str
    priority: Priority
    status: Status
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
    availability_status: Status
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
class SearchResult:
    """Search result data."""
    result_id: str
    content: str
    relevance_score: float
    source_type: str
    source_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentRecommendation:
    """Agent recommendation data."""
    agent_id: str
    recommendation_score: float
    reasoning: List[str]
    specialization_match: str
    workload_impact: float
    success_probability: float
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.reasoning is None:
            self.reasoning = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RiskAssessment:
    """Risk assessment data."""
    risk_id: str
    risk_level: str
    risk_factors: List[str]
    mitigation_strategies: List[str]
    probability: float
    impact: float
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.risk_factors is None:
            self.risk_factors = []
        if self.mitigation_strategies is None:
            self.mitigation_strategies = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SuccessPrediction:
    """Success prediction data."""
    prediction_id: str
    success_probability: float
    confidence_level: float
    key_factors: List[str]
    potential_bottlenecks: List[str]
    recommended_actions: List[str]
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.key_factors is None:
            self.key_factors = []
        if self.potential_bottlenecks is None:
            self.potential_bottlenecks = []
        if self.recommended_actions is None:
            self.recommended_actions = []
        if self.metadata is None:
            self.metadata = {}
