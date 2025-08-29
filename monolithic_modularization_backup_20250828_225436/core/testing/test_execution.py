"""Utilities for executing tests.

This module provides the :class:`TestRunner` and :class:`TestExecutor`
classes responsible for running tests either sequentially or in
parallel. Discovery and reporting are handled by dedicated modules.
"""

from __future__ import annotations

import queue
import threading
from typing import Any, Callable, Dict, List, Optional

from .testing_utils import BaseTest, TestResult, TestStatus


class TestRunner:
    """Execute registered :class:`BaseTest` instances."""

    def __init__(self) -> None:
        self.registered_tests: Dict[str, BaseTest] = {}
        self.results_history: List[TestResult] = []
        self.test_execution_callbacks: Dict[
            str, List[Callable[[TestResult], None]]
        ] = {}
        self.execution_lock = threading.Lock()

    # Registration -------------------------------------------------------
    def register_test(self, test: BaseTest) -> bool:
        """Register a test for execution."""
        if test.test_id in self.registered_tests:
            return False
        self.registered_tests[test.test_id] = test
        return True

    def unregister_test(self, test_id: str) -> bool:
        """Unregister a previously registered test."""
        return self.registered_tests.pop(test_id, None) is not None

    # Execution ----------------------------------------------------------
    def run_test(self, test_id: str) -> Optional[TestResult]:
        """Run a single registered test."""
        if test_id not in self.registered_tests:
            return None
        test = self.registered_tests[test_id]

        if not self._check_dependencies(test):
            result = TestResult(
                test_id=test_id,
                status=TestStatus.SKIPPED,
                message="Dependencies not met",
            )
            self._store_result(result)
            return result

        result = test.run()
        self._store_result(result)
        self._trigger_callbacks(test_id, result)
        return result

    def _check_dependencies(self, test: BaseTest) -> bool:
        """Check if test dependencies are met."""
        for dep_id in test.dependencies:
            dep_result = self._get_latest_result(dep_id)
            if not dep_result or dep_result.status != TestStatus.PASSED:
                return False
        return True

    # Result management --------------------------------------------------
    def _store_result(self, result: TestResult) -> None:
        """Store a test result in history."""
        with self.execution_lock:
            self.results_history.append(result)

    def _get_latest_result(self, test_id: str) -> Optional[TestResult]:
        """Get the latest result for the given test ID."""
        for result in reversed(self.results_history):
            if result.test_id == test_id:
                return result
        return None

    def get_test_result(self, test_id: str) -> Optional[TestResult]:
        """Public wrapper for :func:`_get_latest_result`."""
        return self._get_latest_result(test_id)

    def get_all_results(self) -> List[TestResult]:
        """Return a copy of all stored results."""
        return self.results_history.copy()

    def clear_results(self) -> None:
        """Clear stored results."""
        self.results_history.clear()

    # Callbacks ----------------------------------------------------------
    def add_execution_callback(
        self, test_id: str, callback: Callable[[TestResult], None]
    ) -> None:
        """Register a callback to be invoked when a test completes."""
        self.test_execution_callbacks.setdefault(test_id, []).append(callback)

    def remove_execution_callback(
        self, test_id: str, callback: Callable[[TestResult], None]
    ) -> None:
        """Remove a previously registered callback."""
        callbacks = self.test_execution_callbacks.get(test_id)
        if callbacks and callback in callbacks:
            callbacks.remove(callback)

    def _trigger_callbacks(self, test_id: str, result: TestResult) -> None:
        """Invoke callbacks registered for a given test."""
        for callback in self.test_execution_callbacks.get(test_id, []):
            try:  # pragma: no cover - callbacks should not break execution
                callback(result)
            except Exception:
                pass


class TestExecutor:
    """High level interface for running tests sequentially or in parallel."""

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
        self.test_runner = TestRunner()
        self.execution_queue: List[BaseTest] = []

    # Queue management ---------------------------------------------------
    def add_test_to_queue(self, test: BaseTest) -> None:
        """Add a test to the execution queue."""
        self.execution_queue.append(test)
        self.test_runner.register_test(test)

    def add_tests_to_queue(self, tests: List[BaseTest]) -> None:
        """Add multiple tests to the execution queue."""
        for test in tests:
            self.add_test_to_queue(test)

    # Execution ----------------------------------------------------------
    def execute_queue(self) -> List[TestResult]:
        """Execute all queued tests sequentially."""
        results = [self.test_runner.run_test(t.test_id) for t in self.execution_queue]
        self.execution_queue.clear()
        return [r for r in results if r]

    def execute_parallel(self, tests: List[BaseTest]) -> List[TestResult]:
        """Execute tests in parallel using threads."""
        if not tests:
            return []
        result_queue: "queue.Queue[TestResult]" = queue.Queue()

        def _worker(test: BaseTest) -> None:
            result = self.test_runner.run_test(test.test_id)
            if result:
                result_queue.put(result)

        threads: List[threading.Thread] = []
        for test in tests:
            thread = threading.Thread(target=_worker, args=(test,))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        results: List[TestResult] = []
        while not result_queue.empty():
            results.append(result_queue.get())
        return results

    def clear_results(self) -> None:
        """Clear stored results in the underlying runner."""
        self.test_runner.clear_results()
