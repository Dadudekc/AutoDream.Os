#!/usr/bin/env python3
"""
Message Validation Engine
=========================

Message validation engine for the unified validation system.
Handles message validation for communication systems.
V2 COMPLIANT: Focused message validation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR MESSAGE VALIDATION
@license MIT
"""

import re
import logging
from typing import List, Dict, Any, Optional

from .models.validation_models import (
    ValidationSeverity, ValidationResult, ValidationType
)


class MessageValidationEngine:
    """Message validation engine for communication systems"""
    
    def __init__(self):
        """Initialize message validation engine"""
        self.logger = logging.getLogger(__name__)
        self.pattern = ValidationPatterns.get_pattern("message")
    
    def validate_message(self, message_data: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate message data.
        
        Args:
            message_data: Message data dictionary
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Check required fields
            for field in self.pattern.required_fields:
                if field not in message_data:
                    issues.append(create_validation_issue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate content
            if "content" in message_data:
                content_issues = self._validate_content(message_data["content"])
                issues.extend(content_issues)
            
            # Validate recipient
            if "recipient" in message_data:
                recipient_issues = self._validate_recipient(message_data["recipient"])
                issues.extend(recipient_issues)
            
            # Validate message type
            if "type" in message_data:
                type_issues = self._validate_message_type(message_data["type"])
                issues.extend(type_issues)
            
            # Validate priority
            if "priority" in message_data:
                priority_issues = self._validate_priority(message_data["priority"])
                issues.extend(priority_issues)
            
            # Validate sender
            if "sender" in message_data:
                sender_issues = self._validate_sender(message_data["sender"])
                issues.extend(sender_issues)
            
            # Log validation results
            if issues:
                self.logger.warning(f"Message validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Message validation passed")
                
        except Exception as e:
            issues.append(create_validation_issue(
                message=f"Message validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="message_data",
                value=message_data
            ))
        
        return issues
    
    def _validate_content(self, content: str) -> List[ValidationResult]:
        """Validate message content."""
        issues = []
        
        if not content:
            issues.append(create_validation_issue(
                message="Message content cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="content"
            ))
            return issues
        
        if not isinstance(content, str):
            issues.append(create_validation_issue(
                message="Message content must be a string",
                severity=ValidationSeverity.ERROR,
                field="content",
                value=content
            ))
            return issues
        
        # Check length
        max_length = self.pattern.constraints["max_length"]
        if len(content) > max_length:
            issues.append(create_validation_issue(
                message=f"Message content exceeds maximum length of {max_length} characters",
                severity=ValidationSeverity.WARNING,
                field="content",
                value=len(content),
                suggestion=f"Consider shortening to {max_length} characters or less"
            ))
        
        # Check for potentially problematic content
        if self._contains_suspicious_content(content):
            issues.append(create_validation_issue(
                message="Message content contains potentially suspicious patterns",
                severity=ValidationSeverity.WARNING,
                field="content",
                suggestion="Review content for security concerns"
            ))
        
        return issues
    
    def _validate_recipient(self, recipient: str) -> List[ValidationResult]:
        """Validate message recipient."""
        issues = []
        
        if not recipient:
            issues.append(create_validation_issue(
                message="Recipient cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="recipient"
            ))
            return issues
        
        if not isinstance(recipient, str):
            issues.append(create_validation_issue(
                message="Recipient must be a string",
                severity=ValidationSeverity.ERROR,
                field="recipient",
                value=recipient
            ))
            return issues
        
        # Validate recipient format
        if not self._is_valid_recipient_format(recipient):
            issues.append(create_validation_issue(
                message=f"Invalid recipient format: {recipient}",
                severity=ValidationSeverity.WARNING,
                field="recipient",
                value=recipient,
                suggestion="Use format like 'Agent-X' or 'system'"
            ))
        
        return issues
    
    def _validate_message_type(self, message_type: str) -> List[ValidationResult]:
        """Validate message type."""
        issues = []
        
        if not message_type:
            issues.append(create_validation_issue(
                message="Message type cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="type"
            ))
            return issues
        
        allowed_types = self.pattern.allowed_values["type"]
        if message_type not in allowed_types:
            issues.append(create_validation_issue(
                message=f"Invalid message type: {message_type}",
                severity=ValidationSeverity.ERROR,
                field="type",
                value=message_type,
                suggestion=f"Use one of: {', '.join(allowed_types)}"
            ))
        
        return issues
    
    def _validate_priority(self, priority: str) -> List[ValidationResult]:
        """Validate message priority."""
        issues = []
        
        if not priority:
            issues.append(create_validation_issue(
                message="Priority cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="priority"
            ))
            return issues
        
        allowed_priorities = ["normal", "urgent", "low", "high"]
        if priority not in allowed_priorities:
            issues.append(create_validation_issue(
                message=f"Invalid priority: {priority}",
                severity=ValidationSeverity.WARNING,
                field="priority",
                value=priority,
                suggestion=f"Use one of: {', '.join(allowed_priorities)}"
            ))
        
        return issues
    
    def _validate_sender(self, sender: str) -> List[ValidationResult]:
        """Validate message sender."""
        issues = []
        
        if not sender:
            issues.append(create_validation_issue(
                message="Sender cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="sender"
            ))
            return issues
        
        if not isinstance(sender, str):
            issues.append(create_validation_issue(
                message="Sender must be a string",
                severity=ValidationSeverity.ERROR,
                field="sender",
                value=sender
            ))
            return issues
        
        # Validate sender format
        if not self._is_valid_sender_format(sender):
            issues.append(create_validation_issue(
                message=f"Invalid sender format: {sender}",
                severity=ValidationSeverity.WARNING,
                field="sender",
                value=sender,
                suggestion="Use format like 'Agent-X', 'system', or 'human'"
            ))
        
        return issues
    
    def _contains_suspicious_content(self, content: str) -> bool:
        """Check if content contains suspicious patterns."""
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'data:text/html',  # Data URLs
            r'<iframe.*?>.*?</iframe>',  # Iframe tags
            r'<object.*?>.*?</object>',  # Object tags
            r'<embed.*?>.*?</embed>'  # Embed tags
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _is_valid_recipient_format(self, recipient: str) -> bool:
        """Check if recipient format is valid."""
        valid_patterns = [
            r'^Agent-\d+$',  # Agent-X format
            r'^system$',  # System
            r'^human$',  # Human
            r'^all$',  # All agents
            r'^broadcast$'  # Broadcast
        ]
        
        for pattern in valid_patterns:
            if re.match(pattern, recipient, re.IGNORECASE):
                return True
        
        return False
    
    def _is_valid_sender_format(self, sender: str) -> bool:
        """Check if sender format is valid."""
        valid_patterns = [
            r'^Agent-\d+$',  # Agent-X format
            r'^system$',  # System
            r'^human$',  # Human
            r'^Captain Agent-\d+$'  # Captain Agent-X format
        ]
        
        for pattern in valid_patterns:
            if re.match(pattern, sender, re.IGNORECASE):
                return True
        
        return False
    
    def get_message_validation_result(self, message_data: Dict[str, Any]) -> ValidationResult:
        """Get comprehensive validation result for message."""
        issues = self.validate_message(message_data)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return create_validation_result(
            is_valid=is_valid,
            issues=issues,
            validated_data=message_data,
            validation_type="message"
        )


# Factory function for dependency injection
def create_message_validation_engine() -> MessageValidationEngine:
    """Factory function to create message validation engine"""
    return MessageValidationEngine()


# Export for DI
__all__ = ['MessageValidationEngine', 'create_message_validation_engine']
