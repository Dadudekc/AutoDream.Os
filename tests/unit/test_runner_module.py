from pathlib import Path

from src.testing.runner import TestRunner


def test_test_runner_executes_tests(tmp_path):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_ok():\n    assert 1 == 1\n")

    runner = TestRunner(tmp_path)
    rc, out, err = runner.run(["-q"])
    assert rc == 0
    assert "1 passed" in out
