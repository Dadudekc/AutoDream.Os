"""
ML Validation Framework - V2 Compliant Core
===========================================

Core validation functionality refactored for V2 compliance.
Advanced operations moved to separate modules.

Author: Agent-5 (Coordinator)
License: MIT
"""

import json
import logging
import os
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ValidationStatus(Enum):
    """Enumeration for validation status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


class TestType(Enum):
    """Enumeration for test types."""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    DATA_QUALITY = "data_quality"


@dataclass
class ValidationResult:
    """Data class for validation results."""
    test_name: str
    test_type: TestType
    status: ValidationStatus
    message: str
    timestamp: datetime
    duration: float
    metrics: dict[str, Any] | None = None
    model_name: str | None = None
    version: str | None = None


@dataclass
class TestSuite:
    """Data class for test suite information."""
    suite_name: str
    description: str
    tests: list[Callable]
    timeout: float = 300.0
    retry_count: int = 0


class ValidationFrameworkCore:
    """
    Core ML validation framework functionality.
    Provides basic validation operations and result management.
    """

    def __init__(self, results_path: str = "/app/validation_results"):
        """Initialize the validation framework core."""
        self.results_path = results_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure results directory exists
        os.makedirs(self.results_path, exist_ok=True)

    def run_test(self, test_func: Callable, test_name: str, 
                test_type: TestType, model_name: str = None, 
                version: str = None) -> ValidationResult:
        """Run a single test and return validation result."""
        start_time = datetime.now()
        
        try:
            # Run the test
            result = test_func()
            
            # Determine status based on result
            if isinstance(result, bool):
                status = ValidationStatus.PASSED if result else ValidationStatus.FAILED
                message = f"Test {test_name} {'passed' if result else 'failed'}"
            elif isinstance(result, dict):
                status = ValidationStatus.PASSED if result.get('passed', False) else ValidationStatus.FAILED
                message = result.get('message', f"Test {test_name} completed")
            else:
                status = ValidationStatus.PASSED
                message = f"Test {test_name} completed successfully"
            
            duration = (datetime.now() - start_time).total_seconds()
            
            validation_result = ValidationResult(
                test_name=test_name,
                test_type=test_type,
                status=status,
                message=message,
                timestamp=start_time,
                duration=duration,
                model_name=model_name,
                version=version
            )
            
            self.logger.info(f"Test {test_name} completed with status {status.value}")
            return validation_result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Test {test_name} failed with exception: {e}")
            
            return ValidationResult(
                test_name=test_name,
                test_type=test_type,
                status=ValidationStatus.FAILED,
                message=f"Test failed with exception: {str(e)}",
                timestamp=start_time,
                duration=duration,
                model_name=model_name,
                version=version
            )

    def run_test_suite(self, test_suite: TestSuite, model_name: str = None, 
                      version: str = None) -> list[ValidationResult]:
        """Run a complete test suite."""
        results = []
        
        self.logger.info(f"Running test suite: {test_suite.suite_name}")
        
        for i, test_func in enumerate(test_suite.tests):
            test_name = f"{test_suite.suite_name}_test_{i+1}"
            
            # Run test with retries if configured
            for attempt in range(test_suite.retry_count + 1):
                result = self.run_test(test_func, test_name, TestType.UNIT, model_name, version)
                results.append(result)
                
                # If test passed or no more retries, break
                if result.status == ValidationStatus.PASSED or attempt == test_suite.retry_count:
                    break
                
                self.logger.warning(f"Test {test_name} failed, retrying (attempt {attempt + 1})")
        
        return results

    def save_results(self, results: list[ValidationResult], filename: str = None) -> str:
        """Save validation results to file."""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"validation_results_{timestamp}.json"
            
            file_path = os.path.join(self.results_path, filename)
            
            # Convert results to serializable format
            serializable_results = []
            for result in results:
                data = asdict(result)
                data['timestamp'] = result.timestamp.isoformat()
                data['test_type'] = result.test_type.value
                data['status'] = result.status.value
                serializable_results.append(data)
            
            with open(file_path, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            
            self.logger.info(f"Saved {len(results)} validation results to {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error saving validation results: {e}")
            raise

    def load_results(self, filename: str) -> list[ValidationResult]:
        """Load validation results from file."""
        try:
            file_path = os.path.join(self.results_path, filename)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            results = []
            for item in data:
                # Convert back to ValidationResult objects
                item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                item['test_type'] = TestType(item['test_type'])
                item['status'] = ValidationStatus(item['status'])
                results.append(ValidationResult(**item))
            
            self.logger.info(f"Loaded {len(results)} validation results from {file_path}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error loading validation results: {e}")
            raise

    def get_test_summary(self, results: list[ValidationResult]) -> dict[str, Any]:
        """Get summary statistics for test results."""
        total_tests = len(results)
        passed_tests = len([r for r in results if r.status == ValidationStatus.PASSED])
        failed_tests = len([r for r in results if r.status == ValidationStatus.FAILED])
        warning_tests = len([r for r in results if r.status == ValidationStatus.WARNING])
        skipped_tests = len([r for r in results if r.status == ValidationStatus.SKIPPED])
        
        total_duration = sum(r.duration for r in results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warning_tests,
            "skipped": skipped_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration
        }
