"""
Testing Framework Core Types and Enums
======================================

Defines the fundamental data structures and enums used throughout
the consolidated testing framework.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json


class TestStatus(Enum):
    """Test execution status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    ERROR = "error"


class TestType(Enum):
    """Test type classification"""
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    LOAD = "load"
    STRESS = "stress"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"
    SMOKE = "smoke"
    REGRESSION = "regression"


class TestPriority(Enum):
    """Test priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TestEnvironment(Enum):
    """Test environment types"""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI_CD = "ci_cd"


@dataclass
class TestResult:
    """Represents the result of a single test execution"""
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    priority: TestPriority
    execution_time: float
    start_time: datetime
    end_time: datetime
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "test_type": self.test_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "execution_time": self.execution_time,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "error_message": self.error_message,
            "stack_trace": self.stack_trace,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class TestScenario:
    """Represents a test scenario with multiple test cases"""
    scenario_id: str
    scenario_name: str
    description: str
    test_cases: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    cleanup_actions: List[str] = field(default_factory=list)
    environment_requirements: List[TestEnvironment] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestSuite:
    """Represents a collection of related tests"""
    suite_id: str
    suite_name: str
    description: str
    test_ids: List[str] = field(default_factory=list)
    test_types: List[TestType] = field(default_factory=list)
    priority: TestPriority = TestPriority.NORMAL
    environment: TestEnvironment = TestEnvironment.LOCAL
    timeout: Optional[float] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_test(self, test_id: str) -> None:
        """Add a test to the suite"""
        if test_id not in self.test_ids:
            self.test_ids.append(test_id)
    
    def remove_test(self, test_id: str) -> bool:
        """Remove a test from the suite"""
        if test_id in self.test_ids:
            self.test_ids.remove(test_id)
            return True
        return False
    
    def get_test_count(self) -> int:
        """Get the total number of tests in the suite"""
        return len(self.test_ids)


@dataclass
class TestReport:
    """Comprehensive test execution report"""
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
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate test success rate as percentage"""
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100
    
    @property
    def failure_rate(self) -> float:
        """Calculate test failure rate as percentage"""
        if self.total_tests == 0:
            return 0.0
        return ((self.failed_tests + self.error_tests) / self.total_tests) * 100
    
    def add_test_result(self, result: TestResult) -> None:
        """Add a test result to the report"""
        self.test_results.append(result)
        self.total_tests += 1
        
        if result.status == TestStatus.PASSED:
            self.passed_tests += 1
        elif result.status == TestStatus.FAILED:
            self.failed_tests += 1
        elif result.status == TestStatus.SKIPPED:
            self.skipped_tests += 1
        elif result.status == TestStatus.ERROR:
            self.error_tests += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "report_id": self.report_id,
            "execution_id": self.execution_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "skipped_tests": self.skipped_tests,
            "error_tests": self.error_tests,
            "total_execution_time": self.total_execution_time,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "environment": self.environment.value,
            "test_results": [result.to_dict() for result in self.test_results],
            "test_suites": [suite.__dict__ for suite in self.test_suites],
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def print_summary(self) -> None:
        """Print a formatted summary of the test report"""
        print(f"\n🧪 TEST EXECUTION SUMMARY")
        print(f"=" * 50)
        print(f"Report ID: {self.report_id}")
        print(f"Execution ID: {self.execution_id}")
        print(f"Start Time: {self.start_time}")
        print(f"End Time: {self.end_time}")
        print(f"Total Execution Time: {self.total_execution_time:.2f}s")
        print(f"\n📊 RESULTS:")
        print(f"  Total Tests: {self.total_tests}")
        print(f"  ✅ Passed: {self.passed_tests}")
        print(f"  ❌ Failed: {self.failed_tests}")
        print(f"  ⏭️  Skipped: {self.skipped_tests}")
        print(f"  💥 Errors: {self.error_tests}")
        print(f"  📈 Success Rate: {self.success_rate:.1f}%")
        print(f"  📉 Failure Rate: {self.failure_rate:.1f}%")
        print(f"  🌍 Environment: {self.environment.value}")
