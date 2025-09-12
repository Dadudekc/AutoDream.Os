#!/usr/bin/env python3
"""
Core Validation - Consolidated Validation System
===============================================

Consolidated validation system providing unified validation functionality for:
- Data validation
- Schema validation
- Type validation
- Range validation
- Format validation

This module consolidates validation systems for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# ============================================================================
# VALIDATION TYPES
# ============================================================================


class ValidationType(Enum):
    """Validation type enumeration."""

    REQUIRED = "required"
    TYPE = "type"
    RANGE = "range"
    FORMAT = "format"
    CUSTOM = "custom"


class ValidationLevel(Enum):
    """Validation level enumeration."""

    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ValidationResult:
    """Validation result structure."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_error(self, error: str) -> None:
        """Add validation error."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add validation warning."""
        self.warnings.append(warning)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


# ============================================================================
# VALIDATION RULES
# ============================================================================


@dataclass
class ValidationRule:
    """Validation rule structure."""

    name: str
    validation_type: ValidationType
    required: bool = False
    data_type: type = None
    min_value: int | float | None = None
    max_value: int | float | None = None
    pattern: str | None = None
    custom_validator: callable | None = None
    error_message: str | None = None

    def validate(self, value: Any) -> ValidationResult:
        """Validate a value against this rule."""
        result = ValidationResult(is_valid=True)

        # Required validation
        if self.required and value is None:
            result.add_error(f"{self.name} is required")
            return result

        if value is None:
            return result

        # Type validation
        if self.data_type and not isinstance(value, self.data_type):
            result.add_error(f"{self.name} must be of type {self.data_type.__name__}")
            return result

        # Range validation
        if self.min_value is not None and value < self.min_value:
            result.add_error(f"{self.name} must be >= {self.min_value}")
            return result

        if self.max_value is not None and value > self.max_value:
            result.add_error(f"{self.name} must be <= {self.max_value}")
            return result

        # Format validation
        if self.pattern and isinstance(value, str):
            if not re.match(self.pattern, value):
                result.add_error(f"{self.name} format is invalid")
                return result

        # Custom validation
        if self.custom_validator:
            try:
                if not self.custom_validator(value):
                    result.add_error(f"{self.name} failed custom validation")
                    return result
            except Exception as e:
                result.add_error(f"{self.name} custom validation error: {e}")
                return result

        return result


# ============================================================================
# VALIDATION SCHEMAS
# ============================================================================


