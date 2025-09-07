from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

            import json
from src.core.testing.executor import TestExecutor
from src.core.testing.testing_utils import (
import time
import uuid

"""
Testing Framework Orchestrator
==============================

Manages test suite execution, scheduling, and coordination of the
consolidated testing framework.
"""


    TestStatus,
    TestType,
    TestPriority,
    TestEnvironment,
    TestResult,
    TestSuite,
    TestReport,
    BaseTest,
)


class TestSuiteManager:
    """Manages test suite definitions and organization"""

    def __init__(self):
        self.test_suites = {}
        self.suite_registry = {}

    def create_test_suite(
        self, suite_id: str, suite_name: str, description: str = ""
    ) -> TestSuite:
        """Create a new test suite"""
        suite = TestSuite(
            suite_id=suite_id, suite_name=suite_name, description=description
        )
        self.test_suites[suite_id] = suite
        return suite

    def get_test_suite(self, suite_id: str) -> Optional[TestSuite]:
        """Get a test suite by ID"""
        return self.test_suites.get(suite_id)

    def list_test_suites(self) -> List[TestSuite]:
        """List all available test suites"""
        return list(self.test_suites.values())

    def delete_test_suite(self, suite_id: str) -> bool:
        """Delete a test suite"""
        if suite_id in self.test_suites:
            del self.test_suites[suite_id]
            return True
        return False

    def add_test_to_suite(self, suite_id: str, test_id: str) -> bool:
        """Add a test to a suite"""
        suite = self.get_test_suite(suite_id)
        if suite:
            suite.add_test(test_id)
            return True
        return False

    def remove_test_from_suite(self, suite_id: str, test_id: str) -> bool:
        """Remove a test from a suite"""
        suite = self.get_test_suite(suite_id)
        if suite:
            return suite.remove_test(test_id)
        return False


class TestScheduler:
    """Schedules test execution based on priority and dependencies"""

    def __init__(self):
        self.execution_queue = []
        self.running_tests = set()
        self.completed_tests = set()
        self.failed_tests = set()

    def schedule_test(self, test: BaseTest, priority: TestPriority = None) -> None:
        """Schedule a test for execution"""
        if priority:
            test.priority = priority

        self.execution_queue.append(test)
        # Sort by priority (higher priority first)
        self.execution_queue.sort(key=lambda t: t.priority.value, reverse=True)

    def schedule_suite(
        self, suite: TestSuite, test_registry: Dict[str, BaseTest]
    ) -> None:
        """Schedule all tests in a suite"""
        for test_id in suite.test_ids:
            if test_id in test_registry:
                test = test_registry[test_id]
                self.schedule_test(test, suite.priority)

    def get_next_test(self) -> Optional[BaseTest]:
        """Get the next test to execute"""
        if self.execution_queue:
            return self.execution_queue.pop(0)
        return None

    def mark_test_running(self, test_id: str) -> None:
        """Mark a test as running"""
        self.running_tests.add(test_id)

    def mark_test_completed(self, test_id: str) -> None:
        """Mark a test as completed"""
        if test_id in self.running_tests:
            self.running_tests.remove(test_id)
        self.completed_tests.add(test_id)

    def mark_test_failed(self, test_id: str) -> None:
        """Mark a test as failed"""
        if test_id in self.running_tests:
            self.running_tests.remove(test_id)
        self.failed_tests.add(test_id)

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queued": len(self.execution_queue),
            "running": len(self.running_tests),
            "completed": len(self.completed_tests),
            "failed": len(self.failed_tests),
        }


