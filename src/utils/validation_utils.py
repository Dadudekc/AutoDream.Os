#!/usr/bin/env python3
"""
Validation Utils - Data Validation Functions

This module provides data validation utility functions including:
- Email and URL validation
- Required field validation
- Data type validation
- Format validation

Architecture: Single Responsibility Principle - data validation only
LOC: 150 lines (under 200 limit)
"""

import re
import json
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class ValidationUtils:
    """Data validation utility functions"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address format"""
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        except Exception as e:
            logger.error(f"Email validation error: {e}")
            return False
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format"""
        try:
            pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
            return bool(re.match(pattern, url))
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, str]:
        """Validate that required fields are present and not empty"""
        errors = {}
        
        for field in required_fields:
            if field not in data:
                errors[field] = f"Required field '{field}' is missing"
            elif data[field] is None:
                errors[field] = f"Required field '{field}' cannot be null"
            elif isinstance(data[field], str) and not data[field].strip():
                errors[field] = f"Required field '{field}' cannot be empty"
            elif isinstance(data[field], (list, dict)) and not data[field]:
                errors[field] = f"Required field '{field}' cannot be empty"
        
        return errors
    
    @staticmethod
    def validate_data_types(data: Dict[str, Any], type_schema: Dict[str, type]) -> Dict[str, str]:
        """Validate data types against schema"""
        errors = {}
        
        for field, expected_type in type_schema.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    errors[field] = f"Field '{field}' must be of type {expected_type.__name__}, got {type(data[field]).__name__}"
        
        return errors
    
    @staticmethod
    def validate_json_string(json_str: str) -> bool:
        """Validate if string is valid JSON"""
        try:
            json.loads(json_str)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """Validate file extension"""
        try:
            if not filename:
                return False
            extension = filename.lower().split('.')[-1]
            return extension in [ext.lower() for ext in allowed_extensions]
        except Exception:
            return False
    
    @staticmethod
    def validate_string_length(text: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
        """Validate string length constraints"""
        try:
            if not isinstance(text, str):
                return False
            
            if len(text) < min_length:
                return False
            
            if max_length is not None and len(text) > max_length:
                return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_numeric_range(value: Union[int, float], min_val: Optional[Union[int, float]] = None, 
                             max_val: Optional[Union[int, float]] = None) -> bool:
        """Validate numeric value is within range"""
        try:
            if not isinstance(value, (int, float)):
                return False
            
            if min_val is not None and value < min_val:
                return False
            
            if max_val is not None and value > max_val:
                return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_choice(value: Any, choices: List[Any]) -> bool:
        """Validate value is one of the allowed choices"""
        try:
            return value in choices
        except Exception:
            return False
    
    @staticmethod
    def validate_pattern(text: str, pattern: str) -> bool:
        """Validate text against regex pattern"""
        try:
            return bool(re.match(pattern, text))
        except Exception as e:
            logger.error(f"Pattern validation error: {e}")
            return False


def main():
    """CLI interface for validation utilities testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validation Utils CLI")
    parser.add_argument("--email", help="Validate email address")
    parser.add_argument("--url", help="Validate URL")
    parser.add_argument("--json", help="Validate JSON string")
    parser.add_argument("--file-ext", help="Validate file extension")
    parser.add_argument("--string-length", help="Validate string length")
    parser.add_argument("--numeric-range", help="Validate numeric range")
    parser.add_argument("--choice", help="Validate choice")
    parser.add_argument("--pattern", help="Validate pattern")
    
    args = parser.parse_args()
    
    if args.email:
        is_valid = ValidationUtils.is_valid_email(args.email)
        print(f"Email '{args.email}' is valid: {is_valid}")
    elif args.url:
        is_valid = ValidationUtils.is_valid_url(args.url)
        print(f"URL '{args.url}' is valid: {is_valid}")
    elif args.json:
        is_valid = ValidationUtils.validate_json_string(args.json)
        print(f"JSON string is valid: {is_valid}")
    elif args.file_ext:
        is_valid = ValidationUtils.validate_file_extension(args.file_ext, ["txt", "json", "yaml"])
        print(f"File extension is valid: {is_valid}")
    elif args.string_length:
        is_valid = ValidationUtils.validate_string_length(args.string_length, 1, 100)
        print(f"String length is valid: {is_valid}")
    elif args.numeric_range:
        try:
            value = float(args.numeric_range)
            is_valid = ValidationUtils.validate_numeric_range(value, 0, 100)
            print(f"Numeric range is valid: {is_valid}")
        except ValueError:
            print("Invalid numeric value")
    elif args.choice:
        is_valid = ValidationUtils.validate_choice(args.choice, ["option1", "option2", "option3"])
        print(f"Choice is valid: {is_valid}")
    elif args.pattern:
        is_valid = ValidationUtils.validate_pattern(args.pattern, r'^[A-Za-z0-9]+$')
        print(f"Pattern is valid: {is_valid}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
