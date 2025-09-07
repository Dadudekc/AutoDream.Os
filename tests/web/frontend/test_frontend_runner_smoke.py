from src.web.frontend.frontend_testing import FrontendTestRunner


def test_frontend_test_runner_smoke():
    runner = FrontendTestRunner()
    suites = runner.run_all_tests()
    assert "component" in suites
    assert "routing" in suites
    assert "integration" in suites
