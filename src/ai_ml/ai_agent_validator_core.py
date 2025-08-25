"""Core validation workflow for AI agent configurations."""
from __future__ import annotations

from typing import Any, Dict

from .ai_agent_rules import apply_rules
from .ai_agent_compliance import enforce_compliance


def validate_agent_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Apply rules and compliance checks to an agent configuration.

    Parameters
    ----------
    config:
        Configuration dictionary for an AI agent.

    Returns
    -------
    Dict[str, Any]
        Validated configuration with defaults applied.
    """
    prepared = apply_rules(config)
    enforce_compliance(prepared)
    return prepared


__all__ = ["validate_agent_config"]
