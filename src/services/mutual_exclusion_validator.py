#!/usr/bin/env python3
"""
Mutual Exclusion Validator Module - Agent Cellphone V2
===================================================

Validates flag mutual exclusions and conflicts.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
from typing import List, Tuple, Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class MutualExclusionValidator:
    """Validates mutual exclusion rules between CLI flags."""

    def __init__(self, exclusion_rules: List[Tuple[List[str], List[str]]] = None):
        """Initialize validator with exclusion rules."""
        self.exclusion_rules = exclusion_rules or [
            (['agent'], ['bulk', 'onboarding', 'wrapup']),
        ]

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate mutual exclusion rules.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome
        """
        for primary_flags, conflicting_flags in self.exclusion_rules:
            # Check if any primary flag is set
            primary_set = any(getattr(args, flag, False) for flag in primary_flags)

            if primary_set:
                # Check if any conflicting flags are set
                conflicts_set = any(getattr(args, flag, False) for flag in conflicting_flags)

                if conflicts_set:
                    # Find which flags are set
                    primary_active = [f for f in primary_flags if getattr(args, f, False)]
                    conflicts_active = [f for f in conflicting_flags if getattr(args, f, False)]

                    error = ValidationError(
                        code=ValidationExitCodes.INVALID_FLAGS,
                        message=f"Cannot combine {primary_active} with {conflicts_active}",
                        hint=f"Use either {primary_active[0]} OR {conflicts_active[0]}",
                        correlation_id="mutex_validation",
                        timestamp=datetime.now(),
                        details={
                            "primary_flags": primary_active,
                            "conflicting_flags": conflicts_active,
                            "rule": f"{primary_flags} XOR {conflicting_flags}",
                            "validation_type": "mutual_exclusion"
                        }
                    )
                    return ValidationResult.failure(error)

        return ValidationResult.success()

    def add_rule(self, primary_flags: List[str], conflicting_flags: List[str]):
        """Add a new mutual exclusion rule."""
        self.exclusion_rules.append((primary_flags, conflicting_flags))

    def get_rules_summary(self) -> str:
        """Get summary of all mutual exclusion rules."""
        summary = "Mutual Exclusion Rules:\n"
        for i, (primary, conflicting) in enumerate(self.exclusion_rules, 1):
            summary += f"  {i}. {primary} ↔ {conflicting}\n"
        return summary
