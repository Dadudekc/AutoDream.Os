#!/usr/bin/env python3
"""
Ultimate Validation v88 Data Structures - KISS Compliant
=======================================================

Data structures for Ultimate System Validation Suite v88.0.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist) - KISS Leadership
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TestStatus(Enum):
    """Test status enumeration."""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


class ValidationLevel(Enum):
    """Validation level enumeration."""
    BASIC = "basic"
    ENHANCED = "enhanced"
    ULTIMATE = "ultimate"


@dataclass
class TestResult:
    """Test result data structure."""
    test_name: str
    status: TestStatus
    duration: float
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationMetrics:
    """Validation metrics data structure."""
    timestamp: str
    version: str
    agent: str
    task: str
    tests_run: int
    tests_passed: int
    tests_failed: int
    success_rate: float
    performance_score: float
    v2_compliance_score: float


@dataclass
class SystemHealth:
    """System health data structure."""
    overall_health: float
    performance_health: float
    security_health: float
    compliance_health: float
    recommendations: List[str]
    alerts: List[str]


@dataclass
class ValidationReport:
    """Validation report data structure."""
    metrics: ValidationMetrics
    health: SystemHealth
    test_results: List[TestResult]
    cleanup_recommendations: List[str]
    optimization_opportunities: List[str]
    generated_at: str
