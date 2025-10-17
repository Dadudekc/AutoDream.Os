#!/usr/bin/env python3
"""
Validation Function Consolidation
==================================

Consolidates 77+ duplicate validate_* functions found across src/core.

Created by: Agent-3 (Infrastructure & DevOps Specialist)
Mission: DUP-005 Validation Functions Consolidation
Status: IN PROGRESS - Silent execution mode
"""

from typing import Any, Callable


def validate_non_empty(value: Any, field_name: str = "value") -> tuple[bool, str]:
    """Validate value is not None or empty."""
    if value is None:
        return (False, f"{field_name} cannot be None")
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return (False, f"{field_name} cannot be empty")
    return (True, "")


def validate_type(value: Any, expected_type: type, field_name: str = "value") -> tuple[bool, str]:
    """Validate value is of expected type."""
    if not isinstance(value, expected_type):
        return (False, f"{field_name} must be {expected_type.__name__}, got {type(value).__name__}")
    return (True, "")


def validate_dict_fields(data: dict, required_fields: list[str]) -> tuple[bool, list[str]]:
    """Validate dict has all required fields."""
    missing = [f for f in required_fields if f not in data]
    if missing:
        return (False, missing)
    return (True, [])


def validate_range(value: float, min_val: float, max_val: float, field_name: str = "value") -> tuple[bool, str]:
    """Validate value is within range."""
    if value < min_val or value > max_val:
        return (False, f"{field_name} must be between {min_val} and {max_val}, got {value}")
    return (True, "")


def validate_list_items(items: list, item_validator: Callable[[Any], tuple[bool, str]]) -> tuple[bool, list[str]]:
    """Validate all items in list using validator function."""
    errors = []
    for i, item in enumerate(items):
        is_valid, error = item_validator(item)
        if not is_valid:
            errors.append(f"Item {i}: {error}")
    return (len(errors) == 0, errors)


def validate_enum_value(value: str, valid_values: list[str], field_name: str = "value") -> tuple[bool, str]:
    """Validate value is one of valid enum values."""
    if value not in valid_values:
        return (False, f"{field_name} must be one of {valid_values}, got {value}")
    return (True, "")


def validate_path_exists(path: str, must_be_file: bool = False, must_be_dir: bool = False) -> tuple[bool, str]:
    """Validate path exists and optionally check type."""
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return (False, f"Path does not exist: {path}")
    if must_be_file and not p.is_file():
        return (False, f"Path is not a file: {path}")
    if must_be_dir and not p.is_dir():
        return (False, f"Path is not a directory: {path}")
    return (True, "")


# Consolidating patterns from 77 validate_ functions across src/core
# Common patterns identified: type checking, non-empty, dict fields, ranges, enums, paths
# This eliminates duplication and provides SSOT for validation logic

