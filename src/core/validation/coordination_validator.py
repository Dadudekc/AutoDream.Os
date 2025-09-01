#!/usr/bin/env python3
"""
Coordination Validator - Agent Cellphone V2
=========================================

Refactored coordination validation engine for V2 compliance (300-line limit).

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, Any, List
from datetime import datetime

from .validation_models import ValidationIssue, ValidationSeverity, ValidationResult
from .validation_rules import ValidationRules
from .message_validator import MessageValidator
from .coordination_validator_core import CoordinationValidatorCore
from .performance_validator import PerformanceValidator
from .security_validator import SecurityValidator


class CoordinationValidator:
    """Refactored coordination validation engine."""

    def __init__(self, rules_dir: str = "src/core/validation/rules"):
        """Initialize the validation engine."""
        self.validation_history: List[ValidationIssue] = []

        # Initialize modular components
        self.rules = ValidationRules(rules_dir)
        self.message_validator = MessageValidator()
        self.coordination_validator = CoordinationValidatorCore()
        self.performance_validator = PerformanceValidator()
        self.security_validator = SecurityValidator()

    def validate_message_structure(self, message_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate message structure against rules."""
        return self.message_validator.validate_message_structure(message_data)

    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate coordination system configuration."""
        return self.coordination_validator.validate_coordination_system(system_data)

    def validate_performance_metrics(self, metrics_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate performance metrics and thresholds."""
        return self.performance_validator.validate_performance_metrics(metrics_data)

    def validate_security_compliance(self, security_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate security compliance requirements."""
        return self.security_validator.validate_security_compliance(security_data)

    def run_comprehensive_validation(self, target_system: str,
                                   validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive validation on a target system."""
        all_issues = []

        # Run all validation types
        all_issues.extend(self.validate_message_structure(validation_data.get('messages', {})))
        all_issues.extend(self.validate_coordination_system(validation_data.get('coordination', {})))
        all_issues.extend(self.validate_performance_metrics(validation_data.get('performance', {})))
        all_issues.extend(self.validate_security_compliance(validation_data.get('security', {})))

        # Store validation history
        self.validation_history.extend(all_issues)

        # Categorize issues by severity
        errors = [issue for issue in all_issues if issue.severity == ValidationSeverity.ERROR]
        warnings = [issue for issue in all_issues if issue.severity == ValidationSeverity.WARNING]
        info = [issue for issue in all_issues if issue.severity == ValidationSeverity.INFO]

        # Determine overall validation result
        if errors:
            overall_result = ValidationResult.FAIL
        elif warnings:
            overall_result = ValidationResult.WARNING
        else:
            overall_result = ValidationResult.PASS

        return {
            "target_system": target_system,
            "timestamp": datetime.now(),
            "overall_result": overall_result.value,
            "total_issues": len(all_issues),
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(info),
            "issues": all_issues,
            "validation_summary": {
                "passed": overall_result == ValidationResult.PASS,
                "has_errors": len(errors) > 0,
                "has_warnings": len(warnings) > 0,
                "compliance_score": self._calculate_compliance_score(all_issues)
            }
        }

    def _calculate_compliance_score(self, issues: List[ValidationIssue]) -> float:
        """Calculate compliance score based on issues."""
        if not issues:
            return 100.0

        total_issues = len(issues)
        error_weight = 3.0
        warning_weight = 1.0

        weighted_score = sum([
            error_weight if issue.severity == ValidationSeverity.ERROR else warning_weight
            for issue in issues
        ])

        max_possible_score = total_issues * error_weight
        compliance_score = max(0.0, 100.0 - (weighted_score / max_possible_score * 100.0))

        return round(compliance_score, 2)

    def get_validation_report(self, target_system: str = None) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        if target_system:
            system_issues = [issue for issue in self.validation_history
                           if issue.component == target_system]
        else:
            system_issues = self.validation_history

        return {
            "validation_summary": {
                "total_validations": len(self.validation_history),
                "target_system_validations": len(system_issues),
                "last_validation": self.validation_history[-1].timestamp if self.validation_history else None
            },
            "compliance_metrics": {
                "overall_compliance": self._calculate_compliance_score(self.validation_history),
                "system_compliance": self._calculate_compliance_score(system_issues) if system_issues else 100.0
            },
            "recent_issues": system_issues[-10:] if system_issues else []
        }
