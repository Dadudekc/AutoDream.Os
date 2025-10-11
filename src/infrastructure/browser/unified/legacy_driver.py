"""
DriverManager - Backward compatibility wrapper for UnifiedDriverManager.

DEPRECATED: Use UnifiedDriverManager directly.
V2 Compliance: Adapted from Chat_Mate with V2 patterns
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

import warnings
from typing import Any, Dict, Optional

from .driver_manager import UnifiedDriverManager


class DriverManager:
    """
    Backward compatibility wrapper for UnifiedDriverManager.
    
    DEPRECATED: This class is provided for backward compatibility only.
    Use UnifiedDriverManager directly for new code.
    
    Args:
        driver_options: Dictionary of driver options
    """
    
    def __init__(self, driver_options: Optional[Dict[str, Any]] = None):
        """
        Initialize DriverManager with options.
        
        Args:
            driver_options: Dictionary of driver options
        """
        warnings.warn(
            "DriverManager is deprecated. Use UnifiedDriverManager directly.",
            DeprecationWarning,
            stacklevel=2
        )
        self._unified_manager = UnifiedDriverManager(driver_options or {})
        
    def __getattr__(self, name: str) -> Any:
        """
        Delegate all other attributes to UnifiedDriverManager.
        
        Args:
            name: Attribute name
            
        Returns:
            Attribute value from UnifiedDriverManager
        """
        return getattr(self._unified_manager, name)
        
    def __enter__(self):
        """
        Context manager entry.
        
        Returns:
            Chrome: WebDriver instance
        """
        return self._unified_manager.__enter__()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        
        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        """
        return self._unified_manager.__exit__(exc_type, exc_val, exc_tb)
