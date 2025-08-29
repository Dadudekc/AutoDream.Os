"""Validation data models and enums."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class ValidationSeverity(Enum):
    """Validation severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Validation result status."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


@dataclass
class ValidationRule:
    """Configurable validation rule."""

    rule_id: str
    rule_name: str
    rule_type: str
    description: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    threshold: Optional[float] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Standardized validation result."""

    rule_id: str
    rule_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    field_path: Optional[str] = None
    actual_value: Optional[Any] = None
    expected_value: Optional[Any] = None
