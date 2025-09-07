#!/usr/bin/env python3
"""
Unified Test Runner System V2 - Agent Cellphone V2
==================================================

V2-compliant test runner system (under 500 lines).
Uses modular components from tests/core/ to achieve compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import argparse
import sys
import os
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Color support
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = RESET = ""
    class Style:
        RESET_ALL = ""
    COLOR_AVAILABLE = False

# Import modular components
from .core import (
    TestMode, TestStatus, TestPriority, TestEnvironment,
    TestCategory, TestResult, TestExecutionConfig, TestSuite, TestReport
)


class UnifiedTestRunnerV2:
    """V2-compliant unified test runner (under 500 lines)."""
    
    def __init__(self, repo_root: Path):
        """Initialize the unified test runner."""
        self.repo_root = repo_root
        self.test_categories = self._initialize_test_categories()
        self.execution_config = TestExecutionConfig()
        self.results: List[TestResult] = []
        self.start_time = time.time()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_test_categories(self) -> Dict[str, TestCategory]:
        """Initialize test categories with configuration."""
        return {
            "smoke": TestCategory(
                name="smoke",
                description="Smoke tests for basic functionality validation",
                marker="smoke",
                timeout=60,
                priority=TestPriority.CRITICAL,
                directory="smoke",
                enabled=True,
                parallel=False
            ),
            "unit": TestCategory(
                name="unit",
                description="Unit tests for individual components",
                marker="unit",
                timeout=120,
                priority=TestPriority.CRITICAL,
                directory="unit",
                enabled=True,
                parallel=True
            ),
            "integration": TestCategory(
                name="integration",
                description="Integration tests for component interaction",
                marker="integration",
                timeout=300,
                priority=TestPriority.HIGH,
                directory="integration",
                enabled=True,
                parallel=False
            ),
            "performance": TestCategory(
                name="performance",
                description="Performance and load testing",
                marker="performance",
                timeout=600,
                priority=TestPriority.MEDIUM,
                directory="performance",
                enabled=True,
                parallel=False
            ),
            "security": TestCategory(
                name="security",
                description="Security and vulnerability testing",
                marker="security",
                timeout=180,
                priority=TestPriority.CRITICAL,
                directory="security",
                enabled=True,
                parallel=False
            ),
            "api": TestCategory(
                name="api",
                description="API endpoint testing",
                marker="api",
                timeout=240,
                priority=TestPriority.HIGH,
                directory="api",
                enabled=True,
                parallel=False
            )
        }
    
    def discover_tests(self, category: str = None) -> List[str]:
        """Discover test files in the repository."""
        test_files = []
        test_dir = self.repo_root / "tests"
        
        if not test_dir.exists():
            self.logger.warning(f"Test directory not found: {test_dir}")
            return test_files
        
        # Discover test files
        for test_file in test_dir.rglob("test_*.py"):
            if category and category not in test_file.name:
                continue
            test_files.append(str(test_file))
        
        return test_files
    
    def run_test(self, test_file: str, category: str) -> TestResult:
        """Run a single test file."""
        start_time = time.time()
        test_name = Path(test_file).stem
        
        try:
            # Run test using pytest
            cmd = [
                sys.executable, "-m", "pytest", test_file,
                "-v", "--tb=short", "--no-header"
            ]
            
            if self.execution_config.verbose:
                cmd.append("-s")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.test_categories[category].timeout,
                cwd=self.repo_root
            )
            
            duration = time.time() - start_time
            
            # Determine test status
            if result.returncode == 0:
                status = TestStatus.PASSED
                error_message = None
            else:
                status = TestStatus.FAILED
                error_message = result.stderr
            
            return TestResult(
                test_name=test_name,
                category=category,
                status=status,
                duration=duration,
                output=result.stdout,
                error_message=error_message,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return TestResult(
                test_name=test_name,
                category=category,
                status=TestStatus.TIMEOUT,
                duration=duration,
                output="",
                error_message="Test execution timed out",
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name=test_name,
                category=category,
                status=TestStatus.ERROR,
                duration=duration,
                output="",
                error_message=str(e),
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def run_tests_sequential(self, test_files: List[str], category: str) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        for test_file in test_files:
            result = self.run_test(test_file, category)
            results.append(result)
            
            if self.execution_config.fail_fast and result.status == TestStatus.FAILED:
                break
        
        return results
    
    def run_tests_parallel(self, test_files: List[str], category: str) -> List[TestResult]:
        """Run tests in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.execution_config.max_workers) as executor:
            future_to_test = {
                executor.submit(self.run_test, test_file, category): test_file
                for test_file in test_files
            }
            
            for future in as_completed(future_to_test):
                result = future.result()
                results.append(result)
                
                if self.execution_config.fail_fast and result.status == TestStatus.FAILED:
                    break
        
        return results
    
    def run_category(self, category: str) -> List[TestResult]:
        """Run all tests in a specific category."""
        if category not in self.test_categories:
            self.logger.error(f"Unknown test category: {category}")
            return []
        
        category_config = self.test_categories[category]
        if not category_config.enabled:
            self.logger.info(f"Test category {category} is disabled")
            return []
        
        self.logger.info(f"Running {category} tests...")
        test_files = self.discover_tests(category)
        
        if not test_files:
            self.logger.warning(f"No test files found for category: {category}")
            return []
        
        if category_config.parallel:
            return self.run_tests_parallel(test_files, category)
        else:
            return self.run_tests_sequential(test_files, category)
    
    def run_all_tests(self) -> TestReport:
        """Run all tests based on execution mode."""
        self.logger.info("Starting unified test execution...")
        
        if self.execution_config.mode == TestMode.ALL:
            categories = list(self.test_categories.keys())
        elif self.execution_config.mode == TestMode.CRITICAL:
            categories = [
                cat for cat, config in self.test_categories.items()
                if config.priority == TestPriority.CRITICAL
            ]
        else:
            categories = [self.execution_config.mode.value]
        
        all_results = []
        for category in categories:
            results = self.run_category(category)
            all_results.extend(results)
        
        # Generate report
        total_tests = len(all_results)
        passed = len([r for r in all_results if r.status == TestStatus.PASSED])
        failed = len([r for r in all_results if r.status == TestStatus.FAILED])
        skipped = len([r for r in all_results if r.status == TestStatus.SKIPPED])
        errors = len([r for r in all_results if r.status == TestStatus.ERROR])
        
        duration = time.time() - self.start_time
        
        report = TestReport(
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            results=all_results,
            summary={
                "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0,
                "categories_run": len(categories),
                "execution_mode": self.execution_config.mode.value
            }
        )
        
        self._print_report(report)
        return report
    
    def _print_report(self, report: TestReport):
        """Print test execution report."""
        print(f"\n{Fore.CYAN}=== UNIFIED TEST EXECUTION REPORT ==={Style.RESET_ALL}")
        print(f"Total Tests: {report.total_tests}")
        print(f"Passed: {Fore.GREEN}{report.passed}{Style.RESET_ALL}")
        print(f"Failed: {Fore.RED}{report.failed}{Style.RESET_ALL}")
        print(f"Skipped: {Fore.YELLOW}{report.skipped}{Style.RESET_ALL}")
        print(f"Errors: {Fore.RED}{report.errors}{Style.RESET_ALL}")
        print(f"Duration: {report.duration:.2f} seconds")
        print(f"Success Rate: {report.summary['success_rate']:.1f}%")
        
        if report.failed > 0 or report.errors > 0:
            print(f"\n{Fore.RED}=== FAILED TESTS ==={Style.RESET_ALL}")
            for result in report.results:
                if result.status in [TestStatus.FAILED, TestStatus.ERROR]:
                    print(f"- {result.test_name}: {result.error_message}")


def main():
    """Main entry point for the unified test runner."""
    parser = argparse.ArgumentParser(description="Unified Test Runner V2")
    parser.add_argument("--mode", default="all", choices=[m.value for m in TestMode])
    parser.add_argument("--category", help="Specific test category to run")
    parser.add_argument("--parallel", action="store_true", default=True)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Initialize runner
    repo_root = Path.cwd()
    runner = UnifiedTestRunnerV2(repo_root)
    
    # Configure execution
    runner.execution_config.mode = TestMode(args.mode)
    runner.execution_config.parallel = args.parallel
    runner.execution_config.max_workers = args.max_workers
    runner.execution_config.timeout = args.timeout
    runner.execution_config.verbose = args.verbose
    runner.execution_config.fail_fast = args.fail_fast
    runner.execution_config.output_file = args.output
    
    # Run tests
    report = runner.run_all_tests()
    
    # Exit with appropriate code
    if report.failed > 0 or report.errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
