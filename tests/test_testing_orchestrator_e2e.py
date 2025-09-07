"""End-to-end tests for the lightweight TestingOrchestrator."""
from src.autonomous_development.testing import TestingOrchestrator
from src.autonomous_development.testing.workflow_setup import TestConfig


def test_orchestrator_runs_and_reports(tmp_path):
    """The orchestrator should discover, execute and summarise tests."""
    # Create one passing and one failing test
    passing = tmp_path / "test_pass.py"
    failing = tmp_path / "test_fail.py"
    passing.write_text("def test_pass():\n    assert True\n")
    failing.write_text("def test_fail():\n    assert False\n")

    orchestrator = TestingOrchestrator(TestConfig(test_directory=str(tmp_path)))
    orchestrator.run_tests(test_suite_name="suite")

    summary = orchestrator.get_test_summary("suite")
    assert summary["total_tests"] == 2
    assert summary["passed_tests"] == 1
    assert summary["failed_tests"] == 1
