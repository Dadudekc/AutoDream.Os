from src.testing.orchestrator import TestOrchestrator


def test_orchestrator_runs_all(tmp_path):
    module = tmp_path / "math_ops.py"
    module.write_text("def mul(a, b):\n    return a * b\n")
    test_file = tmp_path / "test_math_ops.py"
    test_file.write_text("from math_ops import mul\n\n\ndef test_mul():\n    assert mul(2, 3) == 6\n")

    orchestrator = TestOrchestrator(tmp_path, tmp_path)
    result = orchestrator.run()
    assert result["passed"] is True
    assert result["coverage"] >= 100.0
