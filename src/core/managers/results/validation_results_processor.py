"""
Validation Results Processor - Phase-2 V2 Compliance Refactoring
================================================================

Handles validation-specific result processing.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any

from .base_results_manager import BaseResultsManager


class ValidationResultsProcessor(BaseResultsManager):
    """Processes validation-specific results."""

    def _process_result_by_type(
        self, context, result_type: str, result_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Process validation results."""
        if result_type == "validation":
            return self._process_validation_result(context, result_data)
        return super()._process_result_by_type(context, result_type, result_data)

    def _process_validation_result(self, context, result_data: dict[str, Any]) -> dict[str, Any]:
        """Process validation result data."""
        try:
            validation_rules = result_data.get("validation_rules", [])
            data_to_validate = result_data.get("data", {})

            validation_results = []
            overall_success = True

            for rule in validation_rules:
                rule_result = self._validate_rule(rule, data_to_validate)
                validation_results.append(
                    {
                        "rule": rule,
                        "passed": rule_result,
                        "field": rule.get("field"),
                        "type": rule.get("type"),
                    }
                )
                if not rule_result:
                    overall_success = False

            return {
                "validation_success": overall_success,
                "validation_results": validation_results,
                "rules_checked": len(validation_rules),
                "rules_passed": sum(1 for r in validation_results if r["passed"]),
                "rules_failed": sum(1 for r in validation_results if not r["passed"]),
                "original_data": data_to_validate,
            }

        except Exception as e:
            context.logger(f"Error processing validation result: {e}")
            return {
                "validation_success": False,
                "error": str(e),
                "original_data": result_data,
            }
