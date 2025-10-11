"""
Unified Browser Infrastructure - Chat_Mate Integration.

V2 Compliance: Public API for Chat_Mate browser automation
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from typing import Optional

from .config import BrowserConfig, config
from .driver_manager import UnifiedDriverManager

# Optional: backward compatibility
try:
    from .legacy_driver import DriverManager

    _LEGACY_AVAILABLE = True
except ImportError:
    DriverManager = None
    _LEGACY_AVAILABLE = False


# Singleton accessor
_manager_instance: UnifiedDriverManager | None = None


def get_driver_manager(driver_options: dict | None = None) -> UnifiedDriverManager:
    """
    Get unified driver manager singleton.

    Args:
        driver_options: Optional driver configuration options

    Returns:
        UnifiedDriverManager: Singleton instance
    """
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = UnifiedDriverManager(driver_options)
    return _manager_instance


def get_driver():
    """
    Get WebDriver instance (convenience method).

    Returns:
        Chrome: WebDriver instance
    """
    return get_driver_manager().get_driver()


__all__ = [
    "UnifiedDriverManager",
    "BrowserConfig",
    "config",
    "get_driver_manager",
    "get_driver",
]

# Add legacy exports if available
if _LEGACY_AVAILABLE:
    __all__.append("DriverManager")
