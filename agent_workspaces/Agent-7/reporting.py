#!/usr/bin/env python3
"""Reporting utilities for quality validation."""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class QualityLevel(Enum):
    """Quality levels for validation"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationStatus(Enum):
    """Validation status results"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class QualityMetric:
    """Quality metric definition"""
    name: str
    description: str
    threshold: float
    current_value: float = 0.0
    status: ValidationStatus = ValidationStatus.SKIPPED
    level: QualityLevel = QualityLevel.MEDIUM


@dataclass
class ValidationResult:
    """Validation result for a quality check"""
    check_name: str
    status: ValidationStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    level: QualityLevel = QualityLevel.MEDIUM


@dataclass
class QualityReport:
    """Comprehensive quality report"""
    overall_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    skipped_checks: int
    validation_results: List[ValidationResult] = field(default_factory=list)
    quality_metrics: List[QualityMetric] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


def print_report(report: QualityReport) -> None:
    """Pretty print a quality report."""
    print("\n" + "=" * 80)
    print("🎯 QUALITY VALIDATION REPORT - Agent-7 (Quality Assurance Manager)")
    print("=" * 80)
    print(f"Overall Quality Score: {report.overall_score:.2f}%")
    print(f"Total Checks: {report.total_checks}")
    print(
        f"Passed: {report.passed_checks} | Failed: {report.failed_checks} | "
        f"Warnings: {report.warning_checks} | Skipped: {report.skipped_checks}"
    )
    print("-" * 80)

    for level in QualityLevel:
        level_results = [r for r in report.validation_results if r.level == level]
        if level_results:
            print(f"\n{level.value.upper()} LEVEL CHECKS:")
            for result in level_results:
                status_icon = (
                    "✅" if result.status == ValidationStatus.PASSED else
                    "❌" if result.status == ValidationStatus.FAILED else
                    "⚠️" if result.status == ValidationStatus.WARNING else
                    "⏭️"
                )
                print(f"  {status_icon} {result.check_name}: {result.message}")

    print("\n" + "=" * 80)
    print("Quality validation completed successfully!")
    print("=" * 80)
