"""
Validation Utilities - Consolidated Validation Functions
========================================================

Centralized validation functions extracted from 73+ duplicate implementations
across the codebase. Part of DUP-005 consolidation mission.

Author: Agent-7 (DUP-005 Mission)
Date: 2025-10-16
Points: Part of 1,500-2,000 pts mission
"""

from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
import re


def validate_import_syntax(import_statement: str) -> bool:
    """
    Validate Python import statement syntax.
    
    Consolidates 4 duplicate implementations from:
    - unified_import_system.py
    - import_mixins_utils.py
    - import_utilities.py
    
    Args:
        import_statement: Python import statement to validate
        
    Returns:
        True if syntax is valid, False otherwise
    """
    if not import_statement or not isinstance(import_statement, str):
        return False
        
    import_statement = import_statement.strip()
    
    # Basic import patterns
    patterns = [
        r'^import\s+[\w\.]+(\s+as\s+\w+)?$',
        r'^from\s+[\w\.]+\s+import\s+[\w\s,\*\(\)]+$',
    ]
    
    return any(re.match(pattern, import_statement) for pattern in patterns)


def validate_import_pattern(pattern: str) -> bool:
    """
    Validate import pattern string.
    
    Consolidates 3 duplicate implementations from:
    - unified_import_system.py
    - import_mixins_registry.py
    - import_registry.py
    
    Args:
        pattern: Import pattern to validate
        
    Returns:
        True if pattern is valid, False otherwise
    """
    if not pattern or not isinstance(pattern, str):
        return False
        
    # Allow wildcards, dots, and alphanumeric characters
    return bool(re.match(r'^[\w\.\*]+$', pattern))


def validate_file_path(file_path: str) -> Dict[str, Any]:
    """
    Validate file path and return validation result.
    
    Consolidates 3 duplicate implementations from:
    - file_utils.py
    - unified_file_utils.py
    - validation_operations.py
    
    Args:
        file_path: Path to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'exists': False,
        'is_file': False,
        'is_readable': False,
        'path': file_path,
        'errors': []
    }
    
    if not file_path:
        result['errors'].append('File path is empty')
        return result
        
    try:
        path = Path(file_path)
        result['exists'] = path.exists()
        result['is_file'] = path.is_file()
        
        if result['is_file']:
            # Check if readable
            try:
                path.read_text()
                result['is_readable'] = True
                result['valid'] = True
            except (PermissionError, OSError) as e:
                result['errors'].append(f'File not readable: {str(e)}')
        elif result['exists']:
            result['errors'].append('Path exists but is not a file')
        else:
            result['errors'].append('File does not exist')
            
    except Exception as e:
        result['errors'].append(f'Path validation error: {str(e)}')
        
    return result


def validate_config(config: Dict[str, Any], required_fields: List[str] = None) -> bool:
    """
    Validate configuration dictionary.
    
    Consolidates 3 duplicate implementations from:
    - config_core.py
    - contracts.py
    - core_configuration_manager.py
    
    Args:
        config: Configuration dictionary to validate
        required_fields: Optional list of required field names
        
    Returns:
        True if config is valid, False otherwise
    """
    if not isinstance(config, dict):
        return False
        
    if not config:
        return False
        
    if required_fields:
        return all(field in config for field in required_fields)
        
    return True


def validate_session(session_id: str, sessions: Dict[str, Any] = None) -> bool:
    """
    Validate session ID and optionally check if it exists.
    
    Consolidates 3 duplicate implementations from:
    - base_session_manager.py
    - rate_limited_session_manager.py
    - session.py
    
    Args:
        session_id: Session identifier to validate
        sessions: Optional dictionary of active sessions
        
    Returns:
        True if session is valid, False otherwise
    """
    if not session_id or not isinstance(session_id, str):
        return False
        
    if sessions is not None:
        return session_id in sessions
        
    # Basic validation - non-empty string
    return len(session_id.strip()) > 0


def validate_coordinates(coordinates: List[int], screen_width: int = 3840, screen_height: int = 2160) -> bool:
    """
    Validate screen coordinates.
    
    Consolidates 2 duplicate implementations from:
    - messaging_pyautogui.py
    - coordinate_handler.py
    
    Args:
        coordinates: List of [x, y] coordinates
        screen_width: Maximum screen width (default: 3840)
        screen_height: Maximum screen height (default: 2160)
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    if not coordinates or not isinstance(coordinates, (list, tuple)):
        return False
        
    if len(coordinates) != 2:
        return False
        
    x, y = coordinates
    
    if not isinstance(x, int) or not isinstance(y, int):
        return False
        
    return (-screen_width <= x <= screen_width and 
            -screen_height <= y <= screen_height)


