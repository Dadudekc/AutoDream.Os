#!/usr/bin/env python3
"""
Cross-Process Messaging Lock System
====================================

Prevents race conditions when multiple agents/processes send messages simultaneously.
Uses file-based locking for cross-process coordination.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13 (Race Condition Fix)
"""

import logging
import os
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Windows compatibility check
WINDOWS = os.name == "nt"

if WINDOWS:
    try:
        import msvcrt  # Windows file locking

        LOCK_AVAILABLE = True
        fcntl = None  # Not available on Windows
    except ImportError:
        LOCK_AVAILABLE = False
        msvcrt = None
        fcntl = None
        logger.warning("⚠️ Windows file locking not available")
else:
    try:
        import fcntl  # POSIX file locking (Linux/Mac)

        LOCK_AVAILABLE = True
        msvcrt = None  # Not available on POSIX
    except ImportError:
        LOCK_AVAILABLE = False
        fcntl = None
        msvcrt = None
        logger.warning("⚠️ POSIX file locking not available")


class CrossProcessMessagingLock:
    """
    Cross-process lock for coordinating PyAutoGUI messaging operations.

    Ensures only ONE process can send messages at a time, preventing:
    - Mouse cursor conflicts
    - Wrong agent targeting
    - Interrupted typing/paste operations
    - Messages going to wrong inboxes
    """

    def __init__(self, lock_dir: Path | None = None, timeout: int = 30):
        """
        Initialize cross-process lock.

        Args:
            lock_dir: Directory for lock file (default: runtime/locks)
            timeout: Maximum time to wait for lock acquisition (seconds)
        """
        self.lock_dir = lock_dir or Path("runtime/locks")
        self.lock_dir.mkdir(parents=True, exist_ok=True)

        self.lock_file_path = self.lock_dir / "messaging_pyautogui.lock"
        self.timeout = timeout
        self.lock_file = None
        self._lock = threading.Lock()  # Thread-level lock within process

    def acquire(self, retry_delay: float = 0.1, use_exponential_backoff: bool = True) -> bool:
        """
        Acquire cross-process lock with exponential backoff retry logic.

        Args:
            retry_delay: Initial delay between retry attempts (seconds)
            use_exponential_backoff: Use exponential backoff strategy

        Returns:
            True if lock acquired successfully, False if timeout
        """
        start_time = time.time()
        current_delay = retry_delay
        max_delay = 2.0  # Cap delay at 2 seconds
        attempt = 0

        while time.time() - start_time < self.timeout:
            try:
                attempt += 1

                # Thread-level lock first (within process)
                if not self._lock.acquire(blocking=False):
                    time.sleep(current_delay)
                    if use_exponential_backoff:
                        current_delay = min(current_delay * 1.5, max_delay)
                    continue

                # Create lock file
                self.lock_file = open(self.lock_file_path, "w")

                # Attempt file lock (cross-process)
                if WINDOWS and LOCK_AVAILABLE:
                    # Windows: Use msvcrt
                    try:
                        msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                        logger.debug(
                            f"✅ Cross-process lock acquired (Windows) after {attempt} attempts"
                        )
                        return True
                    except OSError:
                        self.lock_file.close()
                        self.lock_file = None
                        self._lock.release()
                        time.sleep(current_delay)
                        if use_exponential_backoff:
                            current_delay = min(current_delay * 1.5, max_delay)
                        continue

                elif not WINDOWS and LOCK_AVAILABLE:
                    # POSIX: Use fcntl
                    try:
                        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        logger.debug(
                            f"✅ Cross-process lock acquired (POSIX) after {attempt} attempts"
                        )
                        return True
                    except BlockingIOError:
                        self.lock_file.close()
                        self.lock_file = None
                        self._lock.release()
                        time.sleep(current_delay)
                        if use_exponential_backoff:
                            current_delay = min(current_delay * 1.5, max_delay)
                        continue
                else:
                    # Fallback: No file locking, use thread lock only
                    logger.warning("⚠️ Using thread-level lock only (file locking unavailable)")
                    return True

            except Exception as e:
                logger.error(f"❌ Lock acquisition error: {e}")
                if self.lock_file:
                    self.lock_file.close()
                    self.lock_file = None
                if self._lock.locked():
                    self._lock.release()
                time.sleep(current_delay)
                if use_exponential_backoff:
                    current_delay = min(current_delay * 1.5, max_delay)

        logger.error(f"❌ Lock acquisition timeout after {self.timeout}s ({attempt} attempts)")
        return False

    def release(self):
        """Release cross-process lock."""
        try:
            if self.lock_file:
                # Release file lock
                if WINDOWS and LOCK_AVAILABLE:
                    try:
                        msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                    except:
                        pass
                elif not WINDOWS and LOCK_AVAILABLE:
                    try:
                        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                    except:
                        pass

                self.lock_file.close()
                self.lock_file = None

            # Release thread lock
            if self._lock.locked():
                self._lock.release()

            logger.debug("✅ Cross-process lock released")

        except Exception as e:
            logger.error(f"❌ Lock release error: {e}")

    def __enter__(self):
        """Context manager entry."""
        if not self.acquire():
            raise TimeoutError(f"Failed to acquire messaging lock within {self.timeout}s")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()


# Global lock instance
_global_lock = None


def get_messaging_lock() -> CrossProcessMessagingLock:
    """Get or create global cross-process messaging lock."""
    global _global_lock
    if _global_lock is None:
        _global_lock = CrossProcessMessagingLock()
    return _global_lock


# Convenience decorator
def with_messaging_lock(func):
    """
    Decorator to ensure function executes with cross-process lock.

    Usage:
        @with_messaging_lock
        def send_message_safely(agent_id, message):
            # PyAutoGUI operations here
            pass
    """

    def wrapper(*args, **kwargs):
        lock = get_messaging_lock()
        with lock:
            return func(*args, **kwargs)

    return wrapper
