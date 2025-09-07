#!/usr/bin/env python3
"""
Unified Testing System - Agent Cellphone V2

Consolidates all testing frameworks and utilities into a single,
comprehensive testing system that eliminates duplication and provides
unified interfaces for all testing needs.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3G - Testing Infrastructure Cleanup
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import os
import sys
import time
import subprocess
import unittest
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from .executor import TestExecutor
from .testing_utils import BaseTest, TestType, TestStatus
from .test_categories import TestCategories
from .output_formatter import OutputFormatter
from .testing_orchestrator import TestingOrchestrator
from .testing_reporter import TestingReporter


class TestFramework(Enum):
    """Supported test frameworks"""

    PYTEST = "pytest"
    UNITTEST = "unittest"
    CUSTOM = "custom"


@dataclass
class TestExecutionConfig:
    """Configuration for test execution"""

    framework: TestFramework = TestFramework.PYTEST
    verbose: bool = False
    timeout: int = 300
    parallel: bool = True
    max_workers: int = 4
    coverage: bool = True
    html_report: bool = True
    junit_report: bool = False
    benchmark: bool = False


@dataclass
class TestResult:
    """Unified test result structure"""

    test_id: str
    name: str
    status: TestStatus
    framework: TestFramework
    execution_time: float = 0.0
    output: str = ""
    error_output: str = ""
    coverage_percentage: Optional[float] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class UnifiedTestingSystem:
    """
    Unified Testing System - TASK 3G

    Consolidates all testing functionality into a single system,
    eliminating duplication across multiple test runners and utilities.
    """

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.tests_dir = repo_root / "tests"
        self.results_dir = repo_root / "test_results"
        self.coverage_dir = repo_root / "htmlcov"

        # Core components
        self.test_executor = TestExecutor(max_workers=4)
        self.test_categories = TestCategories()
        self.output_formatter = OutputFormatter()
        self.orchestrator = TestingOrchestrator()
        self.reporter = TestingReporter()

        # Configuration
        self.config = TestExecutionConfig()
        self.results: List[TestResult] = []

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [self.tests_dir, self.results_dir, self.coverage_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def check_prerequisites(self) -> bool:
        """Check if all testing prerequisites are met"""
        self.output_formatter.print_prerequisites_check(
            "Checking testing prerequisites..."
        )

        # Check pytest availability
        if not self._check_pytest():
            return False

        # Check test directory structure
        if not self._check_test_structure():
            return False

        # Check coverage tools
        if not self._check_coverage_tools():
            return False

        self.output_formatter.print_success("All prerequisites met!")
        return True

    def _check_pytest(self) -> bool:
        """Check if pytest is available"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                self.output_formatter.print_success(
                    f"pytest available: {result.stdout.strip()}"
                )
                return True
            else:
                self.output_formatter.print_error("pytest not available")
                return False
        except Exception as e:
            self.output_formatter.print_error(f"pytest check failed: {e}")
            return False

    def _check_test_structure(self) -> bool:
        """Check if test directory structure is valid"""
        if not self.tests_dir.exists():
            self.output_formatter.print_error(
                f"Tests directory not found: {self.tests_dir}"
            )
            return False

        conftest_file = self.tests_dir / "conftest.py"
        if not conftest_file.exists():
            self.output_formatter.print_warning(
                f"conftest.py not found: {conftest_file}"
            )

        return True

    def _check_coverage_tools(self) -> bool:
        """Check if coverage tools are available"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "coverage", "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                self.output_formatter.print_success(
                    f"coverage available: {result.stdout.strip()}"
                )
                return True
            else:
                self.output_formatter.print_warning("coverage not available")
                return False
        except Exception:
            self.output_formatter.print_warning("coverage check failed")
            return False

    def run_tests(
        self,
        category: Optional[str] = None,
        config: Optional[TestExecutionConfig] = None,
    ) -> List[TestResult]:
        """Run tests with unified execution"""
        if config:
            self.config = config

        self.output_formatter.print_banner(str(self.repo_root))

        if not self.check_prerequisites():
            return []

        if category:
            return self._run_category_tests(category)
        else:
            return self._run_all_tests()

    def _run_category_tests(self, category: str) -> List[TestResult]:
        """Run tests for a specific category"""
        category_config = self.test_categories.get_category(category)
        if not category_config:
            self.output_formatter.print_error(f"Unknown test category: {category}")
            return []

        self.output_formatter.print_test_category_header(
            category,
            category_config["description"],
            category_config["timeout"],
            category_config["critical"],
        )

        return self._execute_tests(category_config)

    def _run_all_tests(self) -> List[TestResult]:
        """Run all available tests"""
        self.output_formatter.print_info("Running all test categories...")

        all_results = []
        categories = self.test_categories.get_all_categories()

        for category_name in categories:
            category_config = categories[category_name]
            self.output_formatter.print_test_category_header(
                category_name,
                category_config["description"],
                category_config["timeout"],
                category_config["critical"],
            )

            category_results = self._execute_tests(category_config)
            all_results.extend(category_results)

        return all_results

    def _execute_tests(self, category_config: Dict[str, Any]) -> List[TestResult]:
        """Execute tests for a category"""
        start_time = time.time()

        try:
            if self.config.framework == TestFramework.PYTEST:
                results = self._run_pytest_tests(category_config)
            elif self.config.framework == TestFramework.UNITTEST:
                results = self._run_unittest_tests(category_config)
            else:
                results = self._run_custom_tests(category_config)

            # Add execution metadata
            execution_time = time.time() - start_time
            for result in results:
                result.execution_time = execution_time

            self.results.extend(results)
            return results

        except Exception as e:
            self.output_formatter.print_error(f"Test execution failed: {e}")
            return []

    def _run_pytest_tests(self, category_config: Dict[str, Any]) -> List[TestResult]:
        """Run tests using pytest"""
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--tb=short",
            "--durations=10",
            f"--timeout={category_config['timeout']}",
            str(self.tests_dir),
        ] + category_config.get("command", [])

        if self.config.verbose:
            cmd.append("-s")

        if self.config.coverage:
            cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])

        if self.config.junit_report:
            cmd.extend(["--junitxml", str(self.results_dir / "junit.xml")])

        if self.config.parallel and self.config.max_workers > 1:
            cmd.extend(["-n", str(self.config.max_workers)])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=category_config["timeout"],
                cwd=self.repo_root,
            )

            return self._parse_pytest_output(result, category_config)

        except subprocess.TimeoutExpired:
            self.output_formatter.print_error("Test execution timed out")
            return []
        except Exception as e:
            self.output_formatter.print_error(f"Pytest execution failed: {e}")
            return []

    def _run_unittest_tests(self, category_config: Dict[str, Any]) -> List[TestResult]:
        """Run tests using unittest"""
        try:
            # Discover and run tests
            loader = unittest.TestLoader()
            suite = loader.discover(str(self.tests_dir), pattern="test_*.py")

            runner = unittest.TextTestRunner(verbosity=2 if self.config.verbose else 1)
            result = runner.run(suite)

            return self._parse_unittest_output(result, category_config)

        except Exception as e:
            self.output_formatter.print_error(f"Unittest execution failed: {e}")
            return []

    def _run_custom_tests(self, category_config: Dict[str, Any]) -> List[TestResult]:
        """Run custom test implementations"""
        # This would integrate with our custom TestExecutor
        try:
            # Use the testing core for custom test execution
            tests = self._discover_custom_tests(category_config)
            results = self.test_executor.execute_parallel(tests)

            return self._convert_core_results(results, category_config)

        except Exception as e:
            self.output_formatter.print_error(f"Custom test execution failed: {e}")
            return []

    def _discover_custom_tests(self, category_config: Dict[str, Any]) -> List[BaseTest]:
        """Discover custom tests for execution"""
        tests = []
        test_files = list(self.tests_dir.rglob("test_*.py"))

        for test_file in test_files:
            test = BaseTest(
                test_id=str(test_file),
                name=test_file.stem,
                test_type=TestType.UNIT,
                description=f"Custom test from {test_file}",
            )
            tests.append(test)
            self.test_executor.add_test_to_queue(test)

        return tests

    def _convert_core_results(
        self, core_results: List[Any], category_config: Dict[str, Any]
    ) -> List[TestResult]:
        """Convert core test results to unified format"""
        results = []
        for core_result in core_results:
            result = TestResult(
                test_id=core_result.test_id,
                name=core_result.test_id,
                status=core_result.status,
                framework=TestFramework.CUSTOM,
                execution_time=core_result.execution_time,
            )
            results.append(result)

        return results

    def _parse_pytest_output(
        self, result: subprocess.CompletedProcess, category_config: Dict[str, Any]
    ) -> List[TestResult]:
        """Parse pytest output into unified results"""
        # Simplified parsing - in production this would be more comprehensive
        lines = result.stdout.split("\n")
        results = []

        for line in lines:
            if line.startswith("test_") and (
                "PASSED" in line or "FAILED" in line or "ERROR" in line
            ):
                test_name = line.split()[0]
                status = TestStatus.PASSED if "PASSED" in line else TestStatus.FAILED

                test_result = TestResult(
                    test_id=test_name,
                    name=test_name,
                    status=status,
                    framework=TestFramework.PYTEST,
                    output=result.stdout,
                    error_output=result.stderr,
                )
                results.append(test_result)

        return results

    def _parse_unittest_output(
        self, result: unittest.TestResult, category_config: Dict[str, Any]
    ) -> List[TestResult]:
        """Parse unittest output into unified results"""
        results = []

        # Add successful tests
        for test in result.testsRun:
            test_result = TestResult(
                test_id=str(test),
                name=str(test),
                status=TestStatus.PASSED,
                framework=TestFramework.UNITTEST,
            )
            results.append(test_result)

        # Add failed tests
        for test, traceback in result.failures:
            test_result = TestResult(
                test_id=str(test),
                name=str(test),
                status=TestStatus.FAILED,
                framework=TestFramework.UNITTEST,
                error_output=traceback,
            )
            results.append(test_result)

        # Add error tests
        for test, traceback in result.errors:
            test_result = TestResult(
                test_id=str(test),
                name=str(test),
                status=TestStatus.ERROR,
                framework=TestFramework.UNITTEST,
                error_output=traceback,
            )
            results.append(test_result)

        return results

    def generate_report(self, output_format: str = "console") -> str:
        """Generate comprehensive test report"""
        if output_format == "console":
            return self._generate_console_report()
        elif output_format == "html":
            return self._generate_html_report()
        elif output_format == "json":
            return self._generate_json_report()
        else:
            return self._generate_console_report()

    def _generate_console_report(self) -> str:
        """Generate console-formatted report"""
        if not self.results:
            return "No test results available"

        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        errors = sum(1 for r in self.results if r.status == TestStatus.ERROR)

        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0

        report = f"""
