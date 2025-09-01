#!/usr/bin/env python3
"""
Priority Validator Module - Agent Cellphone V2
===========================================

Validates priority settings and provides warnings for workflow disruption.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
import sys
import logging
from typing import Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class PriorityValidator:
    """Validates priority settings and workflow impact."""

    def __init__(self):
        """Initialize priority validator."""
        self.logger = logging.getLogger(__name__)

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate priority settings and warn about workflow disruption.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome (always success, but may warn)
        """
        # Warn if --high-priority is used with regular priority (default)
        if getattr(args, 'high_priority', False):
            priority_val = getattr(args, 'priority', 'regular')
            if priority_val == 'regular':
                self._warn_high_priority_disruption()

        return ValidationResult.success()

    def _warn_high_priority_disruption(self):
        """Warn about high priority flag disrupting agent workflow."""
        warning_message = (
            "⚠️ HIGH PRIORITY WARNING: --high-priority flag used with regular priority. "
            "This disrupts agent workflow. Consider removing --high-priority unless this is a true emergency. "
            "Use regular priority by default to maintain 8x efficiency workflow."
        )

        self.logger.warning(warning_message)

        # Output to stderr for visibility
        print("⚠️  WARNING: High priority flag disrupts agent workflow!", file=sys.stderr)
        print("   Regular priority is the default and maintains workflow continuity.", file=sys.stderr)
        print("   Only use --high-priority for true emergencies.", file=sys.stderr)

    def get_priority_guidance(self) -> str:
        """Get guidance on priority usage."""
        return """
Priority Usage Guidance:
- Use 'regular' priority by default (maintains 8x efficiency workflow)
- Reserve 'urgent' priority for true emergencies only
- The --high-priority flag should be used sparingly
- Consider workflow impact before using high priority
"""
