#!/usr/bin/env python3
"""
Unified Test Runner System - Agent Cellphone V2
===============================================

Consolidated test runner system that eliminates duplication across
multiple test runner implementations. Provides unified test execution,
configuration, and reporting for all test types.

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
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

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


# ============================================================================
# UNIFIED TEST RUNNER ENUMS AND DATA CLASSES
# ============================================================================

class TestMode(Enum):
    """Test execution mode enumeration."""
    ALL = "all"
    CRITICAL = "critical"
    SMOKE = "smoke"
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    API = "api"
    BEHAVIOR = "behavior"
    DECISION = "decision"
    CUSTOM = "custom"


class TestStatus(Enum):
    """Test execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


class TestPriority(Enum):
    """Test priority enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TestCategory:
    """Test category configuration."""
    name: str
    description: str
    marker: str
    timeout: int
    priority: TestPriority
    directory: str
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    parallel: bool = False
    retry_count: int = 0


@dataclass
class TestResult:
    """Test execution result."""
    test_name: str
    category: str
    status: TestStatus
    duration: float
    output: str
    error_message: Optional[str] = None
    timestamp: str = ""
    retry_count: int = 0


@dataclass
class TestExecutionConfig:
    """Test execution configuration."""
    mode: TestMode = TestMode.ALL
    parallel: bool = True
    max_workers: int = 4
    timeout: int = 300
    verbose: bool = False
    coverage: bool = True
    report_format: str = "text"
    output_file: Optional[str] = None
    fail_fast: bool = False
    retry_failed: bool = True
    max_retries: int = 2


# ============================================================================
# UNIFIED TEST RUNNER SYSTEM
# ============================================================================

class UnifiedTestRunner:
    """Unified test runner consolidating all previous test runners."""
    
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
                parallel=True
            ),
            "behavior": TestCategory(
                name="behavior",
                description="Behavior tree tests",
                marker="behavior",
                timeout=120,
                priority=TestPriority.MEDIUM,
                directory="behavior_trees",
                enabled=True,
                parallel=False
            ),
            "decision": TestCategory(
                name="decision",
                description="Decision engine tests",
                marker="decision",
                timeout=120,
                priority=TestPriority.MEDIUM,
                directory="decision_engines",
                enabled=True,
                parallel=False
            )
        }
    
    def configure_execution(self, config: TestExecutionConfig):
        """Configure test execution parameters."""
        self.execution_config = config
        self.logger.info(f"Test execution configured: {config.mode.value}")
    
    def discover_tests(self, category: Optional[str] = None) -> List[str]:
        """Discover test files in the specified category or all categories."""
        test_files = []
        
        if category:
            categories = [category] if category in self.test_categories else []
        else:
            categories = self.test_categories.keys()
        
        for cat_name in categories:
            cat_config = self.test_categories[cat_name]
            if not cat_config.enabled:
                continue
                
            cat_dir = self.repo_root / "tests" / cat_config.directory
            if cat_dir.exists():
                for test_file in cat_dir.glob("test_*.py"):
                    if test_file.is_file():
                        test_files.append(str(test_file))
        
        # Also check root level test files
        root_tests_dir = self.repo_root / "tests"
        for test_file in root_tests_dir.glob("test_*.py"):
            if test_file.is_file():
                test_files.append(str(test_file))
        
        self.logger.info(f"Discovered {len(test_files)} test files")
        return test_files
    
    def run_tests(self, test_files: List[str]) -> List[TestResult]:
        """Run the specified test files."""
        self.logger.info(f"Starting test execution for {len(test_files)} files")
        self.start_time = time.time()
        
        results = []
        
        if self.execution_config.parallel and len(test_files) > 1:
            results = self._run_tests_parallel(test_files)
        else:
            results = self._run_tests_sequential(test_files)
        
        self.results.extend(results)
        return results
    
    def _run_tests_sequential(self, test_files: List[str]) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        
        for test_file in test_files:
            try:
                result = self._execute_single_test(test_file)
                results.append(result)
                
                if self.execution_config.fail_fast and result.status == TestStatus.FAILED:
                    self.logger.warning("Fail-fast enabled, stopping execution")
                    break
                    
            except Exception as e:
                error_result = TestResult(
                    test_name=test_file,
                    category="unknown",
                    status=TestStatus.ERROR,
                    duration=0.0,
                    output="",
                    error_message=str(e),
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
                results.append(error_result)
        
        return results
    
    def _run_tests_parallel(self, test_files: List[str]) -> List[TestResult]:
        """Run tests in parallel using subprocess."""
        results = []
        
        # For now, implement basic parallel execution
        # In a full implementation, this would use multiprocessing or asyncio
        self.logger.info("Parallel execution not yet implemented, falling back to sequential")
        return self._run_tests_sequential(test_files)
    
    def _execute_single_test(self, test_file: str) -> TestResult:
        """Execute a single test file."""
        start_time = time.time()
        test_name = Path(test_file).name
        
        self.logger.info(f"Executing test: {test_name}")
        
        try:
            # Use pytest to run the test file
            cmd = [
                sys.executable, "-m", "pytest", test_file,
                "-v", "--tb=short"
            ]
            
            if self.execution_config.coverage:
                cmd.extend(["--cov", "--cov-report=term-missing"])
            
            # Execute the test
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.execution_config.timeout,
                cwd=self.repo_root
            )
            
            duration = time.time() - start_time
            
            # Determine test status
            if process.returncode == 0:
                status = TestStatus.PASSED
            else:
                status = TestStatus.FAILED
            
            result = TestResult(
                test_name=test_name,
                category=self._get_test_category(test_file),
                status=status,
                duration=duration,
                output=process.stdout,
                error_message=process.stderr if process.stderr else None,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
            self._log_test_result(result)
            return result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return TestResult(
                test_name=test_name,
                category=self._get_test_category(test_file),
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
                category=self._get_test_category(test_file),
                status=TestStatus.ERROR,
                duration=duration,
                output="",
                error_message=str(e),
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def _get_test_category(self, test_file: str) -> str:
        """Determine the test category based on file path."""
        test_path = Path(test_file)
        
        # Check if it's in a category directory
        for category, config in self.test_categories.items():
            if config.directory in str(test_path):
                return category
        
        # Check file name patterns
        if "smoke" in test_path.name.lower():
            return "smoke"
        elif "unit" in test_path.name.lower():
            return "unit"
        elif "integration" in test_path.name.lower():
            return "integration"
        elif "performance" in test_path.name.lower():
            return "performance"
        elif "security" in test_path.name.lower():
            return "security"
        elif "api" in test_path.name.lower():
            return "api"
        else:
            return "unknown"
    
    def _log_test_result(self, result: TestResult):
        """Log test execution result with color coding."""
        if not COLOR_AVAILABLE:
            self.logger.info(f"{result.test_name}: {result.status.value}")
            return
        
        status_colors = {
            TestStatus.PASSED: Fore.GREEN,
            TestStatus.FAILED: Fore.RED,
            TestStatus.SKIPPED: Fore.YELLOW,
            TestStatus.ERROR: Fore.RED,
            TestStatus.TIMEOUT: Fore.YELLOW
        }
        
        color = status_colors.get(result.status, Fore.WHITE)
        self.logger.info(f"{color}{result.test_name}: {result.status.value}{Style.RESET_ALL}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test execution report."""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in self.results if r.status == TestStatus.FAILED])
        error_tests = len([r for r in self.results if r.status == TestStatus.ERROR])
        skipped_tests = len([r for r in self.results if r.status == TestStatus.SKIPPED])
        
        total_duration = time.time() - self.start_time
        
        # Group results by category
        category_results = {}
        for result in self.results:
            if result.category not in category_results:
                category_results[result.category] = []
            category_results[result.category].append(result)
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "skipped": skipped_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "category_results": category_results,
            "detailed_results": [
                {
                    "test_name": r.test_name,
                    "category": r.category,
                    "status": r.status.value,
                    "duration": r.duration,
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }
        
        return report
    
    def print_summary(self):
        """Print test execution summary to console."""
        if not self.results:
            print("No test results available.")
            return
        
        report = self.generate_report()
        summary = report["summary"]
        
        print("\n" + "="*60)
        print("TEST EXECUTION SUMMARY")
        print("="*60)
        
        if COLOR_AVAILABLE:
            print(f"Total Tests: {Fore.CYAN}{summary['total_tests']}{Style.RESET_ALL}")
            print(f"Passed: {Fore.GREEN}{summary['passed']}{Style.RESET_ALL}")
            print(f"Failed: {Fore.RED}{summary['failed']}{Style.RESET_ALL}")
            print(f"Errors: {Fore.RED}{summary['errors']}{Style.RESET_ALL}")
            print(f"Skipped: {Fore.YELLOW}{summary['skipped']}{Style.RESET_ALL}")
            print(f"Success Rate: {Fore.CYAN}{summary['success_rate']:.1f}%{Style.RESET_ALL}")
            print(f"Total Duration: {Fore.CYAN}{summary['total_duration']:.2f}s{Style.RESET_ALL}")
        else:
            print(f"Total Tests: {summary['total_tests']}")
            print(f"Passed: {summary['passed']}")
            print(f"Failed: {summary['failed']}")
            print(f"Errors: {summary['errors']}")
            print(f"Skipped: {summary['skipped']}")
            print(f"Success Rate: {summary['success_rate']:.1f}%")
            print(f"Total Duration: {summary['total_duration']:.2f}s")
        
        print("="*60)


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point for the unified test runner."""
    parser = argparse.ArgumentParser(
        description="Unified Test Runner - Agent Cellphone V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unified_test_runner.py                    # Run all tests
  python unified_test_runner.py --mode critical   # Run critical tests only
  python unified_test_runner.py --mode smoke      # Run smoke tests
  python unified_test_runner.py --mode unit       # Run unit tests
  python unified_test_runner.py --files test_file.py  # Run specific files
        """
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=[mode.value for mode in TestMode],
        default=TestMode.ALL.value,
        help="Test execution mode"
    )
    
    parser.add_argument(
        "--files", "-f",
        nargs="+",
        help="Specific test files to run"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Enable parallel test execution"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Test execution timeout in seconds"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop execution on first failure"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for test results"
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    repo_root = Path(__file__).parent.parent
    runner = UnifiedTestRunner(repo_root)
    
    # Configure execution
    config = TestExecutionConfig(
        mode=TestMode(args.mode),
        parallel=args.parallel,
        timeout=args.timeout,
        verbose=args.verbose,
        coverage=not args.no_coverage,
        fail_fast=args.fail_fast,
        output_file=args.output
    )
    runner.configure_execution(config)
    
    # Discover and run tests
    if args.files:
        test_files = args.files
    else:
        test_files = runner.discover_tests()
    
    # Run tests
    runner.run_tests(test_files)
    
    # Generate and display results
    runner.print_summary()
    
    # Save results if output file specified
    if args.output:
        report = runner.generate_report()
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nDetailed report saved to: {args.output}")
    
    # Exit with appropriate code
    summary = runner.generate_report()["summary"]
    if summary["failed"] > 0 or summary["errors"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
