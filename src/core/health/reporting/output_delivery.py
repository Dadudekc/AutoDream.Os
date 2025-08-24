from __future__ import annotations

"""Output delivery utilities for health reports."""

import logging
from pathlib import Path
from typing import List

from .models import HealthReport, ReportFormat
from .data_formatter import ReportFormatter

logger = logging.getLogger(__name__)


class ReportDelivery:
    """Handle saving or displaying formatted reports."""

    def __init__(self, reports_dir: str | Path | None = None) -> None:
        self.reports_dir = Path(reports_dir or "health_reports")
        self.reports_dir.mkdir(exist_ok=True)
        self.formatter = ReportFormatter()

    # ------------------------------------------------------------------
    def deliver(self, report: HealthReport, fmt: ReportFormat) -> Path | None:
        """Deliver *report* in the given *fmt*.

        For file based formats a path to the written file is returned.
        For console output ``None`` is returned after printing.
        """

        content = self.formatter.format(report, fmt)
        if fmt == ReportFormat.CONSOLE:
            print(content)
            return None

        extension = fmt.value if fmt != ReportFormat.JSON else "json"
        path = self.reports_dir / f"{report.report_id}.{extension}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Report saved: %s", path)
        return path

    # ------------------------------------------------------------------
    def get_report_history(self, limit: int = 50) -> List[Path]:
        files = sorted(self.reports_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        return files[:limit]

    def cleanup_old_reports(self, days_to_keep: int = 30) -> None:
        cutoff = __import__("datetime").datetime.now().timestamp() - days_to_keep * 86400
        for file in self.reports_dir.glob("*.json"):
            if file.stat().st_mtime < cutoff:
                file.unlink(missing_ok=True)
