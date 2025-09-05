"""
Strategic Oversight Extended Models
===================================

Extended data models for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, extended data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from .enums import ConfidenceLevel, ImpactLevel, EmergencyStatus


@dataclass
class AgentCapabilities:
    """Agent capabilities data."""
    capabilities_id: str
    agent_id: str
    capabilities: List[str]
    proficiency_levels: Dict[str, float]
    specializations: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PatternAnalysis:
    """Pattern analysis data."""
    analysis_id: str
    pattern_type: str
    confidence: float
    frequency: float
    impact: ImpactLevel
    recommendations: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class SuccessPrediction:
    """Success prediction data."""
    prediction_id: str
    mission_id: str
    success_probability: float
    confidence: ConfidenceLevel
    factors: List[str]
    recommendations: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class RiskAssessment:
    """Risk assessment data."""
    assessment_id: str
    risk_type: str
    severity: ImpactLevel
    probability: float
    impact: str
    mitigation_strategies: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterventionHistory:
    """Intervention history data."""
    intervention_id: str
    intervention_type: str
    target_agent: str
    reason: str
    outcome: str
    timestamp: datetime
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class EmergencyAlert:
    """Emergency alert data."""
    alert_id: str
    alert_type: EmergencyStatus
    severity: ImpactLevel
    message: str
    affected_agents: List[str]
    resolution_actions: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PerformanceTrend:
    """Performance trend data."""
    trend_id: str
    metric_name: str
    trend_direction: str
    trend_value: float
    confidence: ConfidenceLevel
    time_period: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CoordinationPattern:
    """Coordination pattern data."""
    pattern_id: str
    pattern_name: str
    pattern_type: str
    frequency: float
    effectiveness: float
    agents_involved: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
