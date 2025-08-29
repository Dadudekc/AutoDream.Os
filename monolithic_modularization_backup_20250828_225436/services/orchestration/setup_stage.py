"""Setup stage utilities for test orchestration."""

from __future__ import annotations

from typing import Dict, Type
import unittest
from unittest.mock import Mock


def initialize_test_suites(
    suites: Dict[str, Type[unittest.TestCase]],
) -> Dict[str, Type[unittest.TestCase]]:
    """Filter and return available test suites.

    Suites provided as :class:`~unittest.mock.Mock` are considered unavailable
    and are excluded from the returned mapping.
    """
    return {name: cls for name, cls in suites.items() if cls is not Mock}


def initialize_metrics() -> Dict[str, float]:
    """Return base metrics dictionary for orchestration."""
    return {
        "total_tests": 0,
        "total_failures": 0,
        "total_errors": 0,
        "success_rate": 0.0,
        "services_tested": 0,
    }
