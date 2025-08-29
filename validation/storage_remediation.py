"""Remediation helpers for storage validation.

These functions generate human readable guidance for resolving
validation failures. They do not mutate the provided data.
"""
from __future__ import annotations

from typing import Iterable

from .storage_rules import VALID_STORAGE_TYPES


def suggest_missing_fields(missing: Iterable[str]) -> str:
    """Return a message suggesting the addition of missing fields."""
    missing_list = ", ".join(sorted(missing))
    return f"Missing required fields: {missing_list}"


def suggest_invalid_type(actual_type: str) -> str:
    """Return a message indicating the storage type is invalid."""
    valid = ", ".join(sorted(VALID_STORAGE_TYPES))
    return f"Invalid storage type '{actual_type}'. Expected one of: {valid}"
