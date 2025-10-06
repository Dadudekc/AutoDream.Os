"""
UI Ops - Unified UI Operations Library
=====================================

Abstraction layer for UI automation operations. Provides consistent interface
for PyAutoGUI operations with backend selection and retry logic.

Features:
- Backend abstraction (PyAutoGUI for production, NoOp for testing)
- Retry logic and error handling
- Throttling and rate limiting
- Environment-based configuration
- Preserves agent messaging and Discord Commander functionality

Usage:
    from src.libs.uiops import UI
    
    # Click at coordinates
    UI.click(100, 200)
    
    # Send hotkey
    UI.hotkey('ctrl', 'c')
    
    # Type text
    UI.type("Hello, Agent!")
    
    # Paste text (faster)
    UI.paste("Long message content")
    
    # Focus window for agent messaging
    UI.focus_window("Cursor")

Environment Variables:
    UI_BACKEND: Backend to use ('pyauto' for production, 'noop' for testing)
    UI_RETRY_ATTEMPTS: Number of retry attempts (default: 3)
    UI_BACKOFF: Backoff delay in seconds (default: 0.4)
    UI_THROTTLE: Throttle delay in seconds (default: 0.15)

Author: Agent-4 (Captain)
License: MIT
"""

from .ui import (
    UI,
    click,
    hotkey,
    press,
    type_text,
    paste_text,
    sleep,
    focus_window,
)

__all__ = [
    "UI",
    "click",
    "hotkey", 
    "press",
    "type_text",
    "paste_text",
    "sleep",
    "focus_window",
]

