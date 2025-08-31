from tests.coordinator import TestCoordinator


def test_coordinator_runs_all(tmp_path):
    module = tmp_path / "math_ops.py"
    module.write_text("def mul(a, b):\n    return a * b\n")
    test_file = tmp_path / "test_math_ops.py"
    test_file.write_text(
        "from math_ops import mul\n\n\ndef test_mul():\n    assert mul(2, 3) == 6\n"
    )

    coordinator = TestCoordinator(tmp_path, tmp_path)
    result = coordinator.run()
    assert result["passed"] is True
    assert result["coverage"] >= 100.0
