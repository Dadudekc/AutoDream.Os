#!/usr/bin/env python3
"""
Message Validation Engine Core - V2 Compliance Module
====================================================

Core engine logic for message validation.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import re
import logging
from typing import List, Dict, Any, Optional
from .models.validation_models import ValidationSeverity, ValidationResult, ValidationType


class MessageValidationEngineCore:
    """Core engine for message validation operations."""
    
    def __init__(self):
        """Initialize message validation engine core."""
        self.logger = logging.getLogger(__name__)
        self.patterns = {
            "message": {
                "required_fields": ["message", "sender", "recipient"],
                "optional_fields": ["priority", "type", "metadata"],
                "field_types": {
                    "message": str,
                    "sender": str,
                    "recipient": str,
                    "priority": str,
                    "type": str,
                    "metadata": dict
                },
                "field_validation": {
                    "message": {
                        "min_length": 1,
                        "max_length": 1000,
                        "pattern": r"^[a-zA-Z0-9\s\-_.,!?@#$%^&*()+=<>:;\"'\\/\[\]{}|`~]*$"
                    },
                    "sender": {
                        "min_length": 1,
                        "max_length": 100,
                        "pattern": r"^[a-zA-Z0-9\-_]+$"
                    },
                    "recipient": {
                        "min_length": 1,
                        "max_length": 100,
                        "pattern": r"^[a-zA-Z0-9\-_]+$"
                    },
                    "priority": {
                        "allowed_values": ["low", "normal", "high", "urgent"]
                    },
                    "type": {
                        "allowed_values": ["text", "broadcast", "onboarding", "agent_to_agent", "system_to_agent", "human_to_agent"]
                    }
                }
            }
        }
    
    def validate_message(self, message_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate message data."""
        issues = []
        
        try:
            pattern = self.patterns["message"]
            
            # Check required fields
            for field in pattern["required_fields"]:
                if field not in message_data:
                    issues.append(ValidationResult(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field,
                        validation_type=ValidationType.MESSAGE
                    ))
            
            # Validate field types
            for field, expected_type in pattern["field_types"].items():
                if field in message_data:
                    if not isinstance(message_data[field], expected_type):
                        issues.append(ValidationResult(
                            message=f"Field '{field}' must be of type {expected_type.__name__}",
                            severity=ValidationSeverity.ERROR,
                            field=field,
                            validation_type=ValidationType.MESSAGE
                        ))
            
            # Validate field values
            for field, validation_rules in pattern["field_validation"].items():
                if field in message_data:
                    field_issues = self._validate_field_value(
                        field, message_data[field], validation_rules
                    )
                    issues.extend(field_issues)
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Message validation error: {e}")
            issues.append(ValidationResult(
                message=f"Validation error: {str(e)}",
                severity=ValidationSeverity.ERROR,
                field="unknown",
                validation_type=ValidationType.MESSAGE
            ))
            return issues
    
    def validate_message_structure(self, message_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate message structure."""
        issues = []
        
        try:
            # Check for required top-level structure
            if not isinstance(message_data, dict):
                issues.append(ValidationResult(
                    message="Message data must be a dictionary",
                    severity=ValidationSeverity.ERROR,
                    field="root",
                    validation_type=ValidationType.MESSAGE
                ))
                return issues
            
            # Check for empty message
            if not message_data:
                issues.append(ValidationResult(
                    message="Message data cannot be empty",
                    severity=ValidationSeverity.ERROR,
                    field="root",
                    validation_type=ValidationType.MESSAGE
                ))
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Message structure validation error: {e}")
            issues.append(ValidationResult(
                message=f"Structure validation error: {str(e)}",
                severity=ValidationSeverity.ERROR,
                field="root",
                validation_type=ValidationType.MESSAGE
            ))
            return issues
    
    def validate_message_content(self, message: str) -> List[ValidationResult]:
        """Validate message content."""
        issues = []
        
        try:
            if not message or not message.strip():
                issues.append(ValidationResult(
                    message="Message content cannot be empty",
                    severity=ValidationSeverity.ERROR,
                    field="message",
                    validation_type=ValidationType.MESSAGE
                ))
                return issues
            
            # Check message length
            if len(message) > 1000:
                issues.append(ValidationResult(
                    message="Message content exceeds maximum length of 1000 characters",
                    severity=ValidationSeverity.ERROR,
                    field="message",
                    validation_type=ValidationType.MESSAGE
                ))
            
            # Check for valid characters
            if not re.match(r"^[a-zA-Z0-9\s\-_.,!?@#$%^&*()+=<>:;\"'\\/\[\]{}|`~]*$", message):
                issues.append(ValidationResult(
                    message="Message content contains invalid characters",
                    severity=ValidationSeverity.WARNING,
                    field="message",
                    validation_type=ValidationType.MESSAGE
                ))
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Message content validation error: {e}")
            issues.append(ValidationResult(
                message=f"Content validation error: {str(e)}",
                severity=ValidationSeverity.ERROR,
                field="message",
                validation_type=ValidationType.MESSAGE
            ))
            return issues
    
    def _validate_field_value(self, field: str, value: Any, rules: Dict[str, Any]) -> List[ValidationResult]:
        """Validate individual field value."""
        issues = []
        
        try:
            # Check minimum length
            if "min_length" in rules and len(str(value)) < rules["min_length"]:
                issues.append(ValidationResult(
                    message=f"Field '{field}' must be at least {rules['min_length']} characters long",
                    severity=ValidationSeverity.ERROR,
                    field=field,
                    validation_type=ValidationType.MESSAGE
                ))
            
            # Check maximum length
            if "max_length" in rules and len(str(value)) > rules["max_length"]:
                issues.append(ValidationResult(
                    message=f"Field '{field}' must be no more than {rules['max_length']} characters long",
                    severity=ValidationSeverity.ERROR,
                    field=field,
                    validation_type=ValidationType.MESSAGE
                ))
            
            # Check pattern
            if "pattern" in rules and not re.match(rules["pattern"], str(value)):
                issues.append(ValidationResult(
                    message=f"Field '{field}' does not match required pattern",
                    severity=ValidationSeverity.ERROR,
                    field=field,
                    validation_type=ValidationType.MESSAGE
                ))
            
            # Check allowed values
            if "allowed_values" in rules and value not in rules["allowed_values"]:
                issues.append(ValidationResult(
                    message=f"Field '{field}' must be one of: {', '.join(rules['allowed_values'])}",
                    severity=ValidationSeverity.ERROR,
                    field=field,
                    validation_type=ValidationType.MESSAGE
                ))
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Field validation error for {field}: {e}")
            issues.append(ValidationResult(
                message=f"Field validation error: {str(e)}",
                severity=ValidationSeverity.ERROR,
                field=field,
                validation_type=ValidationType.MESSAGE
            ))
            return issues
