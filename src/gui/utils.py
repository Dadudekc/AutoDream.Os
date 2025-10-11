"""
GUI System Utilities
===================

Shared utilities and fallback implementations for the GUI system.
Provides graceful degradation when V2 core modules are unavailable.

V2 Compliance: ≤200 lines, single responsibility.

Author: Agent-7 - Repository Cloning Specialist (V2 consolidation)
License: MIT
"""

import logging


# Fallback implementations for V2 integration
def get_coordinate_loader_fallback():
    """Fallback coordinate loader when V2 core unavailable."""
    return None


def get_unified_config_fallback():
    """Fallback unified config when V2 core unavailable."""
    return type('MockConfig', (), {'get_env': lambda x, y=None: y})()


def get_logger_fallback(name):
    """Fallback logger when V2 core unavailable."""
    return logging.getLogger(name)


# Import V2 integration with fallback
try:
    from ..core.coordinate_loader import get_coordinate_loader
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e} - using fallbacks")
    get_coordinate_loader = get_coordinate_loader_fallback
    get_unified_config = get_unified_config_fallback
    get_logger = get_logger_fallback


__all__ = [
    'get_coordinate_loader',
    'get_unified_config',
    'get_logger',
]

