#!/usr/bin/env python3
"""
Validation Models - Agent Cellphone V2
=====================================

Validation models and exceptions for the messaging system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""



class ValidationError(Exception):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None):
        """Initialize validation error."""
        super().__init__(message)
        self.field = field
        self.value = value
        self.message = message
    
    def __str__(self) -> str:
        """String representation of validation error."""
        if self.field:
            return f"Validation error in field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, valid: bool = True, errors: Optional[List[ValidationError]] = None):
        """Initialize validation result."""
        self.valid = valid
        self.errors = errors or []
    
    def add_error(self, error: ValidationError) -> None:
        """Add a validation error."""
        self.errors.append(error)
        self.valid = False
    
    def has_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.errors) > 0
    
    def get_error_messages(self) -> List[str]:
        """Get all error messages."""
        return [str(error) for error in self.errors]
