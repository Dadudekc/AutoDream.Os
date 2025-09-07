"""Orchestrates refactoring metrics workflow."""

from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any, Optional

from .definitions import RefactoringMetrics
from .calculator import update_metrics
from .storage import MetricsStorage


class MetricsManager:
    """High-level interface for metrics collection and storage."""

    def __init__(self, storage_path: Optional[Path] = None):
        self.metrics = RefactoringMetrics()
        self.storage: Optional[MetricsStorage] = None
        if storage_path:
            self.storage = MetricsStorage(storage_path)
            self.metrics = self.storage.load()

    def update(self, task, result: Dict[str, Any]) -> None:
        """Update metrics and persist if storage is configured."""
        update_metrics(self.metrics, task, result)
        if self.storage:
            self.storage.save(self.metrics)

    def snapshot(self) -> Dict[str, Any]:
        """Return current metrics as a dictionary."""
        return asdict(self.metrics)


__all__ = [
    "RefactoringMetrics",
    "update_metrics",
    "MetricsStorage",
    "MetricsManager",
]
