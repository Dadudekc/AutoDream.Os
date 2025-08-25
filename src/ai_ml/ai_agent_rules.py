"""Validation rules for AI agent configurations."""
from __future__ import annotations

from typing import Any, Dict

REQUIRED_FIELDS: Dict[str, Any] = {
    "name": "Unnamed Agent",
    "version": "1.0",
    "capabilities": [],
}


def apply_rules(config: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure required configuration fields are present with defaults.

    Parameters
    ----------
    config:
        Configuration dictionary to validate.

    Returns
    -------
    Dict[str, Any]
        Updated configuration containing required fields.
    """
    updated = dict(config)
    for field, default in REQUIRED_FIELDS.items():
        updated.setdefault(field, default)
    return updated


__all__ = ["apply_rules", "REQUIRED_FIELDS"]
