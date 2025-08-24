"""Orchestrator for the task scheduler components."""

from __future__ import annotations

from .task_scheduler_config import TaskSchedulerConfig, SchedulingMetrics
from .task_scheduler_core import TaskSchedulerCore
from .task_scheduler_manager import TaskSchedulerManager
from .task_scheduler_coordinator import TaskSchedulerCoordinator


class TaskScheduler(
    TaskSchedulerManager,
    TaskSchedulerCoordinator,
    TaskSchedulerCore,
    TaskSchedulerConfig,
):
    """Composite task scheduler composed of modular components."""

    def __init__(self, max_concurrent_tasks: int = 100):
        super().__init__(max_concurrent_tasks)


__all__ = ["TaskScheduler", "SchedulingMetrics"]

