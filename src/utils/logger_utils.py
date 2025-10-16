"""
Logger Utilities - Wrapper for Unified Logging System
======================================================

Provides backward compatibility wrapper for the unified logging system.
Redirects to src.core.unified_logging_system for actual implementation.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 4 (Utilities & Structure)
Date: 2025-10-16
Points: 150 pts
V2 Compliant: ≤400 lines, backward compatibility facade

Architecture:
- Facade pattern for unified_logging_system
- Maintains backward compatibility
- No duplicate logic
- Simple re-export + utility wrapper

Usage:
    from src.utils.logger_utils import create_logger, get_logger
    
    logger = create_logger("my_module")
    logger = get_logger("my_module")
"""

from typing import Optional
import logging

# Import from unified logging system
try:
    from ..core.unified_logging_system import (
        UnifiedLogger,
        setup_logger,
        get_logger as _get_logger
    )
    UNIFIED_LOGGING_AVAILABLE = True
except ImportError:
    # Fallback if unified logging not available
    UNIFIED_LOGGING_AVAILABLE = False
    UnifiedLogger = None  # type: ignore
    setup_logger = None  # type: ignore
    _get_logger = None  # type: ignore


# Re-export for backward compatibility
__all__ = ['UnifiedLogger', 'setup_logger', 'get_logger', 'create_logger']


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance (backward compatible).
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    if UNIFIED_LOGGING_AVAILABLE and _get_logger:
        return _get_logger(name)
    
    # Fallback to standard logging
    return logging.getLogger(name)


def create_logger(
    name: str, 
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Create logger instance (backward compatible).
    
    Args:
        name: Logger name
        level: Log level (default: INFO)
        log_file: Optional log file path
        
    Returns:
        Logger instance
    """
    if UNIFIED_LOGGING_AVAILABLE and setup_logger:
        return setup_logger(name, level)
    
    # Fallback to standard logging
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Add console handler if no handlers exist
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

