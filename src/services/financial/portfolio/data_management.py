"""Data persistence for portfolio performance tracking."""

import json
import logging
from pathlib import Path
from typing import List

from .models import PerformanceReport, PerformanceSnapshot

logger = logging.getLogger(__name__)


class PerformanceDataManager:
    """Handles saving and loading performance data from disk."""

    def __init__(self, data_dir: str = "portfolio_tracking") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_file = self.data_dir / "performance_history.json"
        self.reports_file = self.data_dir / "performance_reports.json"

    # ------------------------------------------------------------------
    def save_snapshot(self, snapshot: PerformanceSnapshot) -> None:
        """Persist a performance snapshot."""

        try:
            history = [s.to_dict() for s in self.load_history()]
            history.append(snapshot.to_dict())
            with open(self.snapshots_file, "w", encoding="utf-8") as fh:
                json.dump(history, fh)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error saving performance snapshot: {exc}")
            raise

    def load_history(self) -> List[PerformanceSnapshot]:
        """Load all saved snapshots."""

        try:
            if not self.snapshots_file.exists():
                return []
            with open(self.snapshots_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return [PerformanceSnapshot.from_dict(d) for d in data]
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error loading performance history: {exc}")
            return []

    def save_report(self, report: PerformanceReport) -> None:
        """Persist a performance report."""

        try:
            reports = []
            if self.reports_file.exists():
                with open(self.reports_file, "r", encoding="utf-8") as fh:
                    reports = json.load(fh)
            reports.append(report.to_dict())
            with open(self.reports_file, "w", encoding="utf-8") as fh:
                json.dump(reports, fh)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error saving performance report: {exc}")
            raise
