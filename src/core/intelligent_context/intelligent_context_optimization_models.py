#!/usr/bin/env python3
"""
Intelligent Context Optimization Models - V2 Compliance Module
=============================================================

Data models for intelligent context optimization operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class OptimizationResult:
    """Result of optimization operation."""

    success: bool
    data: dict[str, Any]
    execution_time: float
    error: str = None


@dataclass
class AgentScore:
    """Agent scoring data."""

    agent_id: str
    score: float
    specialization_match: str
    workload_impact: float
    success_probability: float


@dataclass
class MissionAnalysis:
    """Mission analysis data."""

    similar_missions_count: int
    success_factors: list[str]
    potential_pitfalls: list[str]
    confidence_level: float


@dataclass
class RiskMitigation:
    """Risk mitigation strategy."""

    strategy: str
    priority: str
    effectiveness: float


@dataclass
class SuccessFactor:
    """Success factor analysis."""

    factor: str
    importance: float
    confidence: float
