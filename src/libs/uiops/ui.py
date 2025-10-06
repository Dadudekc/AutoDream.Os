#!/usr/bin/env python3
"""
UI Ops Facade - Unified Interface for UI Operations
==================================================

Public API for UI automation operations. Abstracts PyAutoGUI for testability
and reliability while preserving agent messaging and Discord Commander functionality.

Author: Agent-4 (Captain)
License: MIT
"""

import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Backend selection via environment variable
_UI_BACKEND = os.getenv("UI_BACKEND", "pyauto").lower()
_UI_RETRY_ATTEMPTS = int(os.getenv("UI_RETRY_ATTEMPTS", "3"))
_UI_BACKOFF = float(os.getenv("UI_BACKOFF", "0.4"))
_UI_THROTTLE = float(os.getenv("UI_THROTTLE", "0.15"))

# Global backend instance
_backend: Optional[Any] = None


def _get_backend():
    """Get or create the appropriate backend instance."""
    global _backend
    
    if _backend is None:
        if _UI_BACKEND == "noop":
            from .backends.noop import NoOpBackend
            _backend = NoOpBackend(
                retry_attempts=_UI_RETRY_ATTEMPTS,
                backoff_delay=_UI_BACKOFF,
                throttle_delay=_UI_THROTTLE
            )
            logger.info("Using NoOp backend for dry-run mode")
        elif _UI_BACKEND == "pyauto":
            from .backends.pyauto import PyAutoGUIBackend
            _backend = PyAutoGUIBackend(
                retry_attempts=_UI_RETRY_ATTEMPTS,
                backoff_delay=_UI_BACKOFF,
                throttle_delay=_UI_THROTTLE
            )
            logger.info("Using PyAutoGUI backend for production mode")
        else:
            raise ValueError(f"Unknown UI_BACKEND: {_UI_BACKEND}. Use 'pyauto' or 'noop'")
    
    return _backend


class UI:
    """
    Unified UI operations interface.
    
    Provides consistent API for UI automation with backend abstraction.
    Used by agent messaging system and Discord Commander for screen automation.
    """
    
    @staticmethod
    def click(x: int, y: int) -> bool:
        """
        Click at specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().click(x, y)
        except Exception as e:
            logger.error(f"UI.click({x}, {y}) failed: {e}")
            return False
    
    @staticmethod
    def hotkey(*keys: str) -> bool:
        """
        Send hotkey combination.
        
        Args:
            *keys: Key names (e.g., 'ctrl', 'c', 'v')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().hotkey(*keys)
        except Exception as e:
            logger.error(f"UI.hotkey({', '.join(keys)}) failed: {e}")
            return False
    
    @staticmethod
    def press(key: str) -> bool:
        """
        Press single key.
        
        Args:
            key: Key name (e.g., 'enter', 'tab', 'escape')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().press(key)
        except Exception as e:
            logger.error(f"UI.press('{key}') failed: {e}")
            return False
    
    @staticmethod
    def type(text: str) -> bool:
        """
        Type text character by character.
        
        Args:
            text: Text to type
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().type(text)
        except Exception as e:
            logger.error(f"UI.type({len(text)} chars) failed: {e}")
            return False
    
    @staticmethod
    def paste(text: str) -> bool:
        """
        Paste text from clipboard (faster than typing).
        
        Args:
            text: Text to paste
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().paste(text)
        except Exception as e:
            logger.error(f"UI.paste({len(text)} chars) failed: {e}")
            return False
    
    @staticmethod
    def sleep(seconds: float = 0.0) -> None:
        """
        Sleep for specified duration.
        
        Args:
            seconds: Duration in seconds
        """
        _get_backend().sleep(seconds)
    
    @staticmethod
    def focus_window(title: str) -> bool:
        """
        Focus window by title.
        
        Args:
            title: Window title to focus
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().focus_window(title)
        except Exception as e:
            logger.error(f"UI.focus_window('{title}') failed: {e}")
            return False
    
    @staticmethod
    def is_available() -> bool:
        """
        Check if UI operations are available.
        
        Returns:
            True if available, False otherwise
        """
        try:
            return _get_backend().is_available()
        except Exception:
            return False
    
    @staticmethod
    def get_clipboard() -> str:
        """
        Get clipboard content.
        
        Returns:
            Clipboard content as string
        """
        try:
            return _get_backend().get_clipboard()
        except Exception as e:
            logger.error(f"UI.get_clipboard() failed: {e}")
            return ""
    
    @staticmethod
    def set_clipboard(text: str) -> bool:
        """
        Set clipboard content.
        
        Args:
            text: Text to set in clipboard
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return _get_backend().set_clipboard(text)
        except Exception as e:
            logger.error(f"UI.set_clipboard({len(text)} chars) failed: {e}")
            return False
    
    @staticmethod
    def get_backend_info() -> dict:
        """
        Get information about current backend.
        
        Returns:
            Dictionary with backend information
        """
        backend = _get_backend()
        info = {
            "backend": _UI_BACKEND,
            "retry_attempts": _UI_RETRY_ATTEMPTS,
            "backoff_delay": _UI_BACKOFF,
            "throttle_delay": _UI_THROTTLE,
            "available": backend.is_available()
        }
        
        # Add backend-specific info
        if hasattr(backend, 'get_operation_count'):
            info["operation_count"] = backend.get_operation_count()
        
        return info


# Convenience functions for backward compatibility
def click(x: int, y: int) -> bool:
    """Convenience function for UI.click()."""
    return UI.click(x, y)


def hotkey(*keys: str) -> bool:
    """Convenience function for UI.hotkey()."""
    return UI.hotkey(*keys)


def press(key: str) -> bool:
    """Convenience function for UI.press()."""
    return UI.press(key)


def type_text(text: str) -> bool:
    """Convenience function for UI.type()."""
    return UI.type(text)


def paste_text(text: str) -> bool:
    """Convenience function for UI.paste()."""
    return UI.paste(text)


def sleep(seconds: float = 0.0) -> None:
    """Convenience function for UI.sleep()."""
    UI.sleep(seconds)


def focus_window(title: str) -> bool:
    """Convenience function for UI.focus_window()."""
    return UI.focus_window(title)
