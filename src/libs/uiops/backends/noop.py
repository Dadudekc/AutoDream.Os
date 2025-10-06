#!/usr/bin/env python3
"""
No-op Backend - Dry-run UI Operations
===================================

Dry-run implementation for CI/testing without actual screen automation.
Logs operations instead of executing them.

Author: Agent-4 (Captain)
License: MIT
"""

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class NoOpBackend:
    """Dry-run backend for testing and CI environments."""
    
    def __init__(self, 
                 retry_attempts: int = 3,
                 backoff_delay: float = 0.4,
                 throttle_delay: float = 0.15):
        """Initialize no-op backend."""
        self.retry_attempts = retry_attempts
        self.backoff_delay = backoff_delay
        self.throttle_delay = throttle_delay
        self.last_operation = 0.0
        self.operation_count = 0
        
        logger.info("No-op backend initialized for dry-run mode")
    
    def _throttle(self) -> None:
        """Simulate throttling delay."""
        now = time.time()
        elapsed = now - self.last_operation
        if elapsed < self.throttle_delay:
            time.sleep(self.throttle_delay - elapsed)
        self.last_operation = time.time()
    
    def _log_operation(self, operation_name: str, *args, **kwargs) -> bool:
        """Log operation instead of executing it."""
        self._throttle()
        self.operation_count += 1
        
        # Format arguments for logging
        args_str = ", ".join(str(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        logger.info(f"[DRY-RUN] {operation_name}({all_args}) - Operation #{self.operation_count}")
        return True
    
    def click(self, x: int, y: int) -> bool:
        """Log click operation."""
        return self._log_operation("click", x, y)
    
    def hotkey(self, *keys: str) -> bool:
        """Log hotkey operation."""
        return self._log_operation("hotkey", *keys)
    
    def press(self, key: str) -> bool:
        """Log key press operation."""
        return self._log_operation("press", key)
    
    def type(self, text: str) -> bool:
        """Log text typing operation."""
        return self._log_operation("type", f"'{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def paste(self, text: str) -> bool:
        """Log paste operation."""
        return self._log_operation("paste", f"'{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def sleep(self, seconds: float) -> None:
        """Log sleep operation."""
        if seconds > 0:
            self._log_operation("sleep", seconds)
    
    def focus_window(self, title: str) -> bool:
        """Log window focus operation."""
        return self._log_operation("focus_window", title)
    
    def get_clipboard(self) -> str:
        """Simulate getting clipboard content."""
        self._log_operation("get_clipboard")
        return "[DRY-RUN] Clipboard content"
    
    def set_clipboard(self, text: str) -> bool:
        """Log clipboard set operation."""
        return self._log_operation("set_clipboard", f"'{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def is_available(self) -> bool:
        """No-op backend is always available."""
        return True
    
    def get_operation_count(self) -> int:
        """Get total number of operations performed."""
        return self.operation_count
    
    def reset_operation_count(self) -> None:
        """Reset operation counter."""
        self.operation_count = 0
