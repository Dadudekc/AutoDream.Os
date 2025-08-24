"""Lightweight testing orchestrator.

The orchestrator delegates responsibilities to small modules:
- :mod:`workflow_setup` for locating tests
- :mod:`test_execution` for running tests
- :mod:`result_collation` for summarising outcomes
"""
from typing import Dict, List, Optional

from .workflow_setup import TestConfig, discover_tests
from .test_execution import TestExecutor, TestResult
from .result_collation import TestSuite, collate_results


class TestingOrchestrator:
    """Compose workflow setup, execution and result collation."""

    def __init__(self, config: Optional[TestConfig] = None):
        self.config = config or TestConfig()
        self.executor = TestExecutor()
        self._suites: Dict[str, TestSuite] = {}

    def run_tests(
        self,
        test_files: Optional[List[str]] = None,
        test_suite_name: str = "default",
    ) -> bool:
        """Execute tests and store a summary."""
        files = test_files or discover_tests(self.config)
        results = self.executor.run(files)
        self._suites[test_suite_name] = collate_results(results, test_suite_name)
        return True

    def get_test_summary(self, test_suite_name: Optional[str] = None) -> Dict[str, Dict[str, int]]:
        """Return stored summary information."""
        if test_suite_name:
            suite = self._suites.get(test_suite_name)
            if not suite:
                return {}
            return {
                "total_tests": suite.total_tests,
                "passed_tests": suite.passed_tests,
                "failed_tests": suite.failed_tests,
            }
        return {
            name: {
                "total_tests": s.total_tests,
                "passed_tests": s.passed_tests,
                "failed_tests": s.failed_tests,
            }
            for name, s in self._suites.items()
        }

    def clear_results(self) -> None:
        """Remove stored test suite summaries."""
        self._suites.clear()
