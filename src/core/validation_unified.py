#!/usr/bin/env python3
"""
Validation Unified - Consolidated Validation System
==================================================

Consolidated validation system providing unified validation functionality for:
- Data validation and schema validation
- Input validation and output validation
- Business rule validation and constraint validation
- Validation models and validators
- Validation orchestration and coordination

This module consolidates 6 validation files into 1 unified module for better
maintainability and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# ============================================================================
# VALIDATION ENUMS AND MODELS
# ============================================================================

class ValidationStatus(Enum):
    """Validation status enumeration."""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    ERROR = "error"
    PENDING = "pending"


class ValidationType(Enum):
    """Validation type enumeration."""
    DATA_VALIDATION = "data_validation"
    SCHEMA_VALIDATION = "schema_validation"
    INPUT_VALIDATION = "input_validation"
    OUTPUT_VALIDATION = "output_validation"
    BUSINESS_RULE_VALIDATION = "business_rule_validation"
    CONSTRAINT_VALIDATION = "constraint_validation"


class ValidationSeverity(Enum):
    """Validation severity enumeration."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DataType(Enum):
    """Data type enumeration."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    EMAIL = "email"
    URL = "url"
    PHONE = "phone"
    JSON = "json"
    ARRAY = "array"
    OBJECT = "object"


# ============================================================================
# VALIDATION MODELS
# ============================================================================

@dataclass
class ValidationResult:
    """Validation result model."""
    result_id: str
    validation_type: ValidationType
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    field_name: str | None = None
    field_value: Any = None
    expected_value: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Validation rule model."""
    rule_id: str
    name: str
    validation_type: ValidationType
    field_name: str
    data_type: DataType
    required: bool = False
    min_length: int | None = None
    max_length: int | None = None
    min_value: float | None = None
    max_value: float | None = None
    pattern: str | None = None
    custom_validator: str | None = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationSchema:
    """Validation schema model."""
    schema_id: str
    name: str
    version: str
    rules: list[ValidationRule] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Validation report model."""
    report_id: str
    schema_id: str
    total_validations: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    results: list[ValidationResult] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# VALIDATION INTERFACES
# ============================================================================

class Validator(ABC):
    """Base validator interface."""

    def __init__(self, validator_id: str, name: str):
        self.validator_id = validator_id
        self.name = name
        self.logger = logging.getLogger(f"validator.{name}")
        self.is_active = False

    @abstractmethod
    def validate(self, data: Any, rule: ValidationRule) -> ValidationResult:
        """Validate data against rule."""
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get validator capabilities."""
        pass


