from __future__ import annotations

"""Registry for managing validation rules and validators."""

from typing import Dict, List, Optional

from .base_validator import BaseValidator


class RuleRegistry:
    """Maintain a mapping of validator names to validator instances."""

    def __init__(self) -> None:
        self._validators: Dict[str, BaseValidator] = {}

    # ------------------------------------------------------------------
    # Registry operations
    # ------------------------------------------------------------------
    def register(self, name: str, validator: BaseValidator) -> None:
        """Register a validator instance under the given name."""
        self._validators[name] = validator

    def unregister(self, name: str) -> None:
        """Remove a previously registered validator if it exists."""
        self._validators.pop(name, None)

    def get(self, name: str) -> Optional[BaseValidator]:
        """Return a validator by name if present."""
        return self._validators.get(name)

    def list(self) -> List[str]:
        """List all registered validator names."""
        return list(self._validators.keys())
