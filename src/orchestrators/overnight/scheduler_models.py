"""
Scheduler Models - Task Representations
========================================

Task data models for overnight scheduler.
Extracted from scheduler.py for preventive optimization.

Author: Agent-1 - Autonomous Operations Specialist
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """Task representation for scheduling."""

    id: str
    type: str
    priority: int  # Lower number = higher priority
    agent_id: str
    data: dict[str, Any] = field(default_factory=dict)
    created_time: float = field(default_factory=time.time)
    scheduled_cycle: int | None = None
    dependencies: list[str] = field(default_factory=list)
    estimated_duration: float = 300.0  # seconds
    retry_count: int = 0
    max_retries: int = 3

    def __lt__(self, other):
        """Priority queue ordering (lower priority number = higher priority)."""
        return self.priority < other.priority


# Default task priorities by type
DEFAULT_TASK_PRIORITIES = {
    "system_health": 1,
    "agent_recovery": 2,
    "workflow_execution": 3,
    "monitoring": 4,
    "cleanup": 5,
    "maintenance": 6,
}
