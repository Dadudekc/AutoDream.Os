#!/usr/bin/env python3
"""
FSM Models - Task and Report Data Structures
=============================================

Data models for FSM orchestrator task management.
Extracted from fsm_orchestrator.py for better modularity.

Features:
- Task data structures
- Agent report models
- Task state enumeration

Author: Agent-3 (Infrastructure & DevOps) - Infrastructure Optimization
Original: Agent-5 (Business Intelligence) - C-056
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TaskState(Enum):
    """Task state enumeration for FSM workflow."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Task data structure for FSM orchestrator."""

    id: str
    title: str
    description: str
    state: TaskState
    created_at: str
    updated_at: str
    assigned_agent: str | None = None
    evidence: list[dict[str, Any]] = None
    metadata: dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values for optional fields."""
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentReport:
    """Agent report data structure for task updates."""

    agent_id: str
    task_id: str
    report_type: str  # "update", "completion", "error"
    content: str
    evidence: list[dict[str, Any]]
    timestamp: str
    metadata: dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values for optional fields."""
        if self.metadata is None:
            self.metadata = {}
