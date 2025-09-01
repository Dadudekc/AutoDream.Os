#!/usr/bin/env python3
"""
Message Validator Module - Agent Cellphone V2
==========================================

Validates message content requirements and special cases.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
from typing import Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class MessageValidator:
    """Validates message content requirements."""

    def __init__(self):
        """Initialize message validator."""
        # Special operations that don't require explicit message content
        self.special_operations = ['onboarding', 'onboard', 'wrapup', 'get_next_task']

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate message content requirements.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome
        """
        # Check if this is a message-sending operation
        is_message_op = self._is_message_operation(args)

        if is_message_op and not getattr(args, 'message', None):
            # Check if it's a special case that doesn't require explicit message
            if not self._is_special_case(args):
                error = ValidationError(
                    code=ValidationExitCodes.DEPENDENCY_MISSING,
                    message="--message is required for standard message operations",
                    hint="Add --message \"Your message here\" to the command",
                    correlation_id="message_validation",
                    timestamp=datetime.now(),
                    details={
                        "operation_type": "message_send",
                        "missing": "--message",
                        "example": "python -m src.services.messaging_cli --agent Agent-7 --message \"Hello\"",
                        "validation_type": "message_requirement"
                    }
                )
                return ValidationResult.failure(error)

        return ValidationResult.success()

    def _is_message_operation(self, args: argparse.Namespace) -> bool:
        """Check if this is a message-sending operation."""
        message_indicators = [
            getattr(args, 'message', None),
            getattr(args, 'bulk', False),
            getattr(args, 'onboarding', False),
            getattr(args, 'onboard', False),
            getattr(args, 'wrapup', False),
            getattr(args, 'get_next_task', False)
        ]

        return any(message_indicators)

    def _is_special_case(self, args: argparse.Namespace) -> bool:
        """Check if this is a special case that doesn't require explicit message."""
        for operation in self.special_operations:
            if getattr(args, operation, False):
                return True
        return False

    def add_special_operation(self, operation: str):
        """Add a new special operation that doesn't require explicit message."""
        if operation not in self.special_operations:
            self.special_operations.append(operation)

    def get_special_operations_summary(self) -> str:
        """Get summary of special operations."""
        summary = "Special Operations (no explicit message required):\n"
        for op in self.special_operations:
            summary += f"  --{op.replace('_', '-')}\n"
        return summary
