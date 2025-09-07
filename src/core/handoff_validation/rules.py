"""Common validation rules and constants for handoff validation."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ValidationSeverity(Enum):
    """Validation severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationStatus(Enum):
    """Validation status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationRule:
    """Definition of a validation rule."""

    rule_id: str
    name: str
    description: str
    condition: str
    severity: ValidationSeverity
    timeout: float = 30.0
    retry_count: int = 3
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result produced by a validation check."""

    rule_id: str
    rule_name: str
    status: ValidationStatus
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    error_details: Optional[str] = None
    warning_details: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    severity: ValidationSeverity = ValidationSeverity.MEDIUM


@dataclass
class ValidationSession:
    """Tracks the execution of validation rules for a single handoff."""

    session_id: str
    handoff_id: str
    procedure_id: str
    start_time: float
    end_time: Optional[float] = None
    rules: List[ValidationRule] = field(default_factory=list)
    results: List[ValidationResult] = field(default_factory=list)
    overall_status: ValidationStatus = ValidationStatus.PENDING
    validation_score: float = 0.0
    critical_failures: int = 0
    high_failures: int = 0
    medium_failures: int = 0
    low_failures: int = 0


DEFAULT_RULES: List[ValidationRule] = [
    ValidationRule(
        rule_id="VR001",
        name="Phase Completion Check",
        description="Verify that the source phase has completed all required tasks",
        condition="source_phase_completed",
        severity=ValidationSeverity.CRITICAL,
        timeout=30.0,
        retry_count=3,
    ),
    ValidationRule(
        rule_id="VR002",
        name="Resource Availability Check",
        description="Verify that target resources are available and accessible",
        condition="target_resources_available",
        severity=ValidationSeverity.CRITICAL,
        timeout=45.0,
        retry_count=2,
    ),
    ValidationRule(
        rule_id="VR003",
        name="State Consistency Check",
        description="Verify that system state is consistent across components",
        condition="state_consistency_verified",
        severity=ValidationSeverity.HIGH,
        timeout=60.0,
        retry_count=2,
    ),
    ValidationRule(
        rule_id="VR004",
        name="Agent Readiness Validation",
        description="Verify that target agent is ready to receive handoff",
        condition="target_agent_ready",
        severity=ValidationSeverity.CRITICAL,
        timeout=20.0,
        retry_count=3,
    ),
    ValidationRule(
        rule_id="VR005",
        name="Context Transfer Validation",
        description="Verify that task context was transferred completely",
        condition="context_transfer_complete",
        severity=ValidationSeverity.CRITICAL,
        timeout=30.0,
        retry_count=2,
    ),
    ValidationRule(
        rule_id="VR006",
        name="Connection Stability Check",
        description="Verify that connections are stable and reliable",
        condition="connections_stable",
        severity=ValidationSeverity.HIGH,
        timeout=15.0,
        retry_count=3,
    ),
    ValidationRule(
        rule_id="VR007",
        name="Permission Validation",
        description="Verify that all required permissions are granted",
        condition="permissions_granted",
        severity=ValidationSeverity.MEDIUM,
        timeout=20.0,
        retry_count=2,
    ),
    ValidationRule(
        rule_id="VR008",
        name="Data Integrity Check",
        description="Verify that data integrity is maintained during handoff",
        condition="data_integrity_maintained",
        severity=ValidationSeverity.HIGH,
        timeout=45.0,
        retry_count=2,
    ),
]


def load_rules_from_file(path: Path) -> List[ValidationRule]:
    """Load validation rules from a JSON file."""
    data = json.loads(path.read_text())
    return [ValidationRule(**item) for item in data]
