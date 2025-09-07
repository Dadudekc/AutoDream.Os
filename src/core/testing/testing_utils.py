"""Shared utilities for the testing framework.

Provides core enums, dataclasses and base classes that are used across
all testing modules. Having these definitions in a single module
maintains a clear single source of truth (SSOT) for the framework.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TestStatus(Enum):
    """Execution status for a test case."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TestType(Enum):
    """Categories of tests supported by the framework."""

    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    SMOKE = "smoke"


class TestPriority(Enum):
    """Priority levels for scheduling tests."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TestEnvironment(Enum):
    """Execution environments for tests."""

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI_CD = "ci_cd"


@dataclass
class TestResult:
    """Outcome of a single test execution."""

    test_id: str
    status: TestStatus
    message: str = ""
    execution_time: float = 0.0
    timestamp: float = field(default_factory=time.time)
    details: Dict[str, Any] = field(default_factory=dict)
    error_traceback: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class BaseTest:
    """Base class for all tests in the framework."""

    test_name: str
    test_type: TestType = TestType.UNIT
    priority: TestPriority = TestPriority.NORMAL
    timeout: float = 30.0
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    enabled: bool = True

    def __post_init__(self) -> None:
        self.test_id = str(uuid.uuid4())

    def add_dependency(self, dependency: str) -> None:
        """Record a test dependency."""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    # Core execution -----------------------------------------------------
    def run(self) -> TestResult:
        """Execute the test and return a :class:`TestResult`."""
        start_time = time.time()
        try:
            passed = self.test_logic()
            status = TestStatus.PASSED if passed else TestStatus.FAILED
            message = "Test passed successfully" if passed else "Test assertion failed"
        except Exception as exc:  # pragma: no cover - defensive
            status = TestStatus.ERROR
            message = f"Test execution error: {exc}"
            return TestResult(
                test_id=self.test_id,
                status=status,
                message=message,
                execution_time=time.time() - start_time,
                error_traceback=str(exc),
            )

        return TestResult(
            test_id=self.test_id,
            status=status,
            message=message,
            execution_time=time.time() - start_time,
        )

    def test_logic(self) -> bool:  # pragma: no cover - must be overridden
        """Implement the test's logic. Should return ``True`` on success."""
        raise NotImplementedError


@dataclass
class BaseIntegrationTest(BaseTest):
    """Base test class with setup and teardown hooks."""

    def setup(self) -> None:  # pragma: no cover - to be overridden
        """Prepare the integration test environment."""

    def teardown(self) -> None:  # pragma: no cover - to be overridden
        """Clean up the integration test environment."""

    def run(self) -> TestResult:
        """Run the test with setup and teardown stages."""
        start_time = time.time()
        try:
            self.setup()
            passed = self.test_logic()
            status = TestStatus.PASSED if passed else TestStatus.FAILED
            message = "Test passed successfully" if passed else "Test assertion failed"
        except Exception as exc:  # pragma: no cover - defensive
            status = TestStatus.ERROR
            message = f"Test execution error: {exc}"
            return TestResult(
                test_id=self.test_id,
                status=status,
                message=message,
                execution_time=time.time() - start_time,
                error_traceback=str(exc),
            )
        finally:
            try:
                self.teardown()
            except Exception:
                pass

        return TestResult(
            test_id=self.test_id,
            status=status,
            message=message,
            execution_time=time.time() - start_time,
        )


@dataclass
class TestSuite:
    """Collection of related tests."""

    suite_id: str
    suite_name: str
    description: str = ""
    test_ids: List[str] = field(default_factory=list)
    test_types: List[TestType] = field(default_factory=list)
    priority: TestPriority = TestPriority.NORMAL
    environment: TestEnvironment = TestEnvironment.LOCAL

    def add_test(self, test_id: str) -> None:
        """Add a test to the suite."""
        if test_id not in self.test_ids:
            self.test_ids.append(test_id)

    def remove_test(self, test_id: str) -> bool:
        """Remove a test from the suite."""
        if test_id in self.test_ids:
            self.test_ids.remove(test_id)
            return True
        return False


@dataclass
class TestReport:
    """Aggregated report for a test execution."""

    report_id: str
    execution_id: str
    start_time: datetime
    end_time: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    total_execution_time: float
    test_results: List[TestResult] = field(default_factory=list)
    test_suites: List[TestSuite] = field(default_factory=list)
    environment: TestEnvironment = TestEnvironment.LOCAL

    @property
    def success_rate(self) -> float:
        """Percentage of tests that passed."""
        return (self.passed_tests / self.total_tests * 100) if self.total_tests else 0.0
