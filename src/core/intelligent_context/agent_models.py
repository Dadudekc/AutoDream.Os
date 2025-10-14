#!/usr/bin/env python3
"""
Agent Context Models - V2 Compliance
=====================================

Agent capability and recommendation data structures.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AgentCapability:
    """Agent capability structure for matching and optimization."""

    agent_id: str
    primary_role: str
    skills: set[str] = field(default_factory=set)
    experience_level: str = "intermediate"
    current_workload: int = 0
    success_rate: float = 0.8
    specialization: list[str] = field(default_factory=list)
    availability_status: str = "available"
    last_active: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
            "metadata": self.metadata,
        }


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


__all__ = ["AgentCapability", "AgentRecommendation"]
