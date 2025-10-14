#!/usr/bin/env python3
"""
Intelligent Context Analysis Models
====================================

Data models for agent recommendations, risk assessment, and success prediction.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRecommendation:
    """Agent recommendation structure."""

    agent_id: str
    recommendation_score: float
    reasoning: list[str] = field(default_factory=list)
    specialization_match: str = ""
    workload_impact: float = 0.0
    success_probability: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskAssessment:
    """Risk assessment structure."""

    risk_id: str
    risk_level: str
    risk_factors: list[str] = field(default_factory=list)
    mitigation_strategies: list[str] = field(default_factory=list)
    probability: float = 0.0
    impact: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SuccessPrediction:
    """Success prediction structure."""

    prediction_id: str
    success_probability: float
    confidence_level: float
    key_factors: list[str] = field(default_factory=list)
    potential_bottlenecks: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
