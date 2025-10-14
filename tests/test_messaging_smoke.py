#!/usr/bin/env python3
"""
Messaging System Smoke Tests
=============================

Quick validation tests for concurrent messaging fix.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.smoke
def test_messaging_lock_init():
    """Smoke test: Messaging lock initializes."""
    from src.core.messaging_process_lock import CrossProcessMessagingLock

    lock = CrossProcessMessagingLock(timeout=5)
    assert lock is not None
    assert lock.timeout == 5


@pytest.mark.smoke
def test_messaging_lock_acquire_release():
    """Smoke test: Lock acquire and release works."""
    import tempfile
    from pathlib import Path

    from src.core.messaging_process_lock import CrossProcessMessagingLock

    with tempfile.TemporaryDirectory() as tmpdir:
        lock = CrossProcessMessagingLock(lock_dir=Path(tmpdir), timeout=5)

        # Acquire
        assert lock.acquire()

        # Release
        lock.release()


@pytest.mark.smoke
def test_messaging_lock_context_manager():
    """Smoke test: Lock context manager works."""
    import tempfile
    from pathlib import Path

    from src.core.messaging_process_lock import CrossProcessMessagingLock

    with tempfile.TemporaryDirectory() as tmpdir:
        lock = CrossProcessMessagingLock(lock_dir=Path(tmpdir), timeout=5)

        with lock:
            # Lock held
            pass

        # Lock released automatically


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "smoke"])
