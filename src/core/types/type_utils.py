#!/usr/bin/env python3
"""
Type Utilities - Type Management and Validation Tools
===================================================

Utility functions for type validation, conversion, and management.
Provides helper functions for the unified type system.

Agent: Agent-8 (Type Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Type Registry

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional, Type, Union, get_type_hints
from enum import Enum
import inspect
import json


# Setup logging
logger = logging.getLogger(__name__)


def validate_type(value: Any, expected_type: Union[Type, str], registry=None) -> bool:
    """
    Validate if a value matches the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type (class or type name string)
        registry: Optional type registry for string-based type resolution
        
    Returns:
        True if value matches expected type, False otherwise
    """
    try:
        if isinstance(expected_type, str):
            # String-based type resolution
            if registry:
                actual_type = registry.get_type(expected_type)
                if actual_type:
                    expected_type = actual_type
                else:
                    logger.warning(f"Type '{expected_type}' not found in registry")
                    return False
            else:
                logger.warning("Registry required for string-based type validation")
                return False
        
        if expected_type == Any:
            return True
        
        if expected_type == Optional:
            return True
        
        if hasattr(expected_type, "__origin__") and expected_type.__origin__ == Union:
            # Handle Union types (including Optional)
            return any(validate_type(value, t) for t in expected_type.__args__)
        
        if isinstance(expected_type, type):
            if issubclass(expected_type, Enum):
                # For enums, check if value is a valid enum value
                return value in [e.value for e in expected_type]
            else:
                # For other types, check if value is instance
                return isinstance(value, expected_type)
        
        return False
        
    except Exception as e:
        logger.error(f"Error validating type: {e}")
        return False


def convert_type(value: Any, target_type: Union[Type, str], registry=None) -> Optional[Any]:
    """
    Convert a value to the target type.
    
    Args:
        value: Value to convert
        target_type: Target type (class or type name string)
        registry: Optional type registry for string-based type resolution
        
    Returns:
        Converted value if successful, None otherwise
    """
    try:
        if isinstance(target_type, str):
            # String-based type resolution
            if registry:
                actual_type = registry.get_type(target_type)
                if actual_type:
                    target_type = actual_type
                else:
                    logger.warning(f"Type '{target_type}' not found in registry")
                    return None
            else:
                logger.warning("Registry required for string-based type conversion")
                return None
        
        if target_type == Any:
            return value
        
        if target_type == Optional:
            return value
        
        if hasattr(target_type, "__origin__") and target_type.__origin__ == Union:
            # Handle Union types (including Optional)
            for t in target_type.__args__:
                try:
                    converted = convert_type(value, t, registry)
                    if converted is not None:
                        return converted
                except:
                    continue
            return None
        
        if isinstance(target_type, type):
            if issubclass(target_type, Enum):
                # For enums, try to find matching value
                for enum_value in target_type:
                    if enum_value.value == value:
                        return enum_value
                return None
            else:
                # For other types, try direct conversion
                return target_type(value)
        
        return None
        
    except Exception as e:
        logger.error(f"Error converting type: {e}")
        return None


def get_type_info(type_class: Type) -> Dict[str, Any]:
    """
    Get comprehensive information about a type.
    
    Args:
        type_class: Type class to analyze
        
    Returns:
        Dictionary containing type information
    """
    try:
        type_info = {
            "name": type_class.__name__,
            "module": type_class.__module__,
            "bases": [base.__name__ for base in type_class.__bases__],
            "is_enum": issubclass(type_class, Enum),
            "is_dataclass": hasattr(type_class, "__dataclass_fields__"),
            "is_abstract": inspect.isabstract(type_class),
            "methods": [],
            "properties": [],
            "fields": []
        }
        
        # Get methods
        for name, method in inspect.getmembers(type_class, inspect.isfunction):
            if not name.startswith("_"):
                type_info["methods"].append(name)
        
        # Get properties
        for name, prop in inspect.getmembers(type_class, lambda x: isinstance(x, property)):
            type_info["properties"].append(name)
        
        # Get fields (for dataclasses)
        if type_info["is_dataclass"]:
            type_info["fields"] = list(type_class.__dataclass_fields__.keys())
        
        # Get enum values if it's an enum
        if type_info["is_enum"]:
            type_info["enum_values"] = [e.value for e in type_class]
            type_info["enum_members"] = [e.name for e in type_class]
        
        return type_info
        
    except Exception as e:
        logger.error(f"Error getting type info: {e}")
        return {"error": str(e)}


def register_custom_type(name: str, type_class: Type, registry=None, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Register a custom type in the registry.
    
    Args:
        name: Type name
        type_class: Type class
        registry: Type registry to register with
        metadata: Additional metadata
        
    Returns:
        True if registration successful, False otherwise
    """
    try:
        if not registry:
            logger.error("Registry required for type registration")
            return False
        
        registry.register_type(name, type_class, "custom", metadata or {})
        logger.info(f"Custom type '{name}' registered successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error registering custom type '{name}': {e}")
        return False


