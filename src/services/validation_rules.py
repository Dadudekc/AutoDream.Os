#!/usr/bin/env python3
"""
Validation Rules - Agent Cellphone V2
====================================

Defines validation rules, violation types, and enforcement actions.
Follows Single Responsibility Principle with 200 LOC limit.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ViolationType(Enum):
    """Types of contract violations"""

    SCHEMA_VIOLATION = "schema_violation"
    DEADLINE_MISSED = "deadline_missed"
    DELIVERABLE_MISSING = "deliverable_missing"
    QUALITY_BELOW_STANDARD = "quality_below_standard"
    UNAUTHORIZED_ACTION = "unauthorized_action"
    RESOURCE_EXCEEDED = "resource_exceeded"
    DEPENDENCY_UNMET = "dependency_unmet"


class EnforcementAction(Enum):
    """Enforcement actions for violations"""

    WARNING = "warning"
    SUSPENSION = "suspension"
    TERMINATION = "termination"
    PENALTY_APPLY = "penalty_apply"
    ESCALATION = "escalation"
    NOTIFICATION = "notification"
    AUTOMATIC_CORRECTION = "automatic_correction"


class ValidationSeverity(Enum):
    """Validation issue severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationRule:
    """Contract validation rule definition"""

    rule_id: str
    name: str
    description: str
    rule_type: str
    condition: str
    severity: ValidationSeverity
    enforcement_action: EnforcementAction
    enabled: bool = True


@dataclass
class ValidationResult:
    """Validation result for a contract"""

    contract_id: str
    rule_id: str
    passed: bool
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any]
    timestamp: float


@dataclass
class Violation:
    """Contract violation record"""

    violation_id: str
    contract_id: str
    violation_type: ViolationType
    severity: ValidationSeverity
    description: str
    detected_at: float
    resolved_at: Optional[float] = None
    enforcement_applied: Optional[EnforcementAction] = None
    metadata: Optional[Dict[str, Any]] = None


class ValidationRuleManager:
    """Manages validation rules and their configurations"""

    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self._initialize_default_rules()

    def _initialize_default_rules(self):
        """Initialize default validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="deadline_check",
                name="Deadline Compliance",
                description="Ensure all deliverables meet deadlines",
                rule_type="temporal",
                condition="delivery_date <= deadline",
                severity=ValidationSeverity.ERROR,
                enforcement_action=EnforcementAction.WARNING,
            ),
            ValidationRule(
                rule_id="quality_standard",
                name="Quality Standards",
                description="Verify deliverables meet quality requirements",
                rule_type="quality",
                condition="quality_score >= minimum_standard",
                severity=ValidationSeverity.WARNING,
                enforcement_action=EnforcementAction.NOTIFICATION,
            ),
            ValidationRule(
                rule_id="resource_limit",
                name="Resource Limits",
                description="Check resource usage within allocated limits",
                rule_type="resource",
                condition="resource_usage <= resource_limit",
                severity=ValidationSeverity.WARNING,
                enforcement_action=EnforcementAction.WARNING,
            ),
            ValidationRule(
                rule_id="dependency_check",
                name="Dependency Validation",
                description="Ensure all dependencies are satisfied",
                rule_type="dependency",
                condition="all_dependencies_completed == true",
                severity=ValidationSeverity.ERROR,
                enforcement_action=EnforcementAction.SUSPENSION,
            ),
        ]

        for rule in default_rules:
            self.rules[rule.rule_id] = rule

    def add_rule(self, rule: ValidationRule) -> bool:
        """Add a new validation rule"""
        if rule.rule_id in self.rules:
            return False

        self.rules[rule.rule_id] = rule
        return True

    def get_rule(self, rule_id: str) -> Optional[ValidationRule]:
        """Get a validation rule by ID"""
        return self.rules.get(rule_id)

    def get_all_rules(self) -> Dict[str, ValidationRule]:
        """Get all validation rules"""
        return self.rules.copy()

    def get_rules_by_type(self, rule_type: str) -> List[ValidationRule]:
        """Get rules filtered by type"""
        return [rule for rule in self.rules.values() if rule.rule_type == rule_type]

    def get_rules_by_severity(
        self, severity: ValidationSeverity
    ) -> List[ValidationRule]:
        """Get rules filtered by severity"""
        return [rule for rule in self.rules.values() if rule.severity == severity]

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a validation rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            return True
        return False

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a validation rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            return True
        return False

    def update_rule(self, rule_id: str, **kwargs) -> bool:
        """Update a validation rule"""
        if rule_id not in self.rules:
            return False

        rule = self.rules[rule_id]
        for key, value in kwargs.items():
            if hasattr(rule, key):
                setattr(rule, key, value)

        return True


def main():
    """CLI interface for testing the Validation Rules"""
    import argparse

    parser = argparse.ArgumentParser(description="Validation Rules CLI")
    parser.add_argument("--list", "-l", action="store_true", help="List all rules")
    parser.add_argument("--rule", "-r", help="Show specific rule details")
    parser.add_argument("--type", "-t", help="Filter rules by type")
    parser.add_argument("--severity", "-s", help="Filter rules by severity")
    parser.add_argument("--enable", help="Enable a rule")
    parser.add_argument("--disable", help="Disable a rule")

    args = parser.parse_args()

    manager = ValidationRuleManager()

    if args.list:
        rules = manager.get_all_rules()
        print("📋 All Validation Rules:")
        for rule_id, rule in rules.items():
            status = "✅" if rule.enabled else "❌"
            print(f"  {status} {rule_id}: {rule.name} ({rule.severity.value})")

    elif args.rule:
        rule = manager.get_rule(args.rule)
        if rule:
            print(f"📋 Rule: {rule.name}")
            print(f"  ID: {rule.rule_id}")
            print(f"  Type: {rule.rule_type}")
            print(f"  Severity: {rule.severity.value}")
            print(f"  Action: {rule.enforcement_action.value}")
            print(f"  Enabled: {rule.enabled}")
            print(f"  Description: {rule.description}")
        else:
            print(f"❌ Rule '{args.rule}' not found")

    elif args.type:
        rules = manager.get_rules_by_type(args.type)
        print(f"📋 Rules by Type '{args.type}':")
        for rule in rules:
            status = "✅" if rule.enabled else "❌"
            print(f"  {status} {rule.rule_id}: {rule.name}")

    elif args.severity:
        try:
            severity = ValidationSeverity(args.severity)
            rules = manager.get_rules_by_severity(severity)
            print(f"📋 Rules by Severity '{args.severity}':")
            for rule in rules:
                status = "✅" if rule.enabled else "❌"
                print(f"  {status} {rule.rule_id}: {rule.name}")
        except ValueError:
            print(f"❌ Invalid severity: {args.severity}")

    elif args.enable:
        if manager.enable_rule(args.enable):
            print(f"✅ Rule '{args.enable}' enabled")
        else:
            print(f"❌ Rule '{args.enable}' not found")

    elif args.disable:
        if manager.disable_rule(args.disable):
            print(f"✅ Rule '{args.disable}' disabled")
        else:
            print(f"❌ Rule '{args.disable}' not found")

    else:
        print("Validation Rules - Use --help for options")


if __name__ == "__main__":
    main()
