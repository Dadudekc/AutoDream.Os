import logging
from datetime import datetime

from src.web.frontend.frontend_testing import TestSuite, TestResult
from src.web.frontend.reporting import generate_summary_report


def test_generate_summary_report(caplog):
    suite = TestSuite(
        name="demo",
        description="demo suite",
        tests=[
            TestResult(
                test_name="t1",
                test_type="component",
                status="passed",
                duration=0.1,
                error_message=None,
                component_tested=None,
                route_tested=None,
                timestamp=datetime.now(),
                metadata={},
            )
        ],
        total_tests=1,
        passed_tests=1,
        failed_tests=0,
        skipped_tests=0,
        total_duration=0.1,
        created_at=datetime.now(),
    )
    with caplog.at_level(logging.INFO):
        generate_summary_report({"demo": suite})
    assert "FRONTEND TESTING SUMMARY REPORT" in caplog.text
