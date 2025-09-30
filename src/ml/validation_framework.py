"""
ML Validation Framework - V2 Compliant Main Interface
=====================================================

Main validation framework interface using refactored core components.
Maintains backward compatibility while using V2 compliant modules.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
from collections.abc import Callable
from typing import Any, List

from .validation_framework_core import (
    ValidationFrameworkCore, 
    ValidationResult, 
    TestSuite, 
    ValidationStatus, 
    TestType
)


class ValidationFramework:
    """
    Main ML validation framework interface.
    Provides backward compatibility while using refactored core components.
    """

    def __init__(self, results_path: str = "/app/validation_results"):
        """Initialize the validation framework."""
        self.core = ValidationFrameworkCore(results_path)
        self.logger = logging.getLogger(__name__)

    def run_test(self, test_func: Callable, test_name: str, 
                test_type: TestType, model_name: str = None, 
                version: str = None) -> ValidationResult:
        """Run a single test and return validation result."""
        return self.core.run_test(test_func, test_name, test_type, model_name, version)

    def run_test_suite(self, test_suite: TestSuite, model_name: str = None, 
                      version: str = None) -> List[ValidationResult]:
        """Run a complete test suite."""
        return self.core.run_test_suite(test_suite, model_name, version)

    def save_results(self, results: List[ValidationResult], filename: str = None) -> str:
        """Save validation results to file."""
        return self.core.save_results(results, filename)

    def load_results(self, filename: str) -> List[ValidationResult]:
        """Load validation results from file."""
        return self.core.load_results(filename)

    def get_test_summary(self, results: List[ValidationResult]) -> dict[str, Any]:
        """Get summary statistics for test results."""
        return self.core.get_test_summary(results)