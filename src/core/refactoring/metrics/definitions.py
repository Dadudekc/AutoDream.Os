"""Metric definitions for refactoring processes."""

from dataclasses import dataclass


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


class MetricsManager:
    """Manages refactoring metrics collection and reporting."""
    
    def __init__(self):
        self.metrics = RefactoringMetrics()
    
    def update_metrics(self, **kwargs):
        """Update metrics with new values."""
        for key, value in kwargs.items():
            if hasattr(self.metrics, key):
                setattr(self.metrics, key, value)
    
    def get_metrics(self) -> RefactoringMetrics:
        """Get current metrics."""
        return self.metrics
    
    def reset_metrics(self):
        """Reset all metrics to zero."""
        self.metrics = RefactoringMetrics()


def update_metrics(metrics_manager: MetricsManager, **kwargs):
    """Update metrics using the manager."""
    metrics_manager.update_metrics(**kwargs)