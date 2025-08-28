"""Common automation orchestration utilities."""

import unittest
from typing import Dict, Type


def execute_test_suite(
    suite_class: Type[unittest.TestCase], verbosity: int = 1
) -> Dict[str, float]:
    """Run a unittest TestCase and return summary metrics.

    Args:
        suite_class: TestCase class to execute.
        verbosity: Verbosity level for TextTestRunner.

    Returns:
        Dictionary with total tests, failures, errors, and success rate.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    failures = len(result.failures)
    errors = len(result.errors)
    total = result.testsRun
    success = ((total - failures - errors) / total * 100) if total > 0 else 0
    return {
        "total_tests": total,
        "failures": failures,
        "errors": errors,
        "success_rate": success,
    }
