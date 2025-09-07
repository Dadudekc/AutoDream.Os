"""
Regression Testing Automation for Modularized Components

This module provides automated regression testing capabilities to ensure
that modularization changes don't break existing functionality.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.utils.logger import get_logger

logger = get_logger(__name__)


class TestStatus(Enum):
    """Status of a test execution."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"


class TestPriority(Enum):
    """Priority levels for test execution."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_name: str
    test_file: str
    test_path: str
    status: TestStatus
    execution_time: float
    output: str
    error_message: Optional[str]
    priority: TestPriority
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class TestSuiteResult:
    """Result of a test suite execution."""
    suite_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    timeout_tests: int
    execution_time: float
    success_rate: float
    timestamp: str
    test_results: List[TestResult]


@dataclass
class RegressionTestReport:
    """Comprehensive regression test report."""
    execution_timestamp: str
    total_suites: int
    total_tests: int
    overall_success_rate: float
    total_execution_time: float
    suite_results: List[TestSuiteResult]
    critical_failures: List[TestResult]
    performance_metrics: Dict[str, Any]
    recommendations: List[str]


class TestDiscoveryEngine:
    """Discovers test files and test cases."""
    
    def __init__(self, test_directories: List[Path]):
        self.test_directories = [Path(d) for d in test_directories]
        self.discovered_tests: Dict[str, List[str]] = {}
        
    def discover_tests(self) -> Dict[str, List[str]]:
        """Discover all test files and test cases."""
        logger.info("Starting test discovery...")
        
        for test_dir in self.test_directories:
            if not test_dir.exists():
                logger.warning(f"Test directory does not exist: {test_dir}")
                continue
                
            self._discover_tests_in_directory(test_dir)
        
        logger.info(f"Test discovery completed. Found {sum(len(tests) for tests in self.discovered_tests.values())} test cases across {len(self.discovered_tests)} files.")
        return self.discovered_tests
    
    def _discover_tests_in_directory(self, test_dir: Path):
        """Discover tests in a specific directory."""
        for test_file in test_dir.rglob("test_*.py"):
            try:
                test_cases = self._extract_test_cases(test_file)
                if test_cases:
                    self.discovered_tests[str(test_file)] = test_cases
                    logger.debug(f"Discovered {len(test_cases)} test cases in {test_file}")
            except Exception as e:
                logger.error(f"Error discovering tests in {test_file}: {e}")
    
    def _extract_test_cases(self, test_file: Path) -> List[str]:
        """Extract test case names from a test file."""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_cases = []
            
            # Look for test functions
            import re
            test_function_pattern = r'def\s+(test_\w+)\s*\('
            test_functions = re.findall(test_function_pattern, content)
            test_cases.extend(test_functions)
            
            # Look for test methods in test classes
            test_method_pattern = r'def\s+(test_\w+)\s*\(self'
            test_methods = re.findall(test_method_pattern, content)
            test_cases.extend(test_methods)
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error extracting test cases from {test_file}: {e}")
            return []
    
    def get_test_priorities(self) -> Dict[str, TestPriority]:
        """Assign priorities to test cases based on various factors."""
        priorities = {}
        
        for test_file, test_cases in self.discovered_tests.items():
            for test_case in test_cases:
                priority = self._determine_test_priority(test_file, test_case)
                priorities[f"{test_file}::{test_case}"] = priority
        
        return priorities
    
    def _determine_test_priority(self, test_file: str, test_case: str) -> TestPriority:
        """Determine the priority of a test case."""
        # Critical tests: core functionality, integration tests
        if any(keyword in test_file.lower() for keyword in ['core', 'integration', 'api', 'database']):
            return TestPriority.CRITICAL
        
        # High priority: agent workspace tests, workflow tests
        if any(keyword in test_file.lower() for keyword in ['agent', 'workflow', 'mission', 'contract']):
            return TestPriority.HIGH
        
        # Medium priority: utility tests, helper tests
        if any(keyword in test_file.lower() for keyword in ['util', 'helper', 'support']):
            return TestPriority.MEDIUM
        
        # Low priority: everything else
        return TestPriority.LOW


class TestExecutionEngine:
    """Executes test cases and manages test execution."""
    
    def __init__(self, max_workers: int = 4, timeout: int = 300):
        self.max_workers = max_workers
        self.timeout = timeout
        self.execution_history: List[TestResult] = []
        
    def execute_test_suite(self, test_file: Path, test_cases: List[str], priorities: Dict[str, TestPriority]) -> TestSuiteResult:
        """Execute a test suite and return results."""
        logger.info(f"Executing test suite: {test_file}")
        start_time = time.time()
        
        suite_name = test_file.stem
        test_results = []
        
        # Execute tests with priority ordering
        prioritized_tests = self._prioritize_tests(test_file, test_cases, priorities)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit test execution tasks
            future_to_test = {
                executor.submit(self._execute_single_test, test_file, test_case, priorities): test_case
                for test_case in prioritized_tests
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_test):
                test_case = future_to_test[future]
                try:
                    result = future.result(timeout=self.timeout)
                    test_results.append(result)
                    self.execution_history.append(result)
                except Exception as e:
                    logger.error(f"Error executing test {test_case}: {e}")
                    error_result = TestResult(
                        test_name=test_case,
                        test_file=str(test_file),
                        test_path=f"{test_file}::{test_case}",
                        status=TestStatus.ERROR,
                        execution_time=0.0,
                        output="",
                        error_message=str(e),
                        priority=priorities.get(f"{test_file}::{test_case}", TestPriority.MEDIUM),
                        timestamp=datetime.now().isoformat(),
                        metadata={}
                    )
                    test_results.append(error_result)
        
        execution_time = time.time() - start_time
        
        # Calculate statistics
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in test_results if r.status == TestStatus.FAILED])
        skipped_tests = len([r for r in test_results if r.status == TestStatus.SKIPPED])
        error_tests = len([r for r in test_results if r.status == TestStatus.ERROR])
        timeout_tests = len([r for r in test_results if r.status == TestStatus.TIMEOUT])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return TestSuiteResult(
            suite_name=suite_name,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            error_tests=error_tests,
            timeout_tests=timeout_tests,
            execution_time=execution_time,
            success_rate=success_rate,
            timestamp=datetime.now().isoformat(),
            test_results=test_results
        )
    
    def _prioritize_tests(self, test_file: Path, test_cases: List[str], priorities: Dict[str, TestPriority]) -> List[str]:
        """Prioritize test cases for execution order."""
        priority_order = [TestPriority.CRITICAL, TestPriority.HIGH, TestPriority.MEDIUM, TestPriority.LOW]
        
        prioritized = []
        for priority in priority_order:
            priority_tests = [
                test_case for test_case in test_cases
                if priorities.get(f"{test_file}::{test_case}") == priority
            ]
            prioritized.extend(priority_tests)
        
        return prioritized
    
    def _execute_single_test(self, test_file: Path, test_case: str, priorities: Dict[str, TestPriority]) -> TestResult:
        """Execute a single test case."""
        start_time = time.time()
        test_path = f"{test_file}::{test_case}"
        priority = priorities.get(test_path, TestPriority.MEDIUM)
        
        try:
            # Execute test using pytest
            cmd = [
                sys.executable, "-m", "pytest",
                str(test_file),
                "-k", test_case,
                "--tb=short",
                "--quiet",
                "--no-header",
                "--no-summary"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            
            stdout, stderr = process.communicate(timeout=self.timeout)
            execution_time = time.time() - start_time
            
            # Determine test status
            if process.returncode == 0:
                status = TestStatus.PASSED
                error_message = None
            elif process.returncode == 1:
                status = TestStatus.FAILED
                error_message = stderr if stderr else "Test failed"
            elif process.returncode == 2:
                status = TestStatus.SKIPPED
                error_message = None
            else:
                status = TestStatus.ERROR
                error_message = stderr if stderr else f"Unknown error (exit code: {process.returncode})"
            
            return TestResult(
                test_name=test_case,
                test_file=str(test_file),
                test_path=test_path,
                status=status,
                execution_time=execution_time,
                output=stdout,
                error_message=error_message,
                priority=priority,
                timestamp=datetime.now().isoformat(),
                metadata={
                    "exit_code": process.returncode,
                    "command": " ".join(cmd)
                }
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return TestResult(
                test_name=test_case,
                test_file=str(test_file),
                test_path=test_path,
                status=TestStatus.TIMEOUT,
                execution_time=execution_time,
                output="",
                error_message=f"Test execution timed out after {self.timeout} seconds",
                priority=priority,
                timestamp=datetime.now().isoformat(),
                metadata={"timeout": self.timeout}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_name=test_case,
                test_file=str(test_file),
                test_path=test_path,
                status=TestStatus.ERROR,
                execution_time=execution_time,
                output="",
                error_message=str(e),
                priority=priority,
                timestamp=datetime.now().isoformat(),
                metadata={"error_type": type(e).__name__}
            )


class RegressionTestManager:
    """Manages regression testing workflow."""
    
    def __init__(self, test_directories: List[Path], max_workers: int = 4, timeout: int = 300):
        self.discovery_engine = TestDiscoveryEngine(test_directories)
        self.execution_engine = TestExecutionEngine(max_workers, timeout)
        self.test_results: Dict[str, TestSuiteResult] = {}
        
    def run_regression_tests(self) -> RegressionTestReport:
        """Run comprehensive regression testing."""
        logger.info("Starting regression testing...")
        start_time = time.time()
        
        # Discover tests
        discovered_tests = self.discovery_engine.discover_tests()
        priorities = self.discovery_engine.get_test_priorities()
        
        # Execute test suites
        suite_results = []
        for test_file, test_cases in discovered_tests.items():
            try:
                suite_result = self.execution_engine.execute_test_suite(
                    Path(test_file), test_cases, priorities
                )
                suite_results.append(suite_result)
                self.test_results[test_file] = suite_result
                
            except Exception as e:
                logger.error(f"Error executing test suite {test_file}: {e}")
                # Create error suite result
                error_suite = TestSuiteResult(
                    suite_name=Path(test_file).stem,
                    total_tests=len(test_cases),
                    passed_tests=0,
                    failed_tests=0,
                    skipped_tests=0,
                    error_tests=len(test_cases),
                    timeout_tests=0,
                    execution_time=0.0,
                    success_rate=0.0,
                    timestamp=datetime.now().isoformat(),
                    test_results=[]
                )
                suite_results.append(error_suite)
        
        total_execution_time = time.time() - start_time
        
        # Generate comprehensive report
        report = self._generate_regression_report(suite_results, total_execution_time)
        
        logger.info("Regression testing completed.")
        return report
    
    def _generate_regression_report(self, suite_results: List[TestSuiteResult], total_execution_time: float) -> RegressionTestReport:
        """Generate a comprehensive regression test report."""
        total_suites = len(suite_results)
        total_tests = sum(suite.total_tests for suite in suite_results)
        total_passed = sum(suite.passed_tests for suite in suite_results)
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Collect critical failures
        critical_failures = []
        for suite in suite_results:
            for test_result in suite.test_results:
                if (test_result.status in [TestStatus.FAILED, TestStatus.ERROR] and 
                    test_result.priority == TestPriority.CRITICAL):
                    critical_failures.append(test_result)
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(suite_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(suite_results, critical_failures)
        
        return RegressionTestReport(
            execution_timestamp=datetime.now().isoformat(),
            total_suites=total_suites,
            total_tests=total_tests,
            overall_success_rate=overall_success_rate,
            total_execution_time=total_execution_time,
            suite_results=suite_results,
            critical_failures=critical_failures,
            performance_metrics=performance_metrics,
            recommendations=recommendations
        )
    
    def _calculate_performance_metrics(self, suite_results: List[TestSuiteResult]) -> Dict[str, Any]:
        """Calculate performance metrics from test results."""
        if not suite_results:
            return {}
        
        execution_times = [suite.execution_time for suite in suite_results]
        test_execution_times = []
        
        for suite in suite_results:
            for test_result in suite.test_results:
                test_execution_times.append(test_result.execution_time)
        
        return {
            "average_suite_execution_time": sum(execution_times) / len(execution_times),
            "fastest_suite_execution": min(execution_times),
            "slowest_suite_execution": max(execution_times),
            "average_test_execution_time": sum(test_execution_times) / len(test_execution_times) if test_execution_times else 0,
            "fastest_test_execution": min(test_execution_times) if test_execution_times else 0,
            "slowest_test_execution": max(test_execution_times) if test_execution_times else 0,
            "total_parallel_execution_time": max(execution_times) if execution_times else 0
        }
    
    def _generate_recommendations(self, suite_results: List[TestSuiteResult], critical_failures: List[TestResult]) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Check for critical failures
        if critical_failures:
            recommendations.append("🚨 CRITICAL: Address critical test failures immediately")
            recommendations.append("Review failed critical tests and fix underlying issues")
        
        # Check success rates
        low_success_suites = [suite for suite in suite_results if suite.success_rate < 80]
        if low_success_suites:
            recommendations.append("⚠️ WARNING: Some test suites have low success rates")
            for suite in low_success_suites:
                recommendations.append(f"  - {suite.suite_name}: {suite.success_rate:.1f}% success rate")
        
        # Check for timeouts
        timeout_tests = sum(suite.timeout_tests for suite in suite_results)
        if timeout_tests > 0:
            recommendations.append(f"⏱️ TIMEOUT: {timeout_tests} tests timed out - consider increasing timeout or optimizing slow tests")
        
        # Check for errors
        error_tests = sum(suite.error_tests for suite in suite_results)
        if error_tests > 0:
            recommendations.append(f"❌ ERRORS: {error_tests} tests encountered errors - check test environment and dependencies")
        
        # Performance recommendations
        slow_suites = [suite for suite in suite_results if suite.execution_time > 60]  # > 1 minute
        if slow_suites:
            recommendations.append("🐌 PERFORMANCE: Some test suites are slow - consider parallelization or test optimization")
        
        # General recommendations
        if not recommendations:
            recommendations.append("✅ All tests are performing well - maintain current testing practices")
        
        return recommendations
    
    def save_report(self, report: RegressionTestReport, output_path: Path):
        """Save regression test report to files."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save detailed JSON report
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self._serialize_report(report), f, indent=2, default=str)
        
        # Save human-readable markdown report
        md_path = output_path.with_suffix('.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_markdown_report(report))
        
        logger.info(f"Regression test report saved to {json_path} and {md_path}")
    
    def _serialize_report(self, report: RegressionTestReport) -> Dict[str, Any]:
        """Convert report to serializable format."""
        serialized = asdict(report)
        
        # Convert enums to strings
        for suite_result in serialized['suite_results']:
            for test_result in suite_result['test_results']:
                test_result['status'] = test_result['status'].value
                test_result['priority'] = test_result['priority'].value
        
        return serialized
    
    def _generate_markdown_report(self, report: RegressionTestReport) -> str:
        """Generate a human-readable markdown report."""
        lines = []
        lines.append("# 🧪 REGRESSION TESTING REPORT")
        lines.append(f"**Generated:** {report.execution_timestamp}")
        lines.append(f"**Total Test Suites:** {report.total_suites}")
        lines.append(f"**Total Tests:** {report.total_tests}")
        lines.append(f"**Overall Success Rate:** {report.overall_success_rate:.1f}%")
        lines.append(f"**Total Execution Time:** {report.total_execution_time:.2f} seconds")
        lines.append("")
        
        # Summary
        lines.append("## 📊 EXECUTION SUMMARY")
        lines.append(f"- ✅ **Passed:** {sum(s.passed_tests for s in report.suite_results)}")
        lines.append(f"- ❌ **Failed:** {sum(s.failed_tests for s in report.suite_results)}")
        lines.append(f"- ⏭️ **Skipped:** {sum(s.skipped_tests for s in report.suite_results)}")
        lines.append(f"- ⚠️ **Errors:** {sum(s.error_tests for s in report.suite_results)}")
        lines.append(f"- ⏱️ **Timeouts:** {sum(s.timeout_tests for s in report.suite_results)}")
        lines.append("")
        
        # Critical failures
        if report.critical_failures:
            lines.append("## 🚨 CRITICAL FAILURES")
            for failure in report.critical_failures:
                lines.append(f"- **{failure.test_name}** in {failure.test_file}")
                if failure.error_message:
                    lines.append(f"  - Error: {failure.error_message}")
            lines.append("")
        
        # Suite results
        lines.append("## 📋 SUITE RESULTS")
        for suite in report.suite_results:
            status_emoji = "✅" if suite.success_rate >= 90 else "⚠️" if suite.success_rate >= 80 else "❌"
            lines.append(f"### {status_emoji} {suite.suite_name}")
            lines.append(f"- **Success Rate:** {suite.success_rate:.1f}%")
            lines.append(f"- **Tests:** {suite.passed_tests}/{suite.total_tests} passed")
            lines.append(f"- **Execution Time:** {suite.execution_time:.2f}s")
            lines.append("")
        
        # Performance metrics
        lines.append("## ⚡ PERFORMANCE METRICS")
        for key, value in report.performance_metrics.items():
            if isinstance(value, float):
                lines.append(f"- **{key.replace('_', ' ').title()}:** {value:.2f}s")
            else:
                lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        lines.append("")
        
        # Recommendations
        lines.append("## 💡 RECOMMENDATIONS")
        for recommendation in report.recommendations:
            lines.append(f"- {recommendation}")
        
        return "\n".join(lines)


def run_regression_testing(test_directories: List[Path], output_dir: Path = None) -> RegressionTestReport:
    """Run comprehensive regression testing."""
    if output_dir is None:
        output_dir = Path("reports")
    
    # Create regression test manager
    manager = RegressionTestManager(test_directories)
    
    # Run tests
    report = manager.run_regression_tests()
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"regression_test_report_{timestamp}"
    manager.save_report(report, report_path)
    
    return report


def run_regression_tests_for_file(file_path: Path, test_directories: List[Path]) -> Dict[str, Any]:
    """Run regression tests specifically for a modularized file."""
    # Find related test files
    related_tests = []
    for test_dir in test_directories:
        test_dir_path = Path(test_dir)
        if test_dir_path.exists():
            # Look for test files that might test the given file
            file_name = file_path.stem
            possible_test_files = [
                test_dir_path / f"test_{file_name}.py",
                test_dir_path / file_path.parent.name / f"test_{file_name}.py",
                test_dir_path / "test_modularization" / f"test_{file_name}.py"
            ]
            
            for test_file in possible_test_files:
                if test_file.exists():
                    related_tests.append(test_file)
    
    if not related_tests:
        return {
            "status": "no_tests_found",
            "message": f"No regression tests found for {file_path}",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0
        }
    
    # Run regression tests for related test files
    try:
        manager = RegressionTestManager([Path(test_dir) for test_dir in test_directories])
        
        # Discover and execute tests
        discovered_tests = manager.discovery_engine.discover_tests()
        priorities = manager.discovery_engine.get_test_priorities()
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for test_file in related_tests:
            if str(test_file) in discovered_tests:
                test_cases = discovered_tests[str(test_file)]
                suite_result = manager.execution_engine.execute_test_suite(
                    test_file, test_cases, priorities
                )
                
                total_tests += suite_result.total_tests
                total_passed += suite_result.passed_tests
                total_failed += suite_result.failed_tests
        
        return {
            "status": "completed",
            "message": f"Regression tests completed for {file_path}",
            "tests_run": total_tests,
            "tests_passed": total_passed,
            "tests_failed": total_failed,
            "test_files": [str(tf) for tf in related_tests]
        }
        
    except Exception as e:
        logger.error(f"Error running regression tests for {file_path}: {e}")
        return {
            "status": "error",
            "message": f"Regression test execution failed: {e}",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0
        }
