"""
Message Validator - Unified Validation Framework

This module provides message validation functionality for UnifiedMessage system.
Inherits from BaseValidator and follows the unified validation framework patterns.
Eliminates duplicate validation logic - uses unified system.
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_validator import (
    BaseValidator,
    ValidationRule,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)
from src.services.messaging.models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
)


class MessageValidator(BaseValidator):
    """Validates UnifiedMessage data and structure using unified validation framework"""

    def __init__(self):
        """Initialize message validator"""
        super().__init__("MessageValidator")
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Setup default message validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="unified_message_structure",
                rule_name="Unified Message Structure",
                rule_type="message",
                description="Validate UnifiedMessage structure and format",
                severity=ValidationSeverity.ERROR,
            ),
            ValidationRule(
                rule_id="required_fields",
                rule_name="Required Fields",
                rule_type="message",
                description="Ensure all required UnifiedMessage fields are present",
                severity=ValidationSeverity.ERROR,
            ),
            ValidationRule(
                rule_id="message_format",
                rule_name="Message Format",
                rule_type="message",
                description="Validate UnifiedMessage format and encoding",
                severity=ValidationSeverity.WARNING,
            ),
            ValidationRule(
                rule_id="content_validation",
                rule_name="Content Validation",
                rule_type="message",
                description="Validate UnifiedMessage content and structure",
                severity=ValidationSeverity.WARNING,
            ),
            ValidationRule(
                rule_id="enum_validation",
                rule_name="Enum Validation",
                rule_type="message",
                description="Validate UnifiedMessage enum values",
                severity=ValidationSeverity.ERROR,
            ),
        ]

        for rule in default_rules:
            self.add_validation_rule(rule)

    def validate(
        self, message_data: Dict[str, Any], **kwargs
    ) -> List[ValidationResult]:
        """Validate UnifiedMessage data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during message
            validation.
        """
        results = []

        try:
            # Validate message structure
            structure_results = self._validate_unified_message_structure(message_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = [
                "message_id",
                "message_type",
                "priority",
                "status",
                "sender_id",
                "recipient_id",
                "content",
            ]
            field_results = self._validate_required_fields(
                message_data, required_fields
            )
            results.extend(field_results)

            # Validate enum values
            enum_results = self._validate_enum_values(message_data)
            results.extend(enum_results)

            # Validate timestamp if present
            if "timestamp" in message_data:
                timestamp_result = self._validate_timestamp(message_data["timestamp"])
                if timestamp_result:
                    results.append(timestamp_result)

            # Validate content if present
            if "content" in message_data:
                content_results = self._validate_content(message_data["content"])
                results.extend(content_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_unified_message_validation",
                    rule_name="Overall Unified Message Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="UnifiedMessage validation passed successfully",
                    details={"validated_fields": list(message_data.keys())},
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="validation_exception",
                rule_name="Validation Exception",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Validation failed with exception: {str(e)}",
                details={"exception": str(e)},
            )
            results.append(error_result)

        return results

    def validate_unified_message(
        self, message: UnifiedMessage
    ) -> List[ValidationResult]:
        """Validate a UnifiedMessage instance directly"""
        return self.validate(message.to_dict())

    def _validate_unified_message_structure(
        self, message_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate UnifiedMessage structure specifically"""
        results = []

        # Check for required UnifiedMessage fields
        expected_fields = {
            "message_id": str,
            "message_type": str,
            "priority": str,
            "status": str,
            "sender_id": str,
            "recipient_id": str,
            "content": str,
        }

        for field, expected_type in expected_fields.items():
            if field not in message_data:
                results.append(
                    self._create_result(
                        rule_id="missing_field",
                        rule_name=f"Missing Field: {field}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Required field '{field}' is missing",
                        details={"field": field, "expected_type": str(expected_type)},
                    )
                )
            elif not isinstance(message_data[field], expected_type):
                results.append(
                    self._create_result(
                        rule_id="invalid_field_type",
                        rule_name=f"Invalid Field Type: {field}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{field}' has invalid type",
                        details={
                            "field": field,
                            "expected_type": str(expected_type),
                            "actual_type": str(type(message_data[field])),
                        },
                    )
                )

        return results

    def _validate_enum_values(
        self, message_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate that enum values are valid"""
        results = []

        # Validate message_type
        if "message_type" in message_data:
            try:
                UnifiedMessageType(message_data["message_type"])
            except ValueError:
                results.append(
                    self._create_result(
                        rule_id="invalid_message_type",
                        rule_name="Invalid Message Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid message_type: {message_data['message_type']}",
                        details={"valid_types": [t.value for t in UnifiedMessageType]},
                    )
                )

        # Validate priority
        if "priority" in message_data:
            try:
                UnifiedMessagePriority(message_data["priority"])
            except ValueError:
                results.append(
                    self._create_result(
                        rule_id="invalid_priority",
                        rule_name="Invalid Priority",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid priority: {message_data['priority']}",
                        details={
                            "valid_priorities": [
                                p.value for p in UnifiedMessagePriority
                            ]
                        },
                    )
                )

        # Validate status
        if "status" in message_data:
            try:
                UnifiedMessageStatus(message_data["status"])
            except ValueError:
                results.append(
                    self._create_result(
                        rule_id="invalid_status",
                        rule_name="Invalid Status",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid status: {message_data['status']}",
                        details={
                            "valid_statuses": [s.value for s in UnifiedMessageStatus]
                        },
                    )
                )

        return results

    def _validate_required_fields(
        self, message_data: Dict[str, Any], required_fields: List[str]
    ) -> List[ValidationResult]:
        """Validate that all required fields are present"""
        results = []

        for field in required_fields:
            if field not in message_data or message_data[field] is None:
                results.append(
                    self._create_result(
                        rule_id="missing_required_field",
                        rule_name=f"Missing Required Field: {field}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Required field '{field}' is missing or null",
                        details={"field": field},
                    )
                )
            elif (
                isinstance(message_data[field], str) and not message_data[field].strip()
            ):
                results.append(
                    self._create_result(
                        rule_id="empty_required_field",
                        rule_name=f"Empty Required Field: {field}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Required field '{field}' is empty",
                        details={"field": field},
                    )
                )

        return results

    def _validate_message_format(self, format_data: Any) -> List[ValidationResult]:
        """Validate message format"""
        results = []

        if not isinstance(format_data, str):
            results.append(
                self._create_result(
                    rule_id="invalid_format_type",
                    rule_name="Invalid Format Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="Message format should be a string",
                    details={"actual_type": str(type(format_data))},
                )
            )

        return results

    def _validate_content(self, content: Any) -> List[ValidationResult]:
        """Validate message content"""
        results = []

        if not isinstance(content, str):
            results.append(
                self._create_result(
                    rule_id="invalid_content_type",
                    rule_name="Invalid Content Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="Message content should be a string",
                    details={"actual_type": str(type(content))},
                )
            )
        elif len(content.strip()) == 0:
            results.append(
                self._create_result(
                    rule_id="empty_content",
                    rule_name="Empty Content",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="Message content cannot be empty",
                    details={"content_length": len(content)},
                )
            )

        return results

    def _validate_timestamp(self, timestamp: Any) -> Optional[ValidationResult]:
        """Validate timestamp format"""
        if isinstance(timestamp, str):
            try:
                datetime.fromisoformat(timestamp)
                return None  # Valid timestamp
            except ValueError:
                return self._create_result(
                    rule_id="invalid_timestamp_format",
                    rule_name="Invalid Timestamp Format",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="Timestamp should be in ISO format",
                    details={"timestamp": timestamp},
                )
        elif isinstance(timestamp, datetime):
            return None  # Valid timestamp
        else:
            return self._create_result(
                rule_id="invalid_timestamp_type",
                rule_name="Invalid Timestamp Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Timestamp should be a string or datetime object",
                details={"actual_type": str(type(timestamp))},
            )

    def _validate_message_type(self, message_type: Any) -> Optional[ValidationResult]:
        """Validate message type"""
        if not isinstance(message_type, str):
            return self._create_result(
                rule_id="invalid_message_type_format",
                rule_name="Invalid Message Type Format",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Message type should be a string",
                details={"actual_type": str(type(message_type))},
            )
        return None


# Export the validator
__all__ = ["MessageValidator"]
