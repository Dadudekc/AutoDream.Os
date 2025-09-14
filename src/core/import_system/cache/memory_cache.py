"""
Memory Import Cache
==================

In-memory caching for import operations.
"""

import time
import threading
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Cache entry with timestamp and TTL."""
    value: Any
    timestamp: float
    ttl: int
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return time.time() - self.timestamp > self.ttl


class MemoryImportCache:
    """Thread-safe in-memory cache for import operations."""
    
    def __init__(self, default_ttl: int = 3600):
        """Initialize memory cache with default TTL."""
        self.cache: Dict[str, CacheEntry] = {}
        self.lock = threading.RLock()
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            entry = self.cache.get(key)
            if entry is None:
                return None
            
            if entry.is_expired():
                del self.cache[key]
                return None
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        with self.lock:
            ttl = ttl or self.default_ttl
            self.cache[key] = CacheEntry(
                value=value,
                timestamp=time.time(),
                ttl=ttl
            )
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        with self.lock:
            self.cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count."""
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self.cache[key]
            return len(expired_keys)

