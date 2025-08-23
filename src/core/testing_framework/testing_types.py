#!/usr/bin/env python3
"""
Testing Types - V2 Testing Framework Data Structures
====================================================

Defines all data structures, enums, and types for the testing framework.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime


class TestStatus(Enum):
    """Test execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    ERROR = "error"


class TestType(Enum):
    """Test type enumeration."""
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    LOAD = "load"
    STRESS = "stress"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


class TestPriority(Enum):
    """Test priority enumeration with numeric values."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TestResult:
    """Test execution result data structure."""
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    start_time: float
    end_time: float
    duration: float
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    assertions_passed: int = 0
    assertions_failed: int = 0
    test_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and compute derived fields."""
        if self.duration <= 0:
            self.duration = self.end_time - self.start_time
        
        if self.status == TestStatus.FAILED and not self.error_message:
            self.error_message = "Test failed without specific error message"


@dataclass
class TestScenario:
    """Test scenario configuration and execution plan."""
    scenario_id: str
    name: str
    description: str
    test_type: TestType
    priority: TestPriority
    timeout: float = 300.0
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    setup_steps: List[Callable] = field(default_factory=list)
    test_steps: List[Callable] = field(default_factory=list)
    cleanup_steps: List[Callable] = field(default_factory=list)
    assertions: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scenario configuration."""
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        if self.retry_count > self.max_retries:
            raise ValueError("Retry count cannot exceed max retries")


@dataclass
class TestEnvironment:
    """Test environment configuration."""
    environment_id: str
    name: str
    description: str
    systems: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    config_overrides: Dict[str, Any] = field(default_factory=dict)
    cleanup_on_exit: bool = True
    parallel_execution: bool = False
    max_parallel_tests: int = 5

    def __post_init__(self):
        """Validate environment configuration."""
        if self.max_parallel_tests <= 0:
            raise ValueError("Max parallel tests must be positive")
        if self.parallel_execution and self.max_parallel_tests == 1:
            self.parallel_execution = False


def run_smoke_test() -> bool:
    """Run smoke test for testing types module."""
    try:
        # Test enum creation
        status = TestStatus.PASSED
        test_type = TestType.INTEGRATION
        priority = TestPriority.HIGH
        
        assert status.value == "passed"
        assert test_type.value == "integration"
        assert priority.value == 3
        
        # Test dataclass creation
        result = TestResult(
            test_id="smoke_test",
            test_name="Smoke Test",
            test_type=TestType.UNIT,
            status=TestStatus.PASSED,
            start_time=100.0,
            end_time=110.0,
            duration=10.0
        )
        
        assert result.test_id == "smoke_test"
        assert result.duration == 10.0
        
        # Test scenario creation
        scenario = TestScenario(
            scenario_id="smoke_scenario",
            name="Smoke Scenario",
            description="Smoke test scenario",
            test_type=TestType.INTEGRATION,
            priority=TestPriority.NORMAL
        )
        
        assert scenario.timeout == 300.0
        assert scenario.max_retries == 3
        
        # Test environment creation
        env = TestEnvironment(
            environment_id="smoke_env",
            name="Smoke Environment",
            description="Smoke test environment"
        )
        
        assert env.cleanup_on_exit is True
        assert env.max_parallel_tests == 5
        
        print("✅ Testing Types smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Testing Types smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
