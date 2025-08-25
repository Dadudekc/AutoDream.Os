#!/usr/bin/env python3
"""
Testing Orchestration Core - V2 Testing Framework Core Components
================================================================

Core test suite management and execution logic.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from src.utils.stability_improvements import stability_manager, safe_import

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
        """Get summary of test suite."""
        if not self.tests:
            return {
                "suite_name": self.name,
                "description": self.description,
                "total_tests": 0,
                "status": "empty"
            }
        
        return {
            "suite_name": self.name,
            "description": self.description,
            "total_tests": len(self.tests),
            "environment": self.environment.name if self.environment else None,
            "parallel_execution": self.parallel_execution,
            "max_parallel_tests": self.max_parallel_tests,
            "timeout": self.timeout,
            "retry_failed": self.retry_failed,
            "max_retries": self.max_retries
        }
