#!/usr/bin/env python3
"""
Cache Models
============

Data models for caching system.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class CacheStrategy(Enum):
    """Cache strategy types."""

    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"


@dataclass
class CacheEntry:
    """Cache entry data structure."""

    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int
    ttl: int | None = None
    strategy: CacheStrategy = CacheStrategy.TTL
