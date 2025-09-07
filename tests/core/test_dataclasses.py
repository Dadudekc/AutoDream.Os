#!/usr/bin/env python3
"""
Test Dataclasses - Agent Cellphone V2
===================================

Core dataclass definitions for the unified testing framework.
Extracted from unified_test_runner.py to achieve V2 compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

from .test_enums import TestPriority, TestStatus, TestMode


@dataclass
class TestCategory:
    """Test category configuration."""
    name: str
    description: str
    marker: str
    timeout: int
    priority: TestPriority
    directory: str
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    parallel: bool = False
    retry_count: int = 0


@dataclass
class TestResult:
    """Test execution result."""
    test_name: str
    category: str
    status: TestStatus
    duration: float
    output: str
    error_message: Optional[str] = None
    timestamp: str = ""
    retry_count: int = 0


@dataclass
class TestExecutionConfig:
    """Test execution configuration."""
    mode: TestMode = TestMode.ALL
    parallel: bool = True
    max_workers: int = 4
    timeout: int = 300
    verbose: bool = False
    coverage: bool = True
    report_format: str = "text"
    output_file: Optional[str] = None
    fail_fast: bool = False
    retry_failed: bool = True
    max_retries: int = 2


@dataclass
class TestSuite:
    """Test suite configuration."""
    name: str
    description: str
    categories: List[str] = field(default_factory=list)
    enabled: bool = True
    priority: TestPriority = TestPriority.MEDIUM
    timeout: int = 600
    parallel: bool = False


@dataclass
class TestReport:
    """Test execution report."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    timestamp: datetime
    results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
