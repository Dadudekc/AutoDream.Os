from enum import Enum


class WorkflowType(Enum):
    """Types of automated refactoring workflows"""

    CODE_ANALYSIS = "code_analysis"
    MODULARIZATION = "modularization"
    DUPLICATION_ELIMINATION = "duplication_elimination"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    CODE_STANDARDS_ENFORCEMENT = "code_standards_enforcement"
    ARCHITECTURE_REFACTORING = "architecture_refactoring"


class WorkflowState(Enum):
    """Workflow execution states"""

    PENDING = "pending"
    RUNNING = "running"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class ValidationLevel(Enum):
    """Validation levels for refactoring operations"""

    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    EXHAUSTIVE = "exhaustive"