class ValidationSchema:
    """Validation schema for structured data."""

    def __init__(self, name: str = "default"):
    """# Example usage:
result = __init__("example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value", "example_value")
print(f"Result: {result}")"""
        self.name = name
        self.rules: dict[str, ValidationRule] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_rule(self, field_name: str, rule: ValidationRule) -> None:
        """Add a validation rule for a field."""
        self.rules[field_name] = rule

    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Validate data against schema."""
        result = ValidationResult(is_valid=True)

        # Check required fields
        for field_name, rule in self.rules.items():
            if rule.required and field_name not in data:
                result.add_error(f"Required field '{field_name}' is missing")

        # Validate each field
        for field_name, value in data.items():
            if field_name in self.rules:
                rule_result = self.rules[field_name].validate(value)
                if not rule_result.is_valid:
                    result.errors.extend(rule_result.errors)
                    result.is_valid = False
                result.warnings.extend(rule_result.warnings)
            else:
                result.add_warning(f"Unknown field '{field_name}'")

        return result

    def get_schema_info(self) -> dict[str, Any]:
        """Get schema information."""
        return {
            "name": self.name,
            "field_count": len(self.rules),
            "required_fields": [name for name, rule in self.rules.items() if rule.required],
            "field_types": {
                name: rule.data_type.__name__ if rule.data_type else "any"
                for name, rule in self.rules.items()
            },
        }


# ============================================================================
# VALIDATION VALIDATORS
# ============================================================================


class BaseValidator(ABC):
    """Base validator interface."""

    def __init__(self, name: str = "BaseValidator"):
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """Validate data."""
        pass

    def get_validator_info(self) -> dict[str, Any]:
        """Get validator information."""
        return {"name": self.name, "type": self.__class__.__name__}


class TypeValidator(BaseValidator):
    """Type validator."""

    def __init__(self, expected_type: type, name: str = "TypeValidator"):
        super().__init__(name)
        self.expected_type = expected_type

    def validate(self, data: Any) -> ValidationResult:
        """Validate data type."""
        result = ValidationResult(is_valid=True)

        if not isinstance(data, self.expected_type):
            result.add_error(
                f"Expected type {self.expected_type.__name__}, got {type(data).__name__}"
            )

        return result


class RangeValidator(BaseValidator):
    """Range validator."""

    def __init__(
        self, min_value: float = None, max_value: float = None, name: str = "RangeValidator"
    ):
        super().__init__(name)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, data: Any) -> ValidationResult:
        """Validate data range."""
        result = ValidationResult(is_valid=True)

        if not isinstance(data, (int, float)):
            result.add_error("Data must be numeric for range validation")
            return result

        if self.min_value is not None and data < self.min_value:
            result.add_error(f"Value {data} is below minimum {self.min_value}")

        if self.max_value is not None and data > self.max_value:
            result.add_error(f"Value {data} is above maximum {self.max_value}")

        return result


class FormatValidator(BaseValidator):
    """Format validator."""

    def __init__(self, pattern: str, name: str = "FormatValidator"):
        super().__init__(name)
        self.pattern = pattern
        self.compiled_pattern = re.compile(pattern)

    def validate(self, data: Any) -> ValidationResult:
        """Validate data format."""
        result = ValidationResult(is_valid=True)

        if not isinstance(data, str):
            result.add_error("Data must be string for format validation")
            return result

        if not self.compiled_pattern.match(data):
            result.add_error(f"Data format does not match pattern: {self.pattern}")

        return result


class CustomValidator(BaseValidator):
    """Custom validator."""

    def __init__(self, validator_func: callable, name: str = "CustomValidator"):
        super().__init__(name)
        self.validator_func = validator_func

    def validate(self, data: Any) -> ValidationResult:
        """Validate data using custom function."""
        result = ValidationResult(is_valid=True)

        try:
            if not self.validator_func(data):
                result.add_error("Custom validation failed")
        except Exception as e:
            result.add_error(f"Custom validation error: {e}")

        return result


# ============================================================================
# VALIDATION ORCHESTRATOR
# ============================================================================


class ValidationOrchestrator:
    """Orchestrates validation operations."""

    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validators: dict[str, BaseValidator] = {}
        self.schemas: dict[str, ValidationSchema] = {}
        self.validation_history: list[dict[str, Any]] = []

    def register_validator(self, name: str, validator: BaseValidator) -> bool:
        """Register a validator."""
        try:
            self.validators[name] = validator
            self.logger.info(f"Registered validator: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register validator {name}: {e}")
            return False

    def register_schema(self, name: str, schema: ValidationSchema) -> bool:
        """Register a validation schema."""
        try:
            self.schemas[name] = schema
            self.logger.info(f"Registered schema: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register schema {name}: {e}")
            return False

    def validate(
        self, data: Any, validator_name: str = None, schema_name: str = None
    ) -> ValidationResult:
        """Validate data using specified validator or schema."""
        result = ValidationResult(is_valid=True)

        # Use schema validation if specified
        if schema_name and schema_name in self.schemas:
            if isinstance(data, dict):
                result = self.schemas[schema_name].validate(data)
            else:
                result.add_error("Schema validation requires dictionary data")

        # Use validator if specified
        elif validator_name and validator_name in self.validators:
            result = self.validators[validator_name].validate(data)

        # Default validation based on level
        else:
            result = self._default_validation(data)

        # Record validation history
        self.validation_history.append(
            {
                "timestamp": datetime.now(),
                "validator": validator_name,
                "schema": schema_name,
                "is_valid": result.is_valid,
                "error_count": len(result.errors),
                "warning_count": len(result.warnings),
            }
        )

        return result

    def _default_validation(self, data: Any) -> ValidationResult:
        """Default validation based on validation level."""
        result = ValidationResult(is_valid=True)

        if self.validation_level == ValidationLevel.BASIC:
            # Basic validation - just check if data exists
            if data is None:
                result.add_error("Data is required")

        elif self.validation_level == ValidationLevel.STANDARD:
            # Standard validation - check type and basic constraints
            if data is None:
                result.add_error("Data is required")
            elif isinstance(data, str) and not data.strip():
                result.add_error("String data cannot be empty")
            elif isinstance(data, (list, dict)) and not data:
                result.add_warning("Empty collection data")

        elif self.validation_level == ValidationLevel.STRICT:
            # Strict validation - comprehensive checks
            if data is None:
                result.add_error("Data is required")
            elif isinstance(data, str):
                if not data.strip():
                    result.add_error("String data cannot be empty")
                if len(data) > 1000:
                    result.add_warning("String data is very long")
            elif isinstance(data, (list, dict)):
                if not data:
                    result.add_error("Collection data cannot be empty")
                elif len(data) > 100:
                    result.add_warning("Collection data is very large")

        return result

    def get_validation_stats(self) -> dict[str, Any]:
        """Get validation statistics."""
        total_validations = len(self.validation_history)
        successful_validations = sum(1 for h in self.validation_history if h["is_valid"])

        return {
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": (
                successful_validations / total_validations if total_validations > 0 else 0
            ),
            "registered_validators": len(self.validators),
            "registered_schemas": len(self.schemas),
            "validation_level": self.validation_level.value,
        }

    def clear_history(self) -> None:
        """Clear validation history."""
        self.validation_history.clear()
        self.logger.info("Validation history cleared")


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_validation_rule(
    name: str,
    validation_type: ValidationType,
    required: bool = False,
    data_type: type = None,
    min_value: float = None,
    max_value: float = None,
    pattern: str = None,
    custom_validator: callable = None,
) -> ValidationRule:
    """Create a validation rule."""
    return ValidationRule(
        name=name,
        validation_type=validation_type,
        required=required,
        data_type=data_type,
        min_value=min_value,
        max_value=max_value,
        pattern=pattern,
        custom_validator=custom_validator,
    )


def create_validation_schema(name: str = "default") -> ValidationSchema:
    """Create a validation schema."""
    return ValidationSchema(name)


def create_type_validator(expected_type: type, name: str = "TypeValidator") -> TypeValidator:
    """Create a type validator."""
    return TypeValidator(expected_type, name)


def create_range_validator(
    min_value: float = None, max_value: float = None, name: str = "RangeValidator"
) -> RangeValidator:
    """Create a range validator."""
    return RangeValidator(min_value, max_value, name)


def create_format_validator(pattern: str, name: str = "FormatValidator") -> FormatValidator:
    """Create a format validator."""
    return FormatValidator(pattern, name)


def create_custom_validator(
    validator_func: callable, name: str = "CustomValidator"
) -> CustomValidator:
    """Create a custom validator."""
    return CustomValidator(validator_func, name)


def create_validation_orchestrator(
    validation_level: ValidationLevel = ValidationLevel.STANDARD,
) -> ValidationOrchestrator:
    """Create a validation orchestrator."""
    return ValidationOrchestrator(validation_level)


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main execution function."""
    print("Core Validation - Consolidated Validation System")
    print("=" * 50)

    # Create validation orchestrator
    orchestrator = create_validation_orchestrator(ValidationLevel.STANDARD)
    print(f"Validation orchestrator created: {orchestrator.get_validation_stats()}")

    # Create validation schema
    schema = create_validation_schema("test_schema")
    schema.add_rule(
        "name",
        create_validation_rule("name", ValidationType.REQUIRED, required=True, data_type=str),
    )
    schema.add_rule(
        "age",
        create_validation_rule(
            "age", ValidationType.RANGE, data_type=int, min_value=0, max_value=120
        ),
    )
    schema.add_rule(
        "email",
        create_validation_rule("email", ValidationType.FORMAT, pattern=r"^[^@]+@[^@]+\.[^@]+$"),
    )

    orchestrator.register_schema("test_schema", schema)
    print(f"Validation schema created: {schema.get_schema_info()}")

    # Create validators
    type_validator = create_type_validator(str, "StringValidator")
    range_validator = create_range_validator(0, 100, "AgeValidator")
    format_validator = create_format_validator(r"^[A-Za-z]+$", "NameValidator")

    orchestrator.register_validator("string", type_validator)
    orchestrator.register_validator("age", range_validator)
    orchestrator.register_validator("name", format_validator)

    # Test validation
    test_data = {"name": "Agent-2", "age": 25, "email": "agent2@swarm.ai"}
    result = orchestrator.validate(test_data, schema_name="test_schema")
    print(f"Validation result: {result.to_dict()}")

    print("\nCore Validation initialization complete!")

    return 0  # Success exit code


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
