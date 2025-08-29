#!/usr/bin/env python3
"""
Unified Validation Library

This module provides centralized validation functions for the entire system,
eliminating function duplication and ensuring consistent validation behavior.

Author: Agent-8 (Integration Enhancement Manager)
Contract: DEDUP-002: Function Duplication Elimination
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Validation status enumeration"""
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ValidationResult:
    """Validation result data structure"""
    status: ValidationStatus
    message: str
    errors: List[str]
    warnings: List[str]
    timestamp: datetime
    validated_data: Any = None


class UnifiedValidators:
    """
    Unified validation library for eliminating function duplication.
    
    This class consolidates all common validation logic into a single,
    maintainable location, eliminating the need for duplicate validation
    functions across the codebase.
    """
    
    def __init__(self):
        """Initialize the unified validators."""
        self.validation_history: List[ValidationResult] = []
    
    def validate_config(self, config: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
        """
        Unified configuration validation function.
        
        Args:
            config: Configuration dictionary to validate
            required_fields: List of required field names
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if not isinstance(config, dict):
            errors.append("Configuration must be a dictionary")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Configuration validation failed",
                errors=errors,
                warnings=warnings,
                timestamp=datetime.now(),
                validated_data=config
            )
        
        if required_fields:
            for field in required_fields:
                if field not in config:
                    errors.append(f"Required field '{field}' missing from configuration")
                elif config[field] is None:
                    warnings.append(f"Field '{field}' is None (may cause issues)")
        
        # Validate common configuration patterns
        if 'version' in config:
            if not isinstance(config['version'], str):
                errors.append("Version field must be a string")
        
        if 'enabled' in config:
            if not isinstance(config['enabled'], bool):
                errors.append("Enabled field must be a boolean")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Configuration validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=config
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_transition(self, from_state: str, to_state: str, valid_transitions: Dict[str, List[str]] = None) -> ValidationResult:
        """
        Unified state transition validation function.
        
        Args:
            from_state: Current state name
            to_state: Target state name
            valid_transitions: Dictionary of valid transitions per state
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if not isinstance(from_state, str) or not from_state.strip():
            errors.append("From state must be a non-empty string")
        
        if not isinstance(to_state, str) or not to_state.strip():
            errors.append("To state must be a non-empty string")
        
        if from_state == to_state:
            warnings.append("Transition from state to same state (no-op)")
        
        if valid_transitions:
            if from_state not in valid_transitions:
                errors.append(f"From state '{from_state}' not found in valid transitions")
            elif to_state not in valid_transitions.get(from_state, []):
                errors.append(f"Transition from '{from_state}' to '{to_state}' is not valid")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Transition validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data={"from_state": from_state, "to_state": to_state}
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_state_definition(self, state_def: Dict[str, Any]) -> ValidationResult:
        """
        Unified state definition validation function.
        
        Args:
            state_def: State definition dictionary
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        required_fields = ["name", "type"]
        for field in required_fields:
            if field not in state_def:
                errors.append(f"Required field '{field}' missing from state definition")
        
        if "name" in state_def and not isinstance(state_def["name"], str):
            errors.append("State name must be a string")
        
        if "type" in state_def and not isinstance(state_def["type"], str):
            errors.append("State type must be a string")
        
        if "transitions" in state_def:
            if not isinstance(state_def["transitions"], list):
                errors.append("State transitions must be a list")
            else:
                for transition in state_def["transitions"]:
                    if not isinstance(transition, str):
                        errors.append("State transition must be a string")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"State definition validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=state_def
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_session(self, session_data: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
        """
        Unified session validation function.
        
        Args:
            session_data: Session data dictionary
            required_fields: List of required session fields
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if not isinstance(session_data, dict):
            errors.append("Session data must be a dictionary")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Session validation failed",
                errors=errors,
                warnings=warnings,
                timestamp=datetime.now(),
                validated_data=session_data
            )
        
        if required_fields:
            for field in required_fields:
                if field not in session_data:
                    errors.append(f"Required session field '{field}' missing")
        
        # Validate common session fields
        if "session_id" in session_data:
            if not isinstance(session_data["session_id"], str):
                errors.append("Session ID must be a string")
        
        if "created_at" in session_data:
            if not isinstance(session_data["created_at"], (str, datetime)):
                errors.append("Created at must be a string or datetime")
        
        if "expires_at" in session_data:
            if not isinstance(session_data["expires_at"], (str, datetime)):
                errors.append("Expires at must be a string or datetime")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Session validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=session_data
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_environment(self, env_data: Dict[str, Any] = None) -> ValidationResult:
        """
        Unified environment validation function.
        
        Args:
            env_data: Environment data dictionary (optional)
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if env_data is None:
            # Validate current environment
            try:
                import os
                import sys
                
                # Check Python version
                if sys.version_info < (3, 8):
                    warnings.append("Python version below 3.8 may cause compatibility issues")
                
                # Check common environment variables
                required_env_vars = ["PATH", "PYTHONPATH"]
                for var in required_env_vars:
                    if var not in os.environ:
                        warnings.append(f"Environment variable {var} not set")
                
                # Check working directory
                if not os.getcwd():
                    errors.append("Unable to determine working directory")
                
            except Exception as e:
                errors.append(f"Environment validation failed: {e}")
        else:
            # Validate provided environment data
            if not isinstance(env_data, dict):
                errors.append("Environment data must be a dictionary")
            else:
                for key, value in env_data.items():
                    if not isinstance(key, str):
                        errors.append("Environment key must be a string")
                    if value is None:
                        warnings.append(f"Environment value for '{key}' is None")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Environment validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=env_data
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> ValidationResult:
        """
        Unified workflow validation function.
        
        Args:
            workflow_data: Workflow data dictionary
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        required_fields = ["workflow_id", "states", "transitions"]
        for field in required_fields:
            if field not in workflow_data:
                errors.append(f"Required workflow field '{field}' missing")
        
        if "states" in workflow_data:
            if not isinstance(workflow_data["states"], list):
                errors.append("Workflow states must be a list")
            else:
                for state in workflow_data["states"]:
                    if not isinstance(state, str):
                        errors.append("Workflow state must be a string")
        
        if "transitions" in workflow_data:
            if not isinstance(workflow_data["transitions"], list):
                errors.append("Workflow transitions must be a list")
            else:
                for transition in workflow_data["transitions"]:
                    if not isinstance(transition, dict):
                        errors.append("Workflow transition must be a dictionary")
                    elif "from_state" not in transition or "to_state" not in transition:
                        errors.append("Workflow transition must have 'from_state' and 'to_state'")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Workflow validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=workflow_data
        )
        
        self.validation_history.append(result)
        return result
    
    def validate_data_types(self, data: Dict[str, Any], type_schema: Dict[str, type]) -> ValidationResult:
        """
        Unified data type validation function.
        
        Args:
            data: Data dictionary to validate
            type_schema: Dictionary mapping field names to expected types
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if not isinstance(data, dict):
            errors.append("Data must be a dictionary")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Data type validation failed",
                errors=errors,
                warnings=warnings,
                timestamp=datetime.now(),
                validated_data=data
            )
        
        if not isinstance(type_schema, dict):
            errors.append("Type schema must be a dictionary")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Data type validation failed",
                errors=errors,
                warnings=warnings,
                timestamp=datetime.now(),
                validated_data=data
            )
        
        for field, expected_type in type_schema.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    errors.append(f"Field '{field}' must be of type {expected_type.__name__}, got {type(data[field]).__name__}")
            else:
                warnings.append(f"Field '{field}' not found in data")
        
        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        if warnings and not errors:
            status = ValidationStatus.WARNING
        
        result = ValidationResult(
            status=status,
            message=f"Data type validation completed with {len(errors)} errors, {len(warnings)} warnings",
            errors=errors,
            warnings=warnings,
            timestamp=datetime.now(),
            validated_data=data
        )
        
        self.validation_history.append(result)
        return result
    
    def get_validation_history(self) -> List[ValidationResult]:
        """Get validation history for analysis and debugging."""
        return self.validation_history.copy()
    
    def clear_validation_history(self) -> None:
        """Clear validation history to free memory."""
        self.validation_history.clear()
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get validation statistics for monitoring and analysis."""
        total_validations = len(self.validation_history)
        if total_validations == 0:
            return {
                "total_validations": 0,
                "success_rate": 0.0,
                "error_rate": 0.0,
                "warning_rate": 0.0
            }
        
        valid_count = sum(1 for r in self.validation_history if r.status == ValidationStatus.VALID)
        error_count = sum(1 for r in self.validation_history if r.status == ValidationStatus.INVALID)
        warning_count = sum(1 for r in self.validation_history if r.status == ValidationStatus.WARNING)
        
        return {
            "total_validations": total_validations,
            "success_rate": valid_count / total_validations,
            "error_rate": error_count / total_validations,
            "warning_rate": warning_count / total_validations,
            "valid_count": valid_count,
            "error_count": error_count,
            "warning_count": warning_count
        }


