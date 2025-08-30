"""
Data models and enums for automated integration test suites.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional


class TestSuiteCategory(Enum):
    """Categories of test suites"""
    
    CORE_SYSTEM = "core_system"
    WORKFLOW_SYSTEM = "workflow_system"
    AGENT_MANAGEMENT = "agent_management"
    COMMUNICATION_SYSTEM = "communication_system"
    API_INTEGRATION = "api_integration"
    DATABASE_INTEGRATION = "database_integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPLIANCE = "compliance"


class TestExecutionMode(Enum):
    """Test execution modes"""
    
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PRIORITY_BASED = "priority_based"
    DEPENDENCY_BASED = "dependency_based"


@dataclass
class TestSuiteConfig:
    """Configuration for test suite execution"""
    
    suite_id: str
    name: str
    description: str
    category: TestSuiteCategory
    priority: str  # Using string to avoid circular import
    execution_mode: TestExecutionMode
    timeout: int = 600
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    cleanup_required: bool = True
    parallel_execution: bool = True
    max_parallel_tests: int = 4


@dataclass
class TestSuiteResult:
    """Result of test suite execution"""
    
    suite_id: str
    suite_name: str
    execution_start: datetime
    execution_end: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    skipped_tests: int
    execution_time: float
    status: str
    test_results: List[Dict[str, Any]]
    summary: Dict[str, Any]
    error_details: Optional[str] = None
