#!/usr/bin/env python3
"""
Simple Validation System - V2 Compliant
=======================================

A clean, simple validation system that replaces the overcomplex validation architecture.
Focus: Essential validation only, no overengineering.

@version 2.0.0 - SIMPLIFIED VALIDATION
@license MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Simple validation result."""
    is_valid: bool
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    field: Optional[str] = None


class SimpleValidator:
    """Simple, unified validator for all validation needs."""
    
    def __init__(self):
        self.logger = self._get_logger()
    
    def _get_logger(self):
        """Get logger instance."""
        import logging
        return logging.getLogger(__name__)
    
    def validate_coordinates(self, coords: Tuple[int, int], recipient: str = None) -> ValidationResult:
        """Validate coordinates for PyAutoGUI operations."""
        if not isinstance(coords, tuple) or len(coords) != 2:
            return ValidationResult(False, "Coordinates must be a tuple of (x, y)", ValidationSeverity.ERROR)
        
        x, y = coords
        if not isinstance(x, int) or not isinstance(y, int):
            return ValidationResult(False, "Coordinates must be integers", ValidationSeverity.ERROR)
        
        if x < 0 or y < 0:
            return ValidationResult(False, "Coordinates must be positive", ValidationSeverity.ERROR)
        
        if x > 5000 or y > 5000:
            return ValidationResult(False, "Coordinates seem too large", ValidationSeverity.WARNING)
        
        return ValidationResult(True, "Coordinates valid")
    
    def validate_message(self, message_data: Dict[str, Any]) -> ValidationResult:
        """Validate message data."""
        if not isinstance(message_data, dict):
            return ValidationResult(False, "Message data must be a dictionary", ValidationSeverity.ERROR)
        
        required_fields = ['content', 'recipient', 'sender']
        for field in required_fields:
            if field not in message_data:
                return ValidationResult(False, f"Missing required field: {field}", ValidationSeverity.ERROR)
        
        content = message_data.get('content', '')
        if not isinstance(content, str) or len(content.strip()) == 0:
            return ValidationResult(False, "Message content must be a non-empty string", ValidationSeverity.ERROR)
        
        if len(content) > 2000:
            return ValidationResult(False, "Message content too long", ValidationSeverity.WARNING)
        
        return ValidationResult(True, "Message valid")
    
    def validate_agent_id(self, agent_id: str) -> ValidationResult:
        """Validate agent ID format."""
        if not isinstance(agent_id, str):
            return ValidationResult(False, "Agent ID must be a string", ValidationSeverity.ERROR)
        
        if not agent_id.startswith('Agent-'):
            return ValidationResult(False, "Agent ID must start with 'Agent-'", ValidationSeverity.ERROR)
        
        try:
            agent_num = int(agent_id.split('-')[1])
            if agent_num < 1 or agent_num > 8:
                return ValidationResult(False, "Agent number must be between 1-8", ValidationSeverity.ERROR)
        except (IndexError, ValueError):
            return ValidationResult(False, "Invalid agent ID format", ValidationSeverity.ERROR)
        
        return ValidationResult(True, "Agent ID valid")
    
    def validate_string_length(self, text: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
        """Validate string length."""
        if not isinstance(text, str):
            return ValidationResult(False, "Text must be a string", ValidationSeverity.ERROR)
        
        if len(text) < min_length:
            return ValidationResult(False, f"Text too short (min: {min_length})", ValidationSeverity.ERROR)
        
        if len(text) > max_length:
            return ValidationResult(False, f"Text too long (max: {max_length})", ValidationSeverity.ERROR)
        
        return ValidationResult(True, "String length valid")
    
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate configuration data."""
        if not isinstance(config, dict):
            return ValidationResult(False, "Config must be a dictionary", ValidationSeverity.ERROR)
        
        # Check for required config fields
        required_fields = ['message_history_limit', 'delivery_timeout']
        for field in required_fields:
            if field not in config:
                return ValidationResult(False, f"Missing required config field: {field}", ValidationSeverity.ERROR)
        
        return ValidationResult(True, "Config valid")
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Validate required fields and return missing fields."""
        missing = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing.append(field)
        return missing
    
    def validate_required(self, values: List[Any]) -> bool:
        """Validate that all required values are present and not empty."""
        for value in values:
            if value is None or (isinstance(value, str) and len(value.strip()) == 0):
                return False
        return True


# Global instance
_simple_validator = None

def get_simple_validator() -> SimpleValidator:
    """Get the global simple validator instance."""
    global _simple_validator
    if _simple_validator is None:
        _simple_validator = SimpleValidator()
    return _simple_validator

# Backward compatibility
get_unified_validator = get_simple_validator
