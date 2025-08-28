"""Metrics utilities for tracking refactoring performance."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RefactoringMetrics:
    """Refactoring performance metrics."""
    total_files_processed: int = 0
    total_lines_reduced: int = 0
    total_time_saved: float = 0.0
    duplication_eliminated: float = 0.0
    architecture_improvements: int = 0
    quality_score: float = 0.0
    efficiency_gain: float = 0.0


def update_metrics(metrics: RefactoringMetrics, task, result: Dict[str, Any]) -> None:
    """Update refactoring metrics based on task result."""
    if result.get("success"):
        metrics.total_files_processed += 1
        metrics_data = result.get("metrics", {})
        if task.task_type == "extract_module":
            metrics.total_lines_reduced += metrics_data.get("reduction", 0)
            metrics.architecture_improvements += 1
        elif task.task_type == "consolidate_duplicates":
            metrics.duplication_eliminated += 10.0
            metrics.total_lines_reduced += metrics_data.get("lines_eliminated", 0)
        elif task.task_type == "optimize_architecture":
            metrics.architecture_improvements += 1
            metrics.quality_score += metrics_data.get("quality_improvement", 0)
