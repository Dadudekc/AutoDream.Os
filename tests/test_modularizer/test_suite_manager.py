"""
🧪 REGRESSION TESTING SYSTEM - Test Suite Manager
Extracted from regression_testing_system.py for modularization

This module handles test suite registration, management, and execution.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Callable
from .models import TestStatus, RegressionTestSuite
from .test_executor import TestExecutor


class TestSuiteManager:
    """Manages test suites and their execution."""
    
    def __init__(self, test_executor: TestExecutor):
        self.test_executor = test_executor
        self.test_suites = {}
        self.test_results = {}
        self.execution_history = []
    
    def register_test_suite(self, test_suite: RegressionTestSuite) -> bool:
        """
        Register a test suite for regression testing.
        
        Args:
            test_suite: The test suite to register
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not test_suite.name or test_suite.name in self.test_suites:
                return False
            
            self.test_suites[test_suite.name] = test_suite
            return True
            
        except Exception as e:
            print(f"Error registering test suite: {e}")
            return False
    
    def run_test_suite(self, suite_name: str, comparison_mode: bool = False) -> Dict[str, Any]:
        """
        Run a complete test suite.
        
        Args:
            suite_name: Name of the test suite to run
            comparison_mode: Whether to run in before/after comparison mode
            
        Returns:
            Dictionary containing test suite execution results
        """
        if suite_name not in self.test_suites:
            return {"error": f"Test suite '{suite_name}' not found"}
        
        test_suite = self.test_suites[suite_name]
        results = {
            "suite_name": suite_name,
            "description": test_suite.description,
            "category": test_suite.category,
            "priority": test_suite.priority,
            "total_tests": len(test_suite.tests),
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_timed_out": 0,
            "tests_errored": 0,
            "tests_skipped": 0,
            "execution_time": 0.0,
            "test_results": [],
            "overall_status": TestStatus.PENDING,
            "timestamp": None
        }
        
        try:
            start_time = time.time()
            
            # Run individual tests
            for test_func in test_suite.tests:
                test_result = self.test_executor.run_single_test(
                    test_func, test_suite.timeout, comparison_mode
                )
                results["test_results"].append(test_result)
                
                # Update counters
                if test_result.status == TestStatus.PASSED:
                    results["tests_passed"] += 1
                elif test_result.status == TestStatus.FAILED:
                    results["tests_failed"] += 1
                elif test_result.status == TestStatus.TIMEOUT:
                    results["tests_timed_out"] += 1
                elif test_result.status == TestStatus.ERROR:
                    results["tests_errored"] += 1
                elif test_result.status == TestStatus.SKIPPED:
                    results["tests_skipped"] += 1
            
            # Calculate execution time
            execution_time = time.time() - start_time
            results["execution_time"] = execution_time
            
            # Determine overall status
            if results["tests_failed"] > 0 or results["tests_errored"] > 0:
                results["overall_status"] = TestStatus.FAILED
            elif results["tests_timed_out"] > 0:
                results["overall_status"] = TestStatus.TIMEOUT
            elif results["tests_passed"] == results["total_tests"]:
                results["overall_status"] = TestStatus.PASSED
            else:
                results["overall_status"] = TestStatus.PENDING
            
            # Add timestamp
            results["timestamp"] = datetime.now().isoformat()
            
            # Store results
            self.test_results[suite_name] = results
            self.execution_history.append(results)
            
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = TestStatus.ERROR
            
        return results
    
    def get_test_results(self, suite_name: str = None) -> Dict[str, Any]:
        """Get test results for a specific suite or all suites."""
        if suite_name:
            return self.test_results.get(suite_name, {})
        return self.test_results
    
    def get_execution_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get execution history with optional limit."""
        if limit is None:
            return self.execution_history
        return self.execution_history[-limit:]
    
    def clear_test_results(self, suite_name: str = None) -> bool:
        """Clear test results for a specific suite or all suites."""
        try:
            if suite_name:
                if suite_name in self.test_results:
                    del self.test_results[suite_name]
                return True
            else:
                self.test_results.clear()
                self.execution_history.clear()
                return True
        except Exception:
            return False
