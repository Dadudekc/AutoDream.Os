"""Performance report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class PerformanceReportGenerator(ReportGenerator):
    """Generates performance reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a performance report."""
        benchmarks = data.get("benchmarks", [])
        metrics = data.get("metrics", {})

        total_benchmarks = len(benchmarks)
        passed_benchmarks = sum(1 for b in benchmarks if b.get("status") == "passed")
        performance_score = metrics.get("overall_score", 0.0)

        content = {
            "performance_summary": {
                "total_benchmarks": total_benchmarks,
                "passed_benchmarks": passed_benchmarks,
                "performance_score": performance_score,
                "benchmark_success_rate": (passed_benchmarks / total_benchmarks * 100)
                if total_benchmarks > 0
                else 0,
            },
            "benchmarks": benchmarks,
            "metrics": metrics,
        }

        summary = (
            f"Performance Report: {passed_benchmarks}/{total_benchmarks} benchmarks "
            f"passed (Score: {performance_score:.1f})"
        )

        recommendations = []
        if content["performance_summary"]["benchmark_success_rate"] < 90:
            recommendations.append(
                "Benchmark success rate below 90% - investigate performance issues"
            )
        if performance_score < 70:
            recommendations.append(
                "Performance score below 70 - optimize system performance"
            )

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.PERFORMANCE,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_performance_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )
