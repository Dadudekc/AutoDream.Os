#!/usr/bin/env python3
"""
Mission Context Models - V2 Compliance
=======================================

Mission context data structures for intelligent retrieval.

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


__all__ = ["MissionContext"]
