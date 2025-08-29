"""Storage utilities for refactoring metrics."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from .definitions import RefactoringMetrics


class MetricsStorage:
    """Persist and load metrics data."""

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = (
            Path(file_path) if file_path else Path("refactoring_metrics.json")
        )

    def save(self, metrics: RefactoringMetrics) -> None:
        """Save metrics to JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2)

    def load(self) -> RefactoringMetrics:
        """Load metrics from JSON file."""
        if not self.file_path.exists():
            return RefactoringMetrics()
        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return RefactoringMetrics(**data)
