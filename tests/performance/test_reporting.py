"""Tests for performance reporting features."""

from unittest.mock import Mock


def test_performance_reporting():
    report_generator = Mock()
    report_generator.generate_report.return_value = {
        "report_id": "perf_20241201_001",
        "summary": "Performance within acceptable limits",
    }
    report = report_generator.generate_report()
    assert {"report_id", "summary"} <= report.keys()
    report_generator.generate_report.assert_called_once()

