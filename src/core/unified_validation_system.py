#!/usr/bin/env python3
"""
Unified Validation System - DRY Violation Elimination
====================================================

Eliminates duplicate validation patterns across 8+ modules:
- src/core/validation/coordination_validator.py
- src/utils/config_pattern_scanner.py
- src/services/messaging_core.py
- src/core/validation/javascript_v2_compliance_validator.py
- src/core/validation/agent7_v2_compliance_coordinator.py
- src/core/validation/repository_pattern_validator.py
- src/core/validation/enhanced_cli_validation_framework.py
- src/core/validation/gaming_performance_threshold_checker.py

CONSOLIDATED: Single source of truth for all validation operations.

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violation Elimination
Status: CONSOLIDATED - Validation Duplication Eliminated
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable

# Removed circular import - will use local fallbacks


# ================================
# VALIDATION TYPES
# ================================

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

# ================================
# VALIDATION RESULT
# ================================

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

# ================================
# VALIDATION RULES
# ================================

@dataclass
class ValidationRule:
    """Validation rule definition."""
    
    rule_type: ValidationType
    field_name: str
    parameters: Dict[str, Any]
    severity: ValidationSeverity = ValidationSeverity.MEDIUM
    custom_validator: Optional[Callable] = None
    error_message: Optional[str] = None

# ================================
# UNIFIED VALIDATION SYSTEM
# ================================

class UnifiedValidationSystem:
    """
    Unified validation system that eliminates duplicate validation patterns.
    
    CONSOLIDATES:
    - validate_required_fields(data, required_fields) (duplicated in 8+ files)
    - validate_data_types(data, type_requirements) (duplicated in 8+ files)
    - validate_email (duplicated in 5+ files)
    - validate_url (duplicated in 4+ files)
    - validate_string_length (duplicated in 6+ files)
    - validate_numeric_range (duplicated in 3+ files)
    - validate_regex_pattern (duplicated in 4+ files)
    """
    
    def __init__(self):
        """Initialize unified validation system."""
        self.config = {}
        import logging
        self.logger = logging.getLogger(__name__)
        
        # Validation patterns
        self._patterns = {
            "email": re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            "url": re.compile(r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'),
            "phone": re.compile(r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'),
            "uuid": re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE),
            "alphanumeric": re.compile(r'^[a-zA-Z0-9]+$'),
            "numeric": re.compile(r'^[0-9]+$'),
            "alpha": re.compile(r'^[a-zA-Z]+$')
        }
        
        # Default validation rules
        self._default_rules = {
            "string_length": {"min": 0, "max": 1000},
            "numeric_range": {"min": 0, "max": 999999},
            "required_fields": [],
            "data_types": {}
        }
    
    def validate_required(self, data: Any) -> bool:
        """Validate that data is not None or empty."""
        return data is not None and data != "" and data != []
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
        """
        Validate required fields - consolidates 8+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_pattern_scanner.py
        - src/services/messaging_core.py
        - src/core/validation/javascript_v2_compliance_validator.py
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing_fields.append(field)
        
        is_valid = len(missing_fields) == 0
        errors = [f"Required field missing: {field}" for field in missing_fields] if missing_fields else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.HIGH,
            validation_type=ValidationType.REQUIRED_FIELDS,
            details={"missing_fields": missing_fields}
        )
    
    def validate_data_types(self, data: Dict[str, Any], type_requirements: Dict[str, type]) -> ValidationResult:
        """
        Validate data types - consolidates 8+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_pattern_scanner.py
        - src/services/messaging_core.py
        - src/core/validation/javascript_v2_compliance_validator.py
        """
        invalid_fields = []
        
        for field, expected_type in type_requirements.items():
            if field in data and not isinstance(data[field], expected_type):
                invalid_fields.append(field)
        
        is_valid = len(invalid_fields) == 0
        errors = [f"Invalid type for field '{field}': expected {type_requirements[field].__name__}" 
                 for field in invalid_fields] if invalid_fields else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.DATA_TYPES,
            details={"invalid_fields": invalid_fields}
        )
    
    def validate_email(self, email: str) -> ValidationResult:
        """Validate email format - consolidates 5+ duplicate implementations."""
        if not email:
            return ValidationResult(
                is_valid=False,
                errors=["Email is required"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.EMAIL
            )
        
        is_valid = bool(self._patterns["email"].match(email))
        errors = ["Invalid email format"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.EMAIL
        )
    
    def validate_url(self, url: str) -> ValidationResult:
        """Validate URL format - consolidates 4+ duplicate implementations."""
        if not url:
            return ValidationResult(
                is_valid=False,
                errors=["URL is required"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.URL
            )
        
        is_valid = bool(self._patterns["url"].match(url))
        errors = ["Invalid URL format"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.URL
        )
    
    def validate_string_length(self, value: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
        """Validate string length - consolidates 6+ duplicate implementations."""
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be a string"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.STRING_LENGTH
            )
        
        length = len(value)
        errors = []
        
        if length < min_length:
            errors.append(f"String too short: {length} < {min_length}")
        if length > max_length:
            errors.append(f"String too long: {length} > {max_length}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.STRING_LENGTH,
            details={"length": length, "min_length": min_length, "max_length": max_length}
        )
    
    def validate_numeric_range(self, value: Union[int, float], min_value: float = 0, max_value: float = 999999) -> ValidationResult:
        """Validate numeric range - consolidates 3+ duplicate implementations."""
        if not isinstance(value, (int, float)):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be numeric"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.NUMERIC_RANGE
            )
        
        errors = []
        
        if value < min_value:
            errors.append(f"Value too small: {value} < {min_value}")
        if value > max_value:
            errors.append(f"Value too large: {value} > {max_value}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.NUMERIC_RANGE,
            details={"value": value, "min_value": min_value, "max_value": max_value}
        )
    
    def validate_regex_pattern(self, value: str, pattern_name: str) -> ValidationResult:
        """Validate regex pattern - consolidates 4+ duplicate implementations."""
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be a string"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.REGEX_PATTERN
            )
        
        if pattern_name not in self._patterns:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unknown pattern: {pattern_name}"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.REGEX_PATTERN
            )
        
        is_valid = bool(self._patterns[pattern_name].match(value))
        errors = [f"Value does not match pattern: {pattern_name}"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.REGEX_PATTERN,
            details={"pattern_name": pattern_name}
        )
    
    def validate_custom(self, value: Any, validator: Callable, field_name: str = "field") -> ValidationResult:
        """Validate using custom validator function."""
        try:
            result = validator(value)
            if isinstance(result, bool):
                is_valid = result
                errors = [] if is_valid else [f"Custom validation failed for {field_name}"]
            elif isinstance(result, ValidationResult):
                return result
            else:
                is_valid = bool(result)
                errors = [] if is_valid else [f"Custom validation failed for {field_name}"]
        except Exception as e:
            is_valid = False
            errors = [f"Custom validation error for {field_name}: {str(e)}"]
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.CUSTOM,
            field_name=field_name
        )
    
    def validate_multiple(self, data: Dict[str, Any], rules: List[ValidationRule]) -> List[ValidationResult]:
        """Validate multiple fields with different rules."""
        results = []
        
        for rule in rules:
            if rule.field_name not in data:
                if rule.severity == ValidationSeverity.HIGH:
                    results.append(ValidationResult(
                        is_valid=False,
                        errors=[f"Required field missing: {rule.field_name}"],
                        severity=rule.severity,
                        field_name=rule.field_name,
                        validation_type=rule.rule_type
                    ))
                continue
            
            value = data[rule.field_name]
            
            if rule.rule_type == ValidationType.REQUIRED_FIELDS:
                result = self.validate_required_fields({rule.field_name: value}, [rule.field_name])
            elif rule.rule_type == ValidationType.DATA_TYPES:
                result = self.validate_data_types({rule.field_name: value}, {rule.field_name: rule.parameters.get("type", str)})
            elif rule.rule_type == ValidationType.EMAIL:
                result = self.validate_email(value)
            elif rule.rule_type == ValidationType.URL:
                result = self.validate_url(value)
            elif rule.rule_type == ValidationType.STRING_LENGTH:
                result = self.validate_string_length(value, rule.parameters.get("min", 0), rule.parameters.get("max", 1000))
            elif rule.rule_type == ValidationType.NUMERIC_RANGE:
                result = self.validate_numeric_range(value, rule.parameters.get("min", 0), rule.parameters.get("max", 999999))
            elif rule.rule_type == ValidationType.REGEX_PATTERN:
                result = self.validate_regex_pattern(value, rule.parameters.get("pattern", "alphanumeric"))
            elif rule.rule_type == ValidationType.CUSTOM:
                result = self.validate_custom(value, rule.custom_validator, rule.field_name)
            else:
                result = ValidationResult(
                    is_valid=False,
                    errors=[f"Unknown validation type: {rule.rule_type}"],
                    severity=ValidationSeverity.HIGH,
                    field_name=rule.field_name,
                    validation_type=rule.rule_type
                )
            
            result.field_name = rule.field_name
            result.validation_type = rule.rule_type
            result.severity = rule.severity
            results.append(result)
        
        return results

