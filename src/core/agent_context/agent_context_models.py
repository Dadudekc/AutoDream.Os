#!/usr/bin/env python3
"""
Agent Context Models - V2 Compliance Module
==========================================

Data models and enums for agent context operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class RecommendationType(Enum):
    """Types of agent recommendations."""
    TASK = "task"
    COMMUNICATION = "communication"
    COLLABORATION = "collaboration"
    OPTIMIZATION = "optimization"
    PERFORMANCE = "performance"
    LEARNING = "learning"


class ConfidenceLevel(Enum):
    """Confidence levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class AgentProfile:
    """Agent profile information."""
    
    agent_id: str
    name: str
    role: str
    specialization: List[str] = field(default_factory=list)
    experience_level: str = "intermediate"
    communication_style: str = "professional"
    preferred_task_types: List[str] = field(default_factory=list)
    working_hours: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommunicationPattern:
    """Communication pattern data."""
    
    pattern_id: str
    agent_id: str
    pattern_type: str
    frequency: float
    effectiveness_score: float
    context: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SuccessPattern:
    """Success pattern data."""
    
    pattern_id: str
    agent_id: str
    task_type: str
    success_rate: float
    key_factors: List[str] = field(default_factory=list)
    optimal_conditions: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollaborationHistory:
    """Collaboration history data."""
    
    collaboration_id: str
    agent_id: str
    partner_agent_id: str
    task_description: str
    success: bool
    effectiveness_score: float
    duration_hours: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DomainExpertise:
    """Domain expertise data."""
    
    expertise_id: str
    agent_id: str
    domain: str
    expertise_level: float
    experience_hours: float
    certifications: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics data."""
    
    agent_id: str
    task_completion_rate: float
    average_task_duration: float
    quality_score: float
    collaboration_score: float
    learning_rate: float
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentContext:
    """Comprehensive agent context information."""
    
    agent_id: str
    profile: AgentProfile
    communication_patterns: List[CommunicationPattern] = field(default_factory=list)
    success_patterns: List[SuccessPattern] = field(default_factory=list)
    collaboration_history: List[CollaborationHistory] = field(default_factory=list)
    domain_expertise: List[DomainExpertise] = field(default_factory=list)
    performance_metrics: PerformanceMetrics = None
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "profile": self.profile.__dict__,
            "communication_patterns": [p.__dict__ for p in self.communication_patterns],
            "success_patterns": [p.__dict__ for p in self.success_patterns],
            "collaboration_history": [c.__dict__ for c in self.collaboration_history],
            "domain_expertise": [e.__dict__ for e in self.domain_expertise],
            "performance_metrics": self.performance_metrics.__dict__ if self.performance_metrics else None,
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Recommendation:
    """Agent recommendation with context and confidence."""
    
    recommendation_id: str
    type: RecommendationType
    description: str
    confidence: float
    reasoning: str
    priority: str = "medium"
    implementation_effort: str = "medium"
    expected_impact: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "recommendation_id": self.recommendation_id,
            "type": self.type.value,
            "description": self.description,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "priority": self.priority,
            "implementation_effort": self.implementation_effort,
            "expected_impact": self.expected_impact,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ContextMetrics:
    """Metrics for agent context operations."""
    
    total_agents: int = 0
    total_recommendations: int = 0
    successful_recommendations: int = 0
    failed_recommendations: int = 0
    average_confidence: float = 0.0
    total_communication_patterns: int = 0
    total_success_patterns: int = 0
    total_collaborations: int = 0
    total_domain_expertise: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_agents": self.total_agents,
            "total_recommendations": self.total_recommendations,
            "successful_recommendations": self.successful_recommendations,
            "failed_recommendations": self.failed_recommendations,
            "average_confidence": self.average_confidence,
            "total_communication_patterns": self.total_communication_patterns,
            "total_success_patterns": self.total_success_patterns,
            "total_collaborations": self.total_collaborations,
            "total_domain_expertise": self.total_domain_expertise,
            "last_updated": self.last_updated.isoformat()
        }
