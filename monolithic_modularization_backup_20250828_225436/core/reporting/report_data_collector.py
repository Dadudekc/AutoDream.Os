from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

from .generators import (
from .report_models import ReportConfig, ReportFormat, ReportType, UnifiedReport
from __future__ import annotations

"""Collects and manages report data and generator instances."""



    AnalyticsReportGenerator,
    ComplianceReportGenerator,
    CustomReportGenerator,
    FinancialReportGenerator,
    HealthReportGenerator,
    PerformanceReportGenerator,
    QualityReportGenerator,
    ReportGenerator,
    SecurityReportGenerator,
    TestingReportGenerator,
)


class ReportDataCollector:
    """Handles report generation and history tracking."""

    def __init__(self) -> None:
        self.report_generators: Dict[ReportType, ReportGenerator] = {}
        self.report_history: List[UnifiedReport] = []
        self.max_history = 1000
        self.logger = logging.getLogger(f"{__name__}.ReportDataCollector")
        self._initialize_generators()

    def _initialize_generators(self) -> None:
        """Initialize report generators for each type."""
        for report_type in ReportType:
            config = ReportConfig(
                report_type=report_type,
                format=ReportFormat.JSON,
                output_directory=f"reports/{report_type.value}",
            )

            if report_type == ReportType.TESTING:
                self.report_generators[report_type] = TestingReportGenerator(config)
            elif report_type == ReportType.PERFORMANCE:
                self.report_generators[report_type] = PerformanceReportGenerator(config)
            elif report_type == ReportType.HEALTH:
                self.report_generators[report_type] = HealthReportGenerator(config)
            elif report_type == ReportType.SECURITY:
                self.report_generators[report_type] = SecurityReportGenerator(config)
            elif report_type == ReportType.COMPLIANCE:
                self.report_generators[report_type] = ComplianceReportGenerator(config)
            elif report_type == ReportType.QUALITY:
                self.report_generators[report_type] = QualityReportGenerator(config)
            elif report_type == ReportType.ANALYTICS:
                self.report_generators[report_type] = AnalyticsReportGenerator(config)
            elif report_type == ReportType.FINANCIAL:
                self.report_generators[report_type] = FinancialReportGenerator(config)
            elif report_type == ReportType.CUSTOM:
                self.report_generators[report_type] = CustomReportGenerator(config)
            else:
                self.report_generators[report_type] = ReportGenerator(config)

    def generate(
        self,
        report_type: ReportType,
        data: Dict[str, Any],
        config: Optional[ReportConfig] = None,
    ) -> UnifiedReport:
        """Generate a report and track it in history."""
        if report_type not in self.report_generators:
            raise ValueError(f"No generator available for report type: {report_type}")

        if config:
            generator = self.report_generators[report_type]
            generator.config = config
            generator.output_dir = Path(config.output_directory)

        report = self.report_generators[report_type].generate_report(data)
        self._add_to_history(report)
        self.logger.info(
            f"Generated {report_type.value} report: {report.metadata.report_id}"
        )
        return report

    def get_report_history(
        self, report_type: Optional[ReportType] = None, limit: int = 100
    ) -> List[UnifiedReport]:
        """Return report history filtered by type."""
        if report_type:
            filtered = [
                r for r in self.report_history if r.metadata.report_type == report_type
            ]
            return filtered[-limit:]
        return self.report_history[-limit:]

    def cleanup_old_reports(self, days_to_keep: int = 30) -> int:
        """Remove old reports from history and disk."""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)

        initial_count = len(self.report_history)
        self.report_history = [
            r
            for r in self.report_history
            if r.metadata.timestamp.timestamp() > cutoff_date
        ]
        history_cleaned = initial_count - len(self.report_history)

        files_cleaned = 0
        for generator in self.report_generators.values():
            if hasattr(generator, "output_dir") and generator.output_dir.exists():
                for file_path in generator.output_dir.glob("*"):
                    if file_path.is_file():
                        file_age = (
                            datetime.now().timestamp() - file_path.stat().st_mtime
                        )
                        if file_age > (days_to_keep * 24 * 60 * 60):
                            file_path.unlink()
                            files_cleaned += 1

        total_cleaned = history_cleaned + files_cleaned
        self.logger.info(f"Cleanup completed: {total_cleaned} items removed")
        return total_cleaned

    def _add_to_history(self, report: UnifiedReport) -> None:
        self.report_history.append(report)
        if len(self.report_history) > self.max_history:
            self.report_history = self.report_history[-self.max_history :]
