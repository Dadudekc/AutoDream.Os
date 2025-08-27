from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

from .enums import TaskPriority, TaskType


@dataclass
class SchedulingMetrics:
    """Metrics for monitoring scheduler performance."""

    total_tasks_scheduled: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_scheduling_time: float = 0.0
    average_execution_time: float = 0.0
    tasks_by_priority: Dict[TaskPriority, int] = field(default_factory=dict)
    tasks_by_type: Dict[TaskType, int] = field(default_factory=dict)
    last_update: datetime = field(default_factory=datetime.now)
