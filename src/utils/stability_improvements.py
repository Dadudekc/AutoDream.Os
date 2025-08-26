"""
Stability Improvements and Warning Management Utilities

This module provides utilities to improve code stability and manage warnings
throughout the Agent Cellphone V2 system.
Now inherits from BaseManager for unified functionality.
"""

import warnings
import logging
import functools
import sys
import time

# This line was causing circular import - removed
from typing import Any, Callable, Optional, Type, Union, List, Dict
from contextlib import contextmanager

# Import BaseManager with relative path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
from base_manager import BaseManager

logger = logging.getLogger(__name__)


class StabilityManager(BaseManager):
    """Manages system stability and warning suppression
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self):
        super().__init__(
            manager_id="stability_manager",
            name="Stability Manager",
            description="Manages system stability and warning suppression"
        )
        
        self.suppressed_warnings = set()
        self.warning_counts = {}
        self.stability_metrics = {}
        
        # Stability management tracking
        self.stability_operations: List[Dict[str, Any]] = []
        self.warnings_suppressed = 0
        self.warnings_restored = 0
        self.stability_checks = 0
        self.failed_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Stability Manager initialized")
    
    def suppress_warning(self, warning_type: Type[Warning], message: str = ""):
        """Suppress specific warnings with context"""
        start_time = time.time()
        try:
            if message:
                warnings.filterwarnings("ignore", category=warning_type, message=message)
            else:
                warnings.filterwarnings("ignore", category=warning_type)
            
            self.suppressed_warnings.add((warning_type, message))
            
            # Record successful operation
            self.warnings_suppressed += 1
            self.record_operation("suppress_warning", True, time.time() - start_time)
            
            logger.debug(f"Suppressed warning: {warning_type.__name__} - {message}")
            
        except Exception as e:
            logger.error(f"Failed to suppress warning: {e}")
            self.record_operation("suppress_warning", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "suppress_warning",
                "warning_type": str(warning_type),
                "message": message,
                "error": str(e),
                "timestamp": time.time()
            })
    
    def restore_warnings(self):
        """Restore all suppressed warnings"""
        start_time = time.time()
        try:
            for warning_type, message in self.suppressed_warnings:
                if message:
                    warnings.filterwarnings("default", category=warning_type, message=message)
                else:
                    warnings.filterwarnings("default", category=warning_type)
            
            self.suppressed_warnings.clear()
            
            # Record successful operation
            self.warnings_restored += 1
            self.record_operation("restore_warnings", True, time.time() - start_time)
            
            logger.debug("Restored all warnings to default behavior")
            
        except Exception as e:
            logger.error(f"Failed to restore warnings: {e}")
            self.record_operation("restore_warnings", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "restore_warnings",
                "error": str(e),
                "timestamp": time.time()
            })
    
    def track_warning(self, warning_type: str, context: str = ""):
        """Track warning occurrences for monitoring"""
        start_time = time.time()
        try:
            key = f"{warning_type}:{context}"
            self.warning_counts[key] = self.warning_counts.get(key, 0) + 1
            
            if self.warning_counts[key] > 10:  # Threshold for stability concern
                logger.warning(f"High warning count for {key}: {self.warning_counts[key]} occurrences")
            
            # Record successful operation
            self.stability_checks += 1
            self.record_operation("track_warning", True, time.time() - start_time)
            
        except Exception as e:
            logger.error(f"Failed to track warning: {e}")
            self.record_operation("track_warning", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "track_warning",
                "warning_type": warning_type,
                "context": context,
                "error": str(e),
                "timestamp": time.time()
            })
    
    def get_stability_report(self) -> dict:
        """Generate stability report"""
        start_time = time.time()
        try:
            report = {
                "suppressed_warnings": len(self.suppressed_warnings),
                "warning_counts": self.warning_counts.copy(),
                "stability_metrics": self.stability_metrics.copy()
            }
            
            # Record successful operation
            self.record_operation("get_stability_report", True, time.time() - start_time)
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to get stability report: {e}")
            self.record_operation("get_stability_report", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "get_stability_report",
                "error": str(e),
                "timestamp": time.time()
            })
            return {}

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize stability management system"""
        try:
            self.logger.info("Starting Stability Manager...")
            
            # Clear tracking data
            self.stability_operations.clear()
            self.warnings_suppressed = 0
            self.warnings_restored = 0
            self.stability_checks = 0
            self.failed_operations.clear()
            
            self.logger.info("Stability Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Stability Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup stability management system"""
        try:
            self.logger.info("Stopping Stability Manager...")
            
            # Save stability management data
            self._save_stability_management_data()
            
            self.logger.info("Stability Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Stability Manager: {e}")
            return False
    
    def _on_heartbeat(self) -> bool:
        """Stability management health check"""
        try:
            # Check stability management health
            health_status = self._check_stability_management_health()
            
            # Update metrics
            self.metrics.update(
                operations_count=len(self.stability_operations),
                success_rate=self._calculate_success_rate(),
                average_response_time=self._calculate_average_response_time(),
                health_status=health_status
            )
            
            return health_status == "healthy"
            
        except Exception as e:
            self.logger.error(f"Stability Manager heartbeat failed: {e}")
            return False
    
    def _on_initialize_resources(self) -> bool:
        """Initialize stability management resources"""
        try:
            # Initialize stability tracking
            self.stability_operations = []
            self.warnings_suppressed = 0
            self.warnings_restored = 0
            self.stability_checks = 0
            self.failed_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Stability Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self) -> bool:
        """Cleanup stability management resources"""
        try:
            # Save stability management data
            self._save_stability_management_data()
            
            # Clear tracking data
            self.stability_operations.clear()
            self.warnings_suppressed = 0
            self.warnings_restored = 0
            self.stability_checks = 0
            self.failed_operations.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Stability Manager resources: {e}")
            return False
    
    def _on_recovery_attempt(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info("Attempting Stability Manager recovery...")
            
            # Reinitialize stability tracking
            self.stability_operations = []
            self.warnings_suppressed = 0
            self.warnings_restored = 0
            self.stability_checks = 0
            self.failed_operations = []
            
            self.logger.info("Stability Manager recovery successful")
            return True
                
        except Exception as e:
            self.logger.error(f"Stability Manager recovery attempt failed: {e}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_stability_management_data(self):
        """Save stability management data for persistence"""
        try:
            data = {
                "warnings_suppressed": self.warnings_suppressed,
                "warnings_restored": self.warnings_restored,
                "stability_checks": self.stability_checks,
                "failed_operations": self.failed_operations,
                "timestamp": time.time()
            }
            
            # Save to file or database as needed
            # For now, just log the data
            self.logger.info(f"Stability management data: {data}")
            
        except Exception as e:
            self.logger.error(f"Failed to save stability management data: {e}")
    
    def _check_stability_management_health(self) -> str:
        """Check stability management system health"""
        try:
            # Check if we have recent operations
            if len(self.stability_operations) > 0:
                return "healthy"
            else:
                return "idle"
                
        except Exception as e:
            self.logger.error(f"Stability management health check failed: {e}")
            return "unhealthy"
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if len(self.stability_operations) == 0:
                return 1.0
            
            successful_ops = sum(1 for op in self.stability_operations if op.get("success", False))
            return successful_ops / len(self.stability_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average operation response time"""
        try:
            if len(self.stability_operations) == 0:
                return 0.0
            
            total_time = sum(op.get("duration", 0.0) for op in self.stability_operations)
            return total_time / len(self.stability_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate average response time: {e}")
            return 0.0


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
