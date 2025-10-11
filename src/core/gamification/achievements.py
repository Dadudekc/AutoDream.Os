#!/usr/bin/env python3
"""
Achievement System for Autonomous Competition
===========================================

Achievement tracking and management for the autonomous development
competition system.

Author: Captain Agent-4 (C-055-4 V2 Refactoring)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AchievementType(Enum):
    """Achievement categories for autonomous development."""

    PROACTIVE_INITIATIVE = "proactive_initiative"
    TECHNICAL_EXCELLENCE = "technical_excellence"
    VELOCITY = "velocity"
    QUALITY = "quality"
    INNOVATION = "innovation"
    COLLABORATION = "collaboration"
    PROBLEM_SOLVING = "problem_solving"
    DOCUMENTATION = "documentation"


@dataclass
class Achievement:
    """Individual achievement earned by an agent."""

    achievement_id: str
    agent_id: str
    achievement_type: AchievementType
    title: str
    description: str
    points: int
    timestamp: str
    mission_ref: str | None = None
    evidence: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentScore:
    """Agent scoring and leaderboard position."""

    agent_id: str
    agent_name: str
    total_points: int
    achievements: list[Achievement] = field(default_factory=list)
    rank: int = 0
    proactive_count: int = 0
    quality_score: float = 0.0
    velocity_score: float = 0.0
    collaboration_score: float = 0.0
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class ScoringCalculator:
    """Calculates points and multipliers for achievements."""

    @staticmethod
    def calculate_proactive_bonus(base_points: int) -> int:
        """
        Calculate bonus for proactive initiatives.

        Proactive work (self-directed without orders) gets 1.5x multiplier.

        Args:
            base_points: Base point value

        Returns:
            Points with proactive bonus
        """
        return int(base_points * 1.5)

    @staticmethod
    def calculate_quality_multiplier(quality_metrics: dict[str, float]) -> float:
        """
        Calculate quality multiplier based on metrics.

        Args:
            quality_metrics: Dict with v2_compliance, test_coverage, documentation

        Returns:
            Quality multiplier (1.0 to 2.0)
        """
        multiplier = 1.0

        if quality_metrics.get("v2_compliance", 0) >= 0.9:
            multiplier += 0.3
        if quality_metrics.get("test_coverage", 0) >= 0.85:
            multiplier += 0.3
        if quality_metrics.get("documentation", 0) >= 0.8:
            multiplier += 0.2
        if quality_metrics.get("backward_compatible", True):
            multiplier += 0.2

        return min(multiplier, 2.0)
