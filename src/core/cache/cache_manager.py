"""Orchestrator for cache management components."""
from __future__ import annotations

from .cache_storage import CacheStorage
from .cache_eviction import CacheEviction
from .cache_manager_core import CacheManagerCore


class CacheManager(CacheManagerCore):
    """High-level cache manager combining storage and eviction."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600) -> None:
        storage = CacheStorage()
        eviction = CacheEviction(storage)
        super().__init__(storage, eviction, max_size, default_ttl)
