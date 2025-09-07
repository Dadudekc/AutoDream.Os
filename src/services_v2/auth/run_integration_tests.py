from datetime import datetime
from pathlib import Path
import sys

from auth_integration_test_execution import run_comprehensive_integration_suite
from auth_integration_test_reporting import generate_test_report, save_test_report
from auth_integration_test_setup import setup_logging
import time

#!/usr/bin/env python3
"""
V2 Authentication Integration Test Runner
========================================

Orchestrates setup, execution, and reporting for the V2 authentication
integration tests.
"""


# Add src to path for imports
sys.path.append(str(Path(__file__).resolve().parents[3]))



def main():
    """Main integration test runner."""
    logger = setup_logging()

    logger.info("=" * 80)
    logger.info("🚀 V2 AUTHENTICATION INTEGRATION TEST SUITE")
    logger.info("=" * 80)
    logger.info(f"Started at: {datetime.now()}")
    logger.info("Agent-2: AI & ML Integration Specialist")
    logger.info("Task: Begin integration tests for services_v2/auth. Report in 60m.")
    logger.info("=" * 80)

    start_time = time.time()
    test_results = run_comprehensive_integration_suite(logger)
    total_time = time.time() - start_time

    logger.info("\n" + "=" * 80)
    logger.info("🏁 INTEGRATION TEST SUITE COMPLETED")
    logger.info("=" * 80)
    logger.info(f"Total Tests: {test_results['tests_run']}")
    logger.info(f"Passed: {test_results['tests_passed']}")
    logger.info(f"Failed: {test_results['tests_failed']}")
    logger.info(f"Errors: {test_results.get('tests_error', 0)}")
    logger.info(f"Total Time: {total_time:.2f}s")

    if test_results["tests_run"] > 0:
        success_rate = (
            test_results["tests_passed"] / test_results["tests_run"]
        ) * 100
        logger.info(f"Success Rate: {success_rate:.1f}%")

    report = generate_test_report(test_results, logger)
    save_test_report(report, logger)

    if report["status"] == "PASS":
        logger.info("🎉 ALL TESTS PASSED - System ready for production!")
    else:
        logger.warning("⚠️ Some tests failed - Review recommendations")

    logger.info("=" * 80)
    return report


if __name__ == "__main__":
    main()
