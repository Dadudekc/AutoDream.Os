from __future__ import annotations

"""Components for test orchestration.

This module provides small, focused classes used by the test
orchestrator. Each class has a single responsibility which makes the
system easier to test and maintain.
"""

from dataclasses import dataclass
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


class SubprocessHandler:
    """Execute commands and capture their output."""

    def run(
        self,
        cmd: List[str],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run ``cmd`` and return the completed process information.

        Parameters
        ----------
        cmd:
            Command arguments to execute.
        cwd:
            Optional working directory for the command.
        timeout:
            Maximum time in seconds to allow the command to run.
        """
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


class ResultAggregator:
    """Collect results and provide summary information."""

    def __init__(self) -> None:
        self._results: List[Dict[str, Any]] = []

    def add(self, result: Dict[str, Any]) -> None:
        self._results.append(result)

    def summary(self) -> Dict[str, int]:
        total = len(self._results)
        successes = sum(1 for r in self._results if r.get("success"))
        failures = total - successes
        return {"total": total, "successes": successes, "failures": failures}


@dataclass
class CoverageReporter:
    """Report code coverage based on a JSON file."""

    coverage_file: Path

    def report(self) -> float:
        """Return the percentage of code covered.

        If the coverage file is missing or malformed, ``0.0`` is returned.
        """
        try:
            data = json.loads(self.coverage_file.read_text())
            return float(data.get("totals", {}).get("percent_covered", 0.0))
        except Exception:
            return 0.0


class RunOrchestrator:
    """Coordinate test execution, result aggregation and coverage reporting."""

    def __init__(
        self,
        subprocess_handler: SubprocessHandler,
        aggregator: ResultAggregator,
        coverage_reporter: CoverageReporter,
    ) -> None:
        self._subprocess_handler = subprocess_handler
        self._aggregator = aggregator
        self._coverage_reporter = coverage_reporter

    def run_commands(
        self,
        commands: Iterable[List[str]],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        outputs: List[Dict[str, Any]] = []
        for cmd in commands:
            result = self._subprocess_handler.run(cmd, cwd=cwd, timeout=timeout)
            result["success"] = result["returncode"] == 0
            self._aggregator.add({"success": result["success"]})
            outputs.append(result)

        summary = self._aggregator.summary()
        coverage = self._coverage_reporter.report()
        return {"outputs": outputs, "summary": summary, "coverage": coverage}
