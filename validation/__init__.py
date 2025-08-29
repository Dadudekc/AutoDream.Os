"""Simple storage validation package.

The :func:`validate` function provides a high level interface that
applies the defined rule checks and returns remediation guidance for any
failures.
"""
from __future__ import annotations

from typing import Dict, List

from .storage_checks import check_required_fields, check_storage_type
from .storage_remediation import (
    suggest_invalid_type,
    suggest_missing_fields,
)


def validate(config: Dict[str, object]) -> List[str]:
    """Validate a storage configuration and return remediation messages.

    Parameters
    ----------
    config:
        Mapping describing storage configuration attributes.

    Returns
    -------
    List[str]
        A list of remediation messages. The list is empty when the
        configuration passes all checks.
    """
    messages: List[str] = []

    missing = check_required_fields(config)
    if missing:
        messages.append(suggest_missing_fields(missing))

    invalid_type = check_storage_type(config)
    if invalid_type:
        if invalid_type == "missing":
            if "type" not in missing:
                messages.append(suggest_missing_fields(["type"]))
        else:
            messages.append(suggest_invalid_type(invalid_type))

    return messages


__all__ = ["validate"]
