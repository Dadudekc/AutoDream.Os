#!/usr/bin/env python3
"""
Dependency Validator Module - Agent Cellphone V2
=============================================

Validates flag dependencies and requirements.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
from typing import Dict, List, Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class DependencyValidator:
    """Validates flag dependency requirements."""

    def __init__(self, dependency_rules: Dict[str, List[str]] = None):
        """Initialize validator with dependency rules."""
        self.dependency_rules = dependency_rules or {
            'get_next_task': ['agent'],
            'onboard': ['agent'],
        }

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate dependency requirements.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome
        """
        for flag, required_flags in self.dependency_rules.items():
            # Handle snake_case conversion for flag names
            flag_attr = flag.replace('_', '')

            if getattr(args, flag_attr, False):
                missing_deps = []
                for required in required_flags:
                    if not getattr(args, required, None):
                        missing_deps.append(f"--{required}")

                if missing_deps:
                    error = ValidationError(
                        code=ValidationExitCodes.DEPENDENCY_MISSING,
                        message=f"--{flag.replace('_', '-')} requires {missing_deps}",
                        hint=f"Add {missing_deps[0]} to the command",
                        correlation_id="dep_validation",
                        timestamp=datetime.now(),
                        details={
                            "flag": flag,
                            "required": missing_deps,
                            "command_example": f"python -m src.services.messaging_cli --{flag.replace('_', '-')} --agent Agent-X",
                            "validation_type": "dependency"
                        }
                    )
                    return ValidationResult.failure(error)

        return ValidationResult.success()

    def add_dependency(self, flag: str, required_flags: List[str]):
        """Add a new dependency rule."""
        self.dependency_rules[flag] = required_flags

    def get_dependencies_summary(self) -> str:
        """Get summary of all dependency rules."""
        summary = "Dependency Rules:\n"
        for flag, deps in self.dependency_rules.items():
            summary += f"  --{flag.replace('_', '-')} → {deps}\n"
        return summary
