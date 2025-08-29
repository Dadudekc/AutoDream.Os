"""Calculation logic for refactoring metrics."""

from typing import Dict, Any

from .definitions import RefactoringMetrics


def update_metrics(metrics: RefactoringMetrics, task, result: Dict[str, Any]) -> None:
    """Update refactoring metrics based on task result."""
    if result.get("success"):
        metrics.total_files_processed += 1
        metrics_data = result.get("metrics", {})
        task_type = getattr(task, "task_type", None)

        if task_type == "extract_module":
            metrics.total_lines_reduced += metrics_data.get("reduction", 0)
            metrics.architecture_improvements += 1
        elif task_type == "consolidate_duplicates":
            metrics.duplication_eliminated += metrics_data.get("lines_eliminated", 0)
            metrics.total_lines_reduced += metrics_data.get("lines_eliminated", 0)
        elif task_type == "optimize_architecture":
            metrics.architecture_improvements += 1
            metrics.quality_score += metrics_data.get("quality_improvement", 0)

        metrics.total_time_saved += metrics_data.get("time_saved", 0.0)
        metrics.efficiency_gain += metrics_data.get("efficiency_gain", 0.0)
