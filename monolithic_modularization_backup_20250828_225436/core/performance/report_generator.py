"""Lightweight report generator for performance validation tests."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from .performance_types import (
    PerformanceBenchmark,
    PerformanceLevel,
    OptimizationTarget,
    SystemPerformanceReport,
)


class ReportGenerator:
    """Generate and format performance reports.

    This minimal implementation supports the subset of functionality
    required by the test suite. It deliberately avoids heavy dependencies
    from the full project.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def generate_performance_report(
        self,
        benchmarks: List[PerformanceBenchmark],
        overall_level: PerformanceLevel,
        enterprise_score: float,
        optimization_opportunities: List[OptimizationTarget],
    ) -> SystemPerformanceReport:
        report_id = f"report_{len(benchmarks)}"
        return SystemPerformanceReport(
            report_id=report_id,
            benchmarks=benchmarks,
            overall_level=overall_level,
            enterprise_score=enterprise_score,
            optimization_opportunities=optimization_opportunities,
        )

    def generate_benchmark_summary(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> Dict[str, Any]:
        return {"count": len(benchmarks)}

    def format_report_for_display(self, report: SystemPerformanceReport) -> str:
        return f"Report {report.report_id}: {report.overall_level.value}"
