#!/usr/bin/env python3
"""
Validation Coordinator - Orchestrates different validation engines.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Any, Dict, List

from .models.validation_models import ValidationResult, ValidationRule, ValidationType
from .engines.field_validator import FieldValidator
from .engines.format_validator import FormatValidator
from .engines.range_validator import RangeValidator
from .engines.custom_validator import CustomValidator


class ValidationCoordinator:
    """
    Coordinates different validation engines to provide unified validation.
    
    This class maintains backward compatibility with the original UnifiedValidationSystem
    while providing a clean, modular architecture.
    """
    
    def __init__(self):
        """Initialize the validation coordinator with all engines."""
        self.field_validator = FieldValidator()
        self.format_validator = FormatValidator()
        self.range_validator = RangeValidator()
        self.custom_validator = CustomValidator()
        
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
        """Validate required fields - consolidates 8+ duplicate implementations."""
        return self.field_validator.validate_required_fields(data, required_fields)
    
    def validate_data_types(self, data: Dict[str, Any], type_requirements: Dict[str, type]) -> ValidationResult:
        """Validate data types - consolidates 8+ duplicate implementations."""
        return self.field_validator.validate_data_types(data, type_requirements)
    
    def validate_email(self, email: str) -> ValidationResult:
        """Validate email format - consolidates 5+ duplicate implementations."""
        return self.format_validator.validate_email(email)
    
    def validate_url(self, url: str) -> ValidationResult:
        """Validate URL format - consolidates 4+ duplicate implementations."""
        return self.format_validator.validate_url(url)
    
    def validate_string_length(self, value: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
        """Validate string length - consolidates 6+ duplicate implementations."""
        return self.range_validator.validate_string_length(value, min_length, max_length)
    
    def validate_numeric_range(self, value: Any, min_value: float = 0, max_value: float = 999999) -> ValidationResult:
        """Validate numeric range - consolidates 3+ duplicate implementations."""
        return self.range_validator.validate_numeric_range(value, min_value, max_value)
    
    def validate_regex_pattern(self, value: str, pattern_name: str) -> ValidationResult:
        """Validate regex pattern - consolidates 4+ duplicate implementations."""
        return self.format_validator.validate_regex_pattern(value, pattern_name)
    
    def validate_custom(self, value: Any, validator: Any, field_name: str = "field") -> ValidationResult:
        """Validate using custom validator function."""
        return self.custom_validator.validate_custom(value, validator, field_name)
    
    def validate_hasattr(self, obj: Any, attr_name: str) -> bool:
        """Validate that an object has a specific attribute."""
        return self.custom_validator.validate_hasattr(obj, attr_name)
    
    def validate_multiple(self, data: Dict[str, Any], rules: List[ValidationRule]) -> List[ValidationResult]:
        """Validate multiple fields with different rules."""
        results = []
        
        for rule in rules:
            if rule.field_name not in data:
                if rule.severity.value == "high":
                    results.append(ValidationResult(
                        is_valid=False,
                        errors=[f"Required field missing: {rule.field_name}"],
                        severity=rule.severity,
                        field_name=rule.field_name,
                        validation_type=rule.rule_type
                    ))
                continue
            
            value = data[rule.field_name]
            
            # Route to appropriate validator based on rule type
            if rule.rule_type == ValidationType.REQUIRED_FIELDS:
                result = self.field_validator.validate(value, validation_type=rule.rule_type)
            elif rule.rule_type == ValidationType.DATA_TYPES:
                result = self.field_validator.validate(value, 
                    validation_type=rule.rule_type, 
                    expected_type=rule.parameters.get("type", str))
            elif rule.rule_type == ValidationType.EMAIL:
                result = self.format_validator.validate(value, validation_type=rule.rule_type)
            elif rule.rule_type == ValidationType.URL:
                result = self.format_validator.validate(value, validation_type=rule.rule_type)
            elif rule.rule_type == ValidationType.STRING_LENGTH:
                result = self.range_validator.validate(value, 
                    validation_type=rule.rule_type,
                    min_length=rule.parameters.get("min", 0),
                    max_length=rule.parameters.get("max", 1000))
            elif rule.rule_type == ValidationType.NUMERIC_RANGE:
                result = self.range_validator.validate(value,
                    validation_type=rule.rule_type,
                    min_value=rule.parameters.get("min", 0),
                    max_value=rule.parameters.get("max", 999999))
            elif rule.rule_type == ValidationType.REGEX_PATTERN:
                result = self.format_validator.validate(value,
                    validation_type=rule.rule_type,
                    pattern_name=rule.parameters.get("pattern", "alphanumeric"))
            elif rule.rule_type == ValidationType.CUSTOM:
                result = self.custom_validator.validate(value,
                    validation_type=rule.rule_type,
                    validator=rule.custom_validator,
                    field_name=rule.field_name)
            else:
                result = ValidationResult(
                    is_valid=False,
                    errors=[f"Unknown validation type: {rule.rule_type}"],
                    severity=rule.severity,
                    field_name=rule.field_name,
                    validation_type=rule.rule_type
                )
            
            result.field_name = rule.field_name
            result.validation_type = rule.rule_type
            result.severity = rule.severity
            results.append(result)
        
        return results
