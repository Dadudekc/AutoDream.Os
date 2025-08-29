"""Scanning utilities for detecting sensitive data exposure."""

from typing import Any, Dict, Iterable, List


def scan_sensitive_fields(security_data: Dict[str, Any], sensitive_fields: Iterable[str]) -> List[str]:
    """Return list of sensitive field names that appear to expose data.

    Args:
        security_data: Input dictionary containing security related fields.
        sensitive_fields: Iterable of field name fragments considered sensitive.
    """
    exposures: List[str] = []
    for field_name, field_value in security_data.items():
        lower_name = field_name.lower()
        if any(fragment in lower_name for fragment in sensitive_fields):
            if field_value:  # only flag non-empty values
                exposures.append(field_name)
    return exposures
