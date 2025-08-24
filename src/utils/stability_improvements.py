"""
Stability Improvements and Warning Management Utilities

This module provides utilities to improve code stability and manage warnings
throughout the Agent Cellphone V2 system.
"""

import warnings
import logging
import functools
import sys

# This line was causing circular import - removed
from typing import Any, Callable, Optional, Type, Union
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class StabilityManager:
    """Manages system stability and warning suppression"""
    
    def __init__(self):
        self.suppressed_warnings = set()
        self.warning_counts = {}
        self.stability_metrics = {}
    
    def suppress_warning(self, warning_type: Type[Warning], message: str = ""):
        """Suppress specific warnings with context"""
        if message:
            warnings.filterwarnings("ignore", category=warning_type, message=message)
        else:
            warnings.filterwarnings("ignore", category=warning_type)
        
        self.suppressed_warnings.add((warning_type, message))
        logger.debug(f"Suppressed warning: {warning_type.__name__} - {message}")
    
    def restore_warnings(self):
        """Restore all suppressed warnings"""
        for warning_type, message in self.suppressed_warnings:
            if message:
                warnings.filterwarnings("default", category=warning_type, message=message)
            else:
                warnings.filterwarnings("default", category=warning_type)
        
        self.suppressed_warnings.clear()
        logger.debug("Restored all warnings to default behavior")
    
    def track_warning(self, warning_type: str, context: str = ""):
        """Track warning occurrences for monitoring"""
        key = f"{warning_type}:{context}"
        self.warning_counts[key] = self.warning_counts.get(key, 0) + 1
        
        if self.warning_counts[key] > 10:  # Threshold for stability concern
            logger.warning(f"High warning count for {key}: {self.warning_counts[key]} occurrences")
    
    def get_stability_report(self) -> dict:
        """Generate stability report"""
        return {
            "suppressed_warnings": len(self.suppressed_warnings),
            "warning_counts": self.warning_counts.copy(),
            "stability_metrics": self.stability_metrics.copy()
        }


# Global stability manager instance
stability_manager = StabilityManager()

# Export key functions and classes
__all__ = [
    "StabilityManager",
    "stability_manager", 
    "safe_import",
    "stable_function_call",
    "validate_imports",
    "suppress_warnings_context",
    "setup_stability_improvements",
    "cleanup_stability_improvements"
]


@contextmanager
def suppress_warnings_context(*warning_types: Type[Warning]):
    """Context manager to temporarily suppress warnings"""
    original_filters = warnings.filters[:]
    
    try:
        for warning_type in warning_types:
            warnings.filterwarnings("ignore", category=warning_type)
        yield
    finally:
        warnings.filters[:] = original_filters


def safe_import(module_name: str, fallback: Any = None, 
                warning_message: str = None) -> Any:
    """
    Safely import a module with fallback and proper error handling
    
    Args:
        module_name: Name of the module to import
        fallback: Fallback value if import fails
        warning_message: Custom warning message
    
    Returns:
        Imported module or fallback value
    """
    try:
        module = __import__(module_name)
        logger.debug(f"✅ Successfully imported {module_name}")
        return module
    except ImportError as e:
        if warning_message:
            logger.warning(f"⚠️ {warning_message}: {e}")
        else:
            logger.warning(f"⚠️ Failed to import {module_name}: {e}")
        return fallback
    except Exception as e:
        logger.error(f"❌ Unexpected error importing {module_name}: {e}")
        return fallback


def stable_function_call(func: Callable, *args, 
                        fallback_return: Any = None,
                        max_retries: int = 3,
                        **kwargs) -> Any:
    """
    Execute a function with stability improvements and retry logic
    
    Args:
        func: Function to execute
        fallback_return: Value to return if function fails
        max_retries: Maximum number of retry attempts
        *args, **kwargs: Arguments to pass to function
    
    Returns:
        Function result or fallback value
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            if attempt > 0:
                logger.info(f"✅ Function {func.__name__} succeeded on attempt {attempt + 1}")
            return result
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                logger.warning(f"⚠️ Function {func.__name__} failed (attempt {attempt + 1}): {e}")
                continue
            else:
                logger.error(f"❌ Function {func.__name__} failed after {max_retries} attempts: {e}")
    
    return fallback_return


def validate_imports(required_modules: list, optional_modules: list = None) -> dict:
    """
    Validate module imports and report status
    
    Args:
        required_modules: List of required module names
        optional_modules: List of optional module names
    
    Returns:
        Dictionary with import status for each module
    """
    results = {}
    
    # Check required modules
    for module in required_modules:
        try:
            __import__(module)
            results[module] = {"status": "available", "required": True}
        except ImportError:
            results[module] = {"status": "missing", "required": True}
            logger.error(f"❌ Required module {module} not available")
    
    # Check optional modules
    if optional_modules:
        for module in optional_modules:
            try:
                __import__(module)
                results[module] = {"status": "available", "required": False}
            except ImportError:
                results[module] = {"status": "missing", "required": False}
                logger.info(f"ℹ️ Optional module {module} not available")
    
    return results


def setup_stability_improvements():
    """Initialize stability improvements for the system"""
    # Suppress common deprecation warnings that are known and handled
    stability_manager.suppress_warning(
        DeprecationWarning, 
        ".*unclosed file.*"
    )
    
    # Set up warning filters for better stability
    warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.*")
    
    # Log stability setup
    logger.info("🔧 Stability improvements initialized")
    
    return stability_manager


def cleanup_stability_improvements():
    """Clean up stability improvements and restore default behavior"""
    stability_manager.restore_warnings()
    logger.info("🧹 Stability improvements cleaned up")


# Initialize stability improvements when module is imported
# Note: Don't auto-import to avoid circular import issues
# Use setup_stability_improvements() explicitly when needed
