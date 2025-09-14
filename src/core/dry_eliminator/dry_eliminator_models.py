#!/usr/bin/env python3
"""
DRY Eliminator Models - KISS Compliant
=====================================

Simple data models for DRY elimination.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DRYViolationType(Enum):
    """Types of DRY violations."""

    DUPLICATE_CODE = "duplicate_code"
    DUPLICATE_FUNCTION = "duplicate_function"
    DUPLICATE_CLASS = "duplicate_class"
    DUPLICATE_IMPORT = "duplicate_import"


class EliminationStrategy(Enum):
    """Elimination strategies."""

    CONSOLIDATE = "consolidate"
    EXTRACT = "extract"
    REFACTOR = "refactor"
    REMOVE = "remove"


class ViolationSeverity(Enum):
    """Violation severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DRYViolation:
    """Simple DRY violation data structure."""

    violation_id: str
    violation_type: DRYViolationType
    severity: ViolationSeverity
    file_path: str
    line_number: int
    code_snippet: str
    duplicate_locations: list[str] = field(default_factory=list)
    suggested_strategy: EliminationStrategy = EliminationStrategy.CONSOLIDATE
    estimated_effort: str = "medium"
    potential_savings: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DRYAnalysisResult:
    """Simple DRY analysis result."""

    analysis_id: str
    timestamp: datetime
    total_violations: int
    violations: list[DRYViolation]
    files_analyzed: int
    total_lines: int
    estimated_savings: int
    analysis_duration: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DRYConfiguration:
    """Simple DRY configuration."""

    scan_mode: str = "comprehensive"
    min_duplicate_lines: int = 3
    exclude_patterns: list[str] = field(default_factory=list)
    include_patterns: list[str] = field(default_factory=lambda: ["*.py"])
    max_file_size: int = 10000
    parallel_processing: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DRYMetrics:
    """Simple DRY metrics."""

    violations_found: int = 0
    violations_fixed: int = 0
    lines_eliminated: int = 0
    files_processed: int = 0
    processing_time: float = 0.0
    success_rate: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


# Simple factory functions
def create_dry_violation(
    violation_id: str,
    violation_type: DRYViolationType,
    severity: ViolationSeverity,
    file_path: str,
    line_number: int,
    code_snippet: str,
) -> DRYViolation:
    """Create DRY violation."""
    return DRYViolation(
        violation_id=violation_id,
        violation_type=violation_type,
        severity=severity,
        file_path=file_path,
        line_number=line_number,
        code_snippet=code_snippet,
    )


def create_dry_analysis_result(
    violations: list[DRYViolation], files_analyzed: int, total_lines: int
) -> DRYAnalysisResult:
    """Create DRY analysis result."""
    import uuid

    return DRYAnalysisResult(
        analysis_id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        total_violations=len(violations),
        violations=violations,
        files_analyzed=files_analyzed,
        total_lines=total_lines,
        estimated_savings=sum(v.potential_savings for v in violations),
    )


def create_dry_configuration(**kwargs) -> DRYConfiguration:
    """Create DRY configuration."""
    return DRYConfiguration(**kwargs)


def create_dry_metrics() -> DRYMetrics:
    """Create DRY metrics."""
    return DRYMetrics()


__all__ = [
    "DRYViolationType",
    "EliminationStrategy",
    "ViolationSeverity",
    "DRYViolation",
    "DRYAnalysisResult",
    "DRYConfiguration",
    "DRYMetrics",
    "create_dry_violation",
    "create_dry_analysis_result",
    "create_dry_configuration",
    "create_dry_metrics",
]
