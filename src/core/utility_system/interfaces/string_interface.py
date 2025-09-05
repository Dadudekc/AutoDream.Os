#!/usr/bin/env python3
"""
String Interface - V2 Compliance Module
======================================

Interface definition for string operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IStringManager(ABC):
    """Interface for string operations."""

    @abstractmethod
    def format_string(self, template: str, **kwargs) -> str:
        """Format string with parameters."""
        pass

    @abstractmethod
    def sanitize_string(self, text: str, remove_special: bool = True, normalize_whitespace: bool = True) -> str:
        """Sanitize string."""
        pass

    @abstractmethod
    def validate_string(self, text: str, min_length: int = 0, max_length: int = 1000, allow_empty: bool = True) -> bool:
        """Validate string."""
        pass

    @abstractmethod
    def transform_data(self, data: Any, transformation_type: str, **kwargs) -> Any:
        """Transform data."""
        pass

    @abstractmethod
    def parse_json(self, json_string: str, **kwargs) -> Any:
        """Parse JSON string."""
        pass

    @abstractmethod
    def stringify_json(self, data: Any, **kwargs) -> str:
        """Stringify data to JSON."""
        pass

    @abstractmethod
    def batch_operations(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute batch string operations."""
        pass
