#!/usr/bin/env python3
"""Utility functions for handling test results."""

from __future__ import annotations

import time
from typing import Any

from .testing_types import TestResult


def create_test_result(test: Any, duration: float) -> TestResult:
    """Create a :class:`TestResult` from a finished test instance."""
    return TestResult(
        test_id=f"{test.__class__.__name__}_{int(time.time())}",
        test_name=test.test_name,
        test_type=test.test_type,
        status=test.status,
        start_time=test.start_time or 0,
        end_time=test.end_time or 0,
        duration=duration if test.start_time and test.end_time else 0,
        error_message=getattr(test, "error_message", None),
        error_traceback=getattr(test, "error_traceback", None),
        metrics=getattr(test, "metrics", {}),
        logs=getattr(test, "logs", []),
        assertions_passed=getattr(test, "assertions_passed", 0),
        assertions_failed=getattr(test, "assertions_failed", 0),
        test_data=getattr(test, "test_data", {}),
    )
