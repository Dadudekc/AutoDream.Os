#!/usr/bin/env python3
"""Result aggregation data structures for TestingFrameworkManager."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class TestExecutionResult:
    """Represents the result of a test execution."""

    test_name: str
    test_class: str
    status: str  # "passed", "failed", "error", "skipped"
    execution_time: float
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class TestSuiteResult:
    """Represents the result of a test suite execution."""

    suite_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    skipped_tests: int
    execution_time: float
    start_time: float
    end_time: float
    test_results: List[TestExecutionResult]
    metadata: Dict[str, Any] = None
