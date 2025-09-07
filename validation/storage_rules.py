"""Storage validation rule definitions.

This module contains the data-driven rule sets used by the
storage validation workflow. Separating the rule definitions
from the check implementation keeps the system flexible and
focused on configuration rather than logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class StorageRule:
    """Simple representation of a storage validation rule."""

    rule_id: str
    description: str
    check: str
    remediation: str


# Required fields that every storage configuration must provide.
REQUIRED_FIELDS: set[str] = {"name", "type", "configuration"}

# Supported storage types recognised by the validator.
VALID_STORAGE_TYPES: set[str] = {"file", "database", "cache", "memory"}

# Rule catalogue linking rule identifiers to check and remediation function names.
# The high level validator looks up the functions from the checks and remediation
# modules using these names. This indirect reference keeps this module free from
# hard dependencies on implementation modules.
STORAGE_RULES: Dict[str, StorageRule] = {
    "required_fields": StorageRule(
        rule_id="required_fields",
        description="Ensure mandatory fields are present",
        check="check_required_fields",
        remediation="suggest_missing_fields",
    ),
    "storage_type": StorageRule(
        rule_id="storage_type",
        description="Validate provided storage type",
        check="check_storage_type",
        remediation="suggest_invalid_type",
    ),
}
