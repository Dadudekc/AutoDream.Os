"""
Phase 4 Testing Coordination Models
V2 Compliant data models for testing coordination system
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TestingPhase(Enum):
    """Testing phases for Phase 4 validation"""
    UNIT_TESTING = "unit_testing"
    INTEGRATION_TESTING = "integration_testing"
    SYSTEM_TESTING = "system_testing"
    ACCEPTANCE_TESTING = "acceptance_testing"
    PERFORMANCE_TESTING = "performance_testing"
    COMPATIBILITY_TESTING = "compatibility_testing"


class TestPriority(Enum):
    """Test priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TestCase:
    """Individual test case definition"""
    test_id: str
    name: str
    description: str
    testing_phase: TestingPhase
    priority: TestPriority
    expected_result: str
    test_data: dict[str, Any]
    dependencies: list[str]


@dataclass
class TestSuite:
    """Test suite definition"""
    suite_id: str
    name: str
    description: str
    testing_phase: TestingPhase
    test_cases: list[TestCase]
    prerequisites: list[str]
    timeout: int


@dataclass
class TestExecution:
    """Test execution tracking"""
    execution_id: str
    test_case: TestCase
    status: TestStatus
    start_time: str
    end_time: str
    duration: float
    result: str
    error_message: str
    agent_id: str


@dataclass
class TestingReport:
    """Testing coordination report"""
    report_id: str
    phase: TestingPhase
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    execution_time: float
    coverage_percentage: float
    recommendations: list[str]
