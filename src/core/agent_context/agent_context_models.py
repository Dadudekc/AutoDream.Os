#!/usr/bin/env python3
"""
Agent Context Models - KISS Compliant
=====================================

Simple data models for agent context.

Author: Agent-5 - Business Intelligence Specialist
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

class ConfidenceLevel(Enum):
    """Confidence levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class AgentProfile:
    """Simple agent profile."""
    agent_id: str
    name: str
    role: str
    specialization: List[str] = field(default_factory=list)
    experience_level: str = "intermediate"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Recommendation:
    """Simple recommendation."""
    recommendation_id: str
    agent_id: str
    type: RecommendationType
    message: str
    confidence: ConfidenceLevel
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentContext:
    """Simple agent context."""
    agent_id: str
    current_task: Optional[str] = None
    status: str = "active"
    last_activity: datetime = field(default_factory=datetime.now)
    recommendations: List[Recommendation] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextMetrics:
    """Simple context metrics."""
    total_agents: int = 0
    total_recommendations: int = 0
    active_agents: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

# Simple factory functions
def create_agent_profile(agent_id: str, name: str, role: str) -> AgentProfile:
    """Create agent profile."""
    return AgentProfile(agent_id=agent_id, name=name, role=role)

def create_recommendation(agent_id: str, type: RecommendationType, message: str, 
                         confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM) -> Recommendation:
    """Create recommendation."""
    import uuid
    return Recommendation(
        recommendation_id=str(uuid.uuid4()),
        agent_id=agent_id,
        type=type,
        message=message,
        confidence=confidence
    )

def create_agent_context(agent_id: str) -> AgentContext:
    """Create agent context."""
    return AgentContext(agent_id=agent_id)

def create_context_metrics() -> ContextMetrics:
    """Create context metrics."""
    return ContextMetrics()

__all__ = [
    "RecommendationType", "ConfidenceLevel", "AgentProfile", "Recommendation",
    "AgentContext", "ContextMetrics", "create_agent_profile", "create_recommendation",
    "create_agent_context", "create_context_metrics"
]