"""Validation helpers for the ConfigManager modules.

The validator takes a mapping of section names to validator callables and
provides a tiny facade that reports validation results.  Each validator
returns ``True`` for success and ``False`` or raises an exception for
failure.  The module avoids opinionated schemas to remain adaptable for
varied test scenarios.
"""

from __future__ import annotations

from typing import Any, Callable, Dict


class ConfigValidator:
    """Run validation functions for configuration sections."""

    def __init__(self, validators: Dict[str, Callable[[Dict[str, Any]], bool]]):
        self.validators = validators

    def validate(self, configs: Dict[str, Dict[str, Any]]) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for name, data in configs.items():
            validator = self.validators.get(name)
            if validator is None:
                results[name] = True
                continue
            try:
                results[name] = bool(validator(data))
            except Exception:
                results[name] = False
        return results
