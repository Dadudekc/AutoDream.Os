#!/usr/bin/env python3
"""
Validation Coordinator - V2 Compliance
======================================

Coordinates different validation engines and provides unified validation interface.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ValidationCoordinator:
    """Coordinates different validation engines."""

    def __init__(self):
        """Initialize validation coordinator."""
        self.logger = logger
        self.engines = {}

    def register_engine(self, name: str, engine: Any) -> None:
        """Register a validation engine."""
        self.engines[name] = engine
        self.logger.info(f"Registered validation engine: {name}")

    def validate(self, data: Any, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data using registered engines."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        for rule_name, rule_config in rules.items():
            try:
                if rule_name in self.engines:
                    engine = self.engines[rule_name]
                    engine_result = engine.validate(data, rule_config)
                    if not engine_result.get("valid", True):
                        results["valid"] = False
                        results["errors"].extend(engine_result.get("errors", []))
                        results["warnings"].extend(engine_result.get("warnings", []))
                else:
                    self.logger.warning(f"No engine found for rule: {rule_name}")
            except Exception as e:
                self.logger.error(f"Validation error for rule {rule_name}: {e}")
                results["valid"] = False
                results["errors"].append(f"Validation error: {e}")

        return results

    def get_available_engines(self) -> List[str]:
        """Get list of available validation engines."""
        return list(self.engines.keys())


# Global validation coordinator instance
_validation_coordinator = None


def get_validation_coordinator() -> ValidationCoordinator:
    """Get the global validation coordinator instance."""
    global _validation_coordinator
    if _validation_coordinator is None:
        _validation_coordinator = ValidationCoordinator()
    return _validation_coordinator
