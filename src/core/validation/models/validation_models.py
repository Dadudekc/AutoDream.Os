#!/usr/bin/env python3
"""
Validation Models - Core data structures for validation system.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Callable


class ValidationType(Enum):
    """Types of validation operations."""
    
    REQUIRED_FIELDS = "required_fields"
    DATA_TYPES = "data_types"
    EMAIL = "email"
    URL = "url"
    STRING_LENGTH = "string_length"
    NUMERIC_RANGE = "numeric_range"
    REGEX_PATTERN = "regex_pattern"
    CUSTOM = "custom"


class ValidationSeverity(Enum):
    """Validation severity levels."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    
    is_valid: bool
    errors: List[str] = None
    warnings: List[str] = None
    severity: ValidationSeverity = ValidationSeverity.MEDIUM
    field_name: Optional[str] = None
    validation_type: Optional[ValidationType] = None
    details: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.details is None:
            self.details = {}


@dataclass
class ValidationRule:
    """Validation rule definition."""
    
    rule_type: ValidationType
    field_name: str
    parameters: Dict[str, Any]
    severity: ValidationSeverity = ValidationSeverity.MEDIUM
    custom_validator: Optional[Callable] = None
    error_message: Optional[str] = None


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    
    field_name: str
    issue_type: str
    message: str
    severity: ValidationSeverity
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationSummary:
    """Summary of validation results."""
    
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    is_valid: bool
    issues: List[ValidationIssue] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
