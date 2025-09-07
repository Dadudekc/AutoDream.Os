"""Testing report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class TestingReportGenerator(ReportGenerator):
    """Generates testing reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a testing report."""
        test_results = data.get("test_results", [])
        coverage_data = data.get("coverage_data", {})

        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.get("status") == "passed")
        failed_tests = sum(1 for r in test_results if r.get("status") == "failed")
        coverage_percentage = coverage_data.get("total_coverage", 0.0)

        content = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100)
                if total_tests > 0
                else 0,
            },
            "coverage": coverage_data,
            "test_details": test_results,
        }

        summary = (
            f"Testing Report: {passed_tests}/{total_tests} tests passed "
            f"({content['test_summary']['success_rate']:.1f}% success rate)"
        )

        recommendations = []
        if content["test_summary"]["success_rate"] < 80:
            recommendations.append(
                "Test success rate below 80% - investigate failing tests"
            )
        if coverage_percentage < 70:
            recommendations.append("Test coverage below 70% - add more test cases")

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.TESTING,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_testing_framework",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )
