#!/usr/bin/env python3
"""
Testing Orchestration Runner - V2 Testing Framework Runner Components
===================================================================

Test runner management and execution orchestration.
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
    from .testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from .testing_core import BaseIntegrationTest
    from .testing_orchestration_core import IntegrationTestSuite, TestSuiteResult
except ImportError:
    from testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from testing_core import BaseIntegrationTest
    from testing_orchestration_core import IntegrationTestSuite, TestSuiteResult


class IntegrationTestRunner:
    """Manages and runs multiple test suites."""
    
    def __init__(self):
        self.test_suites: Dict[str, IntegrationTestSuite] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
        
        # Runner configuration
        self.max_concurrent_suites = 3
        self.global_timeout = 1800.0  # 30 minutes default
        self.continue_on_failure = True
        self.generate_reports = True
    
    def add_test_suite(self, suite: IntegrationTestSuite) -> None:
        """Add a test suite to the runner."""
        if not isinstance(suite, IntegrationTestSuite):
            raise ValueError("Suite must be an instance of IntegrationTestSuite")
        
        if suite.name in self.test_suites:
            self.logger.warning(f"Test suite '{suite.name}' already exists, replacing")
        
        self.test_suites[suite.name] = suite
        self.logger.info(f"Added test suite '{suite.name}' to runner")
    
    def remove_test_suite(self, suite_name: str) -> bool:
        """Remove a test suite from the runner."""
        if suite_name in self.test_suites:
            removed_suite = self.test_suites.pop(suite_name)
            self.logger.info(f"Removed test suite '{removed_suite.name}' from runner")
            return True
        return False
    
    def get_test_suite(self, suite_name: str) -> Optional[IntegrationTestSuite]:
        """Get a test suite by name."""
        return self.test_suites.get(suite_name)
    
    def list_test_suites(self) -> List[str]:
        """List all test suite names."""
        return list(self.test_suites.keys())
    
    async def run_test_suite(self, suite_name: str) -> Optional[TestSuiteResult]:
        """Run a specific test suite."""
        if suite_name not in self.test_suites:
            self.logger.error(f"Test suite '{suite_name}' not found")
            return None
        
        suite = self.test_suites[suite_name]
        self.logger.info(f"Running test suite '{suite_name}'")
        
        start_time = time.time()
        try:
            test_results = await suite.run_suite()
            end_time = time.time()
            duration = end_time - start_time
            
            # Calculate summary statistics
            total_tests = len(test_results)
            passed = sum(1 for r in test_results if r.status == TestStatus.PASSED)
            failed = sum(1 for r in test_results if r.status == TestStatus.FAILED)
            skipped = sum(1 for r in test_results if r.status == TestStatus.SKIPPED)
            error = sum(1 for r in test_results if r.status == TestStatus.ERROR)
            timeout = sum(1 for r in test_results if r.status == TestStatus.TIMEOUT)
            
            suite_result = TestSuiteResult(
                suite_name=suite_name,
                total_tests=total_tests,
                passed=passed,
                failed=failed,
                skipped=skipped,
                error=error,
                timeout=timeout,
                duration=duration,
                start_time=start_time,
                end_time=end_time,
                test_results=test_results,
                summary={
                    "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0.0,
                    "status": "completed" if failed == 0 and error == 0 else "failed"
                }
            )
            
            # Record execution
            self.execution_history.append({
                "suite_name": suite_name,
                "timestamp": time.time(),
                "result": suite_result,
                "status": "completed"
            })
            
            self.logger.info(f"Test suite '{suite_name}' completed: {passed}/{total_tests} passed")
            return suite_result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.error(f"Error running test suite '{suite_name}': {e}")
            
            # Record execution failure
            self.execution_history.append({
                "suite_name": suite_name,
                "timestamp": time.time(),
                "error": str(e),
                "duration": duration,
                "status": "failed"
            })
            
            return None
    
    async def run_all_suites(self) -> Dict[str, TestSuiteResult]:
        """Run all test suites."""
        if not self.test_suites:
            self.logger.warning("No test suites to run")
            return {}
        
        self.logger.info(f"Running {len(self.test_suites)} test suites")
        results = {}
        
        for suite_name in self.test_suites:
            try:
                suite_result = await self.run_test_suite(suite_name)
                if suite_result:
                    results[suite_name] = suite_result
                
                # Check if we should continue on failure
                if not self.continue_on_failure and suite_result and suite_result.failed > 0:
                    self.logger.warning(f"Stopping execution due to failure in suite '{suite_name}'")
                    break
                    
            except Exception as e:
                self.logger.error(f"Unexpected error running suite '{suite_name}': {e}")
                if not self.continue_on_failure:
                    break
        
        self.logger.info(f"Completed running {len(results)} test suites")
        return results
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.execution_history.copy()
    
    def get_global_summary(self) -> Dict[str, Any]:
        """Get global summary of all test executions."""
        if not self.execution_history:
            return {"status": "no_executions"}
        
        total_suites = len(self.execution_history)
        successful_suites = sum(1 for h in self.execution_history if h.get("status") == "completed")
        failed_suites = total_suites - successful_suites
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_error = 0
        total_timeout = 0
        
        for history in self.execution_history:
            if "result" in history:
                result = history["result"]
                total_tests += result.total_tests
                total_passed += result.passed
                total_failed += result.failed
                total_skipped += result.skipped
                total_error += result.error
                total_timeout += result.timeout
        
        return {
            "total_suites": total_suites,
            "successful_suites": successful_suites,
            "failed_suites": failed_suites,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "total_error": total_error,
            "total_timeout": total_timeout,
            "overall_success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0.0,
            "last_execution": max(h["timestamp"] for h in self.execution_history) if self.execution_history else None
        }
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
        self.logger.info("Execution history cleared")
    
    def get_runner_config(self) -> Dict[str, Any]:
        """Get runner configuration."""
        return {
            "max_concurrent_suites": self.max_concurrent_suites,
            "global_timeout": self.global_timeout,
            "continue_on_failure": self.continue_on_failure,
            "generate_reports": self.generate_reports,
            "total_suites": len(self.test_suites)
        }
