from typing import Dict, List, Optional, Any
import json
import logging

    import argparse
from .contract_validation_engine import ContractValidationEngine
from .validation_rules import (
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Contract Validation Service - Agent Cellphone V2
===============================================

Coordinator service for contract validation and enforcement.
Follows Single Responsibility Principle with 200 LOC limit.
"""


    ValidationRule,
    ValidationResult,
    Violation,
    ViolationType,
    ValidationSeverity,
    EnforcementAction,
    ValidationRuleManager,
)


class ContractValidationService:
    """Coordinator service for contract validation and enforcement"""

    def __init__(self):
        self.rule_manager = ValidationRuleManager()
        self.validation_engine = ContractValidationEngine()
        self.logger = logging.getLogger(f"{__name__}.ContractValidationService")
        self.violations: Dict[str, Violation] = {}

    def validate_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a contract and return comprehensive results"""
        try:
            validation_results = self.validation_engine.validate_contract(contract_data)

            # Process results and create violations
            violations = []
            for result in validation_results:
                if not result.passed:
                    violation = self.validation_engine.create_violation(result)
                    violations.append(violation)
                    self.violations[violation.violation_id] = violation

            # Prepare response
            response = {
                "contract_id": contract_data.get("contract_id", "unknown"),
                "validation_timestamp": time.time(),
                "total_rules": len(validation_results),
                "passed_rules": sum(1 for r in validation_results if r.passed),
                "failed_rules": len(validation_results)
                - sum(1 for r in validation_results if r.passed),
                "validation_results": [
                    {
                        "rule_id": r.rule_id,
                        "passed": r.passed,
                        "severity": r.severity.value,
                        "message": r.message,
                    }
                    for r in validation_results
                ],
                "violations": [
                    {
                        "violation_id": v.violation_id,
                        "type": v.violation_type.value,
                        "severity": v.severity.value,
                        "description": v.description,
                    }
                    for v in violations
                ],
            }

            self.logger.info(
                f"Contract {contract_data.get('contract_id')} validation completed: {response['passed_rules']}/{response['total_rules']} rules passed"
            )
            return response

        except Exception as e:
            self.logger.error(f"Contract validation failed: {e}")
            return {
                "contract_id": contract_data.get("contract_id", "unknown"),
                "validation_timestamp": time.time(),
                "error": str(e),
                "validation_results": [],
                "violations": [],
            }

    def get_validation_rules(
        self, rule_type: Optional[str] = None, severity: Optional[str] = None
    ) -> List[ValidationRule]:
        """Get validation rules with optional filtering"""
        if rule_type and severity:
            try:
                sev_enum = ValidationSeverity(severity)
                return self.rule_manager.get_rules_by_type(rule_type)
            except ValueError:
                return []
        elif rule_type:
            return self.rule_manager.get_rules_by_type(rule_type)
        elif severity:
            try:
                sev_enum = ValidationSeverity(severity)
                return self.rule_manager.get_rules_by_type(severity)
            except ValueError:
                return []
        else:
            return list(self.rule_manager.get_all_rules().values())

    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a new validation rule"""
        return self.rule_manager.add_rule(rule)

    def get_violations(
        self, contract_id: Optional[str] = None, violation_type: Optional[str] = None
    ) -> List[Violation]:
        """Get violations with optional filtering"""
        violations = list(self.violations.values())

        if contract_id:
            violations = [v for v in violations if v.contract_id == contract_id]

        if violation_type:
            try:
                vtype_enum = ViolationType(violation_type)
                violations = [v for v in violations if v.violation_type == vtype_enum]
            except ValueError:
                violations = []

        return violations

    def resolve_violation(self, violation_id: str, resolution_notes: str = "") -> bool:
        """Mark a violation as resolved"""
        if violation_id in self.violations:
            violation = self.violations[violation_id]
            violation.resolved_at = time.time()
            violation.metadata = violation.metadata or {}
            violation.metadata["resolution_notes"] = resolution_notes
            self.logger.info(f"Violation {violation_id} resolved")
            return True
        return False


def main():
    """CLI interface for testing the Contract Validation Service"""

    parser = argparse.ArgumentParser(description="Contract Validation Service CLI")
    parser.add_argument("--test", "-t", action="store_true", help="Test the service")
    parser.add_argument("--validate", "-v", help="Validate contract JSON file")
    parser.add_argument(
        "--rules", "-r", action="store_true", help="Show validation rules"
    )
    parser.add_argument(
        "--violations", "-i", action="store_true", help="Show violations"
    )

    args = parser.parse_args()

    service = ContractValidationService()

    if args.test:
        print("🧪 Testing Contract Validation Service...")

        test_contract = {
            "contract_id": "test-001",
            "deadline": "2024-12-31",
            "delivery_date": "2024-12-30",
            "quality_score": 85,
            "minimum_standard": 80,
        }

        result = service.validate_contract(test_contract)
        print(
            f"✅ Validation test completed: {result['passed_rules']}/{result['total_rules']} rules passed"
        )

    elif args.validate:
        try:
            with open(args.validate, "r") as f:
                contract_data = json.load(f)

            result = service.validate_contract(contract_data)
            print(f"📋 Validation Results:")
            print(f"  Contract: {result['contract_id']}")
            print(f"  Rules: {result['passed_rules']}/{result['total_rules']} passed")
            print(f"  Violations: {len(result['violations'])}")

        except FileNotFoundError:
            print(f"❌ File not found: {args.validate}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {args.validate}")

    elif args.rules:
        rules = service.get_validation_rules()
        print("📋 Validation Rules:")
        for rule in rules:
            status = "✅" if rule.enabled else "❌"
            print(f"  {status} {rule.rule_id}: {rule.name} ({rule.severity.value})")

    elif args.violations:
        violations = service.get_violations()
        print("📋 Violations:")
        for violation in violations:
            status = "🔴" if not violation.resolved_at else "🟢"
            print(f"  {status} {violation.violation_id}: {violation.description}")

    else:
        print("Contract Validation Service - Use --help for options")


if __name__ == "__main__":
    main()
