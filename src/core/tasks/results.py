"""Result aggregation utilities for task execution."""

from __future__ import annotations

from typing import Any, Dict

from .definitions import (
    DevelopmentTask,
    MockTaskStatus,
    MockTaskPriority,
    MockTaskComplexity,
)


def get_task_statistics(
    tasks: Dict[str, DevelopmentTask], workflow_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """Compute aggregate statistics for a collection of tasks."""
    total_tasks = len(tasks)
    available_tasks = len(
        [t for t in tasks.values() if t.status == MockTaskStatus.AVAILABLE]
    )
    claimed_tasks = len(
        [t for t in tasks.values() if t.status == MockTaskStatus.CLAIMED]
    )
    in_progress_tasks = len(
        [t for t in tasks.values() if t.status == MockTaskStatus.IN_PROGRESS]
    )
    completed_tasks = len(
        [t for t in tasks.values() if t.status == MockTaskStatus.COMPLETED]
    )
    blocked_tasks = len(
        [t for t in tasks.values() if t.status == MockTaskStatus.BLOCKED]
    )

    completed_times = []
    for task in tasks.values():
        if task.status == MockTaskStatus.COMPLETED:
            elapsed = task.get_elapsed_time()
            if elapsed is not None:
                completed_times.append(elapsed)

    avg_completion_time = (
        sum(completed_times) / len(completed_times) if completed_times else 0
    )

    return {
        "total_tasks": total_tasks,
        "available_tasks": available_tasks,
        "claimed_tasks": claimed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "blocked_tasks": blocked_tasks,
        "avg_completion_time_hours": avg_completion_time,
        "workflow_stats": workflow_stats.copy(),
    }


def get_task_summary(
    tasks: Dict[str, DevelopmentTask], workflow_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """Return statistics with completion rate."""
    stats = get_task_statistics(tasks, workflow_stats)
    total = stats["total_tasks"]
    completed = stats["completed_tasks"]
    stats["completion_rate"] = (completed / total * 100) if total else 0
    return stats


def get_priority_distribution(tasks: Dict[str, DevelopmentTask]) -> Dict[str, int]:
    """Count tasks by priority."""
    distribution: Dict[str, int] = {}
    for priority in MockTaskPriority:
        distribution[priority.name] = len(
            [t for t in tasks.values() if t.priority == priority]
        )
    return distribution


def get_complexity_distribution(tasks: Dict[str, DevelopmentTask]) -> Dict[str, int]:
    """Count tasks by complexity."""
    distribution: Dict[str, int] = {}
    for complexity in MockTaskComplexity:
        distribution[complexity.name] = len(
            [t for t in tasks.values() if t.complexity == complexity]
        )
    return distribution


__all__ = [
    "get_task_statistics",
    "get_task_summary",
    "get_priority_distribution",
    "get_complexity_distribution",
]
