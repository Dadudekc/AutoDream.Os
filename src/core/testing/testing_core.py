"""
Testing Framework Core Classes
=============================

Defines the base classes and core functionality for the consolidated
testing framework.
"""

import time
import traceback
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import uuid

from src.core.testing.testing_types import (
    TestStatus,
    TestType,
    TestPriority,
    TestResult,
    TestEnvironment
)


class BaseTest(ABC):
    """Abstract base class for all tests in the framework"""
    
    def __init__(self, test_id: str = None, test_name: str = None):
        self.test_id = test_id or str(uuid.uuid4())
        self.test_name = test_name or self.__class__.__name__
        self.test_type = TestType.UNIT
        self.priority = TestPriority.NORMAL
        self.environment = TestEnvironment.LOCAL
        self.metadata = {}
        self.setup_called = False
        self.teardown_called = False
    
    @abstractmethod
    def test_logic(self) -> bool:
        """Implement the actual test logic here"""
        pass
    
    def setup(self) -> None:
        """Setup method called before test execution"""
        self.setup_called = True
    
    def teardown(self) -> None:
        """Teardown method called after test execution"""
        self.teardown_called = True
    
    def run(self) -> TestResult:
        """Execute the test and return results"""
        start_time = datetime.now()
        start_timestamp = time.time()
        
        try:
            # Setup phase
            self.setup()
            
            # Execute test logic
            result = self.test_logic()
            
            # Determine status
            if result:
                status = TestStatus.PASSED
                error_message = None
                stack_trace = None
            else:
                status = TestStatus.FAILED
                error_message = "Test logic returned False"
                stack_trace = None
                
        except Exception as e:
            status = TestStatus.ERROR
            error_message = str(e)
            stack_trace = traceback.format_exc()
            
        finally:
            # Teardown phase
            try:
                self.teardown()
            except Exception as e:
                # Log teardown errors but don't fail the test
                print(f"Warning: Teardown failed for {self.test_name}: {e}")
        
        end_time = datetime.now()
        end_timestamp = time.time()
        execution_time = end_timestamp - start_timestamp
        
        return TestResult(
            test_id=self.test_id,
            test_name=self.test_name,
            test_type=self.test_type,
            status=status,
            priority=self.priority,
            execution_time=execution_time,
            start_time=start_time,
            end_time=end_time,
            error_message=error_message,
            stack_trace=stack_trace,
            metadata=self.metadata
        )


class BaseIntegrationTest(BaseTest):
    """Base class for integration tests"""
    
    def __init__(self, test_id: str = None, test_name: str = None):
        super().__init__(test_id, test_name)
        self.test_type = TestType.INTEGRATION
        self.priority = TestPriority.HIGH
        self.dependencies = []
        self.cleanup_actions = []
    
    def add_dependency(self, dependency: str) -> None:
        """Add a dependency requirement"""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
    
    def add_cleanup_action(self, action: Callable) -> None:
        """Add a cleanup action to be executed after the test"""
        self.cleanup_actions.append(action)
    
    def teardown(self) -> None:
        """Execute cleanup actions before calling parent teardown"""
        for action in self.cleanup_actions:
            try:
                action()
            except Exception as e:
                print(f"Warning: Cleanup action failed: {e}")
        
        super().teardown()


class TestRunner:
    """Executes individual tests and manages test lifecycle"""
    
    def __init__(self):
        self.test_registry = {}
        self.results_history = []
    
    def register_test(self, test: BaseTest) -> None:
        """Register a test for execution"""
        self.test_registry[test.test_id] = test
    
    def unregister_test(self, test_id: str) -> bool:
        """Unregister a test"""
        if test_id in self.test_registry:
            del self.test_registry[test_id]
            return True
        return False
    
    def run_test(self, test_id: str) -> Optional[TestResult]:
        """Run a single test by ID"""
        if test_id not in self.test_registry:
            return None
        
        test = self.test_registry[test_id]
        result = test.run()
        self.results_history.append(result)
        return result
    
    def run_tests(self, test_ids: List[str]) -> List[TestResult]:
        """Run multiple tests"""
        results = []
        for test_id in test_ids:
            result = self.run_test(test_id)
            if result:
                results.append(result)
        return results
    
    def get_test_result(self, test_id: str) -> Optional[TestResult]:
        """Get the result of a specific test"""
        for result in self.results_history:
            if result.test_id == test_id:
                return result
        return None
    
    def get_all_results(self) -> List[TestResult]:
        """Get all test results"""
        return self.results_history.copy()
    
    def clear_results(self) -> None:
        """Clear the results history"""
        self.results_history.clear()


class TestExecutor:
    """Advanced test executor with parallel execution and result aggregation"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.test_runner = TestRunner()
        self.execution_queue = []
        self.active_executions = {}
    
    def add_test_to_queue(self, test: BaseTest) -> None:
        """Add a test to the execution queue"""
        self.execution_queue.append(test)
        self.test_runner.register_test(test)
    
    def add_tests_to_queue(self, tests: List[BaseTest]) -> None:
        """Add multiple tests to the execution queue"""
        for test in tests:
            self.add_test_to_queue(test)
    
    def execute_queue(self) -> List[TestResult]:
        """Execute all tests in the queue"""
        if not self.execution_queue:
            return []
        
        results = []
        for test in self.execution_queue:
            result = self.test_runner.run_test(test.test_id)
            if result:
                results.append(result)
        
        # Clear the queue after execution
        self.execution_queue.clear()
        return results
    
    def execute_parallel(self, tests: List[BaseTest]) -> List[TestResult]:
        """Execute tests in parallel (simplified implementation)"""
        # For now, implement sequential execution
        # TODO: Implement true parallel execution with threading
        return self.execute_queue()
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        all_results = self.test_runner.get_all_results()
        
        if not all_results:
            return {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "success_rate": 0.0,
                "avg_execution_time": 0.0
            }
        
        total_tests = len(all_results)
        passed = sum(1 for r in all_results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in all_results if r.status == TestStatus.FAILED)
        errors = sum(1 for r in all_results if r.status == TestStatus.ERROR)
        skipped = sum(1 for r in all_results if r.status == TestStatus.SKIPPED)
        
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        avg_execution_time = sum(r.execution_time for r in all_results) / total_tests
        
        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time
        }
    
    def print_execution_summary(self) -> None:
        """Print a summary of execution statistics"""
        stats = self.get_execution_stats()
        
        print(f"\n🚀 TEST EXECUTION SUMMARY")
        print(f"=" * 40)
        print(f"Total Tests: {stats['total_tests']}")
        print(f"✅ Passed: {stats['passed']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"💥 Errors: {stats['errors']}")
        print(f"⏭️  Skipped: {stats['skipped']}")
        print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
        print(f"⏱️  Avg Execution Time: {stats['avg_execution_time']:.2f}s")
