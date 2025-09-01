#!/usr/bin/env python3
"""
CLI Validator Core Module - Agent Cellphone V2
===========================================

Orchestrates all CLI validation components for comprehensive argument validation.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import argparse
import sys
import uuid
import logging
from typing import Tuple, Optional
from datetime import datetime

from .validation_models import ValidationError, ValidationResult, ValidationExitCodes
from .mutual_exclusion_validator import MutualExclusionValidator
from .dependency_validator import DependencyValidator
from .mode_gate_validator import ModeGateValidator
from .message_validator import MessageValidator
from .priority_validator import PriorityValidator
from .system_state_validator import SystemStateValidator

from ..utils.logger import get_messaging_logger


class CLIValidatorCore:
    """
    Core CLI validation orchestrator using modular validation components.

    This class coordinates all validation modules to provide comprehensive
    CLI argument validation following V2 compliance standards.
    """

    def __init__(self):
        """Initialize the CLI validator core with all validation modules."""
        self.logger = get_messaging_logger()
        self.correlation_id = str(uuid.uuid4())[:8]  # Short correlation ID

        # Initialize validation modules
        self.mutual_exclusion_validator = MutualExclusionValidator()
        self.dependency_validator = DependencyValidator()
        self.mode_gate_validator = ModeGateValidator()
        self.message_validator = MessageValidator()
        self.priority_validator = PriorityValidator()
        self.system_state_validator = SystemStateValidator()

        self.logger.info("CLIValidatorCore initialized with modular validation components")

    def validate_args(self, args: argparse.Namespace) -> Tuple[bool, Optional[ValidationError]]:
        """
        Validate CLI arguments comprehensively using all validation modules.

        Args:
            args: Parsed CLI arguments

        Returns:
            Tuple of (is_valid, error_details)
        """
        try:
            # Execute validation modules in logical order
            validations = [
                ("mutual_exclusion", self.mutual_exclusion_validator.validate),
                ("dependencies", self.dependency_validator.validate),
                ("mode_gating", self.mode_gate_validator.validate),
                ("message_requirements", self.message_validator.validate),
                ("priority_settings", self.priority_validator.validate),
                ("system_state", self.system_state_validator.validate),
            ]

            for validation_name, validator_func in validations:
                result = validator_func(args)

                if not result.is_valid and result.error:
                    # Add correlation ID to error
                    result.error.correlation_id = self.correlation_id
                    return False, result.error

            return True, None

        except Exception as e:
            self.logger.error(f"Validation error: {e}", extra={"correlation_id": self.correlation_id})
            error = ValidationError(
                code=ValidationExitCodes.INTERNAL_ERROR,
                message="Internal validation error",
                hint="Check logs with correlation ID",
                correlation_id=self.correlation_id,
                timestamp=datetime.now(),
                details={"exception": str(e), "exception_type": type(e).__name__}
            )
            return False, error

    def report_error(self, error: ValidationError) -> None:
        """Report validation error to user with structured output."""
        # Log structured error
        self.logger.error(
            error.message,
            extra={
                "correlation_id": error.correlation_id,
                "exit_code": error.code,
                "hint": error.hint
            }
        )

        # Output JSON error to stderr for programmatic handling
        print(error.to_json(), file=sys.stderr)

        # Output human-readable error to stdout
        print(f"❌ ERROR (Code {error.code}): {error.message}", file=sys.stderr)
        print(f"💡 HINT: {error.hint}", file=sys.stderr)
        print(f"🔗 Correlation ID: {error.correlation_id}", file=sys.stderr)

    def exit_with_error(self, error: ValidationError) -> None:
        """Exit with appropriate error code."""
        self.report_error(error)
        sys.exit(error.code)

    def get_validation_summary(self) -> str:
        """Get summary of all validation components."""
        summary = "CLI Validation Components:\n"
        summary += self.mutual_exclusion_validator.get_rules_summary()
        summary += "\n"
        summary += self.dependency_validator.get_dependencies_summary()
        summary += "\n"
        summary += self.mode_gate_validator.get_gated_flags_summary()
        summary += "\n"
        summary += self.message_validator.get_special_operations_summary()
        summary += "\n"
        summary += self.priority_validator.get_priority_guidance()
        return summary
