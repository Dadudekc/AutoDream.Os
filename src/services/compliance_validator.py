"""
Compliance Validator - V2 Compliance Module
==========================================

Validates architectural compliance following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any, Dict, List
from .architectural_models import ArchitecturalPrinciple, ComplianceValidationResult


class ComplianceValidator:
    """Validates architectural compliance for agents."""

    def validate_agent_compliance(
        self,
        agent_id: str,
        principle: ArchitecturalPrinciple,
        code_changes: List[str]
    ) -> ComplianceValidationResult:
        """Validate that an agent's changes comply with their assigned principle."""

        issues = []
        recommendations = []

        for change in code_changes:
            # Check for common violations based on principle
            if principle == ArchitecturalPrinciple.SINGLE_RESPONSIBILITY:
                validation_issues = self._validate_single_responsibility(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.DONT_REPEAT_YOURSELF:
                validation_issues = self._validate_dry_principle(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID:
                validation_issues = self._validate_kiss_principle(change)
                issues.extend(validation_issues)
            elif principle == ArchitecturalPrinciple.OPEN_CLOSED:
                validation_issues = self._validate_open_closed(change)
                issues.extend(validation_issues)

        # Generate recommendations based on issues
        recommendations = self._generate_recommendations(principle, issues)

        return ComplianceValidationResult(
            agent_id=agent_id,
            principle=principle,
            compliant=len(issues) == 0,
            issues=issues,
            recommendations=recommendations,
            validated_at=self._get_current_timestamp()
        )

    def _validate_single_responsibility(self, change: str) -> List[str]:
        """Validate Single Responsibility Principle."""
        issues = []
        if "class" in change.lower() and len(change.split()) > 10:
            issues.append("Potential God class detected - class definition too complex")
        if change.count("def ") > 5:
            issues.append("Class has too many methods - consider splitting responsibilities")
        return issues

    def _validate_dry_principle(self, change: str) -> List[str]:
        """Validate DRY Principle."""
        issues = []
        if change.count("def ") > 5:
            issues.append("Multiple similar function definitions detected - consider abstraction")
        if len(change.split("\n")) > 100 and change.count("for ") > 3:
            issues.append("Repeated loop patterns detected - consider utility functions")
        return issues

    def _validate_kiss_principle(self, change: str) -> List[str]:
        """Validate KISS Principle."""
        issues = []
        if len(change.split("\n")) > 50:
            issues.append("Method too long - consider breaking into smaller functions")
        if change.count("if ") > 5:
            issues.append("Too many conditional statements - logic may be overcomplicated")
        if change.count("and ") + change.count("or ") > 3:
            issues.append("Complex boolean expressions - consider simplifying logic")
        return issues

    def _validate_open_closed(self, change: str) -> List[str]:
        """Validate Open-Closed Principle."""
        issues = []
        if "if " in change and "type" in change.lower():
            issues.append("Type checking with if statements - consider polymorphism")
        if "isinstance(" in change:
            issues.append("Runtime type checking - consider interface design")
        return issues

    def _generate_recommendations(
        self,
        principle: ArchitecturalPrinciple,
        issues: List[str]
    ) -> List[str]:
        """Generate recommendations based on validation issues."""
        recommendations = []

        for issue in issues:
            if "God class" in issue:
                recommendations.append("Extract smaller classes with single responsibilities")
            elif "too many methods" in issue:
                recommendations.append("Split class into multiple focused classes")
            elif "similar function" in issue:
                recommendations.append("Create base class or utility functions")
            elif "Method too long" in issue:
                recommendations.append("Break method into smaller, focused methods")
            elif "conditional statements" in issue:
                recommendations.append("Use strategy pattern or polymorphism")
            elif "boolean expressions" in issue:
                recommendations.append("Extract complex conditions into well-named methods")
            elif "type checking" in issue:
                recommendations.append("Implement proper inheritance or interface design")

        return recommendations

    def _get_current_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