# ================================
# GLOBAL VALIDATION INSTANCE
# ================================

# Single global instance to eliminate duplicate validation objects
_unified_validator = None

def get_unified_validator() -> UnifiedValidationSystem:
    """Get global unified validation instance."""
    global _unified_validator
    if _unified_validator is None:
        _unified_validator = UnifiedValidationSystem()
    return _unified_validator

# ================================
# CONVENIENCE FUNCTIONS
# ================================

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """Validate required fields."""
    return get_unified_validator().validate_required_fields(data, required_fields)

def validate_data_types(data: Dict[str, Any], type_requirements: Dict[str, type]) -> ValidationResult:
    """Validate data types."""
    return get_unified_validator().validate_data_types(data, type_requirements)

def validate_email(email: str) -> ValidationResult:
    """Validate email format."""
    return get_unified_validator().validate_email(email)

def validate_url(url: str) -> ValidationResult:
    """Validate URL format."""
    return get_unified_validator().validate_url(url)

def validate_string_length(value: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
    """Validate string length."""
    return get_unified_validator().validate_string_length(value, min_length, max_length)

def validate_numeric_range(value: Union[int, float], min_value: float = 0, max_value: float = 999999) -> ValidationResult:
    """Validate numeric range."""
    return get_unified_validator().validate_numeric_range(value, min_value, max_value)

def validate_regex_pattern(value: str, pattern_name: str) -> ValidationResult:
    """Validate regex pattern."""
    return get_unified_validator().validate_regex_pattern(value, pattern_name)

def validate_custom(value: Any, validator: Callable, field_name: str = "field") -> ValidationResult:
    """Validate using custom validator function."""
    return get_unified_validator().validate_custom(value, validator, field_name)
