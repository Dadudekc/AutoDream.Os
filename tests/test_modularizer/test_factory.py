"""
🧪 REGRESSION TESTING SYSTEM - Test Factory
Extracted from regression_testing_system.py for modularization

This module provides utilities for creating different types of test suites.
"""

from typing import List, Callable
from .models import RegressionTestSuite


class TestSuiteFactory:
    """Factory for creating different types of test suites."""
    
    @staticmethod
    def create_functionality_test_suite(name: str, tests: List[Callable], 
                                      description: str = "") -> RegressionTestSuite:
        """Create a functionality test suite."""
        return RegressionTestSuite(
            name=name,
            description=description or f"Functionality tests for {name}",
            tests=tests,
            category="functionality",
            priority="high",
            timeout=30.0
        )
    
    @staticmethod
    def create_performance_test_suite(name: str, tests: List[Callable], 
                                    description: str = "") -> RegressionTestSuite:
        """Create a performance test suite."""
        return RegressionTestSuite(
            name=name,
            description=description or f"Performance tests for {name}",
            tests=tests,
            category="performance",
            priority="medium",
            timeout=60.0
        )
    
    @staticmethod
    def create_integration_test_suite(name: str, tests: List[Callable], 
                                    description: str = "") -> RegressionTestSuite:
        """Create an integration test suite."""
        return RegressionTestSuite(
            name=name,
            description=description or f"Integration tests for {name}",
            tests=tests,
            category="integration",
            priority="high",
            timeout=45.0
        )
    
    @staticmethod
    def create_regression_test_suite(name: str, tests: List[Callable], 
                                   description: str = "") -> RegressionTestSuite:
        """Create a regression test suite."""
        return RegressionTestSuite(
            name=name,
            description=description or f"Regression tests for {name}",
            tests=tests,
            category="regression",
            priority="critical",
            timeout=90.0
        )
    
    @staticmethod
    def create_custom_test_suite(name: str, tests: List[Callable], 
                               description: str = "", category: str = "custom",
                               priority: str = "medium", timeout: float = 30.0) -> RegressionTestSuite:
        """Create a custom test suite with specified parameters."""
        return RegressionTestSuite(
            name=name,
            description=description or f"Custom tests for {name}",
            tests=tests,
            category=category,
            priority=priority,
            timeout=timeout
        )
