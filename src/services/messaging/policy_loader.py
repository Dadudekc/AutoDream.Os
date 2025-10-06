#!/usr/bin/env python3
"""
Messaging Template Policy Loader
================================

Loads role/channel template selection policy from YAML with sane defaults.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

logger = logging.getLogger(__name__)


DEFAULT_POLICY: Dict[str, Any] = {
    "version": 1,
    "roles": {
        "defaults": {"fallback": "compact"},
        "CAPTAIN": {"default_template": "full"},
    },
    "role_matrix": {
        "CAPTAIN->ANY": "full",
        "ANY->CAPTAIN": "full",
        "ANY->ANY": "compact",
        "NON_CAPTAIN->NON_CAPTAIN": "minimal",
    },
    "channels": {
        "onboarding": "full",
        "passdown": "minimal",
        "standard": "compact",
    },
}


def load_template_policy(policy_path: str = "config/messaging/template_policy.yaml") -> Dict[str, Any]:
    """Load the messaging template policy YAML with defaults if missing.

    Returns a merged policy dict.
    """
    path = Path(policy_path)
    if not path.exists() or not yaml:
        logger.info("Using default messaging template policy")
        return DEFAULT_POLICY

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return _merge_policy(DEFAULT_POLICY, data)
    except Exception as e:  # pragma: no cover
        logger.warning(f"Failed to load policy at {policy_path}: {e}; using defaults")
        return DEFAULT_POLICY


def _merge_policy(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = _merge_policy(merged[k], v)  # type: ignore[arg-type]
        else:
            merged[k] = v
    return merged


def resolve_template_by_roles(policy: Dict[str, Any], sender_role: str, receiver_role: str) -> str:
    """Resolve template from role×role matrix with sensible fallbacks."""
    matrix = policy.get("role_matrix", {})

    def get(key: str) -> str | None:
        val = matrix.get(key)
        return str(val) if val else None

    sender_is_captain = sender_role.upper() == "CAPTAIN"
    receiver_is_captain = receiver_role.upper() == "CAPTAIN"

    # Prefer explicit matrix matches
    if sender_is_captain and (tpl := get("CAPTAIN->ANY")):
        return tpl
    if receiver_is_captain and (tpl := get("ANY->CAPTAIN")):
        return tpl

    if (tpl := get("NON_CAPTAIN->NON_CAPTAIN")) and not sender_is_captain and not receiver_is_captain:
        return tpl

    return matrix.get("ANY->ANY", policy.get("roles", {}).get("defaults", {}).get("fallback", "compact"))


def resolve_template_by_channel(policy: Dict[str, Any], channel: str) -> str:
    channels = policy.get("channels", {})
    return str(channels.get(channel, channels.get("standard", "compact")))


