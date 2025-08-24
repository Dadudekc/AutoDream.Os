"""Utilities for collating and summarising test results."""
from dataclasses import dataclass
from typing import List


@dataclass
class TestResult:
    """Outcome of a single test file."""
    file: str
    returncode: int
    stdout: str
    stderr: str


@dataclass
class TestSummary:
    """Simple summary of executed tests."""
    total: int
    passed: int
    failed: int


def summarize_results(results: List[TestResult]) -> TestSummary:
    """Create a :class:`TestSummary` from individual ``results``."""
    total = len(results)
    passed = len([r for r in results if r.returncode == 0])
    failed = total - passed
    return TestSummary(total=total, passed=passed, failed=failed)
