"""Generate coverage metrics for test suites."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .utils import run_command


class CoverageReporter:
    """Run tests with coverage and report percentage."""

    def __init__(self, source_path: Path, tests_path: Path):
        self.source_path = Path(source_path)
        self.tests_path = Path(tests_path)

    def run(self) -> float:
        """Execute coverage analysis and return total percentage."""
        # Run tests with coverage
        cmd = [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--source",
            str(self.source_path),
            "-m",
            "pytest",
            str(self.tests_path),
        ]
        rc, out, err = run_command(cmd, cwd=self.tests_path)
        if rc != 0:
            raise RuntimeError(f"Coverage run failed: {out} {err}")

        # Produce JSON report
        rc, out, err = run_command(
            [sys.executable, "-m", "coverage", "json", "-o", "coverage.json"],
            cwd=self.tests_path,
        )
        if rc != 0:
            raise RuntimeError(f"Coverage json failed: {out} {err}")

        data = json.loads((self.tests_path / "coverage.json").read_text())
        return float(data.get("totals", {}).get("percent_covered", 0.0))
