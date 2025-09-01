#!/usr/bin/env python3
"""
System State Validator Module - Agent Cellphone V2
===============================================

Validates system state (queue capacity, locks, etc.).

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
from typing import Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes


class SystemStateValidator:
    """Validates system state for messaging operations."""

    def __init__(self):
        """Initialize system state validator."""
        # Queue capacity limits (can be configured)
        self.max_queue_size = 10000
        self.warning_queue_threshold = 8000

    def validate(self, args: argparse.Namespace) -> ValidationResult:
        """
        Validate system state for the requested operation.

        Args:
            args: Parsed CLI arguments

        Returns:
            ValidationResult: Validation outcome
        """
        # Check queue stats if requested
        if hasattr(args, 'queue_stats') and getattr(args, 'queue_stats', False):
            # This would check actual queue state
            # For now, we'll skip as we don't have access to queue from here
            pass

        # Check for queue capacity on enqueue operations
        if self._is_enqueue_operation(args):
            capacity_result = self._validate_queue_capacity()
            if not capacity_result.is_valid:
                return capacity_result

        return ValidationResult.success()

    def _is_enqueue_operation(self, args: argparse.Namespace) -> bool:
        """Check if this operation will enqueue messages."""
        enqueue_indicators = [
            getattr(args, 'message', None),  # Direct message
            getattr(args, 'bulk', False),    # Bulk message
            getattr(args, 'onboarding', False),  # Onboarding
            getattr(args, 'onboard', False), # Single onboarding
            getattr(args, 'wrapup', False)   # Wrapup
        ]

        return any(enqueue_indicators)

    def _validate_queue_capacity(self) -> ValidationResult:
        """Validate queue has capacity for new messages."""
        # This is a placeholder - in real implementation, this would check actual queue
        # For now, we'll assume queue has capacity
        # In production, this would check:
        # - Current queue size
        # - Available capacity
        # - Rate limiting
        # - System resources

        current_size = 0  # Would be retrieved from actual queue
        available_capacity = self.max_queue_size - current_size

        if available_capacity <= 0:
            error = ValidationError(
                code=ValidationExitCodes.QUEUE_FULL,
                message="Message queue is at capacity",
                hint="Wait for queue to process or use --force to override",
                correlation_id="queue_validation",
                timestamp=datetime.now(),
                details={
                    "current_size": current_size,
                    "max_capacity": self.max_queue_size,
                    "validation_type": "queue_capacity"
                }
            )
            return ValidationResult.failure(error)

        if available_capacity < (self.max_queue_size * 0.2):  # Less than 20% capacity
            # This could be a warning, but for now we'll allow it
            pass

        return ValidationResult.success()

    def set_queue_limits(self, max_size: int, warning_threshold: int):
        """Set queue capacity limits."""
        self.max_queue_size = max_size
        self.warning_queue_threshold = warning_threshold

    def get_system_status(self) -> dict:
        """Get current system status."""
        return {
            "queue_capacity": self.max_queue_size,
            "warning_threshold": self.warning_queue_threshold,
            "status": "operational"
        }
