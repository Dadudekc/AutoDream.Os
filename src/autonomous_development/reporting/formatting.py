from typing import Any, Dict, List, Optional, TYPE_CHECKING

    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager_refactored import DevelopmentTaskManager as TaskManager
from .config import (
from __future__ import annotations

"""Utility helpers for formatting development reports.

Functions in this module are intentionally stateless and reusable.  They
consume simple data structures and return formatted strings suitable for
CLI output or message dispatching.
"""


    AGENT1_TEMPLATE,
    COMPLEXITY_ICONS,
    NO_TASKS_TEMPLATE,
    PRIORITY_ICONS,
    PROGRESS_UPDATE_BLOCKERS_TEMPLATE,
    PROGRESS_UPDATE_TEMPLATE,
    REMAINING_TASKS_TEMPLATE,
    STATUS_ICONS,
    TASK_CLAIMED_TEMPLATE,
    WORKFLOW_COMPLETE_TEMPLATE,
    WORKFLOW_START_TEMPLATE,
)

if TYPE_CHECKING:  # pragma: no cover - only for type hints


# ---------------------------------------------------------------------------
# Basic icon helpers
# ---------------------------------------------------------------------------


def _get_priority_icon(priority: int) -> str:
    """Return emoji representing a numeric priority."""
    if priority >= 8:
        return PRIORITY_ICONS["high"]
    if priority >= 5:
        return PRIORITY_ICONS["medium"]
    return PRIORITY_ICONS["low"]


def _get_complexity_icon(complexity: str) -> str:
    """Return emoji representing complexity."""
    return COMPLEXITY_ICONS.get(complexity, COMPLEXITY_ICONS["low"])


def _get_status_icon(status: str) -> str:
    """Return emoji representing task status."""
    return STATUS_ICONS.get(status, "❓")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def format_task_list(tasks: List["DevelopmentTask"]) -> str:
    """Format task list for agents."""
    if not tasks:
        return "No tasks available for claiming."

    task_lines: List[str] = []
    for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
        priority_icon = _get_priority_icon(task.priority)
        complexity_icon = _get_complexity_icon(task.complexity)
        task_lines.append(
            f"{priority_icon} **{task.title}** (Priority: {task.priority})\n"
            f"   {complexity_icon} Complexity: {task.complexity.title()}\n"
            f"   ⏱️ Estimated: {task.estimated_hours}h\n"
            f"   🎯 Skills: {', '.join(task.required_skills)}\n"
            f"   📝 {task.description}\n"
            f"   🆔 Task ID: {task.task_id}\n"
        )
    return "\n".join(task_lines)


def format_progress_summary(task_manager: "TaskManager") -> str:
    """Format progress summary for all agents."""
    active_tasks = [
        t for t in task_manager.tasks.values() if t.status in ["claimed", "in_progress"]
    ]
    if not active_tasks:
        return "No active tasks to report progress on."

    progress_lines: List[str] = []
    for task in active_tasks:
        status_icon = _get_status_icon(task.status)
        progress_lines.append(
            f"{status_icon} **{task.title}** (Agent: {task.claimed_by})\n"
            f"   📊 Progress: {task.progress_percentage:.1f}%\n"
            f"   🚫 Blockers: {', '.join(task.blockers) if task.blockers else 'None'}\n"
        )
    return "\n".join(progress_lines)


def format_cycle_summary(task_manager: "TaskManager") -> str:
    """Format cycle summary with statistics from the task manager."""
    summary = task_manager.get_task_summary()
    cycle_message = f"""🔄 CYCLE COMPLETE - SUMMARY:

📊 Task Status:
   • Total Tasks: {summary['total_tasks']}
   • Available: {summary['available_tasks']}
   • Claimed: {summary['claimed_tasks']}
   • In Progress: {summary['in_progress_tasks']}
   • Completed: {summary['completed_tasks']}
   • Completion Rate: {summary['completion_rate']:.1f}%

⏰ Overnight Progress:
   • Cycles Completed: {summary['workflow_stats']['overnight_cycles']}
   • Autonomous Hours: {summary['workflow_stats']['autonomous_hours']}
   • Total Tasks Completed: {summary['workflow_stats']['total_tasks_completed']}

🎯 Next Cycle: Task review and claiming phase begins..."""
    return cycle_message


