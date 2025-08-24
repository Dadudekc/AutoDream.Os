from dataclasses import dataclass
from typing import List

from .test_execution import TestResult


@dataclass
class TestSuite:
    """Summary information for a collection of tests."""
    name: str
    total_tests: int
    passed_tests: int
    failed_tests: int


def collate_results(results: List[TestResult], suite_name: str) -> TestSuite:
    """Produce a summary for executed test results."""
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    return TestSuite(
        name=suite_name,
        total_tests=len(results),
        passed_tests=passed,
        failed_tests=failed,
    )
