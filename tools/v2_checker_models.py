#!/usr/bin/env python3
"""
V2 Checker Models - Data Structures
====================================

Data models for V2 compliance checker.
Extracted from v2_compliance_checker.py for V2 compliance.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from dataclasses import dataclass


@dataclass
class ComplianceViolation:
    """Represents a V2 compliance violation."""

    file_path: str
    violation_type: str
    severity: str  # CRITICAL, MAJOR, MINOR
    line_number: int | None
    current_value: int
    max_allowed: int
    message: str


@dataclass
class ComplianceReport:
    """V2 compliance scan report."""

    total_files: int
    compliant_files: int
    violations: list[ComplianceViolation]
    compliance_rate: float

    @property
    def has_violations(self) -> bool:
        """Check if report has any violations."""
        return len(self.violations) > 0

    @property
    def critical_violations(self) -> list[ComplianceViolation]:
        """Get critical violations."""
        return [v for v in self.violations if v.severity == "CRITICAL"]

    @property
    def major_violations(self) -> list[ComplianceViolation]:
        """Get major violations."""
        return [v for v in self.violations if v.severity == "MAJOR"]

    @property
    def minor_violations(self) -> list[ComplianceViolation]:
        """Get minor violations."""
        return [v for v in self.violations if v.severity == "MINOR"]