def format_workflow_start_message() -> str:
    """Return workflow start announcement."""
    return WORKFLOW_START_TEMPLATE


def format_agent1_message() -> str:
    """Return Agent-1 role description."""
    return AGENT1_TEMPLATE


def format_no_tasks_message() -> str:
    """Return message when there are no tasks available."""
    return NO_TASKS_TEMPLATE


def format_task_claimed_message(task: "DevelopmentTask") -> str:
    """Return message when a task is claimed."""
    return TASK_CLAIMED_TEMPLATE.format(
        title=task.title,
        task_id=task.task_id,
        priority=task.priority,
        complexity=task.complexity,
        estimated_hours=task.estimated_hours,
        skills=", ".join(task.required_skills),
    )


def format_progress_update_message(
    task: "DevelopmentTask", new_progress: float, blockers: Optional[List[str]] = None
) -> str:
    """Return progress update message for an agent."""
    if blockers:
        return PROGRESS_UPDATE_BLOCKERS_TEMPLATE.format(
            title=task.title,
            progress=new_progress,
            blockers=", ".join(blockers),
        )
    return PROGRESS_UPDATE_TEMPLATE.format(title=task.title, progress=new_progress)


def format_workflow_complete_message(task_manager: "TaskManager") -> str:
    """Return final workflow completion message."""
    stats = task_manager.get_task_summary()["workflow_stats"]
    return WORKFLOW_COMPLETE_TEMPLATE.format(**stats)


def format_remaining_tasks_message(remaining_count: int) -> str:
    """Return message about remaining available tasks."""
    return REMAINING_TASKS_TEMPLATE.format(count=remaining_count)


def format_detailed_task_status(task_manager: "TaskManager") -> str:
    """Format detailed task status for CLI display."""
    summary = task_manager.get_task_summary()
    status_lines = [
        "📋 Current Development Task Status:",
        "=" * 60,
        f"Total Tasks: {summary['total_tasks']}",
        f"Available: {summary['available_tasks']}",
        f"Claimed: {summary['claimed_tasks']}",
        f"In Progress: {summary['in_progress_tasks']}",
        f"Completed: {summary['completed_tasks']}",
        f"Completion Rate: {summary['completion_rate']:.1f}%",
        "",
        "📊 Detailed Task List:",
    ]
    for task in task_manager.tasks.values():
        status_icon = _get_status_icon(task.status)
        status_lines.append(f"{status_icon} {task.task_id}: {task.title}")
        status_lines.append(f"   Status: {task.status}")
        if task.claimed_by:
            status_lines.append(f"   Agent: {task.claimed_by}")
        if task.progress_percentage > 0:
            status_lines.append(f"   Progress: {task.progress_percentage:.1f}%")
        status_lines.append("")
    return "\n".join(status_lines)


def format_workflow_statistics(task_manager: "TaskManager") -> str:
    """Format workflow statistics for CLI display."""
    summary = task_manager.get_task_summary()
    stats = summary["workflow_stats"]
    status_lines = [
        "📊 Autonomous Development Workflow Statistics:",
        "=" * 60,
        "📋 Task Statistics:",
        f"   Total Tasks Created: {stats['total_tasks_created']}",
        f"   Total Tasks Completed: {stats['total_tasks_completed']}",
        f"   Total Tasks Claimed: {stats['total_tasks_claimed']}",
        "",
        "🌙 Overnight Statistics:",
        f"   Overnight Cycles: {stats['overnight_cycles']}",
        f"   Autonomous Hours: {stats['autonomous_hours']}",
    ]
    if stats["total_tasks_created"] > 0:
        completion_rate = (
            stats["total_tasks_completed"] / stats["total_tasks_created"]
        ) * 100
        status_lines.append(f"   Overall Completion Rate: {completion_rate:.1f}%")
    return "\n".join(status_lines)


__all__ = [
    "format_task_list",
    "format_progress_summary",
    "format_cycle_summary",
    "format_workflow_start_message",
    "format_agent1_message",
    "format_no_tasks_message",
    "format_task_claimed_message",
    "format_progress_update_message",
    "format_workflow_complete_message",
    "format_remaining_tasks_message",
    "format_detailed_task_status",
    "format_workflow_statistics",
]
