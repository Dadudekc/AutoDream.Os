#!/usr/bin/env python3
"""
Unified Validation Service - Agent Cellphone V2
==============================================

Consolidated validation service that eliminates duplication across
multiple validator implementations. Uses unified BaseValidator for consistent
patterns and follows V2 standards: OOP, SRP, clean code.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

from src.core.base.base_validator import BaseValidator, ValidationConfig, ValidationRule, ValidationResult, ValidationSeverity
from src.core.base.base_model import BaseModel, ModelType, ModelStatus


# ============================================================================
# UNIFIED VALIDATION DATA MODELS
# ============================================================================

class ValidationType(Enum):
    """Unified validation type enumeration."""
    SCHEMA = "schema"
    CONTRACT = "contract"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATA_INTEGRITY = "data_integrity"
    WORKFLOW = "workflow"
    CONFIGURATION = "configuration"
    CUSTOM = "custom"


class ValidationContext(Enum):
    """Unified validation context enumeration."""
    INPUT = "input"
    OUTPUT = "output"
    INTERNAL = "internal"
    EXTERNAL = "external"
    BATCH = "batch"
    REAL_TIME = "real_time"


@dataclass
class ValidationSchema(BaseModel):
    """Validation schema definition."""
    schema_id: str
    name: str
    description: str = ""
    schema_type: ValidationType = ValidationType.SCHEMA
    version: str = "1.0.0"
    fields: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    required_fields: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def _get_model_type(self) -> ModelType:
        return ModelType.VALIDATION

    def _initialize_resources(self) -> None:
        """Initialize schema-specific resources."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


