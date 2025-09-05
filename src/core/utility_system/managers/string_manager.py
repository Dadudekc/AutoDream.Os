#!/usr/bin/env python3
"""
String Manager - V2 Compliance Module
====================================

Specialized manager for string operations with enhanced validation,
transformation, and performance monitoring.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import json
import re
import time
import asyncio
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass

from ..utility_system_models import UtilityOperationType, StringOperationResult
from ..interfaces.string_interface import IStringManager
from ..validators.string_validator import StringValidator
from ..transformers.string_transformer import StringTransformer


@dataclass
class StringOperationConfig:
    """Configuration for string operations."""
    enable_caching: bool = True
    cache_ttl_seconds: int = 300
    max_string_length: int = 10000
    enable_validation: bool = True
    enable_sanitization: bool = True
    transformation_timeout_ms: int = 5000


class StringManager(IStringManager):
    """Enhanced string manager with validation, transformation, and caching."""

    def __init__(self, config: StringOperationConfig = None):
        """Initialize string manager."""
        self.config = config or StringOperationConfig()
        self.validator = StringValidator()
        self.transformer = StringTransformer()
        self._operation_handlers: Dict[str, Callable] = {
            'format': self._handle_format,
            'sanitize': self._handle_sanitize,
            'validate': self._handle_validate,
            'transform': self._handle_transform,
            'parse_json': self._handle_parse_json,
            'stringify_json': self._handle_stringify_json
        }

    def format_string(self, template: str, **kwargs) -> str:
        """Format string with parameters and validation."""
        start_time = time.time()
        
        try:
            # Validate template
            if not self.validator.validate_template(template):
                raise ValueError("Invalid template format")
            
            # Validate parameters
            if not self.validator.validate_format_parameters(template, kwargs):
                raise ValueError("Invalid format parameters")
            
            # Format string
            formatted = template.format(**kwargs)
            
            # Validate result
            if not self.validator.validate_string_length(formatted, self.config.max_string_length):
                raise ValueError("Formatted string too long")
            
            execution_time = (time.time() - start_time) * 1000
            return formatted
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to format string: {str(e)}", execution_time)

    def sanitize_string(self, text: str, remove_special: bool = True, normalize_whitespace: bool = True) -> str:
        """Sanitize string with enhanced options."""
        start_time = time.time()
        
        try:
            if not isinstance(text, str):
                text = str(text)
            
            # Validate input
            if not self.validator.validate_string_length(text, self.config.max_string_length):
                raise ValueError("Input string too long")
            
            # Apply sanitization
            sanitized = self.transformer.sanitize(text, remove_special, normalize_whitespace)
            
            execution_time = (time.time() - start_time) * 1000
            return sanitized
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to sanitize string: {str(e)}", execution_time)

    def validate_string(self, text: str, min_length: int = 0, max_length: int = 1000, allow_empty: bool = True) -> bool:
        """Validate string with comprehensive checks."""
        start_time = time.time()
        
        try:
            result = self.validator.validate(
                text, 
                min_length=min_length, 
                max_length=max_length, 
                allow_empty=allow_empty
            )
            
            execution_time = (time.time() - start_time) * 1000
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to validate string: {str(e)}", execution_time)

    def transform_data(self, data: Any, transformation_type: str, **kwargs) -> Any:
        """Transform data with enhanced transformation options."""
        start_time = time.time()
        
        try:
            # Validate transformation type
            if not self.validator.validate_transformation_type(transformation_type):
                raise ValueError(f"Invalid transformation type: {transformation_type}")
            
            # Apply transformation
            result = self.transformer.transform(data, transformation_type, **kwargs)
            
            execution_time = (time.time() - start_time) * 1000
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to transform data: {str(e)}", execution_time)

    def parse_json(self, json_string: str, **kwargs) -> Any:
        """Parse JSON string with validation."""
        start_time = time.time()
        
        try:
            # Validate JSON string
            if not self.validator.validate_json_string(json_string):
                raise ValueError("Invalid JSON string")
            
            # Parse JSON
            result = json.loads(json_string, **kwargs)
            
            execution_time = (time.time() - start_time) * 1000
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to parse JSON: {str(e)}", execution_time)

    def stringify_json(self, data: Any, **kwargs) -> str:
        """Stringify data to JSON with validation."""
        start_time = time.time()
        
        try:
            # Validate data is JSON serializable
            if not self.validator.validate_json_serializable(data):
                raise ValueError("Data is not JSON serializable")
            
            # Stringify JSON
            result = json.dumps(data, **kwargs)
            
            # Validate result length
            if not self.validator.validate_string_length(result, self.config.max_string_length):
                raise ValueError("JSON string too long")
            
            execution_time = (time.time() - start_time) * 1000
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise StringOperationError(f"Failed to stringify JSON: {str(e)}", execution_time)

    def extract_patterns(self, text: str, pattern: str, flags: int = 0) -> List[str]:
        """Extract patterns from text using regex."""
        try:
            matches = re.findall(pattern, text, flags)
            return matches
        except Exception:
            return []

    def replace_patterns(self, text: str, pattern: str, replacement: str, flags: int = 0) -> str:
        """Replace patterns in text using regex."""
        try:
            return re.sub(pattern, replacement, text, flags=flags)
        except Exception:
            return text

    def split_string(self, text: str, delimiter: str, maxsplit: int = -1) -> List[str]:
        """Split string with validation."""
        try:
            if not self.validator.validate_string_length(text, self.config.max_string_length):
                raise ValueError("Input string too long")
            
            return text.split(delimiter, maxsplit)
        except Exception:
            return [text]

    def join_strings(self, strings: List[str], delimiter: str = " ") -> str:
        """Join strings with validation."""
        try:
            if not self.validator.validate_string_list(strings):
                raise ValueError("Invalid string list")
            
            result = delimiter.join(strings)
            
            if not self.validator.validate_string_length(result, self.config.max_string_length):
                raise ValueError("Joined string too long")
            
            return result
        except Exception:
            return ""

    def batch_operations(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute batch string operations."""
        results = []
        
        for operation in operations:
            try:
                op_type = operation.get("type")
                handler = self._operation_handlers.get(op_type)
                
                if handler:
                    result = handler(operation)
                    results.append(result)
                else:
                    results.append(None)
                    
            except Exception as e:
                results.append(StringOperationError(f"Operation failed: {str(e)}"))
        
        return results

    async def async_format_string(self, template: str, **kwargs) -> str:
        """Async string formatting."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.format_string, template, **kwargs)

    async def async_transform_data(self, data: Any, transformation_type: str, **kwargs) -> Any:
        """Async data transformation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.transform_data, data, transformation_type, **kwargs)

    def _handle_format(self, operation: Dict[str, Any]) -> str:
        """Handle format operation."""
        return self.format_string(operation["template"], **operation.get("kwargs", {}))

    def _handle_sanitize(self, operation: Dict[str, Any]) -> str:
        """Handle sanitize operation."""
        return self.sanitize_string(
            operation["text"],
            operation.get("remove_special", True),
            operation.get("normalize_whitespace", True)
        )

    def _handle_validate(self, operation: Dict[str, Any]) -> bool:
        """Handle validate operation."""
        return self.validate_string(
            operation["text"],
            operation.get("min_length", 0),
            operation.get("max_length", 1000),
            operation.get("allow_empty", True)
        )

    def _handle_transform(self, operation: Dict[str, Any]) -> Any:
        """Handle transform operation."""
        return self.transform_data(
            operation["data"],
            operation["transformation_type"],
            **operation.get("kwargs", {})
        )

    def _handle_parse_json(self, operation: Dict[str, Any]) -> Any:
        """Handle parse JSON operation."""
        return self.parse_json(operation["json_string"], **operation.get("kwargs", {}))

    def _handle_stringify_json(self, operation: Dict[str, Any]) -> str:
        """Handle stringify JSON operation."""
        return self.stringify_json(operation["data"], **operation.get("kwargs", {}))


class StringOperationError(Exception):
    """Custom exception for string operations."""
    
    def __init__(self, message: str, execution_time_ms: float = 0.0):
        super().__init__(message)
        self.execution_time_ms = execution_time_ms
