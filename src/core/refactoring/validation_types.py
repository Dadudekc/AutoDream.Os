"""Common validation types for refactoring validation phases."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List


class ValidationStatus(Enum):
    """Validation status enumeration."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


class ValidationSeverity(Enum):
    """Validation severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationResult:
    """Validation result data structure."""
    test_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    timestamp: str = ""


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    validation_id: str
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    warning_tests: int
    skipped_tests: int
    execution_time: float
    results: List[ValidationResult]
    summary: Dict[str, Any]
