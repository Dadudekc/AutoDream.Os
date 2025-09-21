#!/usr/bin/env python3
"""
Shared Validation Utilities
===========================

Centralized validation functions for the Agent Cellphone V2 system.
Eliminates duplicate validation logic across the project.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import re
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from datetime import datetime
from .shared_logging import get_module_logger

logger = get_module_logger(__name__)


class ValidationError(Exception):
    """Custom validation error."""
    pass


class SharedValidator:
    """Shared validation utilities."""
    
    @staticmethod
    def validate_not_none(value: Any, field_name: str) -> None:
        """Validate that a value is not None."""
        if value is None:
            raise ValidationError(f"{field_name} cannot be None")
    
    @staticmethod
    def validate_not_empty(value: Union[str, List, Dict], field_name: str) -> None:
        """Validate that a value is not empty."""
        if not value:
            raise ValidationError(f"{field_name} cannot be empty")
    
    @staticmethod
    def validate_string_length(
        value: str, 
        field_name: str, 
        min_length: int = 1, 
        max_length: Optional[int] = None
    ) -> None:
        """Validate string length."""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if len(value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters")
        
        if max_length and len(value) > max_length:
            raise ValidationError(f"{field_name} must be at most {max_length} characters")
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        """Validate agent ID format (Agent-1, Agent-2, etc.)."""
        pattern = r'^Agent-\d+$'
        return bool(re.match(pattern, agent_id))
    
    @staticmethod
    def validate_file_path(file_path: Union[str, Path], must_exist: bool = True) -> Path:
        """Validate file path."""
        path = Path(file_path)
        
        if must_exist and not path.exists():
            raise ValidationError(f"File does not exist: {path}")
        
        return path
    
    @staticmethod
    def validate_directory_path(dir_path: Union[str, Path], must_exist: bool = True) -> Path:
        """Validate directory path."""
        path = Path(dir_path)
        
        if must_exist and not path.exists():
            raise ValidationError(f"Directory does not exist: {path}")
        
        if not path.is_dir():
            raise ValidationError(f"Path is not a directory: {path}")
        
        return path
    
    @staticmethod
    def validate_config_dict(config: Dict[str, Any], required_keys: List[str]) -> None:
        """Validate configuration dictionary has required keys."""
        for key in required_keys:
            if key not in config:
                raise ValidationError(f"Missing required configuration key: {key}")
    
    @staticmethod
    def validate_positive_number(value: Union[int, float], field_name: str) -> None:
        """Validate that a number is positive."""
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field_name} must be a number")
        
        if value <= 0:
            raise ValidationError(f"{field_name} must be positive")
    
    @staticmethod
    def validate_range(
        value: Union[int, float], 
        field_name: str, 
        min_val: Union[int, float], 
        max_val: Union[int, float]
    ) -> None:
        """Validate that a value is within a range."""
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field_name} must be a number")
        
        if value < min_val or value > max_val:
            raise ValidationError(f"{field_name} must be between {min_val} and {max_val}")
    
    @staticmethod
    def validate_enum_value(value: Any, enum_class: type, field_name: str) -> None:
        """Validate that a value is a valid enum value."""
        if not isinstance(value, enum_class):
            raise ValidationError(f"{field_name} must be a valid {enum_class.__name__} value")


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that required fields are present in data."""
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")


def validate_agent_message(message: str) -> None:
    """Validate agent message format."""
    SharedValidator.validate_not_empty(message, "message")
    SharedValidator.validate_string_length(message, "message", max_length=2000)


def validate_coordinates(coords: Dict[str, Any]) -> None:
    """Validate coordinate dictionary."""
    required_keys = ["x", "y"]
    SharedValidator.validate_config_dict(coords, required_keys)
    
    SharedValidator.validate_positive_number(coords["x"], "x coordinate")
    SharedValidator.validate_positive_number(coords["y"], "y coordinate")


def validate_discord_config(config: Dict[str, Any]) -> None:
    """Validate Discord bot configuration."""
    required_keys = ["token", "channel_id"]
    SharedValidator.validate_config_dict(config, required_keys)
    
    SharedValidator.validate_not_empty(config["token"], "Discord token")
    SharedValidator.validate_not_empty(config["channel_id"], "Discord channel ID")


def validate_v2_compliance(file_path: Path) -> Dict[str, Any]:
    """Validate V2 compliance for a file."""
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check file length
        if len(lines) > 400:
            violations.append(f"File exceeds 400 lines: {len(lines)}")
        
        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line.rstrip()) > 100:
                violations.append(f"Line {i} exceeds 100 characters: {len(line.rstrip())}")
        
        return {
            "file_path": str(file_path),
            "line_count": len(lines),
            "violations": violations,
            "compliant": len(violations) == 0
        }
        
    except Exception as e:
        logger.error(f"Error validating file {file_path}: {e}")
        return {
            "file_path": str(file_path),
            "line_count": 0,
            "violations": [f"Error reading file: {e}"],
            "compliant": False
        }


def validate_with_custom_validator(
    value: Any, 
    validator: Callable[[Any], bool], 
    field_name: str,
    error_message: Optional[str] = None
) -> None:
    """Validate using a custom validator function."""
    if not validator(value):
        error_msg = error_message or f"{field_name} validation failed"
        raise ValidationError(error_msg)


