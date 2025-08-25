"""Orchestrates AI agent configuration validation."""
from __future__ import annotations

from typing import Any, Dict

from .ai_agent_validator_core import validate_agent_config
from .ai_agent_rules import apply_rules, REQUIRED_FIELDS
from .ai_agent_compliance import enforce_compliance, ComplianceError


def validate_agent(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate an AI agent configuration using rules and compliance checks."""
    return validate_agent_config(config)


__all__ = [
    "validate_agent",
    "apply_rules",
    "enforce_compliance",
    "ComplianceError",
    "REQUIRED_FIELDS",
]
