"""Validation rules for contract deliverables."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any, List


@dataclass
class ValidationRule:
    """A single validation rule for contract data."""

    rule_id: str
    description: str
    validate: Callable[[Dict[str, Any]], bool]


def default_validation_rules() -> List[ValidationRule]:
    """Return the default set of validation rules."""
    rules: List[ValidationRule] = []

    def has_phases(contract: Dict[str, Any]) -> bool:
        return bool(contract.get("phases"))

    rules.append(
        ValidationRule(
            rule_id="has_phases",
            description="Contract defines at least one phase",
            validate=has_phases,
        )
    )

    def phase_count_matches(contract: Dict[str, Any]) -> bool:
        phases = contract.get("phases")
        total = contract.get("total_phases")
        return (
            isinstance(phases, list) and isinstance(total, int) and len(phases) == total
        )

    rules.append(
        ValidationRule(
            rule_id="phase_count",
            description="total_phases matches number of phases",
            validate=phase_count_matches,
        )
    )

    return rules
