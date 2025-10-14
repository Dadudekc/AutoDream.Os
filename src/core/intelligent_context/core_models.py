#!/usr/bin/env python3
"""
Intelligent Context Core Models
================================

Core data models for mission context and agent capabilities.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MissionContext:
    """Mission context structure for intelligent retrieval."""

    mission_id: str
    mission_type: str
    current_phase: str
    agent_assignments: dict[str, str] = field(default_factory=dict)
    critical_path: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
            "metadata": self.metadata,
        }


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