def get_type_hints_info(type_class: Type) -> Dict[str, Any]:
    """
    Get type hints information for a type.
    
    Args:
        type_class: Type class to analyze
        
    Returns:
        Dictionary containing type hints information
    """
    try:
        type_hints = get_type_hints(type_class)
        
        hints_info = {
            "type_name": type_class.__name__,
            "type_hints": {},
            "annotations": {}
        }
        
        # Process type hints
        for name, hint in type_hints.items():
            hints_info["type_hints"][name] = {
                "hint": str(hint),
                "origin": getattr(hint, "__origin__", None),
                "args": getattr(hint, "__args__", None),
                "is_optional": hint == Optional or (hasattr(hint, "__origin__") and hint.__origin__ == Union and type(None) in hint.__args__)
            }
        
        # Get annotations
        if hasattr(type_class, "__annotations__"):
            hints_info["annotations"] = type_class.__annotations__
        
        return hints_info
        
    except Exception as e:
        logger.error(f"Error getting type hints info: {e}")
        return {"error": str(e)}


def analyze_type_compatibility(type1: Type, type2: Type) -> Dict[str, Any]:
    """
    Analyze compatibility between two types.
    
    Args:
        type1: First type
        type2: Second type
        
    Returns:
        Dictionary containing compatibility analysis
    """
    try:
        compatibility = {
            "type1": type1.__name__,
            "type2": type2.__name__,
            "compatible": False,
            "compatibility_score": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        # Check if types are the same
        if type1 == type2:
            compatibility["compatible"] = True
            compatibility["compatibility_score"] = 1.0
            compatibility["recommendations"].append("Types are identical")
            return compatibility
        
        # Check inheritance relationship
        if issubclass(type1, type2):
            compatibility["compatible"] = True
            compatibility["compatibility_score"] = 0.8
            compatibility["recommendations"].append(f"{type1.__name__} is a subclass of {type2.__name__}")
        elif issubclass(type2, type1):
            compatibility["compatible"] = True
            compatibility["compatibility_score"] = 0.6
            compatibility["recommendations"].append(f"{type2.__name__} is a subclass of {type1.__name__}")
        
        # Check if both are enums
        if issubclass(type1, Enum) and issubclass(type2, Enum):
            compatibility["compatibility_score"] += 0.2
            compatibility["recommendations"].append("Both types are enums")
        
        # Check for common base classes
        common_bases = set(type1.__bases__) & set(type2.__bases__)
        if common_bases:
            compatibility["compatibility_score"] += 0.1 * len(common_bases)
            compatibility["recommendations"].append(f"Common base classes: {[b.__name__ for b in common_bases]}")
        
        # Determine overall compatibility
        compatibility["compatible"] = compatibility["compatibility_score"] >= 0.5
        
        # Generate recommendations
        if not compatibility["compatible"]:
            compatibility["recommendations"].append("Consider using type conversion or adapter pattern")
            compatibility["recommendations"].append("Review type hierarchy for better compatibility")
        
        return compatibility
        
    except Exception as e:
        logger.error(f"Error analyzing type compatibility: {e}")
        return {"error": str(e)}


def generate_type_documentation(type_class: Type) -> str:
    """
    Generate documentation for a type.
    
    Args:
        type_class: Type class to document
        
    Returns:
        Generated documentation string
    """
    try:
        type_info = get_type_info(type_class)
        
        doc = f"# {type_class.__name__}\n\n"
        
        # Add module information
        doc += f"**Module:** {type_class.__module__}\n\n"
        
        # Add base classes
        if type_info["bases"]:
            doc += f"**Base Classes:** {', '.join(type_info['bases'])}\n\n"
        
        # Add class docstring
        if type_class.__doc__:
            doc += f"**Description:** {type_class.__doc__.strip()}\n\n"
        
        # Add enum information
        if type_info["is_enum"]:
            doc += "## Enum Values\n\n"
            for name, value in zip(type_info["enum_members"], type_info["enum_values"]):
                doc += f"- `{name}`: `{value}`\n"
            doc += "\n"
        
        # Add fields information
        if type_info["fields"]:
            doc += "## Fields\n\n"
            for field in type_info["fields"]:
                doc += f"- `{field}`\n"
            doc += "\n"
        
        # Add methods information
        if type_info["methods"]:
            doc += "## Methods\n\n"
            for method in type_info["methods"]:
                doc += f"- `{method}()`\n"
            doc += "\n"
        
        # Add properties information
        if type_info["properties"]:
            doc += "## Properties\n\n"
            for prop in type_info["properties"]:
                doc += f"- `{prop}`\n"
            doc += "\n"
        
        return doc
        
    except Exception as e:
        logger.error(f"Error generating type documentation: {e}")
        return f"Error generating documentation: {e}"


def export_type_schema(type_class: Type, format: str = "json") -> Optional[str]:
    """
    Export type schema in specified format.
    
    Args:
        type_class: Type class to export
        format: Export format ("json" or "yaml")
        
    Returns:
        Exported schema string if successful, None otherwise
    """
    try:
        type_info = get_type_info(type_class)
        type_hints = get_type_hints_info(type_class)
        
        schema = {
            "type_name": type_class.__name__,
            "module": type_class.__module__,
            "info": type_info,
            "type_hints": type_hints,
            "export_timestamp": "2025-01-27"
        }
        
        if format.lower() == "json":
            return json.dumps(schema, indent=2, default=str)
        elif format.lower() == "yaml":
            import yaml
            return yaml.dump(schema, default_flow_style=False)
        else:
            logger.error(f"Unsupported export format: {format}")
            return None
            
    except Exception as e:
        logger.error(f"Error exporting type schema: {e}")
        return None


def validate_type_registry(registry) -> Dict[str, Any]:
    """
    Validate the type registry for consistency and completeness.
    
    Args:
        registry: Type registry to validate
        
    Returns:
        Validation results
    """
    try:
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "total_types": 0,
            "enum_types": 0,
            "other_types": 0,
            "duplicate_names": [],
            "missing_metadata": []
        }
        
        if not registry:
            validation_results["valid"] = False
            validation_results["errors"].append("Registry is None")
            return validation_results
        
        # Count types
        validation_results["total_types"] = len(registry.registered_types)
        validation_results["enum_types"] = len(registry.list_enums())
        validation_results["other_types"] = validation_results["total_types"] - validation_results["enum_types"]
        
        # Check for duplicate names
        seen_names = set()
        for name in registry.registered_types:
            if name in seen_names:
                validation_results["duplicate_names"].append(name)
                validation_results["valid"] = False
            seen_names.add(name)
        
        # Check for missing metadata
        for name in registry.registered_types:
            metadata = registry.get_type_metadata(name)
            if not metadata:
                validation_results["missing_metadata"].append(name)
                validation_results["warnings"].append(f"Missing metadata for type: {name}")
        
        # Generate recommendations
        if validation_results["duplicate_names"]:
            validation_results["errors"].append(f"Duplicate type names found: {validation_results['duplicate_names']}")
        
        if validation_results["missing_metadata"]:
            validation_results["warnings"].append(f"Types missing metadata: {validation_results['missing_metadata']}")
        
        return validation_results
        
    except Exception as e:
        logger.error(f"Error validating type registry: {e}")
        return {"valid": False, "error": str(e)}
