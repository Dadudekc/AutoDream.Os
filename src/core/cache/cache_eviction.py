"""Cache eviction policies."""
from __future__ import annotations

import time


class CacheEviction:
    """Implements simple LRU eviction policy."""

    def __init__(self, storage) -> None:
        self.storage = storage

    def update_access_time(self, key: str) -> None:
        """Update last access time for a key."""
        self.storage.access_times[key] = time.time()

    def evict_oldest(self) -> None:
        """Evict the least recently used item."""
        if not self.storage.access_times:
            return
        oldest_key = min(self.storage.access_times, key=self.storage.access_times.get)
        self.storage.delete_entry(oldest_key)
