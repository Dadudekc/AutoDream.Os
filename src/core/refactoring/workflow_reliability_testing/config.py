
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration models for workflow reliability testing."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .utils import DEFAULT_TIMEOUT, DEFAULT_RETRY_COUNT


class TestType(Enum):
    """Types of reliability tests."""

    FUNCTIONAL = "functional"
    STRESS = "stress"
    LOAD = "load"
    FAILURE_MODE = "failure_mode"
    RECOVERY = "recovery"
    CONSISTENCY = "consistency"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"


class TestResult(Enum):
    """Possible outcomes for reliability tests."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class ReliabilityTest:
    """Definition of a single reliability test."""

    test_id: str
    name: str
    description: str
    test_type: TestType
    test_func: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeout: float = DEFAULT_TIMEOUT
    retry_count: int = DEFAULT_RETRY_COUNT
    weight: float = 1.0
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TestExecutionResult:
    """Result of an executed test."""

    test_id: str
    test_name: str
    test_type: TestType
    result: TestResult
    execution_time: float = 0.0
    retry_count: int = 0
    error_message: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    reliability_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReliabilityTestSuite:
    """Aggregated results for a collection of reliability tests."""

    suite_id: str
    name: str
    description: str
    tests: List[ReliabilityTest]
    start_time: datetime
    end_time: Optional[datetime] = None
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    warning_tests: int = 0
    error_tests: int = 0
    timeout_tests: int = 0
    overall_reliability: float = 0.0
    performance_score: float = 0.0
    stability_score: float = 0.0
    test_results: List[TestExecutionResult] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
