"""Validation helpers for data structures and schema checks."""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DataValidators:
    """Collection of data structure validation helpers."""

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, str]:
        """Validate that required fields are present and not empty."""
        errors: Dict[str, str] = {}

        for field in required_fields:
            if field not in data:
                errors[field] = f"Required field '{field}' is missing"
            elif data[field] is None:
                errors[field] = f"Required field '{field}' cannot be null"
            elif isinstance(data[field], str) and not data[field].strip():
                errors[field] = f"Required field '{field}' cannot be empty"
            elif isinstance(data[field], (list, dict)) and not data[field]:
                errors[field] = f"Required field '{field}' cannot be empty"

        return errors

    @staticmethod
    def validate_data_types(data: Dict[str, Any], type_schema: Dict[str, type]) -> Dict[str, str]:
        """Validate data types against a provided schema."""
        errors: Dict[str, str] = {}

        for field, expected_type in type_schema.items():
            if field in data and not isinstance(data[field], expected_type):
                errors[field] = (
                    f"Field '{field}' must be of type {expected_type.__name__}, "
                    f"got {type(data[field]).__name__}"
                )

        return errors

    @staticmethod
    def validate_json_string(json_str: str) -> bool:
        """Validate that a string contains valid JSON."""
        try:
            json.loads(json_str)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
