#!/usr/bin/env python3
"""Contract validation utilities."""

import logging
from typing import Any, Dict, List

from .contract_models import ContractPriority


class ContractValidator:
    """Validates contract data and structure."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ContractValidator")

    def validate_contract(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate contract data and return validation results."""
        results: List[Dict[str, Any]] = []
        try:
            required = ["title", "description", "priority", "required_capabilities"]
            for field in required:
                if field not in contract_data or not contract_data[field]:
                    results.append(
                        {
                            "field": field,
                            "issue": f"Required field '{field}' is missing or empty",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            if "priority" in contract_data:
                try:
                    ContractPriority(contract_data["priority"])
                except ValueError:
                    results.append(
                        {
                            "field": "priority",
                            "issue": f"Invalid priority value: {contract_data['priority']}",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            if "required_capabilities" in contract_data:
                capabilities = contract_data["required_capabilities"]
                if not isinstance(capabilities, list) or len(capabilities) == 0:
                    results.append(
                        {
                            "field": "required_capabilities",
                            "issue": "Required capabilities must be a non-empty list",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            if not any(
                r["severity"] == "critical" and not r["passed"] for r in results
            ):
                results.append(
                    {
                        "field": "overall",
                        "issue": "Contract validation passed",
                        "severity": "info",
                        "passed": True,
                    }
                )
        except Exception as e:  # pragma: no cover - defensive
            results.append(
                {
                    "field": "validation_error",
                    "issue": f"Validation error: {str(e)}",
                    "severity": "critical",
                    "passed": False,
                }
            )
        return results
