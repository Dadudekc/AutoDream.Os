"""Shared testing data models for frontend tests."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TestResult:
    """Result of a frontend test."""

    test_name: str
    test_type: str
    status: str  # 'passed', 'failed', 'skipped'
    duration: float
    error_message: Optional[str]
    component_tested: Optional[str]
    route_tested: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class TestSuite:
    """Collection of related tests."""

    name: str
    description: str
    tests: List[TestResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    total_duration: float
    created_at: datetime
