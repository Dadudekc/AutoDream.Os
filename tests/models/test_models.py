"""Test models for comprehensive testing."""

from datetime import datetime

# Prevent pytest from collecting these as test classes
__test__ = False


@dataclass
class TestResultModel:
    """Test result model."""

    test_id: str
    status: str
    duration: float
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class TestSuiteModel:
    """Test suite model."""

    suite_id: str
    name: str
    tests: list[TestResultModel]
    start_time: datetime
    end_time: Optional[datetime] = None


class TestStatusEnum:
    """Test status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TestTypeEnum:
    """Test type enumeration."""

    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"


# Backward compatibility aliases
TestResult = TestResultModel
TestSuite = TestSuiteModel
TestStatus = TestStatusEnum
TestType = TestTypeEnum
