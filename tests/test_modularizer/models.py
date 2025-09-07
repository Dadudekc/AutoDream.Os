"""
🧪 REGRESSION TESTING SYSTEM - Data Models
Extracted from regression_testing_system.py for modularization

This module contains the core data structures used by the regression testing system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Callable, Optional


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


@dataclass
class RegressionTestResult:
    """Result of a regression test execution."""
    test_name: str
    status: TestStatus
    execution_time: float
    output: str
    error_message: Optional[str] = None
    before_output: Optional[str] = None
    after_output: Optional[str] = None
    comparison_result: Optional[dict] = None


@dataclass
class RegressionTestSuite:
    """A suite of regression tests."""
    name: str
    description: str
    tests: List[Callable]
    timeout: float = 30.0
    category: str = "general"
    priority: str = "medium"
