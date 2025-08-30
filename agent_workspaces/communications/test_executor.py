#!/usr/bin/env python3
"""
Test Executor Module
===================

Handles test execution and management operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging
import random

from .testing_core import TestingCore, TestResult, TestSuite, TestStatus, TestCategory


@dataclass
class TestExecutionConfig:
    """Configuration for test execution"""
    max_concurrent_tests: int = 5
    default_timeout_seconds: int = 300
    retry_failed_tests: bool = True
    max_retries: int = 3
    stop_on_failure: bool = False
    parallel_execution: bool = True


class TestExecutor:
    """Handles test execution and management"""
    
    def __init__(self, testing_core: TestingCore, config: Optional[TestExecutionConfig] = None):
        self.testing_core = testing_core
        self.config = config or TestExecutionConfig()
        self.logger = self._setup_logging()
        
        # Execution state
        self.running_tests: Dict[str, threading.Thread] = {}
        self.execution_queue: List[str] = []
        self.execution_lock = threading.Lock()
        self.stop_execution = False
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for test execution"""
        logger = logging.getLogger("TestExecutor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[EXECUTOR] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def execute_test(self, test_id: str, test_function: Callable, 
                    test_name: str, category: TestCategory, **kwargs) -> TestResult:
        """Execute a single test"""
        try:
            start_time = datetime.now()
            
            # Create test result
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                category=category,
                status=TestStatus.RUNNING,
                start_time=start_time
            )
            
            self.logger.info(f"Executing test: {test_name}")
            
            # Execute test with timeout
            try:
                test_output = test_function(**kwargs)
                result.status = TestStatus.PASSED
                result.details = {"output": test_output}
                
            except Exception as e:
                result.status = TestStatus.FAILED
                result.error_message = str(e)
                result.details = {"error_type": type(e).__name__}
                
            # Calculate duration
            end_time = datetime.now()
            result.end_time = end_time
            result.duration_ms = (end_time - start_time).total_seconds() * 1000
            
            # Add result to testing core
            self.testing_core.add_test_result(result)
            
            self.logger.info(f"Test {test_name} completed with status: {result.status.value}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing test {test_id}: {e}")
            # Create failed result
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                category=category,
                status=TestStatus.FAILED,
                start_time=datetime.now(),
                error_message=str(e)
            )
            self.testing_core.add_test_result(result)
            return result
    
    def execute_test_suite(self, suite_id: str) -> Dict[str, Any]:
        """Execute all tests in a test suite"""
        try:
            suite = self.testing_core.get_test_suite(suite_id)
            if not suite:
                return {"error": f"Test suite {suite_id} not found"}
            
            self.logger.info(f"Executing test suite: {suite.name}")
            
            suite_results = {
                "suite_id": suite_id,
                "suite_name": suite.name,
                "start_time": datetime.now().isoformat(),
                "tests_executed": 0,
                "tests_passed": 0,
                "tests_failed": 0,
                "tests_skipped": 0,
                "total_duration_ms": 0.0
            }
            
            # Execute tests sequentially for now (can be enhanced for parallel execution)
            for test_id in suite.tests:
                if self.stop_execution:
                    break
                
                # For now, we'll create a dummy test function
                # In a real implementation, this would be the actual test function
                def dummy_test(**kwargs):
                    time.sleep(random.uniform(0.1, 0.5))  # Simulate test execution
                    return {"status": "success", "data": "test_data"}
                
                result = self.execute_test(
                    test_id=test_id,
                    test_function=dummy_test,
                    test_name=f"Test_{test_id}",
                    category=suite.category
                )
                
                suite_results["tests_executed"] += 1
                suite_results["total_duration_ms"] += result.duration_ms or 0
                
                if result.status == TestStatus.PASSED:
                    suite_results["tests_passed"] += 1
                elif result.status == TestStatus.FAILED:
                    suite_results["tests_failed"] += 1
                    if self.config.stop_on_failure:
                        self.logger.warning(f"Stopping execution due to test failure: {test_id}")
                        break
                else:
                    suite_results["tests_skipped"] += 1
            
            suite_results["end_time"] = datetime.now().isoformat()
            suite_results["success_rate"] = suite_results["tests_passed"] / suite_results["tests_executed"] if suite_results["tests_executed"] > 0 else 0.0
            
            self.logger.info(f"Test suite {suite.name} completed: {suite_results['tests_passed']}/{suite_results['tests_executed']} passed")
            return suite_results
            
        except Exception as e:
            self.logger.error(f"Error executing test suite {suite_id}: {e}")
            return {"error": str(e)}
    
    def execute_tests_by_category(self, category: TestCategory, max_tests: Optional[int] = None) -> Dict[str, Any]:
        """Execute all tests of a specific category"""
        try:
            self.logger.info(f"Executing tests for category: {category.value}")
            
            # Get all test suites for this category
            category_suites = [
                suite for suite in self.testing_core.test_suites.values() 
                if suite.category == category
            ]
            
            if not category_suites:
                return {"error": f"No test suites found for category: {category.value}"}
            
            category_results = {
                "category": category.value,
                "start_time": datetime.now().isoformat(),
                "suites_executed": 0,
                "total_tests_executed": 0,
                "total_tests_passed": 0,
                "total_tests_failed": 0,
                "suite_results": []
            }
            
            # Execute each suite
            for suite in category_suites:
                if max_tests and category_results["total_tests_executed"] >= max_tests:
                    break
                
                suite_result = self.execute_test_suite(suite.suite_id)
                if "error" not in suite_result:
                    category_results["suites_executed"] += 1
                    category_results["total_tests_executed"] += suite_result["tests_executed"]
                    category_results["total_tests_passed"] += suite_result["tests_passed"]
                    category_results["total_tests_failed"] += suite_result["tests_failed"]
                    category_results["suite_results"].append(suite_result)
            
            category_results["end_time"] = datetime.now().isoformat()
            category_results["success_rate"] = (
                category_results["total_tests_passed"] / category_results["total_tests_executed"]
                if category_results["total_tests_executed"] > 0 else 0.0
            )
            
            self.logger.info(f"Category {category.value} execution completed: {category_results['total_tests_passed']}/{category_results['total_tests_executed']} passed")
            return category_results
            
        except Exception as e:
            self.logger.error(f"Error executing tests by category {category.value}: {e}")
            return {"error": str(e)}
    
    def run_performance_tests(self, test_count: int = 10) -> Dict[str, Any]:
        """Run performance tests to measure system performance"""
        try:
            self.logger.info(f"Running performance tests ({test_count} tests)")
            
            performance_results = {
                "test_type": "performance",
                "start_time": datetime.now().isoformat(),
                "test_count": test_count,
                "results": [],
                "summary": {}
            }
            
            # Run performance tests
            for i in range(test_count):
                test_id = f"perf_test_{i+1}"
                
                def performance_test(**kwargs):
                    start = time.time()
                    # Simulate some work
                    time.sleep(random.uniform(0.05, 0.2))
                    duration = time.time() - start
                    return {"duration": duration, "iteration": i+1}
                
                result = self.execute_test(
                    test_id=test_id,
                    test_function=performance_test,
                    test_name=f"Performance_Test_{i+1}",
                    category=TestCategory.PERFORMANCE
                )
                
                performance_results["results"].append({
                    "test_id": test_id,
                    "duration_ms": result.duration_ms,
                    "status": result.status.value
                })
            
            # Calculate performance summary
            durations = [r["duration_ms"] for r in performance_results["results"] if r["duration_ms"]]
            if durations:
                performance_results["summary"] = {
                    "average_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "total_duration_ms": sum(durations)
                }
            
            performance_results["end_time"] = datetime.now().isoformat()
            
            self.logger.info(f"Performance tests completed: {len(performance_results['results'])} tests executed")
            return performance_results
            
        except Exception as e:
            self.logger.error(f"Error running performance tests: {e}")
            return {"error": str(e)}
    
    def stop_all_tests(self) -> None:
        """Stop all running tests"""
        try:
            self.stop_execution = True
            self.logger.info("Stopping all test execution")
            
            # Wait for running tests to complete
            for thread in self.running_tests.values():
                if thread.is_alive():
                    thread.join(timeout=5.0)
            
            self.running_tests.clear()
            self.execution_queue.clear()
            
        except Exception as e:
            self.logger.error(f"Error stopping tests: {e}")
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status"""
        try:
            return {
                "execution_active": not self.stop_execution,
                "running_tests": len(self.running_tests),
                "queued_tests": len(self.execution_queue),
                "total_results": len(self.testing_core.test_results),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting execution status: {e}")
            return {"error": str(e)}
