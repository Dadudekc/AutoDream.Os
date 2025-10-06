#!/usr/bin/env python3
"""
PyAutoGUI Backend - Production UI Operations
==========================================

Real PyAutoGUI implementation for production agent messaging and Discord Commander.
This is the PRIMARY backend that agents use for actual screen automation.

Author: Agent-4 (Captain)
License: MIT
"""

import logging
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Lazy import to prevent hard dependency at import time
try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError as e:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False
    logger.error(f"PyAutoGUI not available: {e}")


class PyAutoGUIBackend:
    """Production PyAutoGUI backend for real UI automation."""
    
    def __init__(self, 
                 retry_attempts: int = 3,
                 backoff_delay: float = 0.4,
                 throttle_delay: float = 0.15):
        """Initialize PyAutoGUI backend with retry and throttling."""
        self.retry_attempts = retry_attempts
        self.backoff_delay = backoff_delay
        self.throttle_delay = throttle_delay
        self.last_operation = 0.0
        
        if not PYAUTOGUI_AVAILABLE:
            raise RuntimeError("PyAutoGUI not available - cannot use PyAutoGUI backend")
        
        # Configure PyAutoGUI for reliability
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        logger.info("PyAutoGUI backend initialized for production use")
    
    def _throttle(self) -> None:
        """Ensure minimum delay between operations."""
        now = time.time()
        elapsed = now - self.last_operation
        if elapsed < self.throttle_delay:
            time.sleep(self.throttle_delay - elapsed)
        self.last_operation = time.time()
    
    def _with_retry(self, operation_name: str, operation_func, *args, **kwargs) -> Any:
        """Execute operation with retry logic."""
        last_error = None
        
        for attempt in range(self.retry_attempts):
            try:
                self._throttle()
                result = operation_func(*args, **kwargs)
                if attempt > 0:
                    logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"{operation_name} attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.backoff_delay * (attempt + 1))
        
        logger.error(f"{operation_name} failed after {self.retry_attempts} attempts: {last_error}")
        raise last_error
    
    def click(self, x: int, y: int) -> bool:
        """Click at coordinates with retry logic."""
        def _click():
            pyautogui.click(x, y)
            return True
        
        return self._with_retry(f"click({x}, {y})", _click)
    
    def hotkey(self, *keys: str) -> bool:
        """Send hotkey combination with retry logic."""
        def _hotkey():
            pyautogui.hotkey(*keys)
            return True
        
        return self._with_retry(f"hotkey({', '.join(keys)})", _hotkey)
    
    def press(self, key: str) -> bool:
        """Press single key with retry logic."""
        def _press():
            pyautogui.press(key)
            return True
        
        return self._with_retry(f"press('{key}')", _press)
    
    def type(self, text: str) -> bool:
        """Type text character by character with retry logic."""
        def _type():
            pyautogui.typewrite(text)
            return True
        
        return self._with_retry(f"type({len(text)} chars)", _type)
    
    def paste(self, text: str) -> bool:
        """Paste text from clipboard with fallback to typing."""
        def _paste():
            try:
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                return True
            except Exception as e:
                logger.warning(f"Paste failed, falling back to type: {e}")
                return self.type(text)
        
        return self._with_retry(f"paste({len(text)} chars)", _paste)
    
    def get_clipboard(self) -> str:
        """Get clipboard content."""
        def _get_clipboard():
            return pyperclip.paste()
        
        return self._with_retry("get_clipboard", _get_clipboard)
    
    def set_clipboard(self, text: str) -> bool:
        """Set clipboard content."""
        def _set_clipboard():
            pyperclip.copy(text)
            return True
        
        return self._with_retry(f"set_clipboard({len(text)} chars)", _set_clipboard)
    
    def sleep(self, seconds: float) -> None:
        """Sleep for specified duration."""
        if seconds > 0:
            time.sleep(seconds)
    
    def focus_window(self, title: str) -> bool:
        """Focus window by title with retry logic."""
        def _focus():
            # Use alt+tab to cycle through windows (simplified approach)
            # In a real implementation, this would use platform-specific window management
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)  # Give window time to focus
            return True
        
        return self._with_retry(f"focus_window('{title}')", _focus)
    
    def is_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        return PYAUTOGUI_AVAILABLE
