import importlib.util
from pathlib import Path


def load_reporter():
    spec = importlib.util.spec_from_file_location(
        "reporting", Path(__file__).resolve().parents[2] / "src/ai_ml/testing/reporting.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TestReporter


def test_summarize():
    TestReporter = load_reporter()
    reporter = TestReporter()
    results = [
        {"return_code": 0, "passed": 1, "failed": 0, "total": 1},
        {"return_code": 1, "passed": 0, "failed": 1, "total": 1},
    ]
    summary = reporter.summarize(results)
    assert summary["total_runs"] == 2
    assert summary["successful_runs"] == 1
    assert summary["failed_runs"] == 1
    assert summary["passed"] == 1
    assert summary["failed"] == 1
