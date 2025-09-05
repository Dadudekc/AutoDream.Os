#!/usr/bin/env python3
"""
File Cache - V2 Compliance Module
================================

Caching utilities for file operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import time
from typing import Any, Optional, Dict
from threading import Lock


class FileCache:
    """Simple in-memory cache for file operations."""

    def __init__(self, ttl_seconds: int = 300):
        """Initialize cache."""
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry['timestamp'] < self.ttl_seconds:
                    return entry['value']
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        with self._lock:
            self._cache[key] = {
                'value': value,
                'timestamp': time.time()
            }

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Get cache size."""
        with self._lock:
            return len(self._cache)
