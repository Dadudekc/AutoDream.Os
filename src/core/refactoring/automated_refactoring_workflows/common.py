import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATED = "validated"


class WorkflowType(Enum):
    """Types of automated refactoring workflows."""

    CODE_DUPLICATION_REMOVAL = "code_duplication_removal"
    MONOLITH_BREAKDOWN = "monolith_breakdown"
    SRP_VIOLATION_FIX = "srp_violation_fix"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ARCHITECTURE_CONSOLIDATION = "architecture_consolidation"
    TEST_COVERAGE_IMPROVEMENT = "test_coverage_improvement"


@dataclass
class WorkflowStep:
    """Individual step within a refactoring workflow."""

    step_id: str
    name: str
    description: str
    action: Callable
    dependencies: List[str] = field(default_factory=list)
    estimated_time: float = 0.0  # in minutes
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class WorkflowExecution:
    """Complete workflow execution record."""

    workflow_id: str
    workflow_type: WorkflowType
    target_files: List[str]
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_time: Optional[float] = None
    success_rate: float = 0.0
    validation_results: Dict[str, Any] = field(default_factory=dict)


# Default workflow templates used for setup. Centralized for single-source-of-truth.
DEFAULT_WORKFLOW_TEMPLATES: Dict[WorkflowType, List[Dict[str, Any]]] = {
    WorkflowType.CODE_DUPLICATION_REMOVAL: [
        {
            "step_id": "analysis",
            "name": "Code Duplication Analysis",
            "description": "Analyze codebase for duplicate code patterns",
            "estimated_time": 15.0,
        },
        {
            "step_id": "identification",
            "name": "Duplicate Pattern Identification",
            "description": "Identify specific duplicate code sections",
            "estimated_time": 10.0,
        },
        {
            "step_id": "extraction",
            "name": "Common Code Extraction",
            "description": "Extract common code into reusable functions",
            "estimated_time": 20.0,
        },
        {
            "step_id": "refactoring",
            "name": "Duplicate Code Refactoring",
            "description": "Refactor code to use extracted functions",
            "estimated_time": 25.0,
        },
        {
            "step_id": "validation",
            "name": "Refactoring Validation",
            "description": "Validate that refactoring maintains functionality",
            "estimated_time": 15.0,
        },
    ],
    WorkflowType.MONOLITH_BREAKDOWN: [
        {
            "step_id": "analysis",
            "name": "Monolith Analysis",
            "description": "Analyze monolithic file structure and dependencies",
            "estimated_time": 20.0,
        },
        {
            "step_id": "planning",
            "name": "Breakdown Planning",
            "description": "Plan modular breakdown strategy",
            "estimated_time": 15.0,
        },
        {
            "step_id": "extraction",
            "name": "Module Extraction",
            "description": "Extract logical modules from monolith",
            "estimated_time": 30.0,
        },
        {
            "step_id": "interface",
            "name": "Interface Definition",
            "description": "Define clean interfaces between modules",
            "estimated_time": 20.0,
        },
        {
            "step_id": "testing",
            "name": "Module Testing",
            "description": "Test extracted modules for functionality",
            "estimated_time": 25.0,
        },
    ],
    WorkflowType.SRP_VIOLATION_FIX: [
        {
            "step_id": "violation_analysis",
            "name": "SRP Violation Analysis",
            "description": "Identify Single Responsibility Principle violations",
            "estimated_time": 15.0,
        },
        {
            "step_id": "responsibility_separation",
            "name": "Responsibility Separation",
            "description": "Separate mixed responsibilities into focused classes",
            "estimated_time": 25.0,
        },
        {
            "step_id": "class_restructuring",
            "name": "Class Restructuring",
            "description": "Restructure classes to follow SRP",
            "estimated_time": 20.0,
        },
        {
            "step_id": "dependency_management",
            "name": "Dependency Management",
            "description": "Manage dependencies between separated classes",
            "estimated_time": 15.0,
        },
        {
            "step_id": "validation",
            "name": "SRP Compliance Validation",
            "description": "Validate that classes now follow SRP",
            "estimated_time": 15.0,
        },
    ],
}
