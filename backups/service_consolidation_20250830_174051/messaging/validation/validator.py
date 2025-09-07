"""
Message Validator - Extracted from v2_comprehensive_messaging_system.py

This module handles message validation including:
- Message format validation
- Content validation
- Business rule validation
- Schema validation

Original file: src/core/v2_comprehensive_messaging_system.py
Extraction date: 2024-12-19
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

# Import enums and data structures from consolidated modules
from ..types.v2_message_enums import V2MessageType, V2MessagePriority, V2MessageStatus
from ..models.v2_message import V2Message

# Define missing classes for compatibility
@dataclass
class V2AgentInfo:
    """Agent information for validation"""
    agent_id: str
    status: str


class V2MessageValidator:
    """Message validation implementation - SRP: Validate message content and format"""
    
    def __init__(self):
        self.validation_rules: Dict[V2MessageType, List[callable]] = {}
        self.required_fields: Dict[V2MessageType, List[str]] = {}
        self.field_validators: Dict[str, callable] = {}
        self._setup_default_validators()
        
    def _setup_default_validators(self):
        """Setup default validation rules and field validators"""
        # Required fields for different message types
        self.required_fields = {
            V2MessageType.TASK_ASSIGNMENT: ['sender_id', 'recipient_id', 'subject', 'content', 'task_id'],
            V2MessageType.STATUS_UPDATE: ['sender_id', 'recipient_id', 'subject', 'content'],
            V2MessageType.COORDINATION: ['sender_id', 'recipient_id', 'subject', 'content'],
            V2MessageType.BROADCAST: ['sender_id', 'subject', 'content'],
            V2MessageType.SYSTEM: ['sender_id', 'subject', 'content'],
            V2MessageType.ALERT: ['sender_id', 'subject', 'content', 'priority'],
            V2MessageType.WORKFLOW_UPDATE: ['sender_id', 'recipient_id', 'subject', 'content', 'workflow_id']
        }
        
        # Field validators
        self.field_validators = {
            'message_id': self._validate_uuid,
            'sender_id': self._validate_agent_id,
            'recipient_id': self._validate_agent_id,
            'subject': self._validate_subject,
            'content': self._validate_content,
            'priority': self._validate_priority,
            'timestamp': self._validate_timestamp,
            'task_id': self._validate_uuid,
            'workflow_id': self._validate_uuid
        }
        
    def validate_message(self, message: V2Message) -> Tuple[bool, List[str]]:
        """Validate a message and return validation result with error messages"""
        errors = []
        
        try:
            # Check required fields
            required_fields = self.required_fields.get(message.message_type, [])
            for field in required_fields:
                if not hasattr(message, field) or not getattr(message, field):
                    errors.append(f"Missing required field: {field}")
            
            # Validate field values
            for field_name, validator_func in self.field_validators.items():
                if hasattr(message, field_name):
                    field_value = getattr(message, field_name)
                    if field_value is not None:
                        if not validator_func(field_value):
                            errors.append(f"Invalid value for field: {field_name}")
            
            # Validate message type specific rules
            type_errors = self._validate_message_type_rules(message)
            errors.extend(type_errors)
            
            # Validate business rules
            business_errors = self._validate_business_rules(message)
            errors.extend(business_errors)
            
            return len(errors) == 0, errors
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            errors.append(f"Validation error: {str(e)}")
            return False, errors
    
    def _validate_uuid(self, value: str) -> bool:
        """Validate UUID format"""
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        return bool(uuid_pattern.match(str(value)))
    
    def _validate_agent_id(self, value: str) -> bool:
        """Validate agent ID format"""
        if not value or value == "broadcast":
            return True
        # Agent IDs should be non-empty strings
        return bool(value and isinstance(value, str) and len(value.strip()) > 0)
    
    def _validate_subject(self, value: str) -> bool:
        """Validate subject field"""
        if not value:
            return False
        # Subject should be non-empty and reasonable length
        return bool(isinstance(value, str) and 1 <= len(value.strip()) <= 200)
    
    def _validate_content(self, value: str) -> bool:
        """Validate content field"""
        if not value:
            return False
        # Content should be non-empty and reasonable length
        return bool(isinstance(value, str) and 1 <= len(value.strip()) <= 10000)
    
    def _validate_priority(self, value) -> bool:
        """Validate priority value"""
        from ..v2_comprehensive_messaging_system import V2MessagePriority
        return isinstance(value, V2MessagePriority)
    
    def _validate_timestamp(self, value) -> bool:
        """Validate timestamp value"""
        return isinstance(value, datetime)
    
    def _validate_message_type_rules(self, message: V2Message) -> List[str]:
        """Validate message type specific rules"""
        errors = []
        
        try:
            if message.message_type == V2MessageType.TASK_ASSIGNMENT:
                if not message.task_id:
                    errors.append("Task assignment messages must include task_id")
                    
            elif message.message_type == V2MessageType.WORKFLOW_UPDATE:
                if not message.workflow_id:
                    errors.append("Workflow update messages must include workflow_id")
                    
            elif message.message_type == V2MessageType.ONBOARDING_PHASE:
                if message.phase_number is None:
                    errors.append("Onboarding phase messages must include phase_number")
                    
            elif message.message_type == V2MessageType.BROADCAST:
                if message.recipient_id and message.recipient_id != "broadcast":
                    errors.append("Broadcast messages should not have specific recipient_id")
                    
        except Exception as e:
            logger.error(f"Error validating message type rules: {e}")
            errors.append(f"Message type validation error: {str(e)}")
            
        return errors
    
    def _validate_business_rules(self, message: V2Message) -> List[str]:
        """Validate business logic rules"""
        errors = []
        
        try:
            # Check for circular references
            if message.message_id in message.dependencies:
                errors.append("Message cannot depend on itself")
            
            # Check TTL validity
            if message.ttl is not None and message.ttl <= 0:
                errors.append("TTL must be positive if specified")
            
            # Check retry count validity
            if message.retry_count < 0:
                errors.append("Retry count cannot be negative")
            if message.max_retries < 0:
                errors.append("Max retries cannot be negative")
            if message.retry_count > message.max_retries:
                errors.append("Retry count cannot exceed max retries")
            
            # Check timestamp validity
            if message.timestamp and message.created_at:
                if message.timestamp < message.created_at:
                    errors.append("Timestamp cannot be before creation time")
            
        except Exception as e:
            logger.error(f"Error validating business rules: {e}")
            errors.append(f"Business rule validation error: {str(e)}")
            
        return errors
    
    def add_validation_rule(self, message_type: V2MessageType, validator_func: callable) -> None:
        """Add custom validation rule for message type"""
        if message_type not in self.validation_rules:
            self.validation_rules[message_type] = []
        self.validation_rules[message_type].append(validator_func)
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics for monitoring"""
        return {
            "validation_rules_count": len(self.validation_rules),
            "required_fields_count": len(self.required_fields),
            "field_validators_count": len(self.field_validators)
        }
