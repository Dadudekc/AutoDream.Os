"""
Strategic Oversight Extended Models
===================================

Extended data models for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, extended data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from datetime import datetime

from .enums import ConfidenceLevel, EmergencyStatus, ImpactLevel


@dataclass
class AgentCapabilities:
    """Agent capabilities data."""

    capabilities_id: str
    agent_id: str
    capabilities: list[str]
    proficiency_levels: dict[str, float]
    specializations: list[str]
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
    recommendations: list[str]
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
    factors: list[str]
    recommendations: list[str]
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
    mitigation_strategies: list[str]
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
    affected_agents: list[str]
    resolution_actions: list[str]
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
    agents_involved: list[str]
    created_at: datetime

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
