"""Checking logic for storage validation.

Each check function focuses on a single rule, returning details about
violations without performing any remediation.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from .storage_rules import REQUIRED_FIELDS, VALID_STORAGE_TYPES


def check_required_fields(data: Dict[str, object]) -> List[str]:
    """Return a list of missing required fields."""
    return [field for field in REQUIRED_FIELDS if field not in data]


def check_storage_type(data: Dict[str, object]) -> Optional[str]:
    """Return the invalid storage type or ``None`` if valid.

    If the type field is missing this returns the string ``"missing"``
    so the caller can differentiate between a missing field and an
    unsupported value.
    """
    if "type" not in data:
        return "missing"

    stype = data["type"]
    if not isinstance(stype, str) or stype not in VALID_STORAGE_TYPES:
        return str(stype)
    return None
