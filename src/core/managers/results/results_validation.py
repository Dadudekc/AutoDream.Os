"""Results Validation - V2 Compliance | Agent-5"""

from typing import Any


class ResultsValidator:
    """Validates results against rules."""

    @staticmethod
    def validate_result(result: dict[str, Any], rules: list[dict[str, Any]]) -> bool:
        """Validate result against rules."""
        if not rules:
            return True
        for rule in rules:
            if not ResultsValidator._validate_rule(rule, result.get("data", {})):
                return False
        return True

    @staticmethod
    def _validate_rule(rule: dict[str, Any], data: dict[str, Any]) -> bool:
        """Validate a single rule against data."""
        field = rule.get("field")
        rule_type = rule.get("type")
        expected_value = rule.get("expected_value")
        if field not in data:
            return False
        value = data[field]
        if rule_type == "equals":
            return value == expected_value
        elif rule_type == "not_equals":
            return value != expected_value
        elif rule_type == "greater_than":
            return value > expected_value
        elif rule_type == "less_than":
            return value < expected_value
        elif rule_type == "contains":
            return expected_value in str(value)
        elif rule_type == "not_empty":
            return bool(value)
        elif rule_type == "is_empty":
            return not bool(value)
        return True
