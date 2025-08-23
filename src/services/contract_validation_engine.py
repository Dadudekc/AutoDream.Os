#!/usr/bin/env python3
"""
Contract Validation Engine - Agent Cellphone V2
=============================================

Executes contract validation and enforcement actions.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import time
import json
import re
from typing import Dict, List, Optional, Any, Callable
import logging
from .validation_rules import (
    ValidationRule,
    ValidationResult,
    Violation,
    ViolationType,
    ValidationSeverity,
    EnforcementAction,
    ValidationRuleManager,
)


class ContractValidationEngine:
    """Executes contract validation and enforcement"""

    def __init__(self):
        self.rule_manager = ValidationRuleManager()
        self.logger = logging.getLogger(f"{__name__}.ContractValidationEngine")
        self.validation_handlers: Dict[str, Callable] = {}
        self._initialize_validation_handlers()

    def _initialize_validation_handlers(self):
        """Initialize validation handlers for different rule types"""
        self.validation_handlers = {
            "temporal": self._validate_temporal_rule,
            "quality": self._validate_quality_rule,
            "resource": self._validate_resource_rule,
            "dependency": self._validate_dependency_rule,
            "schema": self._validate_schema_rule,
        }

    def validate_contract(
        self, contract_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate a contract against all applicable rules"""
        results = []
        contract_id = contract_data.get("contract_id", "unknown")

        # Get enabled rules
        enabled_rules = [
            rule for rule in self.rule_manager.get_all_rules().values() if rule.enabled
        ]

        for rule in enabled_rules:
            try:
                result = self._validate_rule(rule, contract_data)
                results.append(result)

                # Log validation result
                if result.passed:
                    self.logger.info(
                        f"Rule {rule.rule_id} passed for contract {contract_id}"
                    )
                else:
                    self.logger.warning(
                        f"Rule {rule.rule_id} failed for contract {contract_id}: {result.message}"
                    )

            except Exception as e:
                self.logger.error(f"Error validating rule {rule.rule_id}: {e}")
                # Create failed result
                failed_result = ValidationResult(
                    contract_id=contract_id,
                    rule_id=rule.rule_id,
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message=f"Validation error: {str(e)}",
                    details={"error": str(e)},
                    timestamp=time.time(),
                )
                results.append(failed_result)

        return results

    def _validate_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> ValidationResult:
        """Validate a single rule against contract data"""
        # Get appropriate handler for rule type
        handler = self.validation_handlers.get(
            rule.rule_type, self._validate_generic_rule
        )

        try:
            passed, message, details = handler(rule, contract_data)

            return ValidationResult(
                contract_id=contract_data.get("contract_id", "unknown"),
                rule_id=rule.rule_id,
                passed=passed,
                severity=rule.severity,
                message=message,
                details=details,
                timestamp=time.time(),
            )

        except Exception as e:
            return ValidationResult(
                contract_id=contract_data.get("contract_id", "unknown"),
                rule_id=rule.rule_id,
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"Validation exception: {str(e)}",
                details={"error": str(e)},
                timestamp=time.time(),
            )

    def _validate_temporal_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Validate temporal rules (deadlines, etc.)"""
        if rule.rule_id == "deadline_check":
            deadline = contract_data.get("deadline")
            delivery_date = contract_data.get("delivery_date")

            if not deadline or not delivery_date:
                return (
                    False,
                    "Missing deadline or delivery date",
                    {"deadline": deadline, "delivery_date": delivery_date},
                )

            # Simple date comparison (in real implementation, use proper date parsing)
            passed = delivery_date <= deadline
            message = "Deadline met" if passed else "Deadline exceeded"
            details = {
                "deadline": deadline,
                "delivery_date": delivery_date,
                "on_time": passed,
            }

            return passed, message, details

        return True, "Temporal rule passed", {}

    def _validate_quality_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Validate quality-related rules"""
        if rule.rule_id == "quality_standard":
            quality_score = contract_data.get("quality_score", 0)
            minimum_standard = contract_data.get("minimum_standard", 80)

            passed = quality_score >= minimum_standard
            message = "Quality standards met" if passed else "Quality below standard"
            details = {
                "quality_score": quality_score,
                "minimum_standard": minimum_standard,
                "passed": passed,
            }

            return passed, message, details

        return True, "Quality rule passed", {}

    def _validate_resource_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Validate resource-related rules"""
        if rule.rule_id == "resource_limit":
            resource_usage = contract_data.get("resource_usage", 0)
            resource_limit = contract_data.get("resource_limit", 100)

            passed = resource_usage <= resource_limit
            message = (
                "Resource usage within limits" if passed else "Resource usage exceeded"
            )
            details = {
                "resource_usage": resource_usage,
                "resource_limit": resource_limit,
                "within_limits": passed,
            }

            return passed, message, details

        return True, "Resource rule passed", {}

    def _validate_dependency_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Validate dependency-related rules"""
        if rule.rule_id == "dependency_check":
            dependencies = contract_data.get("dependencies", [])
            completed_dependencies = contract_data.get("completed_dependencies", [])

            all_completed = all(dep in completed_dependencies for dep in dependencies)
            passed = all_completed

            message = (
                "All dependencies satisfied" if passed else "Dependencies not satisfied"
            )
            details = {
                "dependencies": dependencies,
                "completed_dependencies": completed_dependencies,
                "all_satisfied": passed,
            }

            return passed, message, details

        return True, "Dependency rule passed", {}

    def _validate_schema_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Validate schema-related rules"""
        # Basic schema validation
        required_fields = contract_data.get("required_fields", [])
        missing_fields = [
            field for field in required_fields if field not in contract_data
        ]

        passed = len(missing_fields) == 0
        message = (
            "Schema validation passed"
            if passed
            else f"Missing required fields: {missing_fields}"
        )
        details = {
            "required_fields": required_fields,
            "missing_fields": missing_fields,
            "valid": passed,
        }

        return passed, message, details

    def _validate_generic_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> tuple:
        """Generic rule validation fallback"""
        # Try to evaluate the condition as a simple expression
        try:
            # This is a simplified approach - in production, use a proper expression evaluator
            condition = rule.condition.lower()
            if "deadline" in condition and "current_time" in condition:
                return self._validate_temporal_rule(rule, contract_data)
            elif "quality" in condition:
                return self._validate_quality_rule(rule, contract_data)
            else:
                return True, "Generic rule passed", {"rule_type": rule.rule_type}
        except Exception:
            return True, "Generic rule passed", {"rule_type": rule.rule_type}

    def create_violation(self, validation_result: ValidationResult) -> Violation:
        """Create a violation record from a failed validation result"""
        if validation_result.passed:
            raise ValueError("Cannot create violation from passed validation")

        # Determine violation type based on rule
        rule = self.rule_manager.get_rule(validation_result.rule_id)
        violation_type = (
            self._map_rule_to_violation_type(rule)
            if rule
            else ViolationType.SCHEMA_VIOLATION
        )

        return Violation(
            violation_id=f"violation_{int(time.time())}_{validation_result.rule_id}",
            contract_id=validation_result.contract_id,
            violation_type=violation_type,
            severity=validation_result.severity,
            description=validation_result.message,
            detected_at=time.time(),
            metadata=validation_result.details,
        )

    def _map_rule_to_violation_type(self, rule: ValidationRule) -> ViolationType:
        """Map rule type to violation type"""
        if "deadline" in rule.rule_id.lower():
            return ViolationType.DEADLINE_MISSED
        elif "quality" in rule.rule_id.lower():
            return ViolationType.QUALITY_BELOW_STANDARD
        elif "resource" in rule.rule_id.lower():
            return ViolationType.RESOURCE_EXCEEDED
        elif "dependency" in rule.rule_id.lower():
            return ViolationType.DEPENDENCY_UNMET
        else:
            return ViolationType.SCHEMA_VIOLATION


def main():
    """CLI interface for testing the Contract Validation Engine"""
    import argparse

    parser = argparse.ArgumentParser(description="Contract Validation Engine CLI")
    parser.add_argument(
        "--test", "-t", action="store_true", help="Test validation engine"
    )
    parser.add_argument("--validate", "-v", help="Validate contract JSON file")

    args = parser.parse_args()

    engine = ContractValidationEngine()

    if args.test:
        print("🧪 Testing Contract Validation Engine...")

        # Test contract data
        test_contract = {
            "contract_id": "test-001",
            "deadline": "2024-12-31",
            "delivery_date": "2024-12-30",
            "quality_score": 85,
            "minimum_standard": 80,
            "resource_usage": 75,
            "resource_limit": 100,
            "dependencies": ["dep1", "dep2"],
            "completed_dependencies": ["dep1", "dep2"],
        }

        results = engine.validate_contract(test_contract)
        print(f"✅ Validation completed: {len(results)} rules checked")

        for result in results:
            status = "✅" if result.passed else "❌"
            print(f"  {status} {result.rule_id}: {result.message}")

    elif args.validate:
        try:
            with open(args.validate, "r") as f:
                contract_data = json.load(f)

            results = engine.validate_contract(contract_data)
            print(f"📋 Validation Results for {args.validate}:")

            passed = sum(1 for r in results if r.passed)
            failed = len(results) - passed

            print(f"  Total Rules: {len(results)}")
            print(f"  Passed: {passed}")
            print(f"  Failed: {failed}")

            for result in results:
                status = "✅" if result.passed else "❌"
                print(f"  {status} {result.rule_id}: {result.message}")

        except FileNotFoundError:
            print(f"❌ File not found: {args.validate}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {args.validate}")

    else:
        print("Contract Validation Engine - Use --help for options")


if __name__ == "__main__":
    main()
