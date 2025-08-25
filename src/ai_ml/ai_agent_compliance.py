"""Compliance checks for AI agent configurations."""
from __future__ import annotations

from typing import Any, Dict


class ComplianceError(ValueError):
    """Raised when a configuration fails compliance checks."""


def enforce_compliance(config: Dict[str, Any]) -> None:
    """Validate a configuration against basic compliance rules.

    Parameters
    ----------
    config:
        Configuration dictionary to check.
    """
    if not config.get("name"):
        raise ComplianceError("Agent name must be provided.")
    if not isinstance(config.get("capabilities", []), list):
        raise ComplianceError("Capabilities must be a list.")


__all__ = ["ComplianceError", "enforce_compliance"]
