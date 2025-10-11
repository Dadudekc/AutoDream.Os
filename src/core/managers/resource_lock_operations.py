"""
Resource Lock Operations - Helper Module
========================================

Handles lock operations for CoreResourceManager.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any

from .contracts import ManagerContext, ManagerResult


class LockOperations:
    """Handles lock operations for resource manager."""

    def __init__(self, lock_file: str = "runtime/resource_locks.json"):
        """Initialize lock operations handler."""
        self.operations_count = 0
        self._locks: dict[str, threading.Lock] = {}
        self._lock_file = lock_file

    def handle_operation(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Handle lock operations."""
        operation = payload.get("lock_operation", "")
        lock_id = payload.get("lock_id", "")

        try:
            if operation == "acquire":
                return self._acquire_lock(lock_id)
            elif operation == "release":
                return self._release_lock(lock_id)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown lock operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _acquire_lock(self, lock_id: str) -> ManagerResult:
        """Acquire a lock."""
        if lock_id not in self._locks:
            self._locks[lock_id] = threading.Lock()

        acquired = self._locks[lock_id].acquire(blocking=False)
        self.operations_count += 1
        return ManagerResult(
            success=acquired,
            data={"lock_id": lock_id, "acquired": acquired},
            metrics={},
        )

    def _release_lock(self, lock_id: str) -> ManagerResult:
        """Release a lock."""
        if lock_id in self._locks:
            self._locks[lock_id].release()
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"lock_id": lock_id, "released": True},
                metrics={},
            )
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Lock not found: {lock_id}",
            )

    def load_locks(self) -> None:
        """Load locks from file."""
        try:
            if os.path.exists(self._lock_file):
                with open(self._lock_file, encoding="utf-8") as f:
                    lock_data = json.load(f)
                    # Note: We can't restore actual Lock objects, just track them
                    self._locks = {k: threading.Lock() for k in lock_data.get("locks", [])}
        except Exception:
            pass  # Ignore lock loading errors

    def save_locks(self) -> None:
        """Save locks to file."""
        try:
            lock_data = {"locks": list(self._locks.keys())}
            with open(self._lock_file, "w", encoding="utf-8") as f:
                json.dump(lock_data, f, indent=2)
        except Exception:
            pass  # Ignore lock saving errors

    def clear_locks(self) -> None:
        """Clear all locks."""
        self._locks.clear()

    def get_lock_count(self) -> int:
        """Get active lock count."""
        return len(self._locks)
