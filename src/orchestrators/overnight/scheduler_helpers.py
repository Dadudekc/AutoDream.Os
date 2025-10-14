"""
Scheduler Helper Functions
===========================

Helper functions for task scheduler.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: scheduler.py (TaskScheduler class extraction)
License: MIT
"""

from typing import Any


class SchedulerHelpers:
    """Helper functions for scheduler operations."""

    @staticmethod
    async def load_persisted_tasks(logger) -> None:
        """Load persisted tasks from storage."""
        logger.info("Loading persisted tasks")

    @staticmethod
    def get_scheduler_status(
        strategy: str,
        priority_queue: bool,
        load_balancing: bool,
        max_tasks: int,
        current_cycle: int,
        queue_size: int,
        tracking_status: dict,
        agent_loads: dict,
        task_priorities: dict,
    ) -> dict[str, Any]:
        """Get scheduler status dictionary."""
        return {
            "strategy": strategy,
            "priority_queue": priority_queue,
            "load_balancing": load_balancing,
            "max_tasks_per_cycle": max_tasks,
            "current_cycle": current_cycle,
            "queue_size": queue_size,
            **tracking_status,
            "agent_loads": agent_loads,
            "task_priorities": task_priorities,
        }
