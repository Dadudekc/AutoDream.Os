"""
Stability Improvements and Warning Management Utilities

This module provides utilities to improve code stability and manage warnings
throughout the Agent Cellphone V2 system.
Now standalone to avoid circular imports and ensure SSOT.
"""

import warnings
import logging
import functools
import sys
import time
from typing import Any, Callable, Optional, Type, Union, List, Dict
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class StabilityManager:
    """Manages system stability and warning suppression
    
    Standalone class to avoid circular imports and ensure SSOT
    """
    
    def __init__(self):
        self.manager_id = "stability_manager"
        self.name = "Stability Manager"
        self.description = "Manages system stability and warning suppression"
        
        self.suppressed_warnings = set()
        self.warning_counts = {}
        self.stability_metrics = {}
        
        # Stability management tracking
        self.stability_operations: List[Dict[str, Any]] = []
        self.warnings_suppressed = 0
        self.warnings_restored = 0
        
        # Performance tracking
        self.start_time = time.time()
        self.operation_count = 0
        self.error_count = 0
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"StabilityManager initialized: {self.manager_id}")

    def suppress_warning(self, warning_type: Type[Warning], reason: str = ""):
        """Suppress a specific warning type"""
        try:
            warnings.filterwarnings("ignore", category=warning_type)
            self.suppressed_warnings.add(warning_type.__name__)
            self.warnings_suppressed += 1
            
            self.logger.info(f"Warning suppressed: {warning_type.__name__} - {reason}")
            
            # Track operation
            self._track_operation("suppress_warning", {
                "warning_type": warning_type.__name__,
                "reason": reason,
                "success": True
            })
            
        except Exception as e:
            self.logger.error(f"Failed to suppress warning {warning_type.__name__}: {e}")
            self.error_count += 1
            
            self._track_operation("suppress_warning", {
                "warning_type": warning_type.__name__,
                "reason": reason,
                "success": False,
                "error": str(e)
            })

    def restore_warning(self, warning_type: Type[Warning]):
        """Restore a previously suppressed warning"""
        try:
            warnings.filterwarnings("default", category=warning_type)
            if warning_type.__name__ in self.suppressed_warnings:
                self.suppressed_warnings.remove(warning_type.__name__)
                self.warnings_restored += 1
                
                self.logger.info(f"Warning restored: {warning_type.__name__}")
                
                self._track_operation("restore_warning", {
                    "warning_type": warning_type.__name__,
                    "success": True
                })
                
        except Exception as e:
            self.logger.error(f"Failed to restore warning {warning_type.__name__}: {e}")
            self.error_count += 1
            
            self._track_operation("restore_warning", {
                "warning_type": warning_type.__name__,
                "success": False,
                "error": str(e)
            })

    def get_stability_report(self) -> Dict[str, Any]:
        """Get comprehensive stability report"""
        uptime = time.time() - self.start_time
        
        return {
            "manager_id": self.manager_id,
            "name": self.name,
            "uptime_seconds": uptime,
            "operation_count": self.operation_count,
            "error_count": self.error_count,
            "warnings_suppressed": self.warnings_suppressed,
            "warnings_restored": self.warnings_restored,
            "suppressed_warnings": list(self.suppressed_warnings),
            "success_rate": self._calculate_success_rate(),
            "timestamp": time.time()
        }

    def _track_operation(self, operation_type: str, details: Dict[str, Any]):
        """Track an operation for monitoring"""
        operation = {
            "type": operation_type,
            "timestamp": time.time(),
            "details": details
        }
        
        self.stability_operations.append(operation)
        self.operation_count += 1
        
        # Keep only last 100 operations
        if len(self.stability_operations) > 100:
            self.stability_operations = self.stability_operations[-100:]

    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if not self.stability_operations:
                return 0.0
            
            successful_ops = sum(1 for op in self.stability_operations 
                               if op.get("details", {}).get("success", False))
            return successful_ops / len(self.stability_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0

    def cleanup(self):
        """Cleanup resources and restore all warnings"""
        try:
            # Restore all suppressed warnings
            for warning_name in list(self.suppressed_warnings):
                try:
                    # Find the warning class and restore it
                    for warning_type in [DeprecationWarning, UserWarning, RuntimeWarning, 
                                       FutureWarning, ImportWarning, PendingDeprecationWarning]:
                        if warning_type.__name__ == warning_name:
                            warnings.filterwarnings("default", category=warning_type)
                            break
                except Exception as e:
                    self.logger.warning(f"Could not restore warning {warning_name}: {e}")
            
            self.suppressed_warnings.clear()
            self.logger.info("StabilityManager cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


# Global stability manager instance - now safe to instantiate
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


def validate_imports(required_modules: List[str]) -> Dict[str, bool]:
    """
    Validate that required modules can be imported
    
    Args:
        required_modules: List of module names to validate
    
    Returns:
        Dictionary mapping module names to import success status
    """
    results = {}
    
    for module_name in required_modules:
        try:
            __import__(module_name)
            results[module_name] = True
            logger.debug(f"✅ {module_name} import validated")
        except ImportError:
            results[module_name] = False
            logger.warning(f"⚠️ {module_name} import failed")
        except Exception as e:
            results[module_name] = False
            logger.error(f"❌ {module_name} import error: {e}")
    
    return results


def setup_stability_improvements():
    """Setup stability improvements system"""
    try:
        # Initialize stability manager
        stability_manager.__init__()
        
        # Configure basic warning suppression
        stability_manager.suppress_warning(
            DeprecationWarning, 
            "Suppressing deprecation warnings for stability"
        )
        
        logger.info("✅ Stability improvements setup completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to setup stability improvements: {e}")
        return False


def cleanup_stability_improvements():
    """Cleanup stability improvements system"""
    try:
        if stability_manager:
            stability_manager.cleanup()
        
        logger.info("✅ Stability improvements cleanup completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to cleanup stability improvements: {e}")
        return False
