from testing.infrastructure.executor import run_tests


def test_executor_runs_tests(tmp_path):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_ok():\n    assert 1 == 1\n")

    result = run_tests([test_file], tmp_path)
    assert result["passed"] is True
    assert result["coverage"] >= 100.0
