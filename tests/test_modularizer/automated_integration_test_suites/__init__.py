"""
🧪 AUTOMATED INTEGRATION TEST SUITES - V2-COMPLIANCE-008
Testing Framework Enhancement Manager - Agent-3

This module provides comprehensive automated integration test suites for all major
systems, providing automated testing, validation, and reporting capabilities.
"""

from .models import (
    TestSuiteCategory,
    TestExecutionMode,
    TestSuiteConfig,
    TestSuiteResult
)
from .executor import AutomatedIntegrationTestSuites
from .config import DEFAULT_TEST_SUITES

__all__ = [
    'TestSuiteCategory',
    'TestExecutionMode', 
    'TestSuiteConfig',
    'TestSuiteResult',
    'AutomatedIntegrationTestSuites',
    'DEFAULT_TEST_SUITES',
    'run_test_suite',
    'run_all_test_suites',
    'run_category_suites'
]


# Convenience functions for easy usage
def run_test_suite(suite_id: str):
    """Run a specific test suite."""
    test_suites = AutomatedIntegrationTestSuites()
    return test_suites.run_test_suite(suite_id)


def run_all_test_suites(parallel: bool = True):
    """Run all test suites."""
    test_suites = AutomatedIntegrationTestSuites()
    return test_suites.run_all_test_suites(parallel=parallel)


def run_category_suites(category, parallel: bool = True):
    """Run test suites for a specific category."""
    test_suites = AutomatedIntegrationTestSuites()
    
    # Get suites for the category
    category_suites = [
        suite_id for suite_id, config in test_suites.test_suites.items()
        if config.category == category
    ]
    
    return test_suites.run_all_test_suites(category_suites, parallel=parallel)
