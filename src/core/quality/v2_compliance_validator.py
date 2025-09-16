#!/usr/bin/env python3
"""
V2 Compliance Validator Module - V2 Compliant
Comprehensive V2 compliance validation and quality standards enforcement
V2 Compliance: ≤400 lines for compliance

Author: Agent-7 (Web Development Specialist) - Quality Assurance
License: MIT
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ComplianceLevel(Enum):
    """V2 compliance levels."""

    COMPLIANT = "compliant"  # ≤400 lines
    MINOR_VIOLATION = "minor_violation"  # 401-600 lines
    MAJOR_VIOLATION = "major_violation"  # >600 lines
    CRITICAL_VIOLATION = "critical_violation"  # >1000 lines


class QualityStandard(Enum):
    """Quality standards for validation."""

    V2_COMPLIANCE = "v2_compliance"
    CODE_STRUCTURE = "code_structure"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    SECURITY = "security"


@dataclass
class ComplianceViolation:
    """V2 compliance violation details."""

    file_path: str
    line_count: int
    compliance_level: ComplianceLevel
    violation_type: str
    severity: str
    recommendations: list[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)


@dataclass
class QualityMetrics:
    """Quality metrics for files."""

    file_path: str
    line_count: int
    compliance_score: float
    structure_score: float
    documentation_score: float
    performance_score: float
    security_score: float
    overall_score: float
    violations: list[ComplianceViolation] = field(default_factory=list)
    last_analyzed: datetime = field(default_factory=datetime.now)


class V2ComplianceValidator:
    """
    V2 compliance validator with quality standards enforcement.

    V2 Compliance: Comprehensive validation framework for core systems.
    """

    def __init__(self):
        self.violations: list[ComplianceViolation] = []
        self.quality_metrics: dict[str, QualityMetrics] = {}
        self.web_interface_callbacks = []
        self.validation_thresholds = {
            ComplianceLevel.COMPLIANT: 400,
            ComplianceLevel.MINOR_VIOLATION: 600,
            ComplianceLevel.MAJOR_VIOLATION: 1000,
            ComplianceLevel.CRITICAL_VIOLATION: float("inf"),
        }

        # Quality standards weights
        self.quality_weights = {
            QualityStandard.V2_COMPLIANCE: 0.4,
            QualityStandard.CODE_STRUCTURE: 0.2,
            QualityStandard.DOCUMENTATION: 0.15,
            QualityStandard.PERFORMANCE: 0.15,
            QualityStandard.SECURITY: 0.1,
        }

    async def validate_directory(self, directory_path: str) -> dict[str, Any]:
        """Validate V2 compliance for entire directory."""
        try:
            logger.info(f"🔍 Starting V2 compliance validation for {directory_path}")

            violations = []
            quality_metrics = {}

            # Scan directory for files
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if self._is_analyzable_file(file):
                        file_path = os.path.join(root, file)
                        try:
                            # Analyze file
                            violation = await self._analyze_file(file_path)
                            if violation:
                                violations.append(violation)

                            # Calculate quality metrics
                            metrics = await self._calculate_quality_metrics(file_path)
                            if metrics:
                                quality_metrics[file_path] = metrics

                        except Exception as e:
                            logger.error(f"❌ Failed to analyze {file_path}: {e}")

            # Update internal state
            self.violations.extend(violations)
            self.quality_metrics.update(quality_metrics)

            # Generate validation report
            report = self._generate_validation_report(violations, quality_metrics)

            # Notify web interface
            self._notify_web_interface("validation_completed", report)

            logger.info(
                f"✅ V2 compliance validation completed: {len(violations)} violations found"
            )
            return report

        except Exception as e:
            logger.error(f"❌ Directory validation failed: {e}")
            return {"error": str(e)}

    def _is_analyzable_file(self, filename: str) -> bool:
        """Check if file should be analyzed."""
        analyzable_extensions = {".py", ".js", ".css", ".html", ".ts", ".tsx", ".jsx"}
        return any(filename.endswith(ext) for ext in analyzable_extensions)

    async def _analyze_file(self, file_path: str) -> ComplianceViolation | None:
        """Analyze file for V2 compliance violations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()

            line_count = len(lines)

            # Determine compliance level
            compliance_level = self._determine_compliance_level(line_count)

            if compliance_level == ComplianceLevel.COMPLIANT:
                return None  # No violation

            # Create violation record
            violation = ComplianceViolation(
                file_path=file_path,
                line_count=line_count,
                compliance_level=compliance_level,
                violation_type=self._get_violation_type(compliance_level),
                severity=self._get_severity(compliance_level),
                recommendations=self._get_recommendations(compliance_level, line_count),
            )

            return violation

        except Exception as e:
            logger.error(f"❌ File analysis failed for {file_path}: {e}")
            return None

    def _determine_compliance_level(self, line_count: int) -> ComplianceLevel:
        """Determine compliance level based on line count."""
        if line_count <= 400:
            return ComplianceLevel.COMPLIANT
        elif line_count <= 600:
            return ComplianceLevel.MINOR_VIOLATION
        elif line_count <= 1000:
            return ComplianceLevel.MAJOR_VIOLATION
        else:
            return ComplianceLevel.CRITICAL_VIOLATION

    def _get_violation_type(self, compliance_level: ComplianceLevel) -> str:
        """Get violation type description."""
        violation_types = {
            ComplianceLevel.MINOR_VIOLATION: "Minor V2 Violation",
            ComplianceLevel.MAJOR_VIOLATION: "Major V2 Violation",
            ComplianceLevel.CRITICAL_VIOLATION: "Critical V2 Violation",
        }
        return violation_types.get(compliance_level, "Unknown")

    def _get_severity(self, compliance_level: ComplianceLevel) -> str:
        """Get severity level."""
        severity_levels = {
            ComplianceLevel.MINOR_VIOLATION: "medium",
            ComplianceLevel.MAJOR_VIOLATION: "high",
            ComplianceLevel.CRITICAL_VIOLATION: "critical",
        }
        return severity_levels.get(compliance_level, "unknown")

    def _get_recommendations(self, compliance_level: ComplianceLevel, line_count: int) -> list[str]:
        """Get recommendations for fixing violations."""
        recommendations = []

        if compliance_level == ComplianceLevel.MINOR_VIOLATION:
            recommendations.extend(
                [
                    "Consider extracting utility functions to separate modules",
                    "Split large classes into smaller, focused components",
                    "Move configuration constants to external files",
                ]
            )
        elif compliance_level == ComplianceLevel.MAJOR_VIOLATION:
            recommendations.extend(
                [
                    "Refactor into multiple smaller files (≤400 lines each)",
                    "Apply architectural patterns (Factory, Repository, Service Layer)",
                    "Extract business logic into separate service modules",
                    "Create dedicated utility and helper modules",
                ]
            )
        elif compliance_level == ComplianceLevel.CRITICAL_VIOLATION:
            recommendations.extend(
                [
                    "IMMEDIATE REFACTORING REQUIRED",
                    "Split into multiple files with clear separation of concerns",
                    "Apply comprehensive architectural patterns",
                    "Consider breaking into microservices or modules",
                    "Implement comprehensive testing strategy",
                ]
            )

        # Add specific recommendations based on line count
        if line_count > 1000:
            recommendations.append("CRITICAL: File exceeds 1000 lines - immediate action required")

        return recommendations

    async def _calculate_quality_metrics(self, file_path: str) -> QualityMetrics | None:
        """Calculate comprehensive quality metrics for file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            line_count = len(lines)

            # Calculate individual scores
            compliance_score = self._calculate_compliance_score(line_count)
            structure_score = self._calculate_structure_score(content)
            documentation_score = self._calculate_documentation_score(content)
            performance_score = self._calculate_performance_score(content)
            security_score = self._calculate_security_score(content)

            # Calculate overall score
            overall_score = (
                compliance_score * self.quality_weights[QualityStandard.V2_COMPLIANCE]
                + structure_score * self.quality_weights[QualityStandard.CODE_STRUCTURE]
                + documentation_score * self.quality_weights[QualityStandard.DOCUMENTATION]
                + performance_score * self.quality_weights[QualityStandard.PERFORMANCE]
                + security_score * self.quality_weights[QualityStandard.SECURITY]
            )

            # Get violations for this file
            file_violations = [v for v in self.violations if v.file_path == file_path]

            metrics = QualityMetrics(
                file_path=file_path,
                line_count=line_count,
                compliance_score=compliance_score,
                structure_score=structure_score,
                documentation_score=documentation_score,
                performance_score=performance_score,
                security_score=security_score,
                overall_score=overall_score,
                violations=file_violations,
            )

            return metrics

        except Exception as e:
            logger.error(f"❌ Quality metrics calculation failed for {file_path}: {e}")
            return None

    def _calculate_compliance_score(self, line_count: int) -> float:
        """Calculate V2 compliance score."""
        if line_count <= 400:
            return 100.0
        elif line_count <= 600:
            return 60.0
        elif line_count <= 1000:
            return 30.0
        else:
            return 0.0

    def _calculate_structure_score(self, content: str) -> float:
        """Calculate code structure score."""
        score = 100.0

        # Check for proper imports
        if not content.strip().startswith(("#!/usr/bin/env", "# -*- coding:", '"""', "'''")):
            score -= 10

        # Check for proper class/function structure
        lines = content.splitlines()
        class_count = sum(1 for line in lines if line.strip().startswith("class "))
        function_count = sum(1 for line in lines if line.strip().startswith("def "))

        if class_count > 10:  # Too many classes in one file
            score -= 20
        if function_count > 50:  # Too many functions in one file
            score -= 20

        return max(score, 0.0)

    def _calculate_documentation_score(self, content: str) -> float:
        """Calculate documentation score."""
        score = 100.0

        # Check for module docstring
        if not ('"""' in content[:200] or "'''" in content[:200]):
            score -= 30

        # Check for function/class docstrings
        lines = content.splitlines()
        docstring_count = sum(1 for line in lines if '"""' in line or "'''" in line)
        function_count = sum(1 for line in lines if line.strip().startswith("def "))

        if function_count > 0 and docstring_count < function_count * 0.5:
            score -= 25

        return max(score, 0.0)

    def _calculate_performance_score(self, content: str) -> float:
        """Calculate performance score."""
        score = 100.0

        # Check for performance anti-patterns
        if "time.sleep(" in content:
            score -= 10
        if "while True:" in content:
            score -= 15
        if content.count("import ") > 20:  # Too many imports
            score -= 10

        return max(score, 0.0)

    def _calculate_security_score(self, content: str) -> float:
        """Calculate security score."""
        score = 100.0

        # Check for security issues
        if "eval(" in content:
            score -= 50
        if "exec(" in content:
            score -= 50
        if "os.system(" in content:
            score -= 30
        if "subprocess.call(" in content:
            score -= 20

        return max(score, 0.0)

    def _generate_validation_report(
        self, violations: list[ComplianceViolation], quality_metrics: dict[str, QualityMetrics]
    ) -> dict[str, Any]:
        """Generate comprehensive validation report."""
        try:
            # Calculate summary statistics
            total_files = len(quality_metrics)
            compliant_files = sum(
                1 for metrics in quality_metrics.values() if metrics.compliance_score == 100.0
            )
            violation_count = len(violations)

            # Group violations by severity
            violations_by_severity = {}
            for violation in violations:
                severity = violation.severity
                if severity not in violations_by_severity:
                    violations_by_severity[severity] = []
                violations_by_severity[severity].append(violation)

            # Calculate average quality scores
            avg_scores = {}
            if quality_metrics:
                avg_scores = {
                    "compliance": sum(m.compliance_score for m in quality_metrics.values())
                    / len(quality_metrics),
                    "structure": sum(m.structure_score for m in quality_metrics.values())
                    / len(quality_metrics),
                    "documentation": sum(m.documentation_score for m in quality_metrics.values())
                    / len(quality_metrics),
                    "performance": sum(m.performance_score for m in quality_metrics.values())
                    / len(quality_metrics),
                    "security": sum(m.security_score for m in quality_metrics.values())
                    / len(quality_metrics),
                    "overall": sum(m.overall_score for m in quality_metrics.values())
                    / len(quality_metrics),
                }

            report = {
                "summary": {
                    "total_files_analyzed": total_files,
                    "compliant_files": compliant_files,
                    "violation_count": violation_count,
                    "compliance_rate": (
                        (compliant_files / total_files * 100) if total_files > 0 else 0
                    ),
                    "average_quality_score": avg_scores.get("overall", 0),
                    "validation_timestamp": datetime.now().isoformat(),
                },
                "violations": {
                    "by_severity": {
                        severity: [
                            {
                                "file_path": v.file_path,
                                "line_count": v.line_count,
                                "violation_type": v.violation_type,
                                "recommendations": v.recommendations,
                            }
                            for v in violations_list
                        ]
                        for severity, violations_list in violations_by_severity.items()
                    },
                    "total_count": violation_count,
                },
                "quality_metrics": {
                    "average_scores": avg_scores,
                    "files": {
                        path: {
                            "line_count": metrics.line_count,
                            "compliance_score": metrics.compliance_score,
                            "overall_score": metrics.overall_score,
                            "violation_count": len(metrics.violations),
                        }
                        for path, metrics in quality_metrics.items()
                    },
                },
                "recommendations": self._generate_global_recommendations(
                    violations, quality_metrics
                ),
            }

            return report

        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            return {"error": str(e)}

    def _generate_global_recommendations(
        self, violations: list[ComplianceViolation], quality_metrics: dict[str, QualityMetrics]
    ) -> list[str]:
        """Generate global recommendations based on analysis."""
        recommendations = []

        if violations:
            critical_violations = [
                v for v in violations if v.compliance_level == ComplianceLevel.CRITICAL_VIOLATION
            ]
            major_violations = [
                v for v in violations if v.compliance_level == ComplianceLevel.MAJOR_VIOLATION
            ]

            if critical_violations:
                recommendations.append(
                    f"URGENT: {len(critical_violations)} critical V2 violations require immediate refactoring"
                )

            if major_violations:
                recommendations.append(
                    f"HIGH PRIORITY: {len(major_violations)} major V2 violations need architectural refactoring"
                )

            recommendations.append(
                "Apply architectural patterns (Factory, Repository, Service Layer) to large files"
            )
            recommendations.append("Extract utility functions and constants to separate modules")
            recommendations.append("Implement comprehensive testing for refactored modules")

        # Quality recommendations
        if quality_metrics:
            avg_overall = sum(m.overall_score for m in quality_metrics.values()) / len(
                quality_metrics
            )
            if avg_overall < 70:
                recommendations.append(
                    "Overall quality score below 70% - comprehensive code review recommended"
                )

            low_docs = [m for m in quality_metrics.values() if m.documentation_score < 60]
            if low_docs:
                recommendations.append(f"{len(low_docs)} files need improved documentation")

        return recommendations

    def _notify_web_interface(self, event_type: str, data: dict[str, Any]):
        """Notify web interface of validation events."""
        try:
            for callback in self.web_interface_callbacks:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"❌ Web interface callback error: {e}")
        except Exception as e:
            logger.error(f"❌ Web interface notification failed: {e}")

    def add_web_interface_callback(self, callback):
        """Add web interface callback for real-time updates."""
        self.web_interface_callbacks.append(callback)

    def get_validation_summary(self) -> dict[str, Any]:
        """Get current validation summary for web interface."""
        return {
            "total_violations": len(self.violations),
            "violations_by_severity": {
                severity: len([v for v in self.violations if v.severity == severity])
                for severity in ["medium", "high", "critical"]
            },
            "quality_metrics_count": len(self.quality_metrics),
            "last_validation": datetime.now().isoformat(),
        }


# Global instance for web interface integration
_v2_compliance_validator = None


def get_v2_compliance_validator() -> V2ComplianceValidator:
    """Get the global V2 compliance validator instance."""
    global _v2_compliance_validator
    if _v2_compliance_validator is None:
        _v2_compliance_validator = V2ComplianceValidator()
    return _v2_compliance_validator
