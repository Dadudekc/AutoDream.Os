from __future__ import annotations

"""Facade that wires together report generation, formatting and delivery."""

import logging
from pathlib import Path
from typing import Any, Dict, List

from .models import (
    HealthReport,
    ReportConfig,
    ReportFormat,
    ReportType,
)
from .report_builder import ReportGenerator
from .output_delivery import ReportDelivery

logger = logging.getLogger(__name__)


class HealthReportingGenerator:
    """High level API compatible with the legacy implementation."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.generator = ReportGenerator(charts_dir=self.config.get("charts_dir"))
        self.delivery = ReportDelivery(reports_dir=self.config.get("reports_dir"))
        logger.info("HealthReportingGenerator initialized")

    # ------------------------------------------------------------------
    def generate_report(
        self,
        health_data: Dict[str, Any],
        alerts_data: Dict[str, Any],
        config: ReportConfig,
    ) -> HealthReport:
        """Generate a report and immediately deliver it."""

        report = self.generator.generate_report(health_data, alerts_data, config)
        self.delivery.deliver(report, config.format)
        logger.info("Report generated: %s", report.report_id)
        return report

    # ------------------------------------------------------------------
    def get_report_history(self, limit: int = 50) -> List[Path]:
        return self.delivery.get_report_history(limit)

    def cleanup_old_reports(self, days_to_keep: int = 30) -> None:
        self.delivery.cleanup_old_reports(days_to_keep)

    # ------------------------------------------------------------------
    def run_smoke_test(self) -> bool:
        """Light‑weight smoke test used in the unit tests."""
        try:
            mock_health = {"agents": {"agent_1": {"overall_status": "good", "health_score": 90.0}}}
            mock_alerts = {"alerts": []}
            cfg = ReportConfig(report_type=ReportType.DAILY_SUMMARY, format=ReportFormat.JSON)
            report = self.generate_report(mock_health, mock_alerts, cfg)
            return (self.delivery.reports_dir / f"{report.report_id}.json").exists()
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Smoke test failed: %s", exc)
            return False

    def shutdown(self) -> None:  # pragma: no cover - simple facade
        logger.info("HealthReportingGenerator shutdown complete")


def main() -> None:  # pragma: no cover - CLI helper
    import argparse

    parser = argparse.ArgumentParser(description="Health Reporting Generator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()

    generator = HealthReportingGenerator()
    if args.test:
        success = generator.run_smoke_test()
        generator.shutdown()
        raise SystemExit(0 if success else 1)
    parser.print_help()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
