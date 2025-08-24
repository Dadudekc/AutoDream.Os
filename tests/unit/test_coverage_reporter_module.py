from src.testing.coverage_reporter import CoverageReporter


def test_coverage_reporter_runs(tmp_path):
    module = tmp_path / "mod.py"
    module.write_text("def add(a, b):\n    return a + b\n")
    test_file = tmp_path / "test_mod.py"
    test_file.write_text("from mod import add\n\n\ndef test_add():\n    assert add(1, 2) == 3\n")

    reporter = CoverageReporter(tmp_path, tmp_path)
    coverage = reporter.run()
    assert coverage == 100.0
