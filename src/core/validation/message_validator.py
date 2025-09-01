#!/usr/bin/env python3
"""
Message Validator Module - Agent Cellphone V2
==========================================

Message validation functionality for validation system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any, List

from .validation_models import ValidationIssue, ValidationSeverity


class MessageValidator:
    """Handles message structure validation."""

    def validate_message_structure(self, message_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate message structure against rules."""
        issues = []

        # Check required fields
        required_fields = ['content', 'sender', 'recipient']
        for field in required_fields:
            if field not in message_data:
                issues.append(ValidationIssue(
                    rule_id="required_fields",
                    rule_name="Required Fields",
                    severity=ValidationSeverity.ERROR,
                    message=f"Missing required field: {field}",
                    details={"field": field, "message_data": message_data},
                    timestamp=datetime.now(),
                    component="message_structure"
                ))

        # Check message format
        if 'content' in message_data and not isinstance(message_data['content'], str):
            issues.append(ValidationIssue(
                rule_id="message_format",
                rule_name="Message Format",
                severity=ValidationSeverity.ERROR,
                message="Message content must be a string",
                details={"field": "content", "type": type(message_data['content'])},
                timestamp=datetime.now(),
                component="message_structure"
            ))

        # Check enum values
        if 'message_type' in message_data:
            valid_types = ['text', 'broadcast', 'onboarding']
            if message_data['message_type'] not in valid_types:
                issues.append(ValidationIssue(
                    rule_id="enum_validation",
                    rule_name="Enum Validation",
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid message type: {message_data['message_type']}",
                    details={"valid_types": valid_types, "provided": message_data['message_type']},
                    timestamp=datetime.now(),
                    component="message_structure"
                ))

        return issues
