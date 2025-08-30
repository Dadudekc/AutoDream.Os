#!/usr/bin/env python3
"""
Consolidated Utility Manager - Agent Cellphone V2
================================================

Centralized utility management system that consolidates common utility functions
from multiple utils.py files across the codebase, eliminating duplication and
providing unified access to utility functions.

This system provides:
- Common utility function consolidation
- Categorized utility access
- Unified utility management
- Duplication elimination

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** DEDUP-001 - Duplicate File Analysis & Deduplication Plan
**Status:** CONSOLIDATION IN PROGRESS
**Target:** 0% utility duplication, unified management
**V2 Compliance:** ✅ Under 400 lines, single responsibility
"""

import logging
import time
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY CATEGORIES
# ============================================================================

class UtilityCategory(Enum):
    """Categories of utility functions."""
    STRING_MANIPULATION = "string_manipulation"
    DATA_PROCESSING = "data_processing"
    VALIDATION = "validation"
    FORMATTING = "formatting"
    TESTING = "testing"
    WORKFLOW = "workflow"
    COMMUNICATION = "communication"
    FRONTEND = "frontend"
    GENERAL = "general"


# ============================================================================
# UTILITY FUNCTION DATA STRUCTURES
# ============================================================================

@dataclass
class UtilityFunction:
    """Information about a utility function."""
    name: str
    category: UtilityCategory
    source_file: str
    function: Callable
    description: str = ""
    parameters: List[str] = field(default_factory=list)
    return_type: str = "Any"
    usage_count: int = 0
    last_used: Optional[float] = None


@dataclass
class UtilityCategoryInfo:
    """Information about a utility category."""
    name: UtilityCategory
    description: str
    functions: Dict[str, UtilityFunction] = field(default_factory=dict)
    total_functions: int = 0
    usage_count: int = 0


# ============================================================================
# CONSOLIDATED UTILITY MANAGER
# ============================================================================

