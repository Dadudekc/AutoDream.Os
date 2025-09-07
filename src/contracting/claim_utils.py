"""Shared utilities for contract task management.

This module centralizes common functionality used by contract
management scripts including loading and saving task lists and
validating individual contracts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Allowed status values for contracts
ALLOWED_STATUSES = {"AVAILABLE", "CLAIMED", "COMPLETED"}


def load_tasks(path: str | Path) -> Dict[str, Any]:
    """Load tasks from ``path``.

    Returns an empty dictionary if the file does not exist or cannot be
    decoded.  A message is printed describing the failure.
    """
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR Task list not found: {p}")
    except json.JSONDecodeError as e:
        print(f"ERROR Invalid JSON in task list {p}: {e}")
    except Exception as e:  # pragma: no cover - unexpected errors
        print(f"ERROR Error loading contracts: {e}")
    return {}


def save_tasks(path: str | Path, tasks: Dict[str, Any]) -> bool:
    """Persist ``tasks`` to ``path``.

    Returns ``True`` if saving succeeded, otherwise ``False`` with a
    descriptive message printed to stdout.
    """
    p = Path(path)
    try:
        with p.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:  # pragma: no cover - unexpected errors
        print(f"ERROR Error saving contracts: {e}")
        return False


def validate_contract(contract: Dict[str, Any]) -> bool:
    """Basic validation for an individual contract entry.

    A valid contract must provide a ``contract_id`` and ``status`` field
    with the status being one of :data:`ALLOWED_STATUSES`.  The function
    returns ``True`` when the contract passes validation.
    """
    if not isinstance(contract, dict):
        return False

    contract_id = contract.get("contract_id")
    status = contract.get("status")
    if not contract_id or not isinstance(contract_id, str):
        return False
    if status not in ALLOWED_STATUSES:
        return False
    return True


__all__ = ["load_tasks", "save_tasks", "validate_contract", "ALLOWED_STATUSES"]
