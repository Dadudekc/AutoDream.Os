"""Shared data structures and constants for cleanup validation."""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class CleanupStatus(Enum):
    """Cleanup status enumeration."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class StandardCompliance(Enum):
    """Standard compliance enumeration."""

    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"


@dataclass
class CleanupRequirement:
    """Individual cleanup requirement."""

    requirement_id: str
    description: str
    required: bool
    completed: bool = False
    validation_notes: str = ""
    completion_timestamp: Optional[str] = None
    evidence_files: List[str] | None = None


@dataclass
class StandardRequirement:
    """V2 standard requirement."""

    standard_id: str
    description: str
    required: bool
    compliant: bool = False
    validation_notes: str = ""
    compliance_score: float = 0.0


@dataclass
class CleanupValidation:
    """Cleanup validation result."""

    is_valid: bool
    missing_cleanup: List[str]
    validation_errors: List[str]
    warnings: List[str]
    cleanup_score: float  # 0.0 to 1.0
    standards_score: float  # 0.0 to 1.0
    overall_score: float  # 0.0 to 1.0
    timestamp: str


# Patterns to flag in source files when checking for stray debug code.
DEBUG_PATTERNS: List[str] = ["print(", "debug(", "console.log(", "TODO:", "FIXME:"]


__all__ = [
    "CleanupStatus",
    "StandardCompliance",
    "CleanupRequirement",
    "StandardRequirement",
    "CleanupValidation",
    "DEBUG_PATTERNS",
]