# Global instance for easy access
unified_validators = UnifiedValidators()


# Convenience functions for backward compatibility
def validate_config(config: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
    """Convenience function for configuration validation."""
    return unified_validators.validate_config(config, required_fields)


def validate_transition(from_state: str, to_state: str, valid_transitions: Dict[str, List[str]] = None) -> ValidationResult:
    """Convenience function for transition validation."""
    return unified_validators.validate_transition(from_state, to_state, valid_transitions)


def validate_state_definition(state_def: Dict[str, Any]) -> ValidationResult:
    """Convenience function for state definition validation."""
    return unified_validators.validate_state_definition(state_def)


def validate_session(session_data: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
    """Convenience function for session validation."""
    return unified_validators.validate_session(session_data, required_fields)


def validate_environment(env_data: Dict[str, Any] = None) -> ValidationResult:
    """Convenience function for environment validation."""
    return unified_validators.validate_environment(env_data)


def validate_workflow(workflow_data: Dict[str, Any]) -> ValidationResult:
    """Convenience function for workflow validation."""
    return unified_validators.validate_workflow(workflow_data)


def validate_data_types(data: Dict[str, Any], type_schema: Dict[str, type]) -> ValidationResult:
    """Convenience function for data type validation."""
    return unified_validators.validate_data_types(data, type_schema)


# Example usage and testing
if __name__ == "__main__":
    # Test configuration validation
    test_config = {
        "version": "2.0.0",
        "enabled": True,
        "settings": {"timeout": 30}
    }
    
    result = validate_config(test_config, ["version", "enabled"])
    print(f"Config validation: {result.status.value}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
    
    # Test transition validation
    valid_transitions = {
        "idle": ["running", "paused"],
        "running": ["idle", "paused", "completed"],
        "paused": ["running", "idle"]
    }
    
    result = validate_transition("idle", "running", valid_transitions)
    print(f"Transition validation: {result.status.value}")
    print(f"Errors: {result.errors}")
    
    # Get validation statistics
    stats = unified_validators.get_validation_statistics()
    print(f"Validation statistics: {stats}")
