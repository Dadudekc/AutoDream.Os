import subprocess
from dataclasses import dataclass
from typing import List


@dataclass
class TestResult:
    """Result of executing a single test file."""
    file: str
    passed: bool
    output: str


class TestExecutor:
    """Run tests and collect their results."""

    def run(self, test_files: List[str]) -> List[TestResult]:
        results: List[TestResult] = []
        for path in test_files:
            proc = subprocess.run(
                ["python", "-m", "pytest", path, "-q"],
                capture_output=True,
                text=True,
            )
            results.append(
                TestResult(
                    file=path,
                    passed=proc.returncode == 0,
                    output=proc.stdout + proc.stderr,
                )
            )
        return results
