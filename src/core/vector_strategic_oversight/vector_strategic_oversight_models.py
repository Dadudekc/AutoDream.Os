#!/usr/bin/env python3
"""
Vector Strategic Oversight Models - V2 Compliance Module
=======================================================

Data models and enums for vector strategic oversight operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class InsightType(Enum):
    """Types of swarm coordination insights."""
    MISSION_OPTIMIZATION = "mission_optimization"
    AGENT_COORDINATION = "agent_coordination"
    EMERGENCY_RESPONSE = "emergency_response"
    PATTERN_ANALYSIS = "pattern_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    SUCCESS_PREDICTION = "success_prediction"
    STRATEGIC_RECOMMENDATION = "strategic_recommendation"


class ConfidenceLevel(Enum):
    """Confidence levels for insights and recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ImpactLevel(Enum):
    """Impact levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MissionStatus:
    """Mission status information."""
    
    mission_id: str
    status: str
    progress_percentage: float
    active_agents: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    pending_tasks: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentCapabilities:
    """Agent capabilities information."""
    
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    expertise_areas: List[str] = field(default_factory=list)
    current_load: float = 0.0
    availability_status: str = "available"
    performance_score: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyStatus:
    """Emergency status information."""
    
    emergency_id: str
    severity: str
    description: str
    affected_agents: List[str] = field(default_factory=list)
    response_actions: List[str] = field(default_factory=list)
    resolution_status: str = "active"
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PatternAnalysis:
    """Pattern analysis results."""
    
    analysis_id: str
    pattern_type: str
    confidence: float
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    success_factors: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategicRecommendation:
    """Strategic recommendation structure."""
    
    recommendation_id: str
    type: str
    description: str
    priority: str
    confidence: float
    expected_impact: str
    implementation_effort: str
    reasoning: str
    recommended_actions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SuccessPrediction:
    """Success prediction data."""
    
    prediction_id: str
    mission_id: str
    success_probability: float
    key_factors: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskAssessment:
    """Risk assessment data."""
    
    assessment_id: str
    risk_type: str
    severity: str
    probability: float
    impact: str
    mitigation_strategies: List[str] = field(default_factory=list)
    monitoring_actions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionHistory:
    """Intervention history data."""
    
    intervention_id: str
    intervention_type: str
    target_agent: str
    description: str
    outcome: str
    actions_taken: List[str] = field(default_factory=list)
    effectiveness_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmCoordinationInsight:
    """Swarm coordination insight structure."""
    
    insight_id: str
    insight_type: InsightType
    mission_context: str
    insight_content: str
    confidence_level: ConfidenceLevel
    recommended_actions: List[str] = field(default_factory=list)
    expected_impact: ImpactLevel = ImpactLevel.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "insight_id": self.insight_id,
            "insight_type": self.insight_type.value,
            "mission_context": self.mission_context,
            "insight_content": self.insight_content,
            "confidence_level": self.confidence_level.value,
            "recommended_actions": self.recommended_actions,
            "expected_impact": self.expected_impact.value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class StrategicOversightReport:
    """Comprehensive strategic oversight report."""
    
    report_id: str
    generated_at: datetime = field(default_factory=datetime.now)
    mission_status: MissionStatus = None
    agent_capabilities: List[AgentCapabilities] = field(default_factory=list)
    emergency_status: List[EmergencyStatus] = field(default_factory=list)
    pattern_analysis: List[PatternAnalysis] = field(default_factory=list)
    strategic_recommendations: List[StrategicRecommendation] = field(default_factory=list)
    success_predictions: List[SuccessPrediction] = field(default_factory=list)
    risk_assessment: List[RiskAssessment] = field(default_factory=list)
    intervention_history: List[InterventionHistory] = field(default_factory=list)
    swarm_insights: List[SwarmCoordinationInsight] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at.isoformat(),
            "mission_status": self.mission_status.__dict__ if self.mission_status else None,
            "agent_capabilities": [ac.__dict__ for ac in self.agent_capabilities],
            "emergency_status": [es.__dict__ for es in self.emergency_status],
            "pattern_analysis": [pa.__dict__ for pa in self.pattern_analysis],
            "strategic_recommendations": [sr.__dict__ for sr in self.strategic_recommendations],
            "success_predictions": [sp.__dict__ for sp in self.success_predictions],
            "risk_assessment": [ra.__dict__ for ra in self.risk_assessment],
            "intervention_history": [ih.__dict__ for ih in self.intervention_history],
            "swarm_insights": [si.to_dict() for si in self.swarm_insights],
            "metadata": self.metadata
        }
