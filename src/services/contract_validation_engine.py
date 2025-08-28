#!/usr/bin/env python3
"""
Contract Validation Engine - Agent Cellphone V2
=============================================

Orchestrates validation by coordinating criteria management,
rule evaluation and remediation. Criteria definitions live in
``validation_rules.py`` while the evaluation and remediation
logic are handled by dedicated modules.
"""
import json
import logging
from typing import Any, Dict, List

from .validation_rules import ValidationResult, Violation, ValidationRuleManager
from .validation_evaluator import ValidationEvaluator
from .validation_remediator import RemediationManager


class ContractValidationEngine:
    """Coordinate validation rule evaluation and remediation."""

    def __init__(
        self,
        rule_manager: ValidationRuleManager | None = None,
        evaluator: ValidationEvaluator | None = None,
        remediator: RemediationManager | None = None,
    ) -> None:
        self.rule_manager = rule_manager or ValidationRuleManager()
        self.evaluator = evaluator or ValidationEvaluator()
        self.remediator = remediator or RemediationManager(self.rule_manager)
        self.logger = logging.getLogger(f"{__name__}.ContractValidationEngine")

    # ------------------------------------------------------------------
    def validate_contract(
        self, contract_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate a contract against all enabled rules."""
        enabled_rules = [
            r for r in self.rule_manager.get_all_rules().values() if r.enabled
        ]
        results = self.evaluator.evaluate(enabled_rules, contract_data)
        contract_id = contract_data.get("contract_id", "unknown")
        for result in results:
            log_fn = self.logger.info if result.passed else self.logger.warning
            log_fn(
                "Rule %s %s for contract %s%s",
                result.rule_id,
                "passed" if result.passed else "failed",
                contract_id,
                "" if result.passed else f": {result.message}",
            )
        return results

    def create_violation(self, validation_result: ValidationResult) -> Violation:
        """Delegate violation creation to :class:`RemediationManager`."""
        return self.remediator.create_violation(validation_result)


# ----------------------------------------------------------------------
def main() -> None:
    """CLI interface for testing the Contract Validation Engine."""
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
