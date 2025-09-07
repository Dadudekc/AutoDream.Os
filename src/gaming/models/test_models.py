#!/usr/bin/env python3
"""
Test Models - Gaming Test Runner
==============================

Test models and enums for the gaming test runner system.

Author: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Any


class TestStatus(Enum):
    """Status of test execution."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestType(Enum):
    """Types of tests for gaming systems."""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    STRESS = "stress"
    COMPATIBILITY = "compatibility"
    USER_ACCEPTANCE = "user_acceptance"


@dataclass
class TestResult:
    """Represents the result of a test execution."""
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[float]
    error_message: Optional[str]
    performance_metrics: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class TestSuite:
    """Represents a collection of related tests."""
    suite_id: str
    suite_name: str
    description: str
    tests: List[str]
    dependencies: List[str]
    timeout: int
    metadata: Dict[str, Any]
