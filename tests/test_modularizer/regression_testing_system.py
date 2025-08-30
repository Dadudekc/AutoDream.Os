"""
🧪 REGRESSION TESTING SYSTEM - MODULARIZED VERSION
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive regression testing for modularized components
and ensures quality assurance during the monolithic file modularization mission.

MODULARIZED: Reduced from 823 lines to <400 lines while preserving ALL functionality.
"""

import os
import sys
import pytest
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import from modularized components
from .models import TestStatus, RegressionTestResult, RegressionTestSuite
from .test_executor import TestExecutor
from .test_suite_manager import TestSuiteManager
from .test_factory import TestSuiteFactory
from .test_analyzer import TestAnalyzer


class RegressionTestingSystem:
    """
    Comprehensive regression testing system for modularized components.
    
    This system provides:
    - Automated regression test execution
    - Before/after comparison testing
    - Functionality preservation validation
    - Performance regression detection
    - Integration test regression checking
    - Test result analysis and reporting
    """
    
    def __init__(self):
        self.test_executor = TestExecutor()
        self.test_suite_manager = TestSuiteManager(self.test_executor)
        self.test_analyzer = TestAnalyzer()
        self.timeout_default = 30.0
        
    def register_test_suite(self, test_suite: RegressionTestSuite) -> bool:
        """Register a test suite for regression testing."""
        return self.test_suite_manager.register_test_suite(test_suite)
    
    def run_test_suite(self, suite_name: str, comparison_mode: bool = False) -> Dict[str, Any]:
        """Run a complete test suite."""
        return self.test_suite_manager.run_test_suite(suite_name, comparison_mode)
    
    def run_single_test(self, test_func: Callable, timeout: float = None) -> RegressionTestResult:
        """Run a single regression test."""
        return self.test_executor.run_single_test(test_func, timeout, False)
    
    def get_test_results(self, suite_name: str = None) -> Dict[str, Any]:
        """Get test results for a specific suite or all suites."""
        return self.test_suite_manager.get_test_results(suite_name)
    
    def get_execution_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get execution history with optional limit."""
        return self.test_suite_manager.get_execution_history(limit)
    
    def clear_test_results(self, suite_name: str = None) -> bool:
        """Clear test results for a specific suite or all suites."""
        return self.test_suite_manager.clear_test_results(suite_name)
    
    def assess_regression_compliance(self, suite_name: str) -> Dict[str, Any]:
        """Assess regression compliance for a test suite."""
        test_results = self.get_test_results(suite_name)
        return self.test_analyzer.assess_regression_compliance(test_results)
    
    def generate_test_summary(self, suite_name: str) -> Dict[str, Any]:
        """Generate a summary of test execution results."""
        test_results = self.get_test_results(suite_name)
        return self.test_analyzer.generate_test_summary(test_results)
    
    def analyze_test_trends(self) -> Dict[str, Any]:
        """Analyze trends in test execution over time."""
        execution_history = self.get_execution_history()
        return self.test_analyzer.analyze_test_trends(execution_history)
    
    # Test suite creation methods using factory
    def create_functionality_test_suite(self, name: str, tests: List[Callable], 
                                      description: str = "") -> RegressionTestSuite:
        """Create a functionality test suite."""
        return TestSuiteFactory.create_functionality_test_suite(name, tests, description)
    
    def create_performance_test_suite(self, name: str, tests: List[Callable], 
                                    description: str = "") -> RegressionTestSuite:
        """Create a performance test suite."""
        return TestSuiteFactory.create_performance_test_suite(name, tests, description)
    
    def create_integration_test_suite(self, name: str, tests: List[Callable], 
                                    description: str = "") -> RegressionTestSuite:
        """Create an integration test suite."""
        return TestSuiteFactory.create_integration_test_suite(name, tests, description)
    
    def create_regression_test_suite(self, name: str, tests: List[Callable], 
                                   description: str = "") -> RegressionTestSuite:
        """Create a regression test suite."""
        return TestSuiteFactory.create_regression_test_suite(name, tests, description)
    
    def create_custom_test_suite(self, name: str, tests: List[Callable], 
                               description: str = "", category: str = "custom",
                               priority: str = "medium", timeout: float = 30.0) -> RegressionTestSuite:
        """Create a custom test suite with specified parameters."""
        return TestSuiteFactory.create_custom_test_suite(name, tests, description, category, priority, timeout)
    
    # Convenience methods for backward compatibility
    @property
    def test_suites(self):
        """Get registered test suites."""
        return self.test_suite_manager.test_suites
    
    @property
    def test_results(self):
        """Get test results."""
        return self.test_suite_manager.test_results
    
    @property
    def execution_history(self):
        """Get execution history."""
        return self.test_suite_manager.execution_history


# Test fixtures for pytest
@pytest.fixture
def regression_system():
    """Fixture providing a regression testing system instance."""
    return RegressionTestingSystem()


@pytest.fixture
def sample_test_functions():
    """Fixture providing sample test functions."""
    def test_function_1():
        return "test_result_1"
    
    def test_function_2():
        return "test_result_2"
    
    def test_function_3():
        return "test_result_3"
    
    def test_function_4():
        return "test_result_4"
    
    def test_function_5():
        return "test_result_5"
    
    return [test_function_1, test_function_2, test_function_3, test_function_4, test_function_5]


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])

