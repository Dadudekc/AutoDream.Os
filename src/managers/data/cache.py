"""Caching utilities for data and analytics records."""

from typing import Any, Dict, Optional


class CacheManager:
    """Simple cache manager handling data and analytics caches."""

    def __init__(self, data_records: Dict[str, Any], max_cache_size: int = 1000) -> None:
        self.data_records = data_records
        self.max_cache_size = max_cache_size
        self.data_cache: Dict[str, Any] = {}
        self.analytics_cache: Dict[str, Any] = {}

    # Data cache operations -------------------------------------------------
    def add_data(self, data_id: str, data: Any) -> None:
        """Add a data item to the cache respecting the size limit."""
        if len(self.data_cache) >= self.max_cache_size and self.data_records:
            oldest_id = min(
                self.data_records.keys(),
                key=lambda x: self.data_records[x].last_accessed,
            )
            self.data_cache.pop(oldest_id, None)
        self.data_cache[data_id] = data

    def get_data(self, data_id: str) -> Optional[Any]:
        """Retrieve a data item from cache if present."""
        return self.data_cache.get(data_id)

    def data_size(self) -> int:
        """Return number of items stored in data cache."""
        return len(self.data_cache)

    # Analytics cache operations -------------------------------------------
    def add_analytics(self, data_id: str, analytics: Any) -> None:
        self.analytics_cache[data_id] = analytics

    def get_analytics(self, data_id: str) -> Optional[Any]:
        return self.analytics_cache.get(data_id)

    def analytics_size(self) -> int:
        return len(self.analytics_cache)

    # General utilities ----------------------------------------------------
    def clear(self) -> None:
        self.data_cache.clear()
        self.analytics_cache.clear()
