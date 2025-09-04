#!/usr/bin/env python3
"""
Unified Validation Models - DRY Compliant Consolidation
====================================================

Single source of truth for all validation models.
Consolidates 3+ duplicate validation model files into one unified module.

DRY COMPLIANCE: Eliminates duplicate validation patterns across:
- src/services/validation_models.py
- src/core/validation/validation_models.py
- src/core/ssot/validation_models.py

V2 COMPLIANCE: Under 300-line limit per module
Author: Agent-8 - SSOT Integration Specialist
License: MIT
"""

from ..core.unified_data_processing_system import get_unified_data_processing



# ================================
# VALIDATION SEVERITY LEVELS
# ================================

class ValidationSeverity(Enum):
    """Validation severity levels - consolidated from multiple sources."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    CRITICAL = "CRITICAL"


class ValidationLevel(Enum):
    """Validation levels - consolidated from SSOT models."""

    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    STRESS = "stress"
    INTEGRATION = "integration"


# ================================
# VALIDATION RESULT TYPES
# ================================

class ValidationResult(Enum):
    """Validation result types - consolidated from multiple sources."""

    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PENDING = "PENDING"


class ValidationStatus(Enum):
    """Validation status types."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ================================
# VALIDATION DATA MODELS
# ================================

@dataclass
class ValidationError:
    """
    Structured validation error with correlation ID.

    DRY COMPLIANCE: Single error model for all validation systems.
    """
    code: int
    message: str
    hint: str
    correlation_id: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "code": self.code,
            "message": self.message,
            "hint": self.hint,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details or {}
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValidationError":
        """Create from dictionary."""
        return cls(
            code=data["code"],
            message=data["message"],
            hint=data["hint"],
            correlation_id=data["correlation_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            details=data.get("details")
        )


@dataclass
class ValidationSummary:
    """
    Summary of validation results.

    DRY COMPLIANCE: Single summary model for all validation operations.
    """
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0
    error_checks: int = 0
    validation_level: ValidationLevel = ValidationLevel.BASIC
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_checks == 0:
            return 100.0
        return (self.passed_checks / self.total_checks) * 100.0

    @property
    def has_failures(self) -> bool:
        """Check if validation has any failures."""
        return self.failed_checks > 0 or self.error_checks > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "warning_checks": self.warning_checks,
            "error_checks": self.error_checks,
            "validation_level": self.validation_level.value,
            "success_rate": self.success_rate,
            "has_failures": self.has_failures,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds
        }


@dataclass
class ValidationReport:
    """
    Complete validation report with errors and summary.

    DRY COMPLIANCE: Single report model for all validation operations.
    """
    validation_id: str
    target_system: str
    summary: ValidationSummary
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize validation ID if not provided."""
        if not self.validation_id:
            self.validation_id = f"val_{get_timestamp()}_{hash(self.target_system) % 10000}"

    def add_error(self, error: ValidationError):
        """Add an error to the report."""
        self.errors.append(error)
        self.summary.error_checks += 1
        self.summary.total_checks += 1

    def add_warning(self, warning: ValidationError):
        """Add a warning to the report."""
        self.warnings.append(warning)
        self.summary.warning_checks += 1
        self.summary.total_checks += 1

    def mark_passed(self):
        """Mark a check as passed."""
        self.summary.passed_checks += 1
        self.summary.total_checks += 1

    def finalize(self):
        """Finalize the validation report."""
        self.summary.end_time = datetime.utcnow()
        if self.summary.start_time:
            self.summary.duration_seconds = (
                self.summary.end_time - self.summary.start_time
            ).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "validation_id": self.validation_id,
            "target_system": self.target_system,
            "summary": self.summary.to_dict(),
            "errors": [error.to_dict() for error in self.errors],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "metadata": self.metadata,
            "generated_at": datetime.utcnow().isoformat()
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# ================================
# UTILITY FUNCTIONS
# ================================

def create_validation_error(
    code: int,
    message: str,
    hint: str = "",
    details: Optional[Dict[str, Any]] = None
) -> ValidationError:
    """
    Create a validation error with auto-generated correlation ID.

    DRY COMPLIANCE: Single error creation utility.
    """
    correlation_id = f"err_{get_timestamp()}_{code}_{hash(message) % 10000}"
    return ValidationError(
        code=code,
        message=message,
        hint=hint,
        correlation_id=correlation_id,
        timestamp=datetime.utcnow(),
        details=details
    )


def create_validation_report(
    target_system: str,
    validation_level: ValidationLevel = ValidationLevel.BASIC
) -> ValidationReport:
    """
    Create a new validation report.

    DRY COMPLIANCE: Single report creation utility.
    """
    summary = ValidationSummary(
        validation_level=validation_level,
        start_time=datetime.utcnow()
    )
    return ValidationReport(
        validation_id="",
        target_system=target_system,
        summary=summary
    )


# ================================
# EXPORTS
# ================================

__all__ = [
    # Enums
    "ValidationSeverity",
    "ValidationLevel",
    "ValidationResult",
    "ValidationStatus",

    # Data Classes
    "ValidationError",
    "ValidationSummary",
    "ValidationReport",

    # Utility Functions
    "create_validation_error",
    "create_validation_report"
]
