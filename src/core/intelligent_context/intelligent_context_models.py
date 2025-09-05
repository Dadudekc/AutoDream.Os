#!/usr/bin/env python3
"""
Intelligent Context Models - V2 Compliance Module
================================================

Data models and enums for intelligent context retrieval operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union
from datetime import datetime


class MissionPhase(Enum):
    """Mission phases."""
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMPLETION = "completion"
    EMERGENCY = "emergency"


class AgentStatus(Enum):
    """Agent availability status."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class RiskLevel(Enum):
    """Risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MissionContext:
    """Mission context structure for intelligent retrieval."""
    
    mission_id: str
    mission_type: str
    current_phase: str
    agent_assignments: Dict[str, str] = field(default_factory=dict)
    critical_path: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mission_id": self.mission_id,
            "mission_type": self.mission_type,
            "current_phase": self.current_phase,
            "agent_assignments": self.agent_assignments,
            "critical_path": self.critical_path,
            "risk_factors": self.risk_factors,
            "success_criteria": self.success_criteria,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class AgentCapability:
    """Agent capability structure for matching and optimization."""
    
    agent_id: str
    primary_role: str
    skills: Set[str] = field(default_factory=set)
    experience_level: str = "intermediate"
    current_workload: int = 0
    success_rate: float = 0.8
    specialization: List[str] = field(default_factory=list)
    availability_status: str = "available"
    last_active: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "primary_role": self.primary_role,
            "skills": list(self.skills),
            "experience_level": self.experience_level,
            "current_workload": self.current_workload,
            "success_rate": self.success_rate,
            "specialization": self.specialization,
            "availability_status": self.availability_status,
            "last_active": self.last_active.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class SearchResult:
    """Search result structure."""
    
    result_id: str
    content: str
    relevance_score: float
    source_type: str
    source_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "content": self.content,
            "relevance_score": self.relevance_score,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ContextRetrievalResult:
    """Result of context retrieval operation."""
    
    success: bool
    mission_context: Optional[MissionContext] = None
    search_results: List[SearchResult] = field(default_factory=list)
    agent_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    risk_assessment: Optional[Dict[str, Any]] = None
    success_prediction: Optional[Dict[str, Any]] = None
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "mission_context": self.mission_context.to_dict() if self.mission_context else None,
            "search_results": [r.to_dict() for r in self.search_results],
            "agent_recommendations": self.agent_recommendations,
            "risk_assessment": self.risk_assessment,
            "success_prediction": self.success_prediction,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message
        }


@dataclass
class EmergencyContext:
    """Emergency context structure."""
    
    emergency_id: str
    mission_id: str
    emergency_type: str
    severity_level: str
    affected_agents: List[str] = field(default_factory=list)
    intervention_protocols: List[str] = field(default_factory=list)
    estimated_resolution_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionProtocol:
    """Intervention protocol structure."""
    
    protocol_id: str
    protocol_name: str
    trigger_conditions: List[str] = field(default_factory=list)
    intervention_steps: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    estimated_duration: float = 0.0
    required_agents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRecommendation:
    """Agent recommendation structure."""
    
    agent_id: str
    recommendation_score: float
    reasoning: List[str] = field(default_factory=list)
    specialization_match: str = ""
    workload_impact: float = 0.0
    success_probability: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskAssessment:
    """Risk assessment structure."""
    
    risk_id: str
    risk_level: str
    risk_factors: List[str] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)
    probability: float = 0.0
    impact: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SuccessPrediction:
    """Success prediction structure."""
    
    prediction_id: str
    success_probability: float
    confidence_level: float
    key_factors: List[str] = field(default_factory=list)
    potential_bottlenecks: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextMetrics:
    """Metrics for context retrieval operations."""
    
    total_retrievals: int = 0
    successful_retrievals: int = 0
    failed_retrievals: int = 0
    average_execution_time_ms: float = 0.0
    total_execution_time_ms: float = 0.0
    emergency_interventions: int = 0
    agent_optimizations: int = 0
    risk_assessments: int = 0
    success_predictions: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_retrievals": self.total_retrievals,
            "successful_retrievals": self.successful_retrievals,
            "failed_retrievals": self.failed_retrievals,
            "average_execution_time_ms": self.average_execution_time_ms,
            "total_execution_time_ms": self.total_execution_time_ms,
            "emergency_interventions": self.emergency_interventions,
            "agent_optimizations": self.agent_optimizations,
            "risk_assessments": self.risk_assessments,
            "success_predictions": self.success_predictions,
            "last_updated": self.last_updated.isoformat()
        }