🚀 UNIFIED TESTING SYSTEM REPORT
{'=' * 50}
Total Tests: {total_tests}
✅ Passed: {passed}
❌ Failed: {failed}
💥 Errors: {errors}
📈 Success Rate: {success_rate:.1f}%
"""
        return report

    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        # This would generate a comprehensive HTML report
        return "HTML report generation not implemented yet"

    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        import json

        report_data = {
            "summary": {
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r.status == TestStatus.PASSED),
                "failed": sum(1 for r in self.results if r.status == TestStatus.FAILED),
                "errors": sum(1 for r in self.results if r.status == TestStatus.ERROR),
            },
            "results": [
                {
                    "test_id": r.test_id,
                    "name": r.name,
                    "status": r.status.value,
                    "framework": r.framework.value,
                    "execution_time": r.execution_time,
                }
                for r in self.results
            ],
        }

        return json.dumps(report_data, indent=2)

    def cleanup(self) -> None:
        """Clean up testing resources"""
        try:
            # Clear results
            self.results.clear()

            # Clear test executor
            self.test_executor.test_runner.clear_results()

            self.output_formatter.print_success(
                "Testing system cleaned up successfully"
            )

        except Exception as e:
            self.output_formatter.print_error(f"Cleanup failed: {e}")


def main():
    """Main entry point for unified testing system"""
    repo_root = Path(__file__).parent.parent.parent.parent

    # Initialize unified testing system
    testing_system = UnifiedTestingSystem(repo_root)

    try:
        # Run all tests
        results = testing_system.run_tests()

        # Generate and display report
        report = testing_system.generate_report("console")
        print(report)

        # Cleanup
        testing_system.cleanup()

    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"❌ Testing system error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