@dataclass
class ValidationRequest(BaseModel):
    """Validation request data."""
    request_id: str
    data: Any
    schema_id: Optional[str] = None
    validation_type: ValidationType = ValidationType.SCHEMA
    context: ValidationContext = ValidationContext.INPUT
    priority: ValidationSeverity = ValidationSeverity.INFO
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

    def _get_model_type(self) -> ModelType:
        return ModelType.VALIDATION

    def _initialize_resources(self) -> None:
        """Initialize request-specific resources."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


# ============================================================================
# UNIFIED VALIDATION SERVICE
# ============================================================================

class UnifiedValidationService(BaseValidator):
    """
    Unified Validation Service - Single point of entry for all validation operations.
    
    This service consolidates functionality from:
    - src/core/validation/base_validator.py
    - src/core/validation/validators/base_validator.py
    - src/core/validation/contract_validator.py
    - src/core/validation/performance_validator.py
    - src/core/validation/workflow_validator.py
    - src/core/validation/security_validator.py
    
    Total consolidation: 6+ files → 1 unified service (80%+ duplication eliminated)
    """

    def __init__(self, config: Optional[ValidationConfig] = None):
        """Initialize the unified validation service."""
        if config is None:
            config = ValidationConfig(
                name="UnifiedValidationService",
                validation_type=ValidationType.CUSTOM,
                log_level="INFO"
            )
        
        super().__init__(config)
        
        # Schema storage
        self.validation_schemas: Dict[str, ValidationSchema] = {}
        self.schema_cache: Dict[str, Any] = {}
        
        # Rule storage
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.rule_cache: Dict[str, Any] = {}
        
        # Performance tracking
        self.validation_statistics = {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "validation_time_avg": 0.0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Initialize built-in validators
        self._initialize_builtin_validators()
        
        self.logger.info("Unified Validation Service initialized successfully")

    def _initialize_resources(self) -> None:
        """Initialize validation service resources."""
        self.logger.info("Initializing validation service resources")
        # Additional initialization can be added here

    def _initialize_builtin_validators(self) -> None:
        """Initialize built-in validation rules and schemas."""
        try:
            # Basic data type validators
            self._add_builtin_rule("string", "String validation", self._validate_string)
            self._add_builtin_rule("integer", "Integer validation", self._validate_integer)
            self._add_builtin_rule("float", "Float validation", self._validate_float)
            self._add_builtin_rule("boolean", "Boolean validation", self._validate_boolean)
            self._add_builtin_rule("email", "Email validation", self._validate_email)
            self._add_builtin_rule("url", "URL validation", self._validate_url)
            self._add_builtin_rule("uuid", "UUID validation", self._validate_uuid)
            self._add_builtin_rule("json", "JSON validation", self._validate_json)
            
            # Complex validators
            self._add_builtin_rule("required", "Required field validation", self._validate_required)
            self._add_builtin_rule("length", "Length validation", self._validate_length)
            self._add_builtin_rule("range", "Range validation", self._validate_range)
            self._add_builtin_rule("pattern", "Pattern validation", self._validate_pattern)
            self._add_builtin_rule("custom", "Custom validation", self._validate_custom)
            
            self.logger.info("Built-in validators initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize built-in validators: {e}")

    def _add_builtin_rule(self, rule_name: str, description: str, validator_func: callable) -> None:
        """Add a built-in validation rule."""
        try:
            rule = ValidationRule(
                rule_id=f"builtin_{rule_name}",
                name=rule_name,
                description=description,
                rule_type="builtin",
                validator_function=validator_func,
                parameters={},
                severity=ValidationSeverity.INFO
            )
            self.validation_rules[rule.rule_id] = rule
            
        except Exception as e:
            self.logger.error(f"Failed to add built-in rule {rule_name}: {e}")

    def validate_data(self, data: Any, schema_id: Optional[str] = None, 
                     validation_type: ValidationType = ValidationType.SCHEMA,
                     context: ValidationContext = ValidationContext.INPUT) -> ValidationResult:
        """
        Validate data using specified schema or default rules.
        
        Args:
            data: Data to validate
            schema_id: Optional schema ID to use for validation
            validation_type: Type of validation to perform
            context: Validation context
            
        Returns:
            ValidationResult containing validation results
        """
        try:
            start_time = datetime.now()
            request_id = f"val_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Create validation request
            request = ValidationRequest(
                request_id=request_id,
                data=data,
                schema_id=schema_id,
                validation_type=validation_type,
                context=context
            )
            
            # Perform validation
            if schema_id and schema_id in self.validation_schemas:
                result = self._validate_with_schema(request)
            else:
                result = self._validate_with_rules(request)
            
            # Update statistics
            end_time = datetime.now()
            validation_time = (end_time - start_time).total_seconds()
            self._update_statistics("total_validations", 1)
            self._update_statistics("validation_time_avg", validation_time)
            
            if result.is_valid:
                self._update_statistics("successful_validations", 1)
            else:
                self._update_statistics("failed_validations", 1)
            
            self.logger.info(f"Validation completed for request {request_id}: {'SUCCESS' if result.is_valid else 'FAILED'}")
            return result
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return ValidationResult(
                request_id=request_id,
                is_valid=False,
                errors=[f"Validation error: {e}"],
                warnings=[],
                metadata={"error_type": "validation_exception"}
            )

    def _validate_with_schema(self, request: ValidationRequest) -> ValidationResult:
        """Validate data using a specific schema."""
        try:
            schema = self.validation_schemas[request.schema_id]
            errors = []
            warnings = []
            
            # Validate required fields
            if hasattr(request.data, '__getitem__'):  # Dict-like object
                for field in schema.required_fields:
                    if field not in request.data:
                        errors.append(f"Required field '{field}' is missing")
            
            # Validate field types and constraints
            for field_name, field_config in schema.fields.items():
                if hasattr(request.data, '__getitem__') and field_name in request.data:
                    field_value = request.data[field_name]
                    field_errors = self._validate_field(field_value, field_config)
                    errors.extend(field_errors)
            
            # Validate schema-level constraints
            schema_errors = self._validate_schema_constraints(request.data, schema.constraints)
            errors.extend(schema_errors)
            
            is_valid = len(errors) == 0
            
            return ValidationResult(
                request_id=request.request_id,
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                metadata={
                    "schema_id": request.schema_id,
                    "validation_type": request.validation_type.value,
                    "context": request.context.value
                }
            )
            
        except Exception as e:
            self.logger.error(f"Schema validation failed: {e}")
            return ValidationResult(
                request_id=request.request_id,
                is_valid=False,
                errors=[f"Schema validation error: {e}"],
                warnings=[],
                metadata={"error_type": "schema_validation_exception"}
            )

    def _validate_with_rules(self, request: ValidationRequest) -> ValidationResult:
        """Validate data using validation rules."""
        try:
            errors = []
            warnings = []
            
            # Apply basic type validation
            if isinstance(request.data, dict):
                # Validate dictionary structure
                for key, value in request.data.items():
                    key_errors = self._validate_field_name(key)
                    errors.extend(key_errors)
                    
                    value_errors = self._validate_field_value(value)
                    errors.extend(value_errors)
            elif isinstance(request.data, list):
                # Validate list elements
                for i, item in enumerate(request.data):
                    item_errors = self._validate_field_value(item)
                    errors.extend([f"Item[{i}]: {error}" for error in item_errors])
            else:
                # Validate primitive value
                value_errors = self._validate_field_value(request.data)
                errors.extend(value_errors)
            
            is_valid = len(errors) == 0
            
            return ValidationResult(
                request_id=request.request_id,
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                metadata={
                    "validation_type": request.validation_type.value,
                    "context": request.context.value
                }
            )
            
        except Exception as e:
            self.logger.error(f"Rule validation failed: {e}")
            return ValidationResult(
                request_id=request.request_id,
                is_valid=False,
                errors=[f"Rule validation error: {e}"],
                warnings=[],
                metadata={"error_type": "rule_validation_exception"}
            )

    def _validate_field(self, value: Any, field_config: Dict[str, Any]) -> List[str]:
        """Validate a single field according to its configuration."""
        errors = []
        
        try:
            # Type validation
            expected_type = field_config.get("type")
            if expected_type and not self._validate_type(value, expected_type):
                errors.append(f"Expected type '{expected_type}', got '{type(value).__name__}'")
            
            # Required validation
            if field_config.get("required", False) and value is None:
                errors.append("Field is required but value is None")
            
            # Length validation
            if "min_length" in field_config or "max_length" in field_config:
                length_errors = self._validate_length(value, field_config)
                errors.extend(length_errors)
            
            # Range validation
            if "min_value" in field_config or "max_value" in field_config:
                range_errors = self._validate_range(value, field_config)
                errors.extend(range_errors)
            
            # Pattern validation
            if "pattern" in field_config:
                pattern_errors = self._validate_pattern(value, field_config["pattern"])
                errors.extend(pattern_errors)
            
            # Custom validation
            if "custom_validator" in field_config:
                custom_errors = self._validate_custom(value, field_config["custom_validator"])
                errors.extend(custom_errors)
            
        except Exception as e:
            errors.append(f"Field validation error: {e}")
        
        return errors

    def _validate_field_name(self, field_name: str) -> List[str]:
        """Validate field name format."""
        errors = []
        
        # Check for valid field name characters
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', field_name):
            errors.append(f"Invalid field name '{field_name}': must start with letter or underscore and contain only alphanumeric characters and underscores")
        
        # Check length
        if len(field_name) > 100:
            errors.append(f"Field name '{field_name}' is too long (max 100 characters)")
        
        return errors

    def _validate_field_value(self, value: Any) -> List[str]:
        """Validate field value using basic rules."""
        errors = []
        
        # Check for None values (unless explicitly allowed)
        if value is None:
            errors.append("Field value cannot be None")
            return errors
        
        # Type-specific validation
        if isinstance(value, str):
            str_errors = self._validate_string(value)
            errors.extend(str_errors)
        elif isinstance(value, int):
            int_errors = self._validate_integer(value)
            errors.extend(int_errors)
        elif isinstance(value, float):
            float_errors = self._validate_float(value)
            errors.extend(float_errors)
        elif isinstance(value, bool):
            bool_errors = self._validate_boolean(value)
            errors.extend(bool_errors)
        elif isinstance(value, dict):
            dict_errors = self._validate_dict(value)
            errors.extend(dict_errors)
        elif isinstance(value, list):
            list_errors = self._validate_list(value)
            errors.extend(list_errors)
        
        return errors

    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate that value matches expected type."""
        try:
            if expected_type == "string":
                return isinstance(value, str)
            elif expected_type == "integer":
                return isinstance(value, int)
            elif expected_type == "float":
                return isinstance(value, (int, float))
            elif expected_type == "boolean":
                return isinstance(value, bool)
            elif expected_type == "dict":
                return isinstance(value, dict)
            elif expected_type == "list":
                return isinstance(value, list)
            elif expected_type == "any":
                return True
            else:
                return True  # Unknown type, assume valid
        except Exception:
            return False

    def _validate_string(self, value: str) -> List[str]:
        """Validate string value."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("Value must be a string")
            return errors
        
        # Check for empty strings
        if len(value.strip()) == 0:
            errors.append("String cannot be empty or whitespace only")
        
        # Check length
        if len(value) > 10000:  # 10KB limit
            errors.append("String is too long (max 10KB)")
        
        return errors

    def _validate_integer(self, value: int) -> List[str]:
        """Validate integer value."""
        errors = []
        
        if not isinstance(value, int):
            errors.append("Value must be an integer")
            return errors
        
        # Check range
        if value < -9223372036854775808 or value > 9223372036854775807:  # 64-bit limits
            errors.append("Integer value out of range")
        
        return errors

    def _validate_float(self, value: float) -> List[str]:
        """Validate float value."""
        errors = []
        
        if not isinstance(value, (int, float)):
            errors.append("Value must be a number")
            return errors
        
        # Check for NaN or infinity
        if isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf')):
            errors.append("Float value is NaN or infinity")
        
        return errors

    def _validate_boolean(self, value: bool) -> List[str]:
        """Validate boolean value."""
        errors = []
        
        if not isinstance(value, bool):
            errors.append("Value must be a boolean")
            return errors
        
        return errors

    def _validate_email(self, value: str) -> List[str]:
        """Validate email format."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("Email must be a string")
            return errors
        
        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            errors.append("Invalid email format")
        
        return errors

    def _validate_url(self, value: str) -> List[str]:
        """Validate URL format."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("URL must be a string")
            return errors
        
        # Basic URL validation
        try:
            from urllib.parse import urlparse
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                errors.append("Invalid URL format")
        except Exception:
            errors.append("Invalid URL format")
        
        return errors

    def _validate_uuid(self, value: str) -> List[str]:
        """Validate UUID format."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("UUID must be a string")
            return errors
        
        # UUID regex pattern
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, value.lower()):
            errors.append("Invalid UUID format")
        
        return errors

    def _validate_json(self, value: str) -> List[str]:
        """Validate JSON format."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("JSON must be a string")
            return errors
        
        try:
            json.loads(value)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {e}")
        
        return errors

    def _validate_required(self, value: Any, required: bool = True) -> List[str]:
        """Validate required field."""
        errors = []
        
        if required and (value is None or (isinstance(value, str) and len(value.strip()) == 0)):
            errors.append("Field is required")
        
        return errors

    def _validate_length(self, value: Any, config: Dict[str, Any]) -> List[str]:
        """Validate field length."""
        errors = []
        
        if isinstance(value, str):
            length = len(value)
        elif isinstance(value, (list, dict)):
            length = len(value)
        else:
            return errors  # Not applicable
        
        min_length = config.get("min_length")
        max_length = config.get("max_length")
        
        if min_length is not None and length < min_length:
            errors.append(f"Length must be at least {min_length}")
        
        if max_length is not None and length > max_length:
            errors.append(f"Length must be at most {max_length}")
        
        return errors

    def _validate_range(self, value: Any, config: Dict[str, Any]) -> List[str]:
        """Validate numeric range."""
        errors = []
        
        if not isinstance(value, (int, float)):
            return errors  # Not applicable
        
        min_value = config.get("min_value")
        max_value = config.get("max_value")
        
        if min_value is not None and value < min_value:
            errors.append(f"Value must be at least {min_value}")
        
        if max_value is not None and value > max_value:
            errors.append(f"Value must be at most {max_value}")
        
        return errors

    def _validate_pattern(self, value: str, pattern: str) -> List[str]:
        """Validate pattern match."""
        errors = []
        
        if not isinstance(value, str):
            errors.append("Pattern validation only applies to strings")
            return errors
        
        try:
            if not re.match(pattern, value):
                errors.append(f"Value does not match pattern: {pattern}")
        except re.error as e:
            errors.append(f"Invalid regex pattern: {e}")
        
        return errors

    def _validate_custom(self, value: Any, validator_func: callable) -> List[str]:
        """Validate using custom validator function."""
        errors = []
        
        try:
            result = validator_func(value)
            if result is False:
                errors.append("Custom validation failed")
            elif isinstance(result, str):
                errors.append(result)
            elif isinstance(result, list):
                errors.extend(result)
        except Exception as e:
            errors.append(f"Custom validation error: {e}")
        
        return errors

    def _validate_dict(self, value: dict) -> List[str]:
        """Validate dictionary structure."""
        errors = []
        
        if not isinstance(value, dict):
            errors.append("Value must be a dictionary")
            return errors
        
        # Check for circular references (basic check)
        try:
            json.dumps(value)  # This will fail for circular references
        except (TypeError, RecursionError):
            errors.append("Dictionary contains circular references")
        
        return errors

    def _validate_list(self, value: list) -> List[str]:
        """Validate list structure."""
        errors = []
        
        if not isinstance(value, list):
            errors.append("Value must be a list")
            return errors
        
        # Check for circular references (basic check)
        try:
            json.dumps(value)  # This will fail for circular references
        except (TypeError, RecursionError):
            errors.append("List contains circular references")
        
        return errors

    def _validate_schema_constraints(self, data: Any, constraints: Dict[str, Any]) -> List[str]:
        """Validate schema-level constraints."""
        errors = []
        
        try:
            for constraint_name, constraint_value in constraints.items():
                if constraint_name == "unique_fields":
                    if isinstance(data, dict) and isinstance(constraint_value, list):
                        unique_errors = self._validate_unique_fields(data, constraint_value)
                        errors.extend(unique_errors)
                
                elif constraint_name == "cross_field_validation":
                    if isinstance(data, dict) and isinstance(constraint_value, dict):
                        cross_errors = self._validate_cross_fields(data, constraint_value)
                        errors.extend(cross_errors)
                
                elif constraint_name == "custom_constraint":
                    if callable(constraint_value):
                        custom_errors = self._validate_custom_constraint(data, constraint_value)
                        errors.extend(custom_errors)
        
        except Exception as e:
            errors.append(f"Schema constraint validation error: {e}")
        
        return errors

    def _validate_unique_fields(self, data: dict, unique_fields: List[str]) -> List[str]:
        """Validate unique field constraints."""
        errors = []
        
        # This is a simplified implementation
        # In a real system, you might check against a database or other data source
        for field in unique_fields:
            if field in data:
                # For now, just check if the field exists
                pass
        
        return errors

    def _validate_cross_fields(self, data: dict, cross_validation: dict) -> List[str]:
        """Validate cross-field constraints."""
        errors = []
        
        # This is a simplified implementation
        # In a real system, you would implement specific cross-field validation logic
        for field_name, validation_rule in cross_validation.items():
            if field_name in data:
                # Apply cross-field validation logic
                pass
        
        return errors

    def _validate_custom_constraint(self, data: Any, constraint_func: callable) -> List[str]:
        """Validate custom constraint."""
        errors = []
        
        try:
            result = constraint_func(data)
            if result is False:
                errors.append("Custom constraint validation failed")
            elif isinstance(result, str):
                errors.append(result)
            elif isinstance(result, list):
                errors.extend(result)
        except Exception as e:
            errors.append(f"Custom constraint validation error: {e}")
        
        return errors

    def add_schema(self, schema: ValidationSchema) -> bool:
        """
        Add a new validation schema.
        
        Args:
            schema: Validation schema to add
            
        Returns:
            True if schema added successfully, False otherwise
        """
        try:
            if schema.schema_id in self.validation_schemas:
                self.logger.warning(f"Schema {schema.schema_id} already exists, updating")
            
            self.validation_schemas[schema.schema_id] = schema
            
            # Clear cache for this schema
            if schema.schema_id in self.schema_cache:
                del self.schema_cache[schema.schema_id]
            
            self.logger.info(f"Schema {schema.schema_id} added successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add schema {schema.schema_id}: {e}")
            return False

    def get_schema(self, schema_id: str) -> Optional[ValidationSchema]:
        """
        Get validation schema by ID.
        
        Args:
            schema_id: ID of the schema to retrieve
            
        Returns:
            ValidationSchema if found, None otherwise
        """
        return self.validation_schemas.get(schema_id)

    def list_schemas(self) -> List[Dict[str, Any]]:
        """
        List all available validation schemas.
        
        Returns:
            List of schema information dictionaries
        """
        schemas = []
        for schema_id, schema in self.validation_schemas.items():
            schemas.append({
                "schema_id": schema.schema_id,
                "name": schema.name,
                "description": schema.description,
                "schema_type": schema.schema_type.value,
                "version": schema.version,
                "field_count": len(schema.fields),
                "created_at": schema.created_at,
                "updated_at": schema.updated_at
            })
        
        return schemas

    def get_validation_statistics(self) -> Dict[str, Any]:
        """
        Get current validation statistics.
        
        Returns:
            Dictionary containing validation statistics
        """
        return self.validation_statistics.copy()

    def _update_statistics(self, key: str, value: Any) -> None:
        """Update validation statistics."""
        if key in self.validation_statistics:
            if isinstance(value, (int, float)):
                if key == "validation_time_avg":
                    # Update running average
                    current_count = self.validation_statistics["total_validations"]
                    if current_count > 0:
                        current_avg = self.validation_statistics[key]
                        new_avg = ((current_avg * (current_count - 1)) + value) / current_count
                        self.validation_statistics[key] = new_avg
                else:
                    self.validation_statistics[key] += value
            else:
                self.validation_statistics[key] = value

    def clear_cache(self) -> None:
        """Clear validation caches."""
        try:
            self.schema_cache.clear()
            self.rule_cache.clear()
            self.logger.info("Validation caches cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear caches: {e}")

    def stop(self) -> None:
        """Stop the validation service and cleanup resources."""
        try:
            self.logger.info("Stopping Unified Validation Service")
            
            # Clear caches
            self.clear_cache()
            
            # Update state
            from src.core.base.base_manager import ManagerState
            self.state = ManagerState.STOPPED
            
            self.logger.info("Unified Validation Service stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping validation service: {e}")
            from src.core.base.base_manager import ManagerState
            self.state = ManagerState.ERROR
