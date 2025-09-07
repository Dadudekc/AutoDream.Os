#!/usr/bin/env python3
"""
Test Enums - Agent Cellphone V2
==============================

Core enumeration definitions for the unified testing framework.
Extracted from unified_test_runner.py to achieve V2 compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from enum import Enum


class TestMode(Enum):
    """Test execution mode enumeration."""
    ALL = "all"
    CRITICAL = "critical"
    SMOKE = "smoke"
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    API = "api"
    BEHAVIOR = "behavior"
    DECISION = "decision"
    CUSTOM = "custom"


class TestStatus(Enum):
    """Test execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


class TestPriority(Enum):
    """Test priority enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestEnvironment(Enum):
    """Test environment enumeration."""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI = "ci"
    TESTING = "testing"


class TestLevel(Enum):
    """Test level enumeration."""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    ACCEPTANCE = "acceptance"
    REGRESSION = "regression"


class TestType(Enum):
    """Test type enumeration."""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USABILITY = "usability"
    COMPATIBILITY = "compatibility"
