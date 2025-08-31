"""
Data models and enums for the quality gates system.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


class GateSeverity(Enum):
    """Severity levels for quality gates."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class GateStatus(Enum):
    """Status of a quality gate check."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class QualityGateConfig:
    """Configuration for a quality gate."""
    gate_name: str
    severity: GateSeverity
    enabled: bool
    threshold: float
    weight: float
    description: str
    failure_message: str
    success_message: str


@dataclass
class QualityGateResult:
    """Result of a quality gate check."""
    gate_name: str
    status: GateStatus
    score: float
    threshold: float
    weight: float
    severity: GateSeverity
    details: str
    recommendations: List[str]
    timestamp: str
    execution_time_ms: float


@dataclass
class QualityGateSummary:
    """Summary of all quality gate results."""
    total_gates: int
    passed_gates: int
    failed_gates: int
    warning_gates: int
    error_gates: int
    overall_score: float
    weighted_score: float
    critical_failures: int
    high_failures: int
    medium_failures: int
    low_failures: int
    timestamp: str
