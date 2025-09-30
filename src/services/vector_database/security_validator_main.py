#!/usr/bin/env python3
"""
Vector Database Security Validator - Main
=========================================

Main security validator class for vector database integration.

Author: Agent-2 (Security Specialist)
License: MIT
"""

import logging
from typing import Any

from .security_validator_core import VectorDatabaseSecurityCore

logger = logging.getLogger(__name__)


class VectorDatabaseSecurityValidator:
    """Main security validator for vector database integration."""

    def __init__(self):
        """Initialize security validator."""
        self.core = VectorDatabaseSecurityCore()
        self.security_tests: list[dict[str, Any]] = []
        self.vulnerabilities: list[str] = []
        self.security_score = 0.0

        logger.info("Vector Database Security Validator initialized")

    def validate_security(self) -> dict[str, Any]:
        """Perform comprehensive security validation."""
        try:
            logger.info("🔒 Starting vector database security validation")

            # Delegate to core validation
            validation_results = self.core.validate_security()

            # Update instance variables
            self.security_score = validation_results.get("security_score", 0.0)
            self.vulnerabilities = validation_results.get("vulnerabilities", [])
            self.security_tests = [
                validation_results.get("data_validation", {}),
                validation_results.get("access_control", {}),
                validation_results.get("error_handling", {}),
                validation_results.get("input_validation", {}),
                validation_results.get("configuration_security", {}),
            ]

            logger.info(f"🔒 Security validation completed: {self.security_score}%")
            return validation_results

        except Exception as e:
            logger.error(f"Security validation failed: {e}")
            return {"error": str(e), "security_score": 0, "status": "error"}

    def get_security_score(self) -> float:
        """Get current security score."""
        return self.security_score

    def get_vulnerabilities(self) -> list[str]:
        """Get list of identified vulnerabilities."""
        return self.vulnerabilities

    def get_security_tests(self) -> list[dict[str, Any]]:
        """Get list of security test results."""
        return self.security_tests

    def add_vulnerability(self, vulnerability: str) -> None:
        """Add a vulnerability to the list."""
        if vulnerability not in self.vulnerabilities:
            self.vulnerabilities.append(vulnerability)
            logger.warning(f"Vulnerability added: {vulnerability}")

    def clear_vulnerabilities(self) -> None:
        """Clear all vulnerabilities."""
        self.vulnerabilities.clear()
        logger.info("Vulnerabilities cleared")

    def generate_security_report(self) -> dict[str, Any]:
        """Generate comprehensive security report."""
        try:
            validation_results = self.validate_security()

            report = {
                "summary": {
                    "security_score": self.security_score,
                    "status": validation_results.get("status", "unknown"),
                    "total_vulnerabilities": len(self.vulnerabilities),
                    "total_tests": len(self.security_tests),
                },
                "detailed_results": validation_results,
                "recommendations": validation_results.get("recommendations", []),
                "next_steps": self._generate_next_steps(),
            }

            return report

        except Exception as e:
            logger.error(f"Security report generation failed: {e}")
            return {"error": str(e)}

    def _generate_next_steps(self) -> list[str]:
        """Generate next steps based on security assessment."""
        next_steps = []

        if self.security_score < 60:
            next_steps.extend(
                [
                    "🔴 IMMEDIATE: Conduct comprehensive security audit",
                    "🔴 IMMEDIATE: Implement critical security fixes",
                    "🔴 IMMEDIATE: Review and update security policies",
                    "🔴 IMMEDIATE: Conduct penetration testing",
                ]
            )
        elif self.security_score < 80:
            next_steps.extend(
                [
                    "🟡 PRIORITY: Address identified vulnerabilities",
                    "🟡 PRIORITY: Implement recommended security measures",
                    "🟡 PRIORITY: Conduct security training for team",
                    "🟡 PRIORITY: Update security documentation",
                ]
            )
        else:
            next_steps.extend(
                [
                    "🟢 MAINTAIN: Continue regular security assessments",
                    "🟢 MAINTAIN: Monitor for new vulnerabilities",
                    "🟢 MAINTAIN: Keep security tools updated",
                    "🟢 MAINTAIN: Review security policies quarterly",
                ]
            )

        # Add specific next steps based on vulnerabilities
        if self.vulnerabilities:
            next_steps.append("🔍 SPECIFIC: Address the following vulnerabilities:")
            for vulnerability in self.vulnerabilities[:3]:  # Top 3 vulnerabilities
                next_steps.append(f"  - {vulnerability}")

        return next_steps

    def export_security_report(self, format: str = "json") -> str:
        """Export security report in specified format."""
        try:
            report = self.generate_security_report()

            if format.lower() == "json":
                import json

                return json.dumps(report, indent=2)
            elif format.lower() == "yaml":
                import yaml

                return yaml.dump(report, default_flow_style=False)
            else:
                # Default to text format
                return self._format_text_report(report)

        except Exception as e:
            logger.error(f"Security report export failed: {e}")
            return f"Export failed: {e}"

    def _format_text_report(self, report: dict[str, Any]) -> str:
        """Format security report as text."""
        try:
            lines = []
            lines.append("=" * 60)
            lines.append("VECTOR DATABASE SECURITY REPORT")
            lines.append("=" * 60)
            lines.append("")

            # Summary section
            summary = report.get("summary", {})
            lines.append("SUMMARY:")
            lines.append(f"  Security Score: {summary.get('security_score', 0):.1f}%")
            lines.append(f"  Status: {summary.get('status', 'unknown')}")
            lines.append(f"  Vulnerabilities: {summary.get('total_vulnerabilities', 0)}")
            lines.append(f"  Tests Run: {summary.get('total_tests', 0)}")
            lines.append("")

            # Recommendations section
            recommendations = report.get("recommendations", [])
            if recommendations:
                lines.append("RECOMMENDATIONS:")
                for rec in recommendations:
                    lines.append(f"  {rec}")
                lines.append("")

            # Next steps section
            next_steps = report.get("next_steps", [])
            if next_steps:
                lines.append("NEXT STEPS:")
                for step in next_steps:
                    lines.append(f"  {step}")
                lines.append("")

            lines.append("=" * 60)
            return "\n".join(lines)

        except Exception as e:
            logger.error(f"Text report formatting failed: {e}")
            return f"Report formatting failed: {e}"


# Convenience function for quick security validation
def validate_vector_database_security() -> dict[str, Any]:
    """Quick security validation function."""
    validator = VectorDatabaseSecurityValidator()
    return validator.validate_security()


# Convenience function for generating security report
def generate_security_report() -> dict[str, Any]:
    """Quick security report generation function."""
    validator = VectorDatabaseSecurityValidator()
    return validator.generate_security_report()
