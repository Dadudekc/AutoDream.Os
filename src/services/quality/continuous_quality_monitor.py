#!/usr/bin/env python3
"""
Continuous Quality Monitor - V2 Compliance
===========================================

Real-time quality monitoring system that continuously validates code quality,
enforces V2 compliance, and prevents quality degradation.

V2 Compliance: ≤400 lines, focused quality monitoring
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class QualityViolation:
    """Quality violation data model."""

    file_path: str
    violation_type: str
    severity: str
    line_number: int
    description: str
    timestamp: datetime


@dataclass
class QualityMetrics:
    """Quality metrics data model."""

    total_files: int
    compliant_files: int
    violation_count: int
    quality_score: float
    timestamp: datetime


class ContinuousQualityMonitor:
    """
    Continuous quality monitoring system.

    Monitors code quality in real-time and enforces V2 compliance.
    """

    def __init__(self, project_root: str = ".", check_interval: int = 60):
        """Initialize continuous quality monitor."""
        self.project_root = Path(project_root)
        self.check_interval = check_interval
        self.logger = logging.getLogger(f"{__name__}.ContinuousQualityMonitor")
        self.violations: list[QualityViolation] = []
        self.metrics: QualityMetrics | None = None

        # V2 Compliance rules
        self.v2_rules = {
            "max_file_size": 400,
            "max_classes": 5,
            "max_functions": 10,
            "max_complexity": 10,
            "max_parameters": 5,
            "max_inheritance": 2,
            "max_enums": 3,
        }

    def check_file_compliance(self, file_path: Path) -> list[QualityViolation]:
        """Check single file for V2 compliance violations."""
        violations = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Check file size
            if len(lines) > self.v2_rules["max_file_size"]:
                violations.append(
                    QualityViolation(
                        file_path=str(file_path),
                        violation_type="file_size",
                        severity="CRITICAL",
                        line_number=len(lines),
                        description=f"File size {len(lines)} exceeds limit {self.v2_rules['max_file_size']}",
                        timestamp=datetime.now(),
                    )
                )

            # Check for forbidden patterns
            forbidden_patterns = [
                ("abstract", "Abstract base classes"),
                ("async def", "Excessive async operations"),
                ("threading", "Threading for synchronous operations"),
                ("event sourcing", "Event sourcing for simple operations"),
                ("dependency injection", "Dependency injection for simple objects"),
            ]

            for pattern, description in forbidden_patterns:
                if pattern in content.lower():
                    violations.append(
                        QualityViolation(
                            file_path=str(file_path),
                            violation_type="forbidden_pattern",
                            severity="HIGH",
                            line_number=content.lower().find(pattern) + 1,
                            description=f"Forbidden pattern detected: {description}",
                            timestamp=datetime.now(),
                        )
                    )

        except Exception as e:
            violations.append(
                QualityViolation(
                    file_path=str(file_path),
                    violation_type="file_error",
                    severity="MEDIUM",
                    line_number=0,
                    description=f"Error reading file: {str(e)}",
                    timestamp=datetime.now(),
                )
            )

        return violations

    def scan_project(self) -> QualityMetrics:
        """Scan entire project for quality violations."""
        violations = []
        total_files = 0
        compliant_files = 0

        # Scan Python files
        for file_path in self.project_root.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue

            total_files += 1
            file_violations = self.check_file_compliance(file_path)

            if not file_violations:
                compliant_files += 1
            else:
                violations.extend(file_violations)

        # Calculate quality score
        quality_score = (compliant_files / total_files * 100) if total_files > 0 else 0

        self.metrics = QualityMetrics(
            total_files=total_files,
            compliant_files=compliant_files,
            violation_count=len(violations),
            quality_score=quality_score,
            timestamp=datetime.now(),
        )

        self.violations = violations
        return self.metrics

    def generate_quality_report(self) -> dict[str, Any]:
        """Generate comprehensive quality report."""
        if not self.metrics:
            self.scan_project()

        report = {
            "timestamp": self.metrics.timestamp.isoformat(),
            "metrics": {
                "total_files": self.metrics.total_files,
                "compliant_files": self.metrics.compliant_files,
                "violation_count": self.metrics.violation_count,
                "quality_score": self.metrics.quality_score,
            },
            "violations": [
                {
                    "file_path": v.file_path,
                    "violation_type": v.violation_type,
                    "severity": v.severity,
                    "line_number": v.line_number,
                    "description": v.description,
                    "timestamp": v.timestamp.isoformat(),
                }
                for v in self.violations
            ],
            "summary": {
                "critical_violations": len(
                    [v for v in self.violations if v.severity == "CRITICAL"]
                ),
                "high_violations": len([v for v in self.violations if v.severity == "HIGH"]),
                "medium_violations": len([v for v in self.violations if v.severity == "MEDIUM"]),
            },
        }

        return report

    def start_monitoring(self) -> None:
        """Start continuous quality monitoring."""
        self.logger.info("Starting continuous quality monitoring")

        while True:
            try:
                metrics = self.scan_project()

                if metrics.quality_score < 90:
                    self.logger.warning(f"Quality score below threshold: {metrics.quality_score}%")

                if metrics.violation_count > 0:
                    self.logger.warning(f"Found {metrics.violation_count} quality violations")

                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("Quality monitoring stopped")
                break
            except Exception as e:
                self.logger.error(f"Error in quality monitoring: {e}")
                time.sleep(self.check_interval)

    def get_violation_summary(self) -> str:
        """Get summary of current violations."""
        if not self.violations:
            return "No quality violations detected"

        critical = len([v for v in self.violations if v.severity == "CRITICAL"])
        high = len([v for v in self.violations if v.severity == "HIGH"])
        medium = len([v for v in self.violations if v.severity == "MEDIUM"])

        return f"Quality violations: {critical} critical, {high} high, {medium} medium"


def create_quality_monitor(project_root: str = ".") -> ContinuousQualityMonitor:
    """Create continuous quality monitor instance."""
    return ContinuousQualityMonitor(project_root)


if __name__ == "__main__":
    # Example usage
    monitor = create_quality_monitor()
    metrics = monitor.scan_project()
    report = monitor.generate_quality_report()

    print(f"Quality Score: {metrics.quality_score:.1f}%")
    print(f"Compliant Files: {metrics.compliant_files}/{metrics.total_files}")
    print(f"Violations: {metrics.violation_count}")
    print(monitor.get_violation_summary())
