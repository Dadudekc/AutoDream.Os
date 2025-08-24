"""End-to-end test for the lightweight testing orchestrator."""
from pathlib import Path

from autonomous_development.testing.orchestrator import TestingOrchestrator


def test_orchestrator_runs_tests(tmp_path: Path) -> None:
    """The orchestrator should discover and execute tests."""
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_pass():\n    assert 2 + 2 == 4\n")

    orchestrator = TestingOrchestrator({"test_directory": str(tmp_path)})
    summary = orchestrator.run()

    assert summary.total == 1
    assert summary.passed == 1
    assert summary.failed == 0
