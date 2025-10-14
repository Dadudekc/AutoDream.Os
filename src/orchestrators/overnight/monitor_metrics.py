"""
Monitor Metrics
===============

Performance metrics calculation for progress monitor.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: monitor.py (ProgressMonitor class split)
License: MIT
"""

import time
from typing import Any


class MonitorMetrics:
    """Calculates performance metrics."""

    def __init__(self):
        """Initialize metrics tracker."""
        self.metrics = {
            "cycles_completed": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_cycle_time": 0,
            "average_task_time": 0,
        }

    def update_cycle_metrics(self, cycle_start_times: dict, current_cycle: int) -> None:
        """Update cycle-based metrics."""
        if current_cycle > 1:
            cycle_times = []
            for i in range(1, current_cycle):
                if i in cycle_start_times and i + 1 in cycle_start_times:
                    cycle_time = cycle_start_times[i + 1] - cycle_start_times[i]
                    cycle_times.append(cycle_time)

            if cycle_times:
                self.metrics["average_cycle_time"] = sum(cycle_times) / len(cycle_times)

        self.metrics["cycles_completed"] = current_cycle

    def add_tasks(self, task_count: int) -> None:
        """Add tasks to tracking."""
        self.metrics["total_tasks"] += task_count

    def mark_completed(self, duration: float) -> None:
        """Mark task as completed."""
        self.metrics["completed_tasks"] += 1

        total_completed = self.metrics["completed_tasks"]
        current_avg = self.metrics["average_task_time"]
        self.metrics["average_task_time"] = (
            current_avg * (total_completed - 1) + duration
        ) / total_completed

    def mark_failed(self) -> None:
        """Mark task as failed."""
        self.metrics["failed_tasks"] += 1

    def get_metrics(
        self, start_time: float, current_cycle: int, agent_tasks: dict
    ) -> dict[str, Any]:
        """Get comprehensive performance metrics."""
        current_time = time.time()
        uptime = current_time - start_time if start_time > 0 else 0

        cycles_per_hour = 0
        tasks_per_hour = 0

        if uptime > 0:
            cycles_per_hour = (current_cycle * 3600) / uptime
            tasks_per_hour = (self.metrics["total_tasks"] * 3600) / uptime

        return {
            **self.metrics,
            "uptime_seconds": uptime,
            "uptime_hours": uptime / 3600,
            "cycles_per_hour": cycles_per_hour,
            "tasks_per_hour": tasks_per_hour,
            "current_cycle": current_cycle,
            "active_agents": len([a for a, task in agent_tasks.items() if task is not None]),
        }
