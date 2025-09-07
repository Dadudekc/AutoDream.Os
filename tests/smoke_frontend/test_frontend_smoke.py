"""Smoke test for frontend testing runner."""

from src.web.frontend.frontend_testing import FrontendTestRunner


def test_frontend_runner_smoke():
    runner = FrontendTestRunner()
    suite = runner.run_component_tests()
    assert suite.total_tests > 0
    assert suite.passed_tests == suite.total_tests
