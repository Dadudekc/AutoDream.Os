"""Data validation routines for schema enforcement."""

from typing import Any, Dict, List


class DataValidator:
    """Provides validation helpers for data records."""

    def __init__(self, data_schemas: Dict[str, Any]):
        self.data_schemas = data_schemas

    def validate_data_against_schema(self, data: Any, schema_name: str) -> bool:
        """Validate data against a named schema."""
        try:
            schema = self.data_schemas[schema_name]
            if isinstance(data, dict):
                for field in schema.fields:
                    if field.get("required") and field["name"] not in data:
                        return False
                for field_name, value in data.items():
                    field_schema = next(
                        (f for f in schema.fields if f["name"] == field_name),
                        None,
                    )
                    if field_schema and not self.validate_field_value(
                        value, field_schema, schema.validation_rules.get(field_name, [])
                    ):
                        return False
            return True
        except Exception:
            return False

    def validate_field_value(
        self, value: Any, field_schema: Dict[str, Any], rules: List[str]
    ) -> bool:
        """Validate an individual field value according to schema and rules."""
        try:
            expected_type = field_schema.get("type")
            if expected_type == "string" and not isinstance(value, str):
                return False
            if expected_type == "float" and not isinstance(value, (int, float)):
                return False
            if expected_type == "integer" and not isinstance(value, int):
                return False
            if expected_type == "datetime" and not isinstance(value, (str, object)):
                return False

            for rule in rules:
                if rule.startswith("min:"):
                    if value < float(rule.split(":")[1]):
                        return False
                elif rule.startswith("max:"):
                    if value > float(rule.split(":")[1]):
                        return False
                elif rule == "positive" and value <= 0:
                    return False
                elif rule == "non_negative" and value < 0:
                    return False
                elif rule == "finite" and not (
                    isinstance(value, (int, float)) and abs(value) < float("inf")
                ):
                    return False
            return True
        except Exception:
            return False
