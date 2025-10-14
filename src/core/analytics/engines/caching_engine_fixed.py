#!/usr/bin/env python3
"""
Caching Engine - Memory-Safe Version
====================================

Simple caching with LRU eviction to prevent memory leaks.

FIXES:
- Added max_size limit (prevents unbounded growth)
- LRU eviction (removes least recently used)
- Memory leak prevention

Author: Agent-5 (original), Agent-8 (memory-safe fix)
License: MIT
"""

import logging
from collections import OrderedDict
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class CachingEngine:
    """Memory-safe caching engine with LRU eviction."""

    def __init__(self, config=None, max_size: int = 1000):
        """
        Initialize caching engine with memory limits.

        Args:
            config: Configuration dictionary
            max_size: Maximum cache entries (default: 1000)
        """
        self.config = config or {}
        self.logger = logger
        self.max_size = max_size
        self.cache = OrderedDict()  # LRU support
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "evictions": 0}

    def get(self, key: str) -> Any | None:
        """Get value from cache (LRU: moves to end)."""
        try:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                self.stats["hits"] += 1
                self.logger.debug(f"Cache hit: {key}")
                return self.cache[key]
            else:
                self.stats["misses"] += 1
                self.logger.debug(f"Cache miss: {key}")
                return None
        except Exception as e:
            self.logger.error(f"Error getting from cache: {e}")
            return None

    def set(self, key: str, value: Any) -> bool:
        """Set value in cache with LRU eviction."""
        try:
            # If key exists, move to end
            if key in self.cache:
                self.cache.move_to_end(key)

            self.cache[key] = value
            self.stats["sets"] += 1

            # Evict if over max_size (LRU: remove from front)
            if len(self.cache) > self.max_size:
                evicted_key = next(iter(self.cache))
                del self.cache[evicted_key]
                self.stats["evictions"] += 1
                self.logger.debug(f"Cache eviction (LRU): {evicted_key}")

            self.logger.debug(f"Cache set: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            if key in self.cache:
                del self.cache[key]
                self.logger.debug(f"Cache deleted: {key}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting from cache: {e}")
            return False

    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            self.cache.clear()
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics including evictions."""
        try:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

            return {
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "sets": self.stats["sets"],
                "evictions": self.stats["evictions"],
                "hit_rate": hit_rate,
                "cache_size": len(self.cache),
                "max_size": self.max_size,
                "memory_safe": True,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting cache stats: {e}")
            return {}

    def get_status(self) -> dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "utilization": f"{(len(self.cache) / self.max_size) * 100:.1f}%",
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "evictions": self.stats["evictions"],
            "memory_safe": True,
            "timestamp": datetime.now().isoformat(),
        }
