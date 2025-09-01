#!/usr/bin/env python3
"""
Mode Gate Validator Module - Agent Cellphone V2
============================================

Validates pyautogui-specific flags are only used with pyautogui mode.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
from typing import List, Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class ModeGateValidator:
    """Validates mode-specific flag usage."""

    def __init__(self, mode_gated_flags: List[str] = None):
        """Initialize validator with gated flags."""
        self.mode_gated_flags = mode_gated_flags or ['no_paste', 'new_tab_method']

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate that pyautogui-specific flags are only used with pyautogui mode.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome
        """
        current_mode = getattr(args, 'mode', 'pyautogui')

        if current_mode == 'inbox':
            # Check if any pyautogui-only flags are set
            gated_flags_set = []
            for flag in self.mode_gated_flags:
                flag_name = flag.replace('_', '')
                if getattr(args, flag_name, False):
                    gated_flags_set.append(f"--{flag.replace('_', '-')}")

            if gated_flags_set:
                error = ValidationError(
                    code=ValidationExitCodes.MODE_MISMATCH,
                    message=f"Flags {gated_flags_set} only work with --mode pyautogui",
                    hint="Remove pyautogui-only flags or switch to --mode pyautogui",
                    correlation_id="mode_gate_validation",
                    timestamp=datetime.now(),
                    details={
                        "incompatible_flags": gated_flags_set,
                        "current_mode": "inbox",
                        "required_mode": "pyautogui",
                        "correction": f"Add --mode pyautogui or remove {gated_flags_set[0]}",
                        "validation_type": "mode_gating"
                    }
                )
                return ValidationResult.failure(error)

        return ValidationResult.success()

    def add_gated_flag(self, flag: str):
        """Add a new mode-gated flag."""
        if flag not in self.mode_gated_flags:
            self.mode_gated_flags.append(flag)

    def get_gated_flags_summary(self) -> str:
        """Get summary of all gated flags."""
        summary = "Mode-Gated Flags (PyAutoGUI only):\n"
        for flag in self.mode_gated_flags:
            summary += f"  --{flag.replace('_', '-')}\n"
        return summary