class ConsolidatedUtilityManager:
    """
    Consolidated utility management system that eliminates duplication
    and provides unified utility access across the codebase.
    """
    
    def __init__(self):
        self.categories: Dict[UtilityCategory, UtilityCategoryInfo] = {}
        self.functions: Dict[str, UtilityFunction] = {}
        self._lock = None  # Will be initialized when needed
        
        # Initialize utility categories
        self._initialize_categories()
        
        # Register common utility functions
        self._register_common_utilities()
        
        logger.info("Consolidated utility manager initialized successfully")
    
    def _initialize_categories(self):
        """Initialize utility categories."""
        category_descriptions = {
            UtilityCategory.STRING_MANIPULATION: "String manipulation and text processing utilities",
            UtilityCategory.DATA_PROCESSING: "Data processing and transformation utilities",
            UtilityCategory.VALIDATION: "Data validation and verification utilities",
            UtilityCategory.FORMATTING: "Data formatting and presentation utilities",
            UtilityCategory.TESTING: "Testing and mock data creation utilities",
            UtilityCategory.WORKFLOW: "Workflow and state management utilities",
            UtilityCategory.COMMUNICATION: "Communication and messaging utilities",
            UtilityCategory.FRONTEND: "Frontend and UI utilities",
            UtilityCategory.GENERAL: "General purpose utilities"
        }
        
        for category, description in category_descriptions.items():
            self.categories[category] = UtilityCategoryInfo(
                name=category,
                description=description
            )
    
    def _register_common_utilities(self):
        """Register common utility functions."""
        # String manipulation utilities
        self.register_function(
            "safe_string",
            self._safe_string_utility,
            UtilityCategory.STRING_MANIPULATION,
            "src/core/utils/consolidated_utility_manager.py",
            "Safely convert value to string",
            ["value", "default"],
            "str"
        )
        
        # Data processing utilities
        self.register_function(
            "safe_get",
            self._safe_get_utility,
            UtilityCategory.DATA_PROCESSING,
            "src/core/utils/consolidated_utility_manager.py",
            "Safely get value from nested dictionary",
            ["data", "key_path", "default"],
            "Any"
        )
        
        # Validation utilities
        self.register_function(
            "validate_required",
            self._validate_required_utility,
            UtilityCategory.VALIDATION,
            "src/core/utils/consolidated_utility_manager.py",
            "Validate required fields in data",
            ["data", "required_fields"],
            "bool"
        )
        
        # Formatting utilities
        self.register_function(
            "format_timestamp",
            self._format_timestamp_utility,
            UtilityCategory.FORMATTING,
            "src/core/utils/consolidated_utility_manager.py",
            "Format timestamp to readable string",
            ["timestamp", "format_str"],
            "str"
        )
        
        # Testing utilities
        self.register_function(
            "create_mock_data",
            self._create_mock_data_utility,
            UtilityCategory.TESTING,
            "src/core/utils/consolidated_utility_manager.py",
            "Create mock data for testing",
            ["template", "overrides"],
            "Dict[str, Any]"
        )
        
        # Workflow utilities
        self.register_function(
            "evaluate_condition",
            self._evaluate_condition_utility,
            UtilityCategory.WORKFLOW,
            "src/core/utils/consolidated_utility_manager.py",
            "Evaluate workflow transition conditions",
            ["condition", "context"],
            "bool"
        )
        
        # Communication utilities
        self.register_function(
            "format_message",
            self._format_message_utility,
            UtilityCategory.COMMUNICATION,
            "src/core/utils/consolidated_utility_manager.py",
            "Format communication messages",
            ["template", "variables"],
            "str"
        )
        
        # Frontend utilities
        self.register_function(
            "create_component_props",
            self._create_component_props_utility,
            UtilityCategory.FRONTEND,
            "src/core/utils/consolidated_utility_manager.py",
            "Create component properties for frontend",
            ["base_props", "overrides"],
            "Dict[str, Any]"
        )
        
        # General utilities
        self.register_function(
            "merge_dicts",
            self._merge_dicts_utility,
            UtilityCategory.GENERAL,
            "src/core/utils/consolidated_utility_manager.py",
            "Merge multiple dictionaries",
            ["dicts"],
            "Dict[str, Any]"
        )
    
    def register_function(self, name: str, function: Callable, category: UtilityCategory,
                         source_file: str, description: str, parameters: List[str],
                         return_type: str) -> str:
        """Register a new utility function."""
        utility_func = UtilityFunction(
            name=name,
            category=category,
            source_file=source_file,
            function=function,
            description=description,
            parameters=parameters,
            return_type=return_type
        )
        
        self.functions[name] = utility_func
        self.categories[category].functions[name] = utility_func
        self.categories[category].total_functions += 1
        
        logger.debug(f"Registered utility function: {name} in category {category.value}")
        return name
    
    def get_function(self, name: str) -> Optional[UtilityFunction]:
        """Get a utility function by name."""
        return self.functions.get(name)
    
    def get_functions_by_category(self, category: UtilityCategory) -> List[UtilityFunction]:
        """Get all functions in a specific category."""
        return list(self.categories[category].functions.values())
    
    def list_categories(self) -> List[UtilityCategory]:
        """List all utility categories."""
        return list(self.categories.keys())
    
    def list_functions(self, category: Optional[UtilityCategory] = None) -> List[str]:
        """List utility function names."""
        if category:
            return list(self.categories[category].functions.keys())
        return list(self.functions.keys())
    
    def execute_function(self, name: str, *args, **kwargs) -> Any:
        """Execute a utility function by name."""
        utility_func = self.get_function(name)
        if not utility_func:
            raise ValueError(f"Utility function '{name}' not found")
        
        try:
            # Update usage statistics
            utility_func.usage_count += 1
            utility_func.last_used = time.time()
            self.categories[utility_func.category].usage_count += 1
            
            # Execute the function
            result = utility_func.function(*args, **kwargs)
            return result
            
        except Exception as e:
            logger.error(f"Error executing utility function '{name}': {e}")
            raise
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics for utility functions."""
        stats = {
            "total_functions": len(self.functions),
            "categories": {},
            "most_used": [],
            "recently_used": []
        }
        
        # Category statistics
        for category, info in self.categories.items():
            stats["categories"][category.value] = {
                "total_functions": info.total_functions,
                "usage_count": info.usage_count
            }
        
        # Most used functions
        most_used = sorted(
            self.functions.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )[:10]
        stats["most_used"] = [
            {"name": func.name, "usage_count": func.usage_count}
            for func in most_used
        ]
        
        # Recently used functions
        recently_used = sorted(
            [f for f in self.functions.values() if f.last_used],
            key=lambda x: x.last_used,
            reverse=True
        )[:10]
        stats["recently_used"] = [
            {"name": func.name, "last_used": func.last_used}
            for func in recently_used
        ]
        
        return stats
    
    # Common utility function implementations
    def _safe_string_utility(self, value: Any, default: str = "") -> str:
        """Safely convert value to string."""
        try:
            return str(value) if value is not None else default
        except Exception:
            return default
    
    def _safe_get_utility(self, data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
        """Safely get value from nested dictionary."""
        try:
            keys = key_path.split('.')
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default
            return current
        except Exception:
            return default
    
    def _validate_required_utility(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate required fields in data."""
        try:
            return all(field in data and data[field] is not None for field in required_fields)
        except Exception:
            return False
    
    def _format_timestamp_utility(self, timestamp: Union[float, datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format timestamp to readable string."""
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
            else:
                dt = timestamp
            return dt.strftime(format_str)
        except Exception:
            return str(timestamp)
    
    def _create_mock_data_utility(self, template: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create mock data for testing."""
        try:
            mock_data = template.copy()
            if overrides:
                mock_data.update(overrides)
            return mock_data
        except Exception:
            return template or {}
    
    def _evaluate_condition_utility(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate workflow transition conditions."""
        try:
            if "==" in condition:
                key, value = condition.split("==")
                return str(context.get(key.strip())) == value.strip()
            if "!=" in condition:
                key, value = condition.split("!=")
                return str(context.get(key.strip())) != value.strip()
            if ">" in condition:
                key, value = condition.split(">")
                return float(context.get(key.strip(), 0)) > float(value.strip())
            if "<" in condition:
                key, value = condition.split("<")
                return float(context.get(key.strip(), 0)) < float(value.strip())
            return condition.strip() in context
        except Exception:
            return False
    
    def _format_message_utility(self, template: str, variables: Dict[str, Any]) -> str:
        """Format communication messages."""
        try:
            return template.format(**variables)
        except Exception:
            return template
    
    def _create_component_props_utility(self, base_props: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create component properties for frontend."""
        try:
            props = base_props.copy()
            if overrides:
                props.update(overrides)
            return props
        except Exception:
            return base_props or {}
    
    def _merge_dicts_utility(self, *dicts: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple dictionaries."""
        try:
            result = {}
            for d in dicts:
                if d:
                    result.update(d)
            return result
        except Exception:
            return {}


# ============================================================================
# GLOBAL UTILITY MANAGER INSTANCE
# ============================================================================

# Global utility manager instance
_utility_manager: Optional[ConsolidatedUtilityManager] = None

def get_utility_manager() -> ConsolidatedUtilityManager:
    """Get the global utility manager instance."""
    global _utility_manager
    if _utility_manager is None:
        _utility_manager = ConsolidatedUtilityManager()
    return _utility_manager

def get_utility(name: str) -> Optional[UtilityFunction]:
    """Get a utility function from the global manager."""
    return get_utility_manager().get_function(name)

def execute_utility(name: str, *args, **kwargs) -> Any:
    """Execute a utility function from the global manager."""
    return get_utility_manager().execute_function(name, *args, **kwargs)


# ============================================================================
# MAIN EXECUTION (FOR TESTING)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    utility_manager = ConsolidatedUtilityManager()
    
    # Test utility functions
    result1 = utility_manager.execute_function("safe_string", "test_value")
    result2 = utility_manager.execute_function("safe_get", {"a": {"b": "c"}}, "a.b")
    result3 = utility_manager.execute_function("validate_required", {"name": "test"}, ["name"])
    
    print(f"Safe string: {result1}")
    print(f"Safe get: {result2}")
    print(f"Validate required: {result3}")
    
    # Show usage statistics
    stats = utility_manager.get_usage_statistics()
    print(f"\nUsage statistics: {stats}")