def validate_forecast_accuracy(forecast: Dict[str, Any], actual: Dict[str, Any]) -> float:
    """
    Validate forecast accuracy against actual results.
    
    Consolidates 2 duplicate implementations from:
    - analytics_engine.py
    - forecast_generator.py
    
    Args:
        forecast: Forecast data dictionary
        actual: Actual results dictionary
        
    Returns:
        Accuracy score (0.0 to 1.0)
    """
    if not forecast or not actual:
        return 0.0
        
    try:
        forecast_value = float(forecast.get('value', 0))
        actual_value = float(actual.get('value', 0))
        
        if actual_value == 0:
            return 1.0 if forecast_value == 0 else 0.0
            
        error = abs(forecast_value - actual_value) / abs(actual_value)
        accuracy = max(0.0, 1.0 - error)
        
        return accuracy
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def validate_hasattr(obj: Any, attr: str) -> bool:
    """
    Safely validate if object has attribute.
    
    From unified_validation_orchestrator.py
    
    Args:
        obj: Object to check
        attr: Attribute name
        
    Returns:
        True if object has attribute, False otherwise
    """
    return hasattr(obj, attr)


def validate_type(obj: Any, expected_type: type) -> bool:
    """
    Validate object type.
    
    From unified_validation_orchestrator.py
    
    Args:
        obj: Object to validate
        expected_type: Expected type
        
    Returns:
        True if object matches type, False otherwise
    """
    return isinstance(obj, expected_type)


def validate_not_none(obj: Any) -> bool:
    """
    Validate object is not None.
    
    From unified_validation_orchestrator.py
    
    Args:
        obj: Object to validate
        
    Returns:
        True if object is not None, False otherwise
    """
    return obj is not None


def validate_not_empty(obj: Any) -> bool:
    """
    Validate object is not empty.
    
    From unified_validation_orchestrator.py
    
    Args:
        obj: Object to validate (string, list, dict, etc.)
        
    Returns:
        True if object is not empty, False otherwise
    """
    if obj is None:
        return False
    if isinstance(obj, (str, list, dict, tuple)):
        return len(obj) > 0
    return True


def validate_range(value: float, min_val: float, max_val: float) -> bool:
    """
    Validate value is within range.
    
    From unified_validation_orchestrator.py
    
    Args:
        value: Value to validate
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
        
    Returns:
        True if value is in range, False otherwise
    """
    try:
        return min_val <= float(value) <= max_val
    except (ValueError, TypeError):
        return False


def validate_regex(value: str, pattern: str) -> bool:
    """
    Validate string against regex pattern.
    
    From unified_validation_orchestrator.py
    
    Args:
        value: String to validate
        pattern: Regex pattern
        
    Returns:
        True if string matches pattern, False otherwise
    """
    if not isinstance(value, str):
        return False
    try:
        return bool(re.match(pattern, value))
    except re.error:
        return False


def validate_custom(obj: Any, validator_func: Callable[[Any], bool]) -> bool:
    """
    Validate object using custom validator function.
    
    From unified_validation_orchestrator.py
    
    Args:
        obj: Object to validate
        validator_func: Custom validation function
        
    Returns:
        True if validation passes, False otherwise
    """
    try:
        return validator_func(obj)
    except Exception:
        return False


# Export all validation functions
__all__ = [
    'validate_import_syntax',
    'validate_import_pattern',
    'validate_file_path',
    'validate_config',
    'validate_session',
    'validate_coordinates',
    'validate_forecast_accuracy',
    'validate_hasattr',
    'validate_type',
    'validate_not_none',
    'validate_not_empty',
    'validate_range',
    'validate_regex',
    'validate_custom',
]
