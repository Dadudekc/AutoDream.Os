#!/usr/bin/env python3
"""
Progress Models - Progress Data Models
====================================

Progress tracking data models and structures.
Part of the modularization of unified_progress_tracking.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ProgressMilestone:
    """Progress milestone definition."""

    id: str
    name: str
    description: str
    phase: str
    target_date: datetime
    completed: bool = False
    completion_date: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentProgress:
    """Agent progress tracking."""

    agent_id: str
    agent_name: str
    current_phase: str
    milestones: list[ProgressMilestone] = field(default_factory=list)
    progress_percentage: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemProgress:
    """System-wide progress tracking."""

    system_name: str
    overall_phase: str
    total_milestones: int = 0
    completed_milestones: int = 0
    agent_progress: list[AgentProgress] = field(default_factory=list)
    progress_percentage: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SuperiorityMetrics:
    """Superiority benchmark metrics."""

    consolidation_efficiency: float = 0.0
    qc_compliance: float = 0.0
    integration_success: float = 0.0
    progress_velocity: float = 0.0
    blocker_resolution: float = 0.0
    overall_score: float = 0.0
    last_calculated: datetime = field(default_factory=datetime.now)

