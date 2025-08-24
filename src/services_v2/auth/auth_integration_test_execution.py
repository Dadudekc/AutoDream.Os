#!/usr/bin/env python3
"""Execution helpers for authentication integration tests."""

import time
import logging

try:  # Attempt to import integration components
    from auth_service import AuthService
    from auth_integration_tester import AuthIntegrationTester
    INTEGRATION_AVAILABLE = True
except ImportError as e:  # pragma: no cover - import check
    print(f"Warning: Integration components not available: {e}")
    INTEGRATION_AVAILABLE = False

from auth_integration_test_validation import (
    run_basic_functionality_tests,
    run_performance_tests,
    run_integration_tests,
)


def run_basic_tests_only(logger: logging.Logger) -> dict:
    """Run basic tests when integration components are not available."""
    logger.info("🔧 Running Basic Tests Only")
    logger.info("-" * 40)

    try:
        # Initialize basic auth service
        auth_service = AuthService()

        # Run basic functionality tests
        basic_results = run_basic_functionality_tests(auth_service, logger)

        # Run performance tests
        perf_results = run_performance_tests(auth_service, logger)

        # Run integration tests
        integration_results = run_integration_tests(auth_service, logger)

        # Combine results
        total_tests = (
            basic_results["tests_run"]
            + perf_results["tests_run"]
            + integration_results["tests_run"]
        )
        total_passed = (
            basic_results["tests_passed"]
            + perf_results["tests_passed"]
            + integration_results["tests_passed"]
        )
        total_failed = (
            basic_results["tests_failed"]
            + perf_results["tests_failed"]
            + integration_results["tests_failed"]
        )

        combined_results = {
            "tests_run": total_tests,
            "tests_passed": total_passed,
            "tests_failed": total_failed,
            "tests_error": 0,
            "total_time": 0,
            "integration_status": {"basic_mode": True, "integration_components": False},
            "performance_metrics": {},
            "test_details": (
                basic_results["test_details"]
                + perf_results["test_details"]
                + integration_results["test_details"]
            ),
        }

        # Cleanup
        auth_service.shutdown()

        return combined_results

    except Exception as e:  # pragma: no cover - logging
        logger.error(f"❌ Basic tests failed: {e}")
        return {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 1,
            "tests_error": 0,
            "total_time": 0,
            "integration_status": {"error": str(e)},
            "performance_metrics": {},
            "test_details": [
                {
                    "test": "Basic Tests",
                    "status": "ERROR",
                    "duration": 0,
                    "details": str(e),
                }
            ],
        }


def run_comprehensive_integration_suite(logger: logging.Logger) -> dict:
    """Run the comprehensive integration test suite."""
    logger.info("🚀 Running Comprehensive Integration Test Suite")
    logger.info("=" * 60)

    if not INTEGRATION_AVAILABLE:
        logger.warning(
            "⚠️ Integration components not available, running basic tests only"
        )
        return run_basic_tests_only(logger)

    try:
        # Initialize integration tester
        integration_tester = AuthIntegrationTester()

        # Run tests via new orchestrator
        start_time = time.time()
        report = integration_tester.run()
        total_time = time.time() - start_time

        test_results = {
            "tests_run": report.summary["total"],
            "tests_passed": report.summary["passed"],
            "tests_failed": report.summary["failed"],
            "tests_error": 0,
            "total_time": total_time,
            "integration_status": {},
            "performance_metrics": {},
            "test_details": [
                {
                    "test": r.name,
                    "status": "PASS" if r.passed else "FAIL",
                    "duration": r.duration,
                    "details": r.details,
                }
                for r in report.results
            ],
        }

        return test_results

    except Exception as e:  # pragma: no cover - logging
        logger.error(f"❌ Comprehensive integration suite failed: {e}")
        return {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 1,
            "tests_error": 0,
            "total_time": 0,
            "integration_status": {"error": str(e)},
            "performance_metrics": {},
            "test_details": [
                {
                    "test": "Comprehensive Integration Suite",
                    "status": "ERROR",
                    "duration": 0,
                    "details": str(e),
                }
            ],
        }
