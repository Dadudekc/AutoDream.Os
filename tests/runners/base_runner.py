"""
Base Test Runner - Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - Unified Test Runner System

Common functionality for all test runners, eliminating duplication
across the previous 3 separate test runners.
"""

import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod

from tests.testing_config import (
    REPO_ROOT,
    TESTS_DIR,
    SRC_DIR,
    RESULTS_DIR,
    COVERAGE_DIR,
)
from tests.submodules.environment_setup import prepare_environment
from tests.submodules.cleanup import cleanup_artifacts


class BaseTestRunner(ABC):
    """Base class for all test runners with common functionality."""

    def __init__(self, repo_root: Path = REPO_ROOT):
        """Initialize the base test runner."""
        self.repo_root = repo_root
        self.tests_dir = TESTS_DIR
        self.src_dir = SRC_DIR
        self.results_dir = RESULTS_DIR
        self.coverage_dir = COVERAGE_DIR

        # Ensure environment is prepared
        prepare_environment()

        self.results = {}
        self.start_time = None
        self.end_time = None

    def discover_tests(
        self, test_type: Optional[str] = None, pattern: str = "test_*.py"
    ) -> List[Path]:
        """Discover test files based on type and pattern."""
        if not self.tests_dir.exists():
            print(f"❌ Test directory not found: {self.tests_dir}")
            return []

        test_files = []

        if test_type:
            # Specific test type directory
            type_dir = self.tests_dir / test_type
            if type_dir.exists():
                test_files.extend(type_dir.rglob(pattern))
            else:
                print(f"⚠️ Test type directory not found: {type_dir}")
        else:
            # All test files
            test_files.extend(self.tests_dir.rglob(pattern))
            # Also include root-level test files
            test_files.extend(self.repo_root.glob(pattern))

        return sorted(set(test_files))  # Remove duplicates and sort

    def build_pytest_command(
        self,
        test_paths: List[Path],
        coverage: bool = True,
        parallel: bool = False,
        verbose: bool = True,
        markers: Optional[List[str]] = None,
    ) -> List[str]:
        """Build pytest command with specified options."""
        cmd = ["python", "-m", "pytest"]

        # Add test paths
        for test_path in test_paths:
            cmd.append(str(test_path))

        # Add options
        if verbose:
            cmd.append("-v")

        if coverage:
            cmd.extend(
                [
                    "--cov=src",
                    "--cov-report=html",
                    "--cov-report=term-missing",
                    "--cov-report=json",
                ]
            )

        if parallel:
            cmd.extend(["-n", "auto"])

        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])

        # Standard pytest options
        cmd.extend(
            [
                "--tb=short",
                "--strict-markers",
                "--disable-warnings",
                f"--html={self.results_dir}/report.html",
                "--self-contained-html",
            ]
        )

        return cmd

    def cleanup(self) -> None:
        """Clean up any generated test artifacts."""
        cleanup_artifacts()

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"

        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"📊 Results saved to: {filepath}")
        return filepath

    def print_summary(self, results: Dict[str, Any]):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 70)

        execution = results.get("execution", {})
        print(f"Duration: {execution.get('duration', 0):.2f}s")
        print(f"Command: {execution.get('command', 'Unknown')}")
        print(f"Return Code: {execution.get('returncode', 'Unknown')}")

        print(f"\n📈 Test Results:")
        print(f"  Tests Run: {results.get('tests_run', 0)}")
        print(f"  Passed: {results.get('passed', 0)}")
        print(f"  Failed: {results.get('failed', 0)}")
        print(f"  Skipped: {results.get('skipped', 0)}")
        print(f"  Errors: {results.get('errors', 0)}")

        summary = results.get("summary", "UNKNOWN")
        if summary == "PASSED":
            print(f"\n✅ Overall Status: {summary}")
        elif summary == "FAILED":
            print(f"\n❌ Overall Status: {summary}")
        else:
            print(f"\n⚠️ Overall Status: {summary}")

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Run the test suite.

        Args:
            **kwargs: Implementation-specific parameters.

        Returns:
            Dict[str, Any]: A summary of test results.
        """
        raise NotImplementedError("run must be implemented by subclasses")
