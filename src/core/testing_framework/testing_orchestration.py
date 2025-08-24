#!/usr/bin/env python3
"""
Testing Orchestration - V2 Testing Framework Orchestration
==========================================================

Contains test suite management, test execution orchestration, and test runner functionality.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import asyncio
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from unittest.mock import Mock, AsyncMock

# Import our types and core classes
try:
    from .testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from .testing_core import BaseIntegrationTest
except ImportError:
    from testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from testing_core import BaseIntegrationTest


@dataclass
class TestSuiteResult:
    """Result of a test suite execution."""
    suite_name: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    error: int
    timeout: int
    duration: float
    start_time: float
    end_time: float
    test_results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class IntegrationTestSuite:
    """Manages a collection of integration tests."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.tests: List[BaseIntegrationTest] = []
        self.environment: Optional[TestEnvironment] = None
        self.logger = logging.getLogger(f"suite.{name}")
        
        # Suite configuration
        self.parallel_execution = False
        self.max_parallel_tests = 5
        self.timeout = 300.0  # 5 minutes default
        self.retry_failed = True
        self.max_retries = 2
    
    def add_test(self, test: BaseIntegrationTest) -> None:
        """Add a test to the suite."""
        if not isinstance(test, BaseIntegrationTest):
            raise ValueError("Test must be an instance of BaseIntegrationTest")
        
        self.tests.append(test)
        self.logger.info(f"Added test '{test.test_name}' to suite '{self.name}'")
    
    def remove_test(self, test_name: str) -> bool:
        """Remove a test from the suite by name."""
        for i, test in enumerate(self.tests):
            if test.test_name == test_name:
                removed_test = self.tests.pop(i)
                self.logger.info(f"Removed test '{removed_test.test_name}' from suite '{self.name}'")
                return True
        return False
    
    def set_environment(self, environment: TestEnvironment) -> None:
        """Set the test environment for the suite."""
        self.environment = environment
        self.parallel_execution = environment.parallel_execution
        self.max_parallel_tests = environment.max_parallel_tests
        self.logger.info(f"Set environment '{environment.name}' for suite '{self.name}'")
    
    async def run_suite(self) -> List[TestResult]:
        """Run all tests in the suite."""
        if not self.tests:
            self.logger.warning(f"No tests in suite '{self.name}'")
            return []
        
        self.logger.info(f"Starting suite '{self.name}' with {len(self.tests)} tests")
        start_time = time.time()
        
        if self.parallel_execution:
            results = await self._run_parallel()
        else:
            results = await self._run_sequential()
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.logger.info(f"Suite '{self.name}' completed in {duration:.2f}s")
        return results
    
    async def _run_sequential(self) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        
        for test in self.tests:
            try:
                self.logger.info(f"Running test '{test.test_name}'")
                result = await test.run()
                results.append(result)
                
                if result.status == TestStatus.FAILED and self.retry_failed:
                    result = await self._retry_test(test)
                    results.append(result)
                    
            except Exception as e:
                self.logger.error(f"Error running test '{test.test_name}': {e}")
                error_result = TestResult(
                    test_id=f"{test.test_name}_error",
                    test_name=test.test_name,
                    test_type=test.test_type,
                    status=TestStatus.ERROR,
                    start_time=time.time(),
                    end_time=time.time(),
                    duration=0.0,
                    error_message=str(e),
                    error_traceback=str(e.__traceback__)
                )
                results.append(error_result)
        
        return results
    
    async def _run_parallel(self) -> List[TestResult]:
        """Run tests in parallel."""
        semaphore = asyncio.Semaphore(self.max_parallel_tests)
        
        async def run_test_with_semaphore(test: BaseIntegrationTest) -> TestResult:
            async with semaphore:
                try:
                    return await test.run()
                except Exception as e:
                    self.logger.error(f"Error running test '{test.test_name}': {e}")
                    return TestResult(
                        test_id=f"{test.test_name}_error",
                        test_name=test.test_name,
                        test_type=test.test_type,
                        status=TestStatus.ERROR,
                        start_time=time.time(),
                        end_time=time.time(),
                        duration=0.0,
                        error_message=str(e),
                        error_traceback=str(e.__traceback__)
                    )
        
        tasks = [run_test_with_semaphore(test) for test in self.tests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and convert to list
        valid_results = []
        for result in results:
            if isinstance(result, TestResult):
                valid_results.append(result)
            else:
                self.logger.error(f"Test returned exception: {result}")
        
        return valid_results
    
    async def _retry_test(self, test: BaseIntegrationTest) -> TestResult:
        """Retry a failed test."""
        for attempt in range(self.max_retries):
            self.logger.info(f"Retrying test '{test.test_name}' (attempt {attempt + 1}/{self.max_retries})")
            
            try:
                result = await test.run()
                if result.status == TestStatus.PASSED:
                    self.logger.info(f"Test '{test.test_name}' passed on retry")
                    return result
            except Exception as e:
                self.logger.warning(f"Retry attempt {attempt + 1} failed: {e}")
        
        self.logger.error(f"Test '{test.test_name}' failed after {self.max_retries} retries")
        return TestResult(
            test_id=f"{test.test_name}_retry_failed",
            test_name=test.test_name,
            test_type=test.test_type,
            status=TestStatus.FAILED,
            start_time=time.time(),
            end_time=time.time(),
            duration=0.0,
            error_message=f"Failed after {self.max_retries} retries"
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the test suite."""
        if not hasattr(self, '_last_results'):
            return {
                "name": self.name,
                "description": self.description,
                "total_tests": len(self.tests),
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "error": 0,
                "timeout": 0,
                "success_rate": 0.0
            }
        
        total = len(self._last_results)
        passed = sum(1 for r in self._last_results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self._last_results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self._last_results if r.status == TestStatus.SKIPPED)
        error = sum(1 for r in self._last_results if r.status == TestStatus.ERROR)
        timeout = sum(1 for r in self._last_results if r.status == TestStatus.TIMEOUT)
        
        success_rate = (passed / total * 100) if total > 0 else 0.0
        
        return {
            "name": self.name,
            "description": self.description,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
            "timeout": timeout,
            "success_rate": success_rate
        }


class IntegrationTestRunner:
    """Orchestrates multiple test suites."""
    
    def __init__(self):
        self.test_suites: List[IntegrationTestSuite] = []
        self.logger = logging.getLogger("test_runner")
        self.global_config = {
            "parallel_suites": False,
            "max_parallel_suites": 3,
            "stop_on_failure": False,
            "generate_report": True,
            "report_format": "json"
        }
    
    def add_test_suite(self, suite: IntegrationTestSuite) -> None:
        """Add a test suite to the runner."""
        if not isinstance(suite, IntegrationTestSuite):
            raise ValueError("Suite must be an instance of IntegrationTestSuite")
        
        self.test_suites.append(suite)
        self.logger.info(f"Added test suite '{suite.name}' to runner")
    
    def remove_test_suite(self, suite_name: str) -> bool:
        """Remove a test suite from the runner by name."""
        for i, suite in enumerate(self.test_suites):
            if suite.name == suite_name:
                removed_suite = self.test_suites.pop(i)
                self.logger.info(f"Removed test suite '{removed_suite.name}' from runner")
                return True
        return False
    
    def set_global_config(self, config: Dict[str, Any]) -> None:
        """Set global configuration for the test runner."""
        self.global_config.update(config)
        self.logger.info(f"Updated global configuration: {config}")
    
    async def run_all_suites(self) -> Dict[str, List[TestResult]]:
        """Run all test suites."""
        if not self.test_suites:
            self.logger.warning("No test suites in runner")
            return {}
        
        self.logger.info(f"Starting {len(self.test_suites)} test suites")
        start_time = time.time()
        
        if self.global_config["parallel_suites"]:
            results = await self._run_suites_parallel()
        else:
            results = await self._run_suites_sequential()
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.logger.info(f"All test suites completed in {duration:.2f}s")
        return results
    
    async def _run_suites_sequential(self) -> Dict[str, List[TestResult]]:
        """Run test suites sequentially."""
        results = {}
        
        for suite in self.test_suites:
            try:
                self.logger.info(f"Running suite '{suite.name}'")
                suite_results = await suite.run_suite()
                results[suite.name] = suite_results
                
                # Store results for summary generation
                suite._last_results = suite_results
                
                # Check if we should stop on failure
                if (self.global_config["stop_on_failure"] and 
                    any(r.status == TestStatus.FAILED for r in suite_results)):
                    self.logger.warning(f"Stopping on failure in suite '{suite.name}'")
                    break
                    
            except Exception as e:
                self.logger.error(f"Error running suite '{suite.name}': {e}")
                results[suite.name] = []
        
        return results
    
    async def _run_suites_parallel(self) -> Dict[str, List[TestResult]]:
        """Run test suites in parallel."""
        semaphore = asyncio.Semaphore(self.global_config["max_parallel_suites"])
        
        async def run_suite_with_semaphore(suite: IntegrationTestSuite) -> tuple[str, List[TestResult]]:
            async with semaphore:
                try:
                    results = await suite.run_suite()
                    suite._last_results = results
                    return suite.name, results
                except Exception as e:
                    self.logger.error(f"Error running suite '{suite.name}': {e}")
                    return suite.name, []
        
        tasks = [run_suite_with_semaphore(suite) for suite in self.test_suites]
        suite_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert results to dictionary
        results = {}
        for result in suite_results:
            if isinstance(result, tuple) and len(result) == 2:
                suite_name, test_results = result
                results[suite_name] = test_results
            else:
                self.logger.error(f"Suite returned exception: {result}")
        
        return results
    
    def get_global_summary(self) -> Dict[str, Any]:
        """Get a global summary of all test suites."""
        if not self.test_suites:
            return {
                "total_suites": 0,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "error": 0,
                "timeout": 0,
                "overall_success_rate": 0.0
            }
        
        total_suites = len(self.test_suites)
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_error = 0
        total_timeout = 0
        
        suite_summaries = []
        
        for suite in self.test_suites:
            summary = suite.get_summary()
            suite_summaries.append(summary)
            
            total_tests += summary["total_tests"]
            total_passed += summary["passed"]
            total_failed += summary["failed"]
            total_skipped += summary["skipped"]
            total_error += summary["error"]
            total_timeout += summary["timeout"]
        
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0.0
        
        return {
            "total_suites": total_suites,
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "error": total_error,
            "timeout": total_timeout,
            "overall_success_rate": overall_success_rate,
            "suite_summaries": suite_summaries
        }


class TestExecutor:
    """Executes individual tests with proper lifecycle management."""
    
    def __init__(self):
        self.logger = logging.getLogger("test_executor")
        self.execution_history: List[TestResult] = []
    
    async def execute_test(self, test: BaseIntegrationTest, timeout: float = 300.0) -> TestResult:
        """Execute a single test with timeout protection."""
        try:
            self.logger.info(f"Executing test '{test.test_name}' with timeout {timeout}s")
            
            # Execute test with timeout
            result = await asyncio.wait_for(test.run(), timeout=timeout)
            
            # Store in history
            self.execution_history.append(result)
            
            self.logger.info(f"Test '{test.test_name}' completed with status: {result.status.value}")
            return result
            
        except asyncio.TimeoutError:
            self.logger.error(f"Test '{test.test_name}' timed out after {timeout}s")
            
            timeout_result = TestResult(
                test_id=f"{test.test_name}_timeout",
                test_name=test.test_name,
                test_type=test.test_type,
                status=TestStatus.TIMEOUT,
                start_time=time.time(),
                end_time=time.time(),
                duration=timeout,
                error_message=f"Test timed out after {timeout} seconds"
            )
            
            self.execution_history.append(timeout_result)
            return timeout_result
            
        except Exception as e:
            self.logger.error(f"Error executing test '{test.test_name}': {e}")
            
            error_result = TestResult(
                test_id=f"{test.test_name}_error",
                test_name=test.test_name,
                test_type=test.test_type,
                status=TestStatus.ERROR,
                start_time=time.time(),
                end_time=time.time(),
                duration=0.0,
                error_message=str(e),
                error_traceback=str(e.__traceback__)
            )
            
            self.execution_history.append(error_result)
            return error_result
    
    def get_execution_history(self) -> List[TestResult]:
        """Get the execution history of all tests."""
        return self.execution_history.copy()
    
    def clear_history(self) -> None:
        """Clear the execution history."""
        self.execution_history.clear()
        self.logger.info("Execution history cleared")


class TestOrchestrator:
    """High-level test orchestration and coordination."""
    
    def __init__(self):
        self.runner = IntegrationTestRunner()
        self.executor = TestExecutor()
        self.logger = logging.getLogger("test_orchestrator")
        
        # Orchestration configuration
        self.config = {
            "auto_retry_failed": True,
            "generate_reports": True,
            "notify_on_completion": False,
            "cleanup_after_execution": True
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the test orchestrator."""
        self.config.update(config)
        self.logger.info(f"Updated orchestrator configuration: {config}")
    
    async def run_test_suite(self, suite: IntegrationTestSuite) -> Dict[str, Any]:
        """Run a single test suite with orchestration."""
        self.logger.info(f"Orchestrating test suite '{suite.name}'")
        
        try:
            # Add suite to runner
            self.runner.add_test_suite(suite)
            
            # Run the suite
            results = await self.runner.run_all_suites()
            
            # Generate summary
            summary = self.runner.get_global_summary()
            
            # Generate report if enabled
            if self.config["generate_reports"]:
                report = self._generate_report(suite.name, results.get(suite.name, []))
                summary["report"] = report
            
            # Cleanup if enabled
            if self.config["cleanup_after_execution"]:
                self.runner.remove_test_suite(suite.name)
            
            self.logger.info(f"Test suite '{suite.name}' orchestration completed")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error orchestrating test suite '{suite.name}': {e}")
            return {
                "error": str(e),
                "suite_name": suite.name,
                "status": "failed"
            }
    
    async def run_multiple_suites(self, suites: List[IntegrationTestSuite]) -> Dict[str, Any]:
        """Run multiple test suites with orchestration."""
        self.logger.info(f"Orchestrating {len(suites)} test suites")
        
        try:
            # Add all suites to runner
            for suite in suites:
                self.runner.add_test_suite(suite)
            
            # Run all suites
            results = await self.runner.run_all_suites()
            
            # Generate global summary
            summary = self.runner.get_global_summary()
            
            # Generate reports if enabled
            if self.config["generate_reports"]:
                reports = {}
                for suite_name, suite_results in results.items():
                    reports[suite_name] = self._generate_report(suite_name, suite_results)
                summary["reports"] = reports
            
            # Cleanup if enabled
            if self.config["cleanup_after_execution"]:
                for suite in suites:
                    self.runner.remove_test_suite(suite.name)
            
            self.logger.info(f"Multiple test suites orchestration completed")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error orchestrating multiple test suites: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _generate_report(self, suite_name: str, results: List[TestResult]) -> Dict[str, Any]:
        """Generate a test report for a suite."""
        if not results:
            return {"suite_name": suite_name, "status": "no_results"}
        
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        error = sum(1 for r in results if r.status == TestStatus.ERROR)
        timeout = sum(1 for r in results if r.status == TestStatus.TIMEOUT)
        
        success_rate = (passed / total * 100) if total > 0 else 0.0
        
        return {
            "suite_name": suite_name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
            "timeout": timeout,
            "success_rate": success_rate,
            "execution_time": sum(r.duration for r in results if r.duration > 0),
            "timestamp": time.time()
        }


def run_smoke_test() -> bool:
    """Run smoke test for testing orchestration module."""
    try:
        print("🧪 Testing Testing Orchestration Module...")
        
        # Test IntegrationTestSuite
        suite = IntegrationTestSuite("Test Suite", "Test description")
        assert suite.name == "Test Suite"
        assert suite.description == "Test description"
        assert len(suite.tests) == 0
        print("✅ IntegrationTestSuite creation successful")
        
        # Test IntegrationTestRunner
        runner = IntegrationTestRunner()
        assert len(runner.test_suites) == 0
        runner.add_test_suite(suite)
        assert len(runner.test_suites) == 1
        print("✅ IntegrationTestRunner creation and suite addition successful")
        
        # Test TestExecutor
        executor = TestExecutor()
        assert len(executor.execution_history) == 0
        print("✅ TestExecutor creation successful")
        
        # Test TestOrchestrator
        orchestrator = TestOrchestrator()
        assert orchestrator.runner is not None
        assert orchestrator.executor is not None
        print("✅ TestOrchestrator creation successful")
        
        print("🎉 All testing orchestration smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Testing orchestration smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
