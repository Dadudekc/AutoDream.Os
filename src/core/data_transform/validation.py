from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict

from ..data_sources.models import DataType


class DataValidationEngine:
    """Unified data validation engine for all data sources."""

    def __init__(self) -> None:
        self.validation_rules = {
            DataType.MARKET: {
                "required_fields": ["symbol", "price", "timestamp"],
                "price_validation": lambda x: isinstance(x, (int, float)) and x > 0,
                "timestamp_validation": lambda x: isinstance(x, str) and len(x) > 0,
            },
            DataType.SENTIMENT: {
                "required_fields": ["score", "confidence", "source"],
                "score_validation": lambda x: isinstance(x, (int, float)) and -1 <= x <= 1,
                "confidence_validation": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
            },
            DataType.FINANCIAL: {
                "required_fields": ["amount", "currency", "date"],
                "amount_validation": lambda x: isinstance(x, (int, float)) and x >= 0,
                "currency_validation": lambda x: isinstance(x, str) and len(x) == 3,
            },
        }

    def validate_data(self, data: Any, data_type: DataType) -> Dict[str, Any]:
        """Validate data against type-specific rules."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validation_time": datetime.now(timezone.utc).isoformat(),
        }

        if data_type not in self.validation_rules:
            result["warnings"].append(f"No validation rules for {data_type}")
            return result

        rules = self.validation_rules[data_type]

        if isinstance(data, dict):
            for field in rules.get("required_fields", []):
                if field not in data:
                    result["valid"] = False
                    result["errors"].append(f"Missing required field: {field}")

        for rule_name, validation_func in rules.items():
            if rule_name.endswith("_validation") and callable(validation_func):
                field = rule_name.replace("_validation", "")
                value = data.get(field) if isinstance(data, dict) else data
                try:
                    if not validation_func(value):
                        result["valid"] = False
                        result["errors"].append(f"Validation failed for {rule_name}")
                except Exception as exc:  # pragma: no cover - defensive
                    result["valid"] = False
                    result["errors"].append(f"Validation error for {rule_name}: {exc}")
        return result

    def get_validation_rules(self, data_type: DataType) -> Dict[str, Any]:
        """Get validation rules for a specific data type."""
        return self.validation_rules.get(data_type, {})
