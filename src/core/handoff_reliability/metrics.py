from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TestType(Enum):
    """Reliability test types."""

    RELIABILITY = "reliability"
    PERFORMANCE = "performance"
    STRESS = "stress"
    FAILURE_INJECTION = "failure_injection"
    CONCURRENCY = "concurrency"
    ENDURANCE = "endurance"


class TestStatus(Enum):
    """Test status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class TestConfiguration:
    """Configuration for reliability tests."""

    test_id: str
    test_type: TestType
    procedure_id: str
    iterations: int = 100
    timeout: float = 30.0
    concurrent_limit: int = 10
    failure_rate: float = 0.0  # 0.0 = no failures, 1.0 = 100% failures
    stress_factor: float = 1.0  # 1.0 = normal load, >1.0 = increased load
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    """Result of a reliability test."""

    test_id: str
    test_type: TestType
    procedure_id: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    iterations: int = 0
    successful_iterations: int = 0
    failed_iterations: int = 0
    timeout_iterations: int = 0
    total_duration: float = 0.0
    average_duration: float = 0.0
    min_duration: float = 0.0
    max_duration: float = 0.0
    p95_duration: float = 0.0
    p99_duration: float = 0.0
    success_rate: float = 0.0
    throughput: float = 0.0
    error_details: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class TestSession:
    """Tracks a reliability test session."""

    session_id: str
    test_config: TestConfiguration
    start_time: float
    end_time: Optional[float] = None
    status: TestStatus = TestStatus.PENDING
    current_iteration: int = 0
    results: List[TestResult] = field(default_factory=list)
    active_tests: List[str] = field(default_factory=list)
    error_details: Optional[str] = None


def update_reliability_metrics(metrics: Dict[str, Any], test_result: TestResult) -> None:
    """Update reliability performance metrics."""

    metrics["total_tests"] += 1

    if test_result.error_details:
        metrics["failed_tests"] += 1
    else:
        metrics["successful_tests"] += 1

    metrics["total_iterations"] += test_result.iterations
    metrics["successful_iterations"] += test_result.successful_iterations
    metrics["failed_iterations"] += test_result.failed_iterations

    if metrics["total_tests"] > 0:
        metrics["average_success_rate"] = (
            metrics["successful_iterations"] / metrics["total_iterations"]
            if metrics["total_iterations"] > 0
            else 0.0
        )
        metrics["average_duration"] = (
            test_result.duration / metrics["total_tests"] if test_result.duration else 0.0
        )

    test_type = test_result.test_type.value
    if test_type not in metrics["test_type_performance"]:
        metrics["test_type_performance"][test_type] = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "average_success_rate": 0.0,
            "average_duration": 0.0,
        }

    type_metrics = metrics["test_type_performance"][test_type]
    type_metrics["total"] += 1

    if test_result.error_details:
        type_metrics["failed"] += 1
    else:
        type_metrics["successful"] += 1

    if type_metrics["total"] > 0:
        type_metrics["average_success_rate"] = (
            type_metrics["successful"] / type_metrics["total"]
        )
        type_metrics["average_duration"] = (
            (
                type_metrics["average_duration"] * (type_metrics["total"] - 1)
                + (test_result.duration or 0.0)
            )
            / type_metrics["total"]
        )
