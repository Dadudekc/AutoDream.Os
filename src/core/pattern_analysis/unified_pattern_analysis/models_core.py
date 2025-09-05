#!/usr/bin/env python3
"""
Pattern Analysis Models Core - V2 Compliance Module
===================================================

Core data models for pattern analysis operations.
Extracted from models.py for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid


class PatternType(Enum):
    """Pattern types."""
    MISSION_SUCCESS = "mission_success"
    FAILURE_PATTERN = "failure_pattern"
    PERFORMANCE_TREND = "performance_trend"
    COORDINATION_PATTERN = "coordination_pattern"
    RESOURCE_UTILIZATION = "resource_utilization"
    TIMING_PATTERN = "timing_pattern"


class RecommendationType(Enum):
    """Recommendation types."""
    OPTIMIZATION = "optimization"
    PREVENTION = "prevention"
    ENHANCEMENT = "enhancement"
    MITIGATION = "mitigation"
    STRATEGIC = "strategic"


class ImpactLevel(Enum):
    """Impact levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MissionPattern:
    """Mission pattern data."""
    pattern_id: str
    pattern_type: PatternType
    agent_id: str
    mission_id: str
    timestamp: datetime
    success_rate: float
    execution_time: float
    resource_usage: Dict[str, Any]
    context_data: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type.value,
            "agent_id": self.agent_id,
            "mission_id": self.mission_id,
            "timestamp": self.timestamp.isoformat(),
            "success_rate": self.success_rate,
            "execution_time": self.execution_time,
            "resource_usage": self.resource_usage,
            "context_data": self.context_data,
            "metadata": self.metadata
        }


@dataclass
class PatternCorrelation:
    """Pattern correlation data."""
    correlation_id: str
    pattern_a_id: str
    pattern_b_id: str
    correlation_strength: float
    correlation_type: str
    confidence_level: float
    analysis_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "correlation_id": self.correlation_id,
            "pattern_a_id": self.pattern_a_id,
            "pattern_b_id": self.pattern_b_id,
            "correlation_strength": self.correlation_strength,
            "correlation_type": self.correlation_type,
            "confidence_level": self.confidence_level,
            "analysis_timestamp": self.analysis_timestamp.isoformat()
        }


@dataclass
class MissionContext:
    """Mission context data."""
    context_id: str
    agent_id: str
    mission_type: str
    environment: str
    resource_constraints: Dict[str, Any]
    performance_metrics: Dict[str, float]
    historical_data: List[Dict[str, Any]]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "context_id": self.context_id,
            "agent_id": self.agent_id,
            "mission_type": self.mission_type,
            "environment": self.environment,
            "resource_constraints": self.resource_constraints,
            "performance_metrics": self.performance_metrics,
            "historical_data": self.historical_data,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class StrategicRecommendation:
    """Strategic recommendation data."""
    recommendation_id: str
    pattern_id: str
    recommendation_type: RecommendationType
    impact_level: ImpactLevel
    title: str
    description: str
    implementation_priority: int
    expected_benefit: str
    implementation_steps: List[str]
    success_metrics: Dict[str, Any]
    created_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "recommendation_id": self.recommendation_id,
            "pattern_id": self.pattern_id,
            "recommendation_type": self.recommendation_type.value,
            "impact_level": self.impact_level.value,
            "title": self.title,
            "description": self.description,
            "implementation_priority": self.implementation_priority,
            "expected_benefit": self.expected_benefit,
            "implementation_steps": self.implementation_steps,
            "success_metrics": self.success_metrics,
            "created_timestamp": self.created_timestamp.isoformat()
        }


def create_pattern_id() -> str:
    """Create unique pattern ID."""
    return f"pattern_{uuid.uuid4().hex[:12]}"


def create_correlation_id() -> str:
    """Create unique correlation ID."""
    return f"corr_{uuid.uuid4().hex[:12]}"


def create_context_id() -> str:
    """Create unique context ID."""
    return f"ctx_{uuid.uuid4().hex[:12]}"


def create_recommendation_id() -> str:
    """Create unique recommendation ID."""
    return f"rec_{uuid.uuid4().hex[:12]}"
