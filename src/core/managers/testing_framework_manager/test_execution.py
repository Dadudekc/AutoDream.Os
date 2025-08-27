#!/usr/bin/env python3
"""Test execution utilities for the testing framework manager."""

import logging
import time
import unittest
from typing import Any, Dict, List, Type

from .result_aggregation import TestExecutionResult, TestSuiteResult

logger = logging.getLogger(__name__)


class TestExecutionMixin:
    """Mixin providing test suite execution and orchestration."""

    def run_test_suite(
        self, suite_name: str, test_classes: List[Type[unittest.TestCase]] = None
    ) -> TestSuiteResult:
        """Run a complete test suite."""
        try:
            start_time = time.time()
            if suite_name not in self._test_suites:
                if test_classes:
                    suite = unittest.TestSuite()
                    for test_class in test_classes:
                        suite.addTests(
                            unittest.TestLoader().loadTestsFromTestCase(test_class)
                        )
                    self._test_suites[suite_name] = suite
                else:
                    raise ValueError(
                        f"Test suite '{suite_name}' not found and no test classes provided"
                    )
            suite = self._test_suites[suite_name]
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            end_time = time.time()
            execution_time = end_time - start_time
            suite_result = TestSuiteResult(
                suite_name=suite_name,
                total_tests=result.testsRun,
                passed_tests=result.testsRun
                - len(result.failures)
                - len(result.errors),
                failed_tests=len(result.failures),
                error_tests=len(result.errors),
                skipped_tests=len(result.skipped) if hasattr(result, "skipped") else 0,
                execution_time=execution_time,
                start_time=start_time,
                end_time=end_time,
                test_results=[],
                metadata={"runner_type": "unittest.TextTestRunner"},
            )
            for test, traceback in result.failures:
                test_result = TestExecutionResult(
                    test_name=test._testMethodName,
                    test_class=test.__class__.__name__,
                    status="failed",
                    execution_time=0.0,
                    error_message=str(traceback),
                    metadata={"test_id": str(test)},
                )
                suite_result.test_results.append(test_result)
            for test, traceback in result.errors:
                test_result = TestExecutionResult(
                    test_name=test._testMethodName,
                    test_class=test.__class__.__name__,
                    status="error",
                    execution_time=0.0,
                    error_message=str(traceback),
                    metadata={"test_id": str(test)},
                )
                suite_result.test_results.append(test_result)
            self._test_results.append(suite_result)
            self._performance_metrics[suite_name].append(execution_time)
            logger.info(
                "Test suite '%s' executed: %d/%d passed",
                suite_name,
                suite_result.passed_tests,
                suite_result.total_tests,
            )
            return suite_result
        except Exception as e:
            logger.error(f"Failed to run test suite '{suite_name}': {e}")
            raise

    def run_tdd_tests(
        self, test_categories: List[str] = None
    ) -> Dict[str, TestSuiteResult]:
        """Run TDD tests organized by category."""
        try:
            if not test_categories:
                test_categories = ["unit", "integration", "smoke"]
            results: Dict[str, TestSuiteResult] = {}
            for category in test_categories:
                category_tests = self._find_tests_by_category(category)
                if category_tests:
                    suite_name = f"tdd_{category}_tests"
                    result = self.run_test_suite(suite_name, category_tests)
                    results[category] = result
            logger.info("TDD tests executed for categories: %s", list(results.keys()))
            return results
        except Exception as e:
            logger.error(f"Failed to run TDD tests: {e}")
            raise

    def run_smoke_tests(self) -> TestSuiteResult:
        """Run smoke tests for basic system validation."""
        try:
            smoke_tests = self._find_smoke_tests()
            if smoke_tests:
                return self.run_test_suite("smoke_tests", smoke_tests)
            logger.warning("No smoke tests found")
            return None
        except Exception as e:
            logger.error(f"Failed to run smoke tests: {e}")
            raise

    def orchestrate_test_execution(
        self, execution_plan: Dict[str, Any]
    ) -> Dict[str, TestSuiteResult]:
        """Orchestrate complex test execution based on a plan."""
        try:
            results: Dict[str, TestSuiteResult] = {}
            test_suites = execution_plan.get("test_suites", [])
            execution_order = execution_plan.get("execution_order", "sequential")
            parallel_suites = execution_plan.get("parallel_suites", [])
            if execution_order == "parallel" and parallel_suites:
                for suite_name in parallel_suites:
                    if suite_name in self._test_suites:
                        result = self.run_test_suite(suite_name)
                        results[suite_name] = result
            for suite_name in test_suites:
                if suite_name not in results and suite_name in self._test_suites:
                    result = self.run_test_suite(suite_name)
                    results[suite_name] = result
            logger.info(
                "Test orchestration completed: %d suites executed", len(results)
            )
            return results
        except Exception as e:
            logger.error(f"Failed to orchestrate test execution: {e}")
            raise

    def _find_tests_by_category(self, category: str) -> List[Type[unittest.TestCase]]:
        """Find test classes by category (placeholder)."""
        return []

    def _find_smoke_tests(self) -> List[Type[unittest.TestCase]]:
        """Find smoke test classes (placeholder)."""
        return []
