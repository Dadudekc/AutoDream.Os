"""Base Test Runner - shared functionality for running tests."""
from pathlib import Path
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

from .generation import build_pytest_command, discover_tests
from .execution import execute_command
from .reporting import parse_test_results, save_results, print_summary


class BaseTestRunner(ABC):
    """Base class for all test runners with common functionality."""

    def __init__(self, repo_root: Path):
        """Initialize the base test runner."""
        self.repo_root = repo_root
        self.tests_dir = repo_root / "tests"
        self.src_dir = repo_root / "src"
        self.results_dir = repo_root / "test_results"
        self.coverage_dir = repo_root / "htmlcov"
        self.results_dir.mkdir(exist_ok=True)
        self.coverage_dir.mkdir(exist_ok=True)

    def discover_tests(
        self, test_type: Optional[str] = None, pattern: str = "test_*.py"
    ) -> List[Path]:
        """Discover test files based on type and pattern."""
        return discover_tests(self.tests_dir, self.repo_root, test_type, pattern)

    def build_pytest_command(
        self,
        test_paths: List[Path],
        coverage: bool = True,
        parallel: bool = False,
        verbose: bool = True,
        markers: Optional[List[str]] = None,
    ) -> List[str]:
        """Build pytest command with specified options."""
        return build_pytest_command(
            test_paths,
            self.results_dir,
            coverage=coverage,
            parallel=parallel,
            verbose=verbose,
            markers=markers,
        )

    def execute_command(self, cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
        """Execute command and return results."""
        return execute_command(cmd, cwd=self.repo_root, timeout=timeout)

    def parse_test_results(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse test execution results."""
        return parse_test_results(execution_result)

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to file."""
        return save_results(results, self.results_dir, filename)

    def print_summary(self, results: Dict[str, Any]):
        """Print test results summary."""
        print_summary(results)

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Abstract method for running tests."""
        raise NotImplementedError
