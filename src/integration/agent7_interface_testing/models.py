#!/usr/bin/env python3
"""
Agent-7 Interface Testing Models
===============================

Data models and enums for Agent-7 Repository Management Interface Testing
V2 Compliant: ≤400 lines, focused data structures
"""

from dataclasses import dataclass
from enum import Enum


class TestCategory(Enum):
    """Test category enumeration"""

    FUNCTIONALITY = "functionality"
    VSCODE_CUSTOMIZATION = "vscode_customization"
    CROSS_PLATFORM = "cross_platform"
    INTEGRATION = "integration"


class TestStatus(Enum):
    """Test status enumeration"""

    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"
    SKIPPED = "skipped"


@dataclass
class TestResult:
    """Test result structure"""

    test_id: str
    test_name: str
    category: TestCategory
    status: TestStatus
    score: float
    issues: list[str]
    recommendations: list[str]
    execution_time: float


@dataclass
class InterfaceAnalysis:
    """Interface analysis structure"""

    interface_name: str
    component_count: int
    method_count: int
    complexity_score: float
    maintainability_score: float
    testability_score: float
    issues: list[str]
    recommendations: list[str]


@dataclass
class ValidationReport:
    """Validation report structure"""

    report_id: str
    interface_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    success_rate: float
    overall_score: float
    test_results: list[TestResult]
    analysis: InterfaceAnalysis
    generated_at: str


@dataclass
class RepositoryTestData:
    """Repository test data structure"""

    repository_url: str
    repository_name: str
    expected_status: str
    test_scenario: str
    expected_outcome: str


@dataclass
class InterfaceMetrics:
    """Interface metrics structure"""

    response_time: float
    memory_usage: float
    cpu_usage: float
    error_rate: float
    throughput: float
    availability: float
