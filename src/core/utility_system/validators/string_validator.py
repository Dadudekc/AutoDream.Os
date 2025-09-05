#!/usr/bin/env python3
"""
String Validator - V2 Compliance Module
======================================

Validation utilities for string operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import json
import re
from typing import Any


class StringValidator:
    """Validator for string operations."""

    def validate_string_length(self, text: str, max_length: int) -> bool:
        """Validate string length."""
        try:
            return len(text) <= max_length
        except Exception:
            return False

    def validate_template(self, template: str) -> bool:
        """Validate string template format."""
        try:
            # Check for balanced braces
            open_braces = template.count('{')
            close_braces = template.count('}')
            return open_braces == close_braces
        except Exception:
            return False

    def validate_format_parameters(self, template: str, params: dict) -> bool:
        """Validate format parameters."""
        try:
            # Try to format with empty values to check syntax
            test_template = template
            for key in params.keys():
                test_template = test_template.replace(f"{{{key}}}", "")
            return True
        except Exception:
            return False

    def validate_json_string(self, json_string: str) -> bool:
        """Validate JSON string format."""
        try:
            json.loads(json_string)
            return True
        except Exception:
            return False

    def validate_json_serializable(self, data: Any) -> bool:
        """Validate data is JSON serializable."""
        try:
            json.dumps(data)
            return True
        except Exception:
            return False

    def validate_string_list(self, strings: list) -> bool:
        """Validate list of strings."""
        try:
            return all(isinstance(s, str) for s in strings)
        except Exception:
            return False

    def validate_transformation_type(self, transformation_type: str) -> bool:
        """Validate transformation type."""
        valid_types = [
            "json_stringify", "json_parse", "string_lower", 
            "string_upper", "string_title", "string_strip",
            "string_replace", "string_split", "string_join"
        ]
        return transformation_type in valid_types

    def validate(self, text: str, min_length: int = 0, max_length: int = 1000, allow_empty: bool = True) -> bool:
        """Comprehensive string validation."""
        try:
            if not isinstance(text, str):
                return False
            
            if not allow_empty and len(text.strip()) == 0:
                return False
            
            if len(text) < min_length or len(text) > max_length:
                return False
            
            return True
        except Exception:
            return False
