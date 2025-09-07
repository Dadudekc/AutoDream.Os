"""Execution engine for running validations."""

from typing import Dict, List

from ..validation_manager import ValidationManager
from ..base_validator import ValidationResult


def run_validations(
    manager: ValidationManager, data: Dict[str, object]
) -> Dict[str, List[ValidationResult]]:
    """Execute all registered validators using the provided manager."""
    return manager.validate_all(data)
