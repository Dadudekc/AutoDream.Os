#!/usr/bin/env python3
"""
Pattern Analysis Models - V2 Compliance Module
=============================================

Data models and enums for pattern analysis operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PatternType(Enum):
    """Types of mission patterns."""

    SUCCESS = "success"
    FAILURE = "failure"
    COORDINATION = "coordination"
    RESOURCE = "resource"
    TIMING = "timing"
    COMMUNICATION = "communication"


class RecommendationType(Enum):
    """Types of strategic recommendations."""

    PATTERN_ADOPTION = "pattern_adoption"
    RISK_MITIGATION = "risk_mitigation"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    COORDINATION_ENHANCEMENT = "coordination_enhancement"
    TIMING_OPTIMIZATION = "timing_optimization"


class ImpactLevel(Enum):
    """Impact levels for recommendations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MissionPattern:
    """Mission pattern structure for analysis."""

    pattern_id: str
    pattern_type: str
    mission_type: str
    success_indicators: list[str] = field(default_factory=list)
    failure_indicators: list[str] = field(default_factory=list)
    optimal_conditions: dict[str, Any] = field(default_factory=dict)
    risk_factors: list[str] = field(default_factory=list)
    success_rate: float = 0.0
    average_duration: float = 0.0
    confidence_score: float = 0.0
    usage_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PatternCorrelation:
    """Pattern correlation structure."""

    correlation_id: str
    pattern_a: str
    pattern_b: str
    correlation_strength: float
    correlation_type: str  # "success", "failure", "resource", "time"
    evidence_count: int = 0
    confidence_score: float = 0.0
    last_analyzed: datetime = field(default_factory=datetime.now)


@dataclass
class MissionContext:
    """Mission context for pattern analysis."""

    mission_id: str
    mission_type: str
    agent_assignments: list[str] = field(default_factory=list)
    mission_goals: list[str] = field(default_factory=list)
    available_resources: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    mission_priority: str = "medium"
    estimated_duration: float = 0.0
    start_time: datetime | None = None


@dataclass
class StrategicRecommendation:
    """Strategic recommendation structure."""

    recommendation_id: str
    mission_context: str
    recommendation_type: str
    confidence_score: float
    expected_impact: str
    implementation_steps: list[str] = field(default_factory=list)
    risk_assessment: str = "medium"
    resource_requirements: dict[str, Any] = field(default_factory=dict)
    success_metrics: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PatternAnalysisResult:
    """Result of pattern analysis operation."""

    success: bool
    pattern_success_probability: float
    analysis_confidence: float
    identified_patterns: list[MissionPattern] = field(default_factory=list)
    recommendations: list[StrategicRecommendation] = field(default_factory=list)
    correlations: list[PatternCorrelation] = field(default_factory=list)
    risk_assessment: dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    error_message: str | None = None


@dataclass
class PatternMetrics:
    """Metrics for pattern analysis performance."""

    total_patterns: int = 0
    successful_analyses: int = 0
    average_confidence: float = 0.0
    pattern_usage_count: int = 0
    correlation_count: int = 0
    recommendation_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_patterns": self.total_patterns,
            "successful_analyses": self.successful_analyses,
            "average_confidence": self.average_confidence,
            "pattern_usage_count": self.pattern_usage_count,
            "correlation_count": self.correlation_count,
            "recommendation_count": self.recommendation_count,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class PatternAnalysisConfig:
    """Configuration for pattern analysis operations."""

    min_confidence_threshold: float = 0.7
    max_patterns_per_analysis: int = 10
    correlation_threshold: float = 0.3
    success_rate_threshold: float = 0.8
    enable_correlation_analysis: bool = True
    enable_recommendation_generation: bool = True
    enable_risk_assessment: bool = True
    max_recommendations: int = 5
    pattern_retention_days: int = 30