class TestOrchestrator:
    """Main orchestrator for the testing framework"""

    def __init__(self, results_dir: str = "test_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)

        self.test_executor = TestExecutor()
        self.suite_manager = TestSuiteManager()
        self.scheduler = TestScheduler()

        self.test_registry = {}
        self.execution_history = []
        self.current_execution = None

        # Initialize default test suites
        self._initialize_default_suites()

    def _initialize_default_suites(self) -> None:
        """Initialize default test suites"""
        # Unit tests suite
        unit_suite = self.suite_manager.create_test_suite(
            "unit", "Unit Tests", "Basic unit tests for individual components"
        )
        unit_suite.test_types = [TestType.UNIT]
        unit_suite.priority = TestPriority.NORMAL

        # Integration tests suite
        integration_suite = self.suite_manager.create_test_suite(
            "integration", "Integration Tests", "Tests for component integration"
        )
        integration_suite.test_types = [TestType.INTEGRATION]
        integration_suite.priority = TestPriority.HIGH

        # Smoke tests suite
        smoke_suite = self.suite_manager.create_test_suite(
            "smoke", "Smoke Tests", "Basic functionality verification tests"
        )
        smoke_suite.test_types = [TestType.SMOKE]
        smoke_suite.priority = TestPriority.CRITICAL

        # Performance tests suite
        performance_suite = self.suite_manager.create_test_suite(
            "performance", "Performance Tests", "Performance and load testing"
        )
        performance_suite.test_types = [
            TestType.PERFORMANCE,
            TestType.LOAD,
            TestType.STRESS,
        ]
        performance_suite.priority = TestPriority.HIGH

    def register_test(self, test: BaseTest) -> str:
        """Register a test with the orchestrator"""
        test_id = test.test_id
        self.test_registry[test_id] = test
        self.test_executor.add_test_to_queue(test)
        return test_id

    def register_tests(self, tests: List[BaseTest]) -> List[str]:
        """Register multiple tests"""
        test_ids = []
        for test in tests:
            test_id = self.register_test(test)
            test_ids.append(test_id)
        return test_ids

    def run_test(self, test_id: str) -> Optional[TestResult]:
        """Run a single test"""
        if test_id not in self.test_registry:
            return None

        test = self.test_registry[test_id]
        result = test.run()

        if result:
            self._record_result(result)

        return result

    def run_test_suite(self, suite_id: str) -> List[TestResult]:
        """Run all tests in a specific suite"""
        suite = self.suite_manager.get_test_suite(suite_id)
        if not suite:
            return []

        results = []
        for test_id in suite.test_ids:
            if test_id in self.test_registry:
                result = self.run_test(test_id)
                if result:
                    results.append(result)

        return results

    def run_all_tests(self) -> List[TestResult]:
        """Run all registered tests"""
        return self.test_executor.execute_queue()

    def run_tests_by_type(self, test_type: TestType) -> List[TestResult]:
        """Run tests of a specific type"""
        results = []
        for test in self.test_registry.values():
            if test.test_type == test_type:
                result = test.run()
                if result:
                    results.append(result)
                    self._record_result(result)

        return results

    def run_tests_by_priority(self, priority: TestPriority) -> List[TestResult]:
        """Run tests of a specific priority"""
        results = []
        for test in self.test_registry.values():
            if test.priority == priority:
                result = test.run()
                if result:
                    results.append(result)
                    self._record_result(result)

        return results

    def _record_result(self, result: TestResult) -> None:
        """Record a test result"""
        self.execution_history.append(result)

        # Update scheduler status
        if result.status == TestStatus.PASSED:
            self.scheduler.mark_test_completed(result.test_id)
        elif result.status in [TestStatus.FAILED, TestStatus.ERROR]:
            self.scheduler.mark_test_failed(result.test_id)

    def get_test_summary(self) -> Dict[str, Any]:
        """Get a summary of all test results"""
        if not self.execution_history:
            return {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "success_rate": 0.0,
                "total_execution_time": 0.0,
            }

        total_tests = len(self.execution_history)
        passed = sum(1 for r in self.execution_history if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.execution_history if r.status == TestStatus.FAILED)
        errors = sum(1 for r in self.execution_history if r.status == TestStatus.ERROR)
        skipped = sum(
            1 for r in self.execution_history if r.status == TestStatus.SKIPPED
        )

        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        total_execution_time = sum(r.execution_time for r in self.execution_history)

        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "success_rate": success_rate,
            "total_execution_time": total_execution_time,
        }

    def get_test_results(self, test_id: str = None) -> List[TestResult]:
        """Get test results, optionally filtered by test ID"""
        if test_id:
            return [r for r in self.execution_history if r.test_id == test_id]
        return self.execution_history.copy()

    def export_results(self, format: str = "json") -> str:
        """Export test results in specified format"""
        if format.lower() == "json":
            results_data = [result.to_dict() for result in self.execution_history]

            return json.dumps(results_data, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def save_results(self, filename: str = None) -> str:
        """Save test results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"

        filepath = self.results_dir / filename
        results_json = self.export_results("json")

        with open(filepath, "w") as f:
            f.write(results_json)

        return str(filepath)

    def clear_results(self) -> None:
        """Clear all test results"""
        self.execution_history.clear()
        self.test_executor.clear_results()

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        summary = self.get_test_summary()
        queue_status = self.scheduler.get_queue_status()

        return {
            "system_status": "operational",
            "test_summary": summary,
            "queue_status": queue_status,
            "registered_tests": len(self.test_registry),
            "available_suites": len(self.suite_manager.list_test_suites()),
            "results_directory": str(self.results_dir),
        }

    def print_status(self) -> None:
        """Print current system status"""
        status = self.get_system_status()

        print(f"\n🧪 TESTING FRAMEWORK STATUS")
        print(f"=" * 50)
        print(f"System Status: {status['system_status']}")
        print(f"Registered Tests: {status['registered_tests']}")
        print(f"Available Suites: {status['available_suites']}")
        print(f"Results Directory: {status['results_directory']}")

        summary = status["test_summary"]
        print(f"\n📊 TEST SUMMARY:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  ✅ Passed: {summary['passed']}")
        print(f"  ❌ Failed: {summary['failed']}")
        print(f"  💥 Errors: {summary['errors']}")
        print(f"  ⏭️  Skipped: {summary['skipped']}")
        print(f"  📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"  ⏱️  Total Time: {summary['total_execution_time']:.2f}s")

        queue = status["queue_status"]
        print(f"\n🔄 QUEUE STATUS:")
        print(f"  Queued: {queue['queued']}")
        print(f"  Running: {queue['running']}")
        print(f"  Completed: {queue['completed']}")
        print(f"  Failed: {queue['failed']}")