class SchemaValidator(ABC):
    """Base schema validator interface."""

    def __init__(self, validator_id: str, name: str):
        self.validator_id = validator_id
        self.name = name
        self.logger = logging.getLogger(f"schema_validator.{name}")
        self.is_active = False

    @abstractmethod
    def validate_schema(self, data: dict[str, Any], schema: ValidationSchema) -> ValidationReport:
        """Validate data against schema."""
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get schema validator capabilities."""
        pass


# ============================================================================
# VALIDATORS
# ============================================================================

class DataTypeValidator(Validator):
    """Data type validator implementation."""

    def __init__(self, validator_id: str = None):
        super().__init__(
            validator_id or str(uuid.uuid4()),
            "DataTypeValidator"
        )

    def validate(self, data: Any, rule: ValidationRule) -> ValidationResult:
        """Validate data type."""
        try:
            # Check if data is required
            if rule.required and (data is None or data == ""):
                return ValidationResult(
                    result_id=str(uuid.uuid4()),
                    validation_type=rule.validation_type,
                    status=ValidationStatus.INVALID,
                    severity=ValidationSeverity.ERROR,
                    message=f"Field '{rule.field_name}' is required",
                    field_name=rule.field_name,
                    field_value=data
                )

            # Skip validation if data is None and not required
            if data is None and not rule.required:
                return ValidationResult(
                    result_id=str(uuid.uuid4()),
                    validation_type=rule.validation_type,
                    status=ValidationStatus.VALID,
                    severity=ValidationSeverity.INFO,
                    message=f"Field '{rule.field_name}' is valid (optional)",
                    field_name=rule.field_name,
                    field_value=data
                )

            # Validate data type
            if not self._validate_type(data, rule.data_type):
                return ValidationResult(
                    result_id=str(uuid.uuid4()),
                    validation_type=rule.validation_type,
                    status=ValidationStatus.INVALID,
                    severity=ValidationSeverity.ERROR,
                    message=f"Field '{rule.field_name}' must be of type {rule.data_type.value}",
                    field_name=rule.field_name,
                    field_value=data,
                    expected_value=rule.data_type.value
                )

            return ValidationResult(
                result_id=str(uuid.uuid4()),
                validation_type=rule.validation_type,
                status=ValidationStatus.VALID,
                severity=ValidationSeverity.INFO,
                message=f"Field '{rule.field_name}' has valid type",
                field_name=rule.field_name,
                field_value=data
            )
        except Exception as e:
            self.logger.error(f"Failed to validate data type: {e}")
            return ValidationResult(
                result_id=str(uuid.uuid4()),
                validation_type=rule.validation_type,
                status=ValidationStatus.INVALID,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation error: {e}",
                field_name=rule.field_name,
                field_value=data
            )

    def get_capabilities(self) -> list[str]:
        """Get data type validation capabilities."""
        return ["data_type_validation", "type_checking", "required_field_validation"]

    def _validate_type(self, data: Any, data_type: DataType) -> bool:
        """Validate data against specific type."""
        try:
            if data_type == DataType.STRING:
                return isinstance(data, str)
            elif data_type == DataType.INTEGER:
                return isinstance(data, int) or (isinstance(data, str) and data.isdigit())
            elif data_type == DataType.FLOAT:
                return isinstance(data, (int, float)) or (isinstance(data, str) and self._is_float(data))
            elif data_type == DataType.BOOLEAN:
                return isinstance(data, bool) or data in ["true", "false", "1", "0", "yes", "no"]
            elif data_type == DataType.EMAIL:
                return isinstance(data, str) and self._is_valid_email(data)
            elif data_type == DataType.URL:
                return isinstance(data, str) and self._is_valid_url(data)
            elif data_type == DataType.PHONE:
                return isinstance(data, str) and self._is_valid_phone(data)
            elif data_type == DataType.JSON:
                return self._is_valid_json(data)
            elif data_type == DataType.ARRAY:
                return isinstance(data, list)
            elif data_type == DataType.OBJECT:
                return isinstance(data, dict)
            else:
                return True
        except Exception:
            return False

    def _is_float(self, value: str) -> bool:
        """Check if string is a valid float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_valid_email(self, email: str) -> bool:
        """Check if string is a valid email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _is_valid_url(self, url: str) -> bool:
        """Check if string is a valid URL."""
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return re.match(pattern, url) is not None

    def _is_valid_phone(self, phone: str) -> bool:
        """Check if string is a valid phone number."""
        pattern = r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'
        return re.match(pattern, phone) is not None

    def _is_valid_json(self, data: Any) -> bool:
        """Check if data is valid JSON."""
        try:
            if isinstance(data, str):
                json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False


class ConstraintValidator(Validator):
    """Constraint validator implementation."""

    def __init__(self, validator_id: str = None):
        super().__init__(
            validator_id or str(uuid.uuid4()),
            "ConstraintValidator"
        )

    def validate(self, data: Any, rule: ValidationRule) -> ValidationResult:
        """Validate constraints."""
        try:
            # Skip validation if data is None and not required
            if data is None and not rule.required:
                return ValidationResult(
                    result_id=str(uuid.uuid4()),
                    validation_type=rule.validation_type,
                    status=ValidationStatus.VALID,
                    severity=ValidationSeverity.INFO,
                    message=f"Field '{rule.field_name}' is valid (optional)",
                    field_name=rule.field_name,
                    field_value=data
                )

            # Validate length constraints
            if isinstance(data, str):
                if rule.min_length is not None and len(data) < rule.min_length:
                    return ValidationResult(
                        result_id=str(uuid.uuid4()),
                        validation_type=rule.validation_type,
                        status=ValidationStatus.INVALID,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{rule.field_name}' must be at least {rule.min_length} characters",
                        field_name=rule.field_name,
                        field_value=data,
                        expected_value=f"min_length: {rule.min_length}"
                    )

                if rule.max_length is not None and len(data) > rule.max_length:
                    return ValidationResult(
                        result_id=str(uuid.uuid4()),
                        validation_type=rule.validation_type,
                        status=ValidationStatus.INVALID,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{rule.field_name}' must be at most {rule.max_length} characters",
                        field_name=rule.field_name,
                        field_value=data,
                        expected_value=f"max_length: {rule.max_length}"
                    )

            # Validate numeric constraints
            if isinstance(data, (int, float)):
                if rule.min_value is not None and data < rule.min_value:
                    return ValidationResult(
                        result_id=str(uuid.uuid4()),
                        validation_type=rule.validation_type,
                        status=ValidationStatus.INVALID,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{rule.field_name}' must be at least {rule.min_value}",
                        field_name=rule.field_name,
                        field_value=data,
                        expected_value=f"min_value: {rule.min_value}"
                    )

                if rule.max_value is not None and data > rule.max_value:
                    return ValidationResult(
                        result_id=str(uuid.uuid4()),
                        validation_type=rule.validation_type,
                        status=ValidationStatus.INVALID,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{rule.field_name}' must be at most {rule.max_value}",
                        field_name=rule.field_name,
                        field_value=data,
                        expected_value=f"max_value: {rule.max_value}"
                    )

            # Validate pattern constraints
            if rule.pattern and isinstance(data, str):
                if not re.match(rule.pattern, data):
                    return ValidationResult(
                        result_id=str(uuid.uuid4()),
                        validation_type=rule.validation_type,
                        status=ValidationStatus.INVALID,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{rule.field_name}' does not match required pattern",
                        field_name=rule.field_name,
                        field_value=data,
                        expected_value=f"pattern: {rule.pattern}"
                    )

            return ValidationResult(
                result_id=str(uuid.uuid4()),
                validation_type=rule.validation_type,
                status=ValidationStatus.VALID,
                severity=ValidationSeverity.INFO,
                message=f"Field '{rule.field_name}' meets all constraints",
                field_name=rule.field_name,
                field_value=data
            )
        except Exception as e:
            self.logger.error(f"Failed to validate constraints: {e}")
            return ValidationResult(
                result_id=str(uuid.uuid4()),
                validation_type=rule.validation_type,
                status=ValidationStatus.INVALID,
                severity=ValidationSeverity.CRITICAL,
                message=f"Constraint validation error: {e}",
                field_name=rule.field_name,
                field_value=data
            )

    def get_capabilities(self) -> list[str]:
        """Get constraint validation capabilities."""
        return ["constraint_validation", "length_validation", "range_validation", "pattern_validation"]


# ============================================================================
# SCHEMA VALIDATORS
# ============================================================================

class JSONSchemaValidator(SchemaValidator):
    """JSON schema validator implementation."""

    def __init__(self, validator_id: str = None):
        super().__init__(
            validator_id or str(uuid.uuid4()),
            "JSONSchemaValidator"
        )

    def validate_schema(self, data: dict[str, Any], schema: ValidationSchema) -> ValidationReport:
        """Validate data against schema."""
        try:
            report = ValidationReport(
                report_id=str(uuid.uuid4()),
                schema_id=schema.schema_id
            )

            # Create validators
            data_type_validator = DataTypeValidator()
            constraint_validator = ConstraintValidator()

            # Validate each field
            for rule in schema.rules:
                if not rule.enabled:
                    continue

                field_value = data.get(rule.field_name)
                report.total_validations += 1

                # Validate data type
                type_result = data_type_validator.validate(field_value, rule)
                report.results.append(type_result)

                if type_result.status == ValidationStatus.VALID:
                    # Validate constraints
                    constraint_result = constraint_validator.validate(field_value, rule)
                    report.results.append(constraint_result)

                    if constraint_result.status == ValidationStatus.VALID:
                        report.valid_count += 1
                    else:
                        report.invalid_count += 1
                        if constraint_result.severity == ValidationSeverity.WARNING:
                            report.warning_count += 1
                        elif constraint_result.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]:
                            report.error_count += 1
                else:
                    report.invalid_count += 1
                    if type_result.severity == ValidationSeverity.WARNING:
                        report.warning_count += 1
                    elif type_result.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]:
                        report.error_count += 1

            return report
        except Exception as e:
            self.logger.error(f"Failed to validate schema: {e}")
            return ValidationReport(
                report_id=str(uuid.uuid4()),
                schema_id=schema.schema_id,
                total_validations=0,
                valid_count=0,
                invalid_count=1,
                error_count=1,
                results=[ValidationResult(
                    result_id=str(uuid.uuid4()),
                    validation_type=ValidationType.SCHEMA_VALIDATION,
                    status=ValidationStatus.INVALID,
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Schema validation error: {e}"
                )]
            )

    def get_capabilities(self) -> list[str]:
        """Get JSON schema validation capabilities."""
        return ["json_schema_validation", "field_validation", "schema_validation"]


# ============================================================================
# VALIDATION MANAGER
# ============================================================================

class ValidationManager:
    """Validation management system."""

    def __init__(self):
        self.validators: list[Validator] = []
        self.schema_validators: list[SchemaValidator] = []
        self.schemas: dict[str, ValidationSchema] = {}
        self.logger = logging.getLogger("validation_manager")

    def register_validator(self, validator: Validator) -> bool:
        """Register validator."""
        try:
            self.validators.append(validator)
            self.logger.info(f"Validator {validator.name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register validator {validator.name}: {e}")
            return False

    def register_schema_validator(self, validator: SchemaValidator) -> bool:
        """Register schema validator."""
        try:
            self.schema_validators.append(validator)
            self.logger.info(f"Schema validator {validator.name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register schema validator {validator.name}: {e}")
            return False

    def register_schema(self, schema: ValidationSchema) -> bool:
        """Register validation schema."""
        try:
            self.schemas[schema.schema_id] = schema
            self.logger.info(f"Schema {schema.name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register schema {schema.name}: {e}")
            return False

    def validate_data(self, data: Any, rule: ValidationRule) -> ValidationResult:
        """Validate data using appropriate validator."""
        for validator in self.validators:
            if rule.validation_type in validator.get_capabilities():
                return validator.validate(data, rule)

        # Fallback to first available validator
        if self.validators:
            return self.validators[0].validate(data, rule)

        return ValidationResult(
            result_id=str(uuid.uuid4()),
            validation_type=rule.validation_type,
            status=ValidationStatus.INVALID,
            severity=ValidationSeverity.ERROR,
            message="No validator available"
        )

    def validate_schema(self, data: dict[str, Any], schema_id: str) -> ValidationReport | None:
        """Validate data against schema."""
        schema = self.schemas.get(schema_id)
        if not schema:
            self.logger.error(f"Schema {schema_id} not found")
            return None

        for validator in self.schema_validators:
            if "schema_validation" in validator.get_capabilities():
                return validator.validate_schema(data, schema)

        return None

    def get_validation_status(self) -> dict[str, Any]:
        """Get validation system status."""
        return {
            "validators_registered": len(self.validators),
            "schema_validators_registered": len(self.schema_validators),
            "schemas_registered": len(self.schemas)
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_validator(validator_type: str, validator_id: str = None) -> Validator | None:
    """Create validator by type."""
    validators = {
        "data_type": DataTypeValidator,
        "constraint": ConstraintValidator
    }

    validator_class = validators.get(validator_type)
    if validator_class:
        return validator_class(validator_id)

    return None


def create_schema_validator(validator_type: str, validator_id: str = None) -> SchemaValidator | None:
    """Create schema validator by type."""
    validators = {
        "json": JSONSchemaValidator
    }

    validator_class = validators.get(validator_type)
    if validator_class:
        return validator_class(validator_id)

    return None


def create_validation_manager() -> ValidationManager:
    """Create validation manager."""
    return ValidationManager()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("Validation Unified - Consolidated Validation System")
    print("=" * 55)

    # Create validation manager
    manager = create_validation_manager()
    print("✅ Validation manager created")

    # Create and register validators
    validator_types = ["data_type", "constraint"]

    for validator_type in validator_types:
        validator = create_validator(validator_type)
        if validator and manager.register_validator(validator):
            print(f"✅ {validator.name} registered")
        else:
            print(f"❌ Failed to register {validator_type} validator")

    # Create and register schema validators
    schema_validator_types = ["json"]

    for validator_type in schema_validator_types:
        validator = create_schema_validator(validator_type)
        if validator and manager.register_schema_validator(validator):
            print(f"✅ {validator.name} registered")
        else:
            print(f"❌ Failed to register {validator_type} schema validator")

    # Test validation functionality
    test_rule = ValidationRule(
        rule_id="test_rule_001",
        name="Test Rule",
        validation_type=ValidationType.DATA_VALIDATION,
        field_name="test_field",
        data_type=DataType.STRING,
        required=True,
        min_length=3,
        max_length=10
    )

    result = manager.validate_data("test", test_rule)
    if result.status == ValidationStatus.VALID:
        print(f"✅ Validation test passed: {result.message}")
    else:
        print(f"❌ Validation test failed: {result.message}")

    status = manager.get_validation_status()
    print(f"✅ Validation system status: {status}")

    print(f"\nTotal validators registered: {len(manager.validators)}")
    print(f"Total schema validators registered: {len(manager.schema_validators)}")
    print("Validation Unified system test completed successfully!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
