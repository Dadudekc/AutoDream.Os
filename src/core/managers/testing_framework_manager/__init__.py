#!/usr/bin/env python3
"""Testing framework manager package providing orchestration, results, and configuration modules."""

from .test_orchestration import TestingFrameworkManager
from .result_aggregation import TestExecutionResult, TestSuiteResult
from .configuration import TestConfiguration

__all__ = [
    "TestingFrameworkManager",
    "TestExecutionResult",
    "TestSuiteResult",
    "TestConfiguration",
]
