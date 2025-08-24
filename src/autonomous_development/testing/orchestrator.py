"""Lightweight testing orchestrator."""
from typing import Any, Dict, List

from .workflow_setup import discover_tests, initialize_config
from .test_executor import run_tests
from .result_collation import summarize_results, TestResult, TestSummary


class TestingOrchestrator:
    """Coordinate test discovery, execution and collation."""

    __test__ = False  # Prevent pytest from collecting this class as a test

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = initialize_config(config)
        self.results: List[TestResult] = []

    def run(self) -> TestSummary:
        """Discover and execute tests, returning a summary."""
        test_files = discover_tests(self.config["test_directory"])
        self.results = run_tests(test_files, self.config)
        return summarize_results(self.results)
