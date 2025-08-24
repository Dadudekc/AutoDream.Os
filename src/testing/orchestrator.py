"""Thin orchestrator wiring testing utilities together."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from .dependency_manager import DependencyManager
from .runner import TestRunner
from .coverage_reporter import CoverageReporter


class TestOrchestrator:
    """Coordinate dependency checks, test execution and coverage."""

    def __init__(self, source_path: Path, tests_path: Path):
        self.source_path = Path(source_path)
        self.tests_path = Path(tests_path)
        self.dependency_manager = DependencyManager()
        self.test_runner = TestRunner(self.tests_path)
        self.coverage_reporter = CoverageReporter(self.source_path, self.tests_path)

    def run(self) -> Dict[str, float | bool]:
        """Run dependency checks, tests and coverage reporting."""
        deps = self.dependency_manager.ensure(["pytest", "coverage"])
        if not all(deps.values()):
            missing = ", ".join(name for name, ok in deps.items() if not ok)
            raise RuntimeError(f"Missing dependencies: {missing}")

        rc, out, err = self.test_runner.run(["-q"])
        if rc != 0:
            raise RuntimeError(f"Tests failed: {out} {err}")

        coverage = self.coverage_reporter.run()
        return {"passed": True, "coverage": coverage}
