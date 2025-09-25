#!/usr/bin/env python3
"""
Testing Validation Models
========================

Data models for Team Beta Testing Validation System
V2 Compliant: ≤400 lines, focused data structures
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class TestStatus(Enum):
    """Test status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TestCategory(Enum):
    """Test category enumeration"""
    FUNCTIONAL = "functional"
    INTEGRATION = "integration"
    COMPATIBILITY = "compatibility"
    PERFORMANCE = "performance"
    USABILITY = "usability"


@dataclass
class TestCase:
    """Test case structure"""
    name: str
    category: TestCategory
    description: str
    status: TestStatus
    duration: float
    errors: List[str]
    warnings: List[str]
    platform: str


@dataclass
class TestResult:
    """Test result structure"""
    test_case: TestCase
    success: bool
    output: str
    metrics: Dict[str, Any]
    recommendations: List[str]


@dataclass
class PlatformInfo:
    """Platform information structure"""
    system: str
    release: str
    version: str
    machine: str
    processor: str
    python_version: str


@dataclass
class TestMetrics:
    """Test metrics structure"""
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    total_duration: float
    success_rate: float


@dataclass
class ValidationReport:
    """Validation report structure"""
    report_id: str
    platform_info: PlatformInfo
    test_metrics: TestMetrics
    test_results: List[TestResult]
    overall_status: str
    generated_at: str