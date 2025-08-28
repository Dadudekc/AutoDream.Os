"""Report generation helpers.

Currently only a performance report is implemented.  Additional report
builders can be added here in the future without touching the manager.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from src.core.task_manager import DevelopmentTaskManager as TaskManager


def generate_performance_report(task_manager: "TaskManager") -> Dict[str, Any]:
    """Create a performance report from task manager statistics."""
    summary = task_manager.get_task_summary()
    stats = summary["workflow_stats"]

    total_tasks = summary["total_tasks"]
    completed_tasks = summary["completed_tasks"]

    efficiency_score = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0
    avg_cycle_efficiency = (
        completed_tasks / stats["overnight_cycles"]
        if stats["overnight_cycles"] > 0
        else 0.0
    )

    report = {
        "summary": summary,
        "workflow_stats": stats,
        "performance_metrics": {
            "efficiency_score": efficiency_score,
            "avg_cycle_efficiency": avg_cycle_efficiency,
            "task_completion_rate": summary["completion_rate"],
            "autonomous_productivity": completed_tasks
            / max(stats["autonomous_hours"], 1),
        },
        "generated_at": datetime.utcnow().isoformat(),
    }
    return report


__all__ = ["generate_performance_report"]
