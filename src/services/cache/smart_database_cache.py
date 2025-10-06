#!/usr/bin/env python3
"""
Smart Database Cache - V2 Compliance
=====================================

Intelligent caching system that optimizes database operations,
reduces query load, and improves system performance.

V2 Compliance: ≤400 lines, focused caching system
Author: Agent-6 (Quality Assurance Specialist)
"""

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class CacheEntry:
    """Cache entry data model."""

    key: str
    value: Any
    timestamp: datetime
    ttl: int  # Time to live in seconds
    access_count: int = 0
    last_accessed: datetime = None

    def __post_init__(self):
        if self.last_accessed is None:
            self.last_accessed = self.timestamp

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() > self.timestamp + timedelta(seconds=self.ttl)

    def touch(self) -> None:
        """Update access information."""
        self.access_count += 1
        self.last_accessed = datetime.now()


class SmartDatabaseCache:
    """
    Smart database caching system.

    Provides intelligent caching with TTL, LRU eviction, and performance optimization.
    """

    def __init__(self, cache_dir: str = "cache", max_size: int = 1000, default_ttl: int = 3600):
        """Initialize smart database cache."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.logger = logging.getLogger(f"{__name__}.SmartDatabaseCache")

        # In-memory cache for fast access
        self.memory_cache: dict[str, CacheEntry] = {}
        self.access_order: List[str] = []  # LRU tracking

        # Performance metrics
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _generate_key(self, query: str, params: dict[str, Any] = None) -> str:
        """Generate cache key from query and parameters."""
        key_data = {"query": query}
        if params:
            key_data["params"] = sorted(params.items())

        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _evict_lru(self) -> None:
        """Evict least recently used entries."""
        if len(self.memory_cache) < self.max_size:
            return

        # Remove oldest accessed entries
        entries_to_remove = len(self.memory_cache) - self.max_size + 1

        # Sort by last accessed time
        sorted_keys = sorted(
            self.memory_cache.keys(), key=lambda k: self.memory_cache[k].last_accessed
        )

        for key in sorted_keys[:entries_to_remove]:
            self._remove_entry(key)
            self.evictions += 1

    def _remove_entry(self, key: str) -> None:
        """Remove cache entry."""
        if key in self.memory_cache:
            del self.memory_cache[key]
            if key in self.access_order:
                self.access_order.remove(key)

    def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        expired_keys = [key for key, entry in self.memory_cache.items() if entry.is_expired()]

        for key in expired_keys:
            self._remove_entry(key)

    def get(self, query: str, params: dict[str, Any] = None) -> Any | None:
        """Get value from cache."""
        key = self._generate_key(query, params)

        if key in self.memory_cache:
            entry = self.memory_cache[key]

            if entry.is_expired():
                self._remove_entry(key)
                self.misses += 1
                return None

            # Update access information
            entry.touch()

            # Update LRU order
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)

            self.hits += 1
            return entry.value

        self.misses += 1
        return None

    def set(self, query: str, value: Any, params: dict[str, Any] = None, ttl: int = None) -> None:
        """Set value in cache."""
        key = self._generate_key(query, params)
        ttl = ttl or self.default_ttl

        # Cleanup expired entries
        self._cleanup_expired()

        # Evict LRU if needed
        self._evict_lru()

        # Create cache entry
        entry = CacheEntry(key=key, value=value, timestamp=datetime.now(), ttl=ttl)

        self.memory_cache[key] = entry

        # Update LRU order
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def invalidate(self, pattern: str = None) -> int:
        """Invalidate cache entries matching pattern."""
        if pattern is None:
            # Clear all cache
            count = len(self.memory_cache)
            self.memory_cache.clear()
            self.access_order.clear()
            return count

        # Remove entries matching pattern
        keys_to_remove = [key for key in self.memory_cache.keys() if pattern in key]

        for key in keys_to_remove:
            self._remove_entry(key)

        return len(keys_to_remove)

    def get_stats(self) -> dict[str, Any]:
        """Get cache performance statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "evictions": self.evictions,
            "cache_size": len(self.memory_cache),
            "max_size": self.max_size,
            "memory_usage": len(self.memory_cache) / self.max_size * 100,
        }

    def optimize(self) -> dict[str, Any]:
        """Optimize cache performance."""
        # Cleanup expired entries
        self._cleanup_expired()

        # Get optimization stats
        stats = self.get_stats()

        # Log optimization results
        self.logger.info(
            f"Cache optimized: {stats['cache_size']} entries, {stats['hit_rate']:.1f}% hit rate"
        )

        return stats

    def persist_to_disk(self, filename: str = "cache_backup.json") -> bool:
        """Persist cache to disk."""
        try:
            cache_file = self.cache_dir / filename

            # Prepare serializable data
            cache_data = {
                "entries": {},
                "stats": self.get_stats(),
                "timestamp": datetime.now().isoformat(),
            }

            for key, entry in self.memory_cache.items():
                if not entry.is_expired():
                    cache_data["entries"][key] = {
                        "value": entry.value,
                        "timestamp": entry.timestamp.isoformat(),
                        "ttl": entry.ttl,
                        "access_count": entry.access_count,
                        "last_accessed": entry.last_accessed.isoformat(),
                    }

            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Failed to persist cache: {e}")
            return False


def create_smart_cache(cache_dir: str = "cache") -> SmartDatabaseCache:
    """Create smart database cache instance."""
    return SmartDatabaseCache(cache_dir)


if __name__ == "__main__":
    # Example usage
    cache = create_smart_cache()

    # Test caching
    cache.set("SELECT * FROM users", {"users": [{"id": 1, "name": "test"}]})
    result = cache.get("SELECT * FROM users")

    print(f"Cache result: {result}")
    print(f"Cache stats: {cache.get_stats()}")


