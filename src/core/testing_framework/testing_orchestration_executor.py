#!/usr/bin/env python3
"""
Testing Orchestration Executor - V2 Testing Framework Execution Components
=======================================================================

Test execution management and orchestration.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from src.utils.stability_improvements import stability_manager, safe_import

# Import our types and core classes
try:
    from .testing_types import (
        TestStatus,
        TestType,
        TestPriority,
        TestResult,
        TestScenario,
        TestEnvironment,
    )
    from .base_test import BaseIntegrationTest
    from .testing_orchestration_core import IntegrationTestSuite
except ImportError:
    from testing_types import (
        TestStatus,
        TestType,
        TestPriority,
        TestResult,
        TestScenario,
        TestEnvironment,
    )
    from base_test import BaseIntegrationTest
    from testing_orchestration_core import IntegrationTestSuite


@dataclass
class ExecutionConfig:
    """Configuration for test execution."""
    max_parallel_tests: int = 5
    timeout_per_test: float = 300.0  # 5 minutes
    retry_failed_tests: bool = True
    max_retries: int = 2
    continue_on_failure: bool = True
    generate_detailed_logs: bool = True
    cleanup_after_execution: bool = True


class TestExecutor:
    """Executes individual tests and manages execution lifecycle."""
    
    def __init__(self, config: Optional[ExecutionConfig] = None):
        self.config = config or ExecutionConfig()
        self.execution_history: List[Dict[str, Any]] = []
        self.active_tests: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)
        
        # Execution statistics
        self.total_tests_executed = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.total_error = 0
        self.total_timeout = 0
    
    async def execute_test(self, test: BaseIntegrationTest, suite_name: str = "unknown") -> TestResult:
        """Execute a single test."""
        if not isinstance(test, BaseIntegrationTest):
            raise ValueError("Test must be an instance of BaseIntegrationTest")
        
        test_id = f"{suite_name}.{test.test_name}"
        start_time = time.time()
        
        self.logger.info(f"Executing test: {test_id}")
        
        # Record test start
        self.active_tests[test_id] = {
            "start_time": start_time,
            "suite_name": suite_name,
            "test_name": test.test_name,
            "status": "running"
        }
        
        try:
            # Execute the test
            result = await test.run()
            end_time = time.time()
            duration = end_time - start_time
            
            # Update result with execution metadata
            result.start_time = start_time
            result.end_time = end_time
            result.duration = duration
            
            # Update statistics
            self._update_statistics(result.status)
            
            # Record successful execution
            self.execution_history.append({
                "test_id": test_id,
                "suite_name": suite_name,
                "test_name": test.test_name,
                "status": "completed",
                "result": result,
                "duration": duration,
                "timestamp": time.time()
            })
            
            self.logger.info(f"Test {test_id} completed: {result.status.value}")
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            # Create error result
            result = TestResult(
                test_id=test_id,
                test_name=test.test_name,
                test_type=test.test_type,
                status=TestStatus.ERROR,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                error_message=str(e),
                error_traceback=str(e.__traceback__)
            )
            
            # Update statistics
            self._update_statistics(TestStatus.ERROR)
            
            # Record failed execution
            self.execution_history.append({
                "test_id": test_id,
                "suite_name": suite_name,
                "test_name": test.test_name,
                "status": "failed",
                "result": result,
                "error": str(e),
                "duration": duration,
                "timestamp": time.time()
            })
            
            self.logger.error(f"Test {test_id} failed: {e}")
        
        finally:
            # Cleanup active test record
            if test_id in self.active_tests:
                del self.active_tests[test_id]
        
        return result
    
    async def execute_test_suite(self, suite: IntegrationTestSuite) -> List[TestResult]:
        """Execute all tests in a test suite."""
        if not isinstance(suite, IntegrationTestSuite):
            raise ValueError("Suite must be an instance of IntegrationTestSuite")
        
        self.logger.info(f"Executing test suite: {suite.name}")
        
        results = []
        for test in suite.tests:
            try:
                result = await self.execute_test(test, suite.name)
                results.append(result)
                
                # Check if we should continue on failure
                if not self.config.continue_on_failure and result.status == TestStatus.FAILED:
                    self.logger.warning(f"Stopping execution due to test failure: {test.test_name}")
                    break
                    
            except Exception as e:
                self.logger.error(f"Unexpected error executing test {test.test_name}: {e}")
                if not self.config.continue_on_failure:
                    break
        
        self.logger.info(f"Test suite {suite.name} execution completed: {len(results)} tests")
        return results
    
    def _update_statistics(self, status: TestStatus) -> None:
        """Update execution statistics."""
        self.total_tests_executed += 1
        
        if status == TestStatus.PASSED:
            self.total_passed += 1
        elif status == TestStatus.FAILED:
            self.total_failed += 1
        elif status == TestStatus.SKIPPED:
            self.total_skipped += 1
        elif status == TestStatus.ERROR:
            self.total_error += 1
        elif status == TestStatus.TIMEOUT:
            self.total_timeout += 1
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all test executions."""
        if self.total_tests_executed == 0:
            return {"status": "no_tests_executed"}
        
        success_rate = (self.total_passed / self.total_tests_executed * 100)
        
        return {
            "total_tests_executed": self.total_tests_executed,
            "total_passed": self.total_passed,
            "total_failed": self.total_failed,
            "total_skipped": self.total_skipped,
            "total_error": self.total_error,
            "total_timeout": self.total_timeout,
            "success_rate": success_rate,
            "active_tests": len(self.active_tests),
            "execution_history_count": len(self.execution_history)
        }
    
    def get_active_tests(self) -> Dict[str, Dict[str, Any]]:
        """Get currently active tests."""
        return self.active_tests.copy()
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.execution_history.copy()
    
    def clear_history(self) -> None:
        """Clear execution history and statistics."""
        self.execution_history.clear()
        self.active_tests.clear()
        self.total_tests_executed = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.total_error = 0
        self.total_timeout = 0
        self.logger.info("Execution history and statistics cleared")
    
    def get_config(self) -> Dict[str, Any]:
        """Get executor configuration."""
        return {
            "max_parallel_tests": self.config.max_parallel_tests,
            "timeout_per_test": self.config.timeout_per_test,
            "retry_failed_tests": self.config.retry_failed_tests,
            "max_retries": self.config.max_retries,
            "continue_on_failure": self.config.continue_on_failure,
            "generate_detailed_logs": self.config.generate_detailed_logs,
            "cleanup_after_execution": self.config.cleanup_after_execution
        }
    
    def update_config(self, **kwargs) -> None:
        """Update executor configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config key: {key}")
