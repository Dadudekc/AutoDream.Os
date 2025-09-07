#!/usr/bin/env python3
"""
Validation Result Model - Consistent Validation Result Structure

This module provides the data structures for validation results, ensuring
consistent behavior across all validation operations in the unified system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Dict


class ValidationStatus(Enum):
    """Validation status enumeration for consistent status reporting."""
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PENDING = "PENDING"
    SKIPPED = "SKIPPED"


@dataclass
class ValidationResult:
    """
    Comprehensive validation result data structure.
    
    This class provides a consistent way to represent validation results
    across all validation operations in the unified system.
    """
    
    # Core validation information
    status: ValidationStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Validation details
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    
    # Data context
    validated_data: Any = None
    field_path: Optional[str] = None
    validation_rule: Optional[str] = None
    
    # Performance metrics
    validation_time_ms: Optional[float] = None
    memory_usage_kb: Optional[float] = None
    
    # Metadata
    validator_name: Optional[str] = None
    validator_version: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """
        Check if validation was successful.
        
        Returns:
            True if status is VALID, False otherwise
        """
        return self.status == ValidationStatus.VALID
    
    def has_errors(self) -> bool:
        """
        Check if validation has errors.
        
        Returns:
            True if there are errors, False otherwise
        """
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """
        Check if validation has warnings.
        
        Returns:
            True if there are warnings, False otherwise
        """
        return len(self.warnings) > 0
    
    def get_error_summary(self) -> str:
        """
        Get a summary of validation errors.
        
        Returns:
            Formatted string summary of errors
        """
        if not self.errors:
            return "No validation errors"
        
        error_count = len(self.errors)
        if error_count == 1:
            return f"1 validation error: {self.errors[0]}"
        else:
            return f"{error_count} validation errors: {'; '.join(self.errors[:3])}"
    
    def get_warning_summary(self) -> str:
        """
        Get a summary of validation warnings.
        
        Returns:
            Formatted string summary of warnings
        """
        if not self.warnings:
            return "No validation warnings"
        
        warning_count = len(self.warnings)
        if warning_count == 1:
            return f"1 validation warning: {self.warnings[0]}"
        else:
            return f"{warning_count} validation warnings: {'; '.join(self.warnings[:3])}"
    
    def add_error(self, error: str) -> None:
        """
        Add a validation error.
        
        Args:
            error: Error message to add
        """
        self.errors.append(error)
        if self.status == ValidationStatus.VALID:
            self.status = ValidationStatus.INVALID
    
    def add_warning(self, warning: str) -> None:
        """
        Add a validation warning.
        
        Args:
            warning: Warning message to add
        """
        self.warnings.append(warning)
        if self.status == ValidationStatus.VALID and not self.errors:
            self.status = ValidationStatus.WARNING
    
    def add_info(self, info: str) -> None:
        """
        Add informational message.
        
        Args:
            info: Informational message to add
        """
        self.info.append(info)
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """
        Merge another validation result into this one.
        
        Args:
            other: Another validation result to merge
            
        Returns:
            Merged validation result
        """
        # Merge errors and warnings
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)
        
        # Update status based on merged results
        if self.errors:
            self.status = ValidationStatus.INVALID
        elif self.warnings:
            self.status = ValidationStatus.WARNING
        else:
            self.status = ValidationStatus.VALID
        
        # Merge context
        self.context.update(other.context)
        
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert validation result to dictionary format.
        
        Returns:
            Dictionary representation of validation result
        """
        return {
            'status': self.status.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'field_path': self.field_path,
            'validation_rule': self.validation_rule,
            'validator_name': self.validator_name,
            'validator_version': self.validator_version,
            'validation_time_ms': self.validation_time_ms,
            'memory_usage_kb': self.memory_usage_kb,
            'context': self.context
        }
    
    def __str__(self) -> str:
        """String representation of validation result."""
        status_str = f"Status: {self.status.value}"
        message_str = f"Message: {self.message}"
        
        if self.errors:
            error_str = f"Errors: {len(self.errors)}"
        else:
            error_str = "Errors: None"
        
        if self.warnings:
            warning_str = f"Warnings: {len(self.warnings)}"
        else:
            warning_str = "Warnings: None"
        
        return f"{status_str} | {message_str} | {error_str} | {warning_str}"
    
    def __repr__(self) -> str:
        """Detailed string representation of validation result."""
        return (f"ValidationResult(status={self.status.value}, "
                f"message='{self.message}', "
                f"errors={len(self.errors)}, "
                f"warnings={len(self.warnings)})")
