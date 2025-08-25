"""Cache storage module handling data with TTL."""
from __future__ import annotations

from typing import Any, Dict, Optional
import time


class CacheStorage:
    """In-memory storage for cache entries with TTL support."""

    def __init__(self) -> None:
        self.data: Dict[str, Dict[str, Any]] = {}
        self.access_times: Dict[str, float] = {}

    def get_entry(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve raw cache entry."""
        return self.data.get(key)

    def set_entry(self, key: str, value: Any, ttl: int) -> None:
        """Store a value with a time-to-live."""
        self.data[key] = {"value": value, "expires_at": time.time() + ttl}
        self.access_times[key] = time.time()

    def delete_entry(self, key: str) -> bool:
        """Remove a cache entry."""
        if key in self.data:
            del self.data[key]
            del self.access_times[key]
            return True
        return False

    def is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if a cache entry has expired."""
        return time.time() > entry["expires_at"]

    def clear_expired(self) -> None:
        """Remove all expired cache entries."""
        expired_keys = [key for key, entry in self.data.items() if self.is_expired(entry)]
        for key in expired_keys:
            self.delete_entry(key)
