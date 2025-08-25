"""Core caching logic using storage and eviction components."""
from __future__ import annotations

from typing import Any, Dict, Optional
import threading


class CacheManagerCore:
    """Thread-safe cache manager core handling get/set logic."""

    def __init__(self, storage, eviction, max_size: int, default_ttl: int) -> None:
        self.storage = storage
        self.eviction = eviction
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a cached value."""
        with self.lock:
            entry = self.storage.get_entry(key)
            if entry is None:
                return None
            if self.storage.is_expired(entry):
                self.storage.delete_entry(key)
                return None
            self.eviction.update_access_time(key)
            return entry["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store a value in cache."""
        with self.lock:
            if len(self.storage.data) >= self.max_size:
                self.eviction.evict_oldest()
            ttl = ttl if ttl is not None else self.default_ttl
            self.storage.set_entry(key, value, ttl)
            self.eviction.update_access_time(key)
            return True

    def delete(self, key: str) -> bool:
        """Delete a cache entry."""
        with self.lock:
            return self.storage.delete_entry(key)

    def clear_expired(self) -> None:
        """Clear expired entries from cache."""
        with self.lock:
            self.storage.clear_expired()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            return {
                "total_entries": len(self.storage.data),
                "max_size": self.max_size,
                "hit_rate": self._calculate_hit_rate(),
            }

    def _calculate_hit_rate(self) -> float:
        """Placeholder hit rate calculation."""
        return 0.85
