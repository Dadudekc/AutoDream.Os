#!/usr/bin/env python3
"""
Unified Reporting Framework - Agent Cellphone V2

Consolidates all scattered reporting implementations into a single,
unified framework eliminating 100% duplication.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3I - Reporting Systems Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional

from ..base_manager import (
    BaseManager,
    ManagerConfig,
    ManagerMetrics,
    ManagerPriority,
    ManagerStatus,
)
from .report_data_collector import ReportDataCollector
from .report_formatter import ReportFormatter
from .report_models import ReportConfig, ReportFormat, ReportType, UnifiedReport
from .report_output import ReportOutput


class UnifiedReportingFramework(BaseManager):
    """Central coordinator for report generation, formatting and output."""

    def __init__(
        self,
        manager_id: str,
        name: str = "Unified Reporting Framework",
        description: str = "",
    ) -> None:
        super().__init__(manager_id, name, description)

        self.collector = ReportDataCollector()
        self.formatter = ReportFormatter()
        self.output = ReportOutput(self.formatter, self.collector)

        self.logger.info(f"UnifiedReportingFramework initialized: {manager_id}")

    def generate_report(
        self,
        report_type: ReportType,
        data: Dict[str, Any],
        config: Optional[ReportConfig] = None,
    ) -> UnifiedReport:
        try:
            return self.collector.generate(report_type, data, config)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(
                f"Failed to generate {report_type.value} report: {e}"
            )
            raise

    def format_report(self, report: UnifiedReport, format_type: ReportFormat) -> str:
        try:
            return self.formatter.format(report, format_type)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to format report: {e}")
            return f"Error formatting report: {str(e)}"

    def save_report(
        self,
        report: UnifiedReport,
        format_type: Optional[ReportFormat] = None,
        filename: Optional[str] = None,
    ) -> str:
        try:
            return self.output.save(report, format_type, filename)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to save report: {e}")
            raise

    def get_report_history(
        self, report_type: Optional[ReportType] = None, limit: int = 100
    ) -> List[UnifiedReport]:
        return self.collector.get_report_history(report_type, limit)

    def cleanup_old_reports(self, days_to_keep: int = 30) -> int:
        return self.collector.cleanup_old_reports(days_to_keep)

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "total_reports_generated": len(self.collector.report_history),
            "generators_available": len(self.collector.report_generators),
            "supported_report_types": [
                rt.value for rt in self.collector.report_generators.keys()
            ],
            "supported_formats": [rf.value for rf in ReportFormat],
            "last_report_time": self.collector.report_history[-1].metadata.timestamp.isoformat()
            if self.collector.report_history
            else None,
        }


def main() -> int:
    """Main entry point for unified reporting framework."""
    framework = UnifiedReportingFramework("test_manager", "Test Reporting Framework")

    # Generate test report
    test_data = {
        "test_results": [
            {"name": "test_1", "status": "passed", "duration": 0.5},
            {"name": "test_2", "status": "failed", "duration": 1.2},
            {"name": "test_3", "status": "passed", "duration": 0.8},
        ],
        "coverage_data": {"total_coverage": 85.5},
    }

    try:
        report = framework.generate_report(ReportType.TESTING, test_data)
        print(f"Generated report: {report.metadata.report_id}")

        # Format and save
        _ = framework.format_report(report, ReportFormat.JSON)
        file_path = framework.save_report(report, ReportFormat.TEXT)
        print(f"Report saved to: {file_path}")

        status = framework.get_system_status()
        print(f"System status: {status}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
