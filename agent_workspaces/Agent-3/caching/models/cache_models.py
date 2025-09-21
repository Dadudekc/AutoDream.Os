#!/usr/bin/env python3
"""
Cache Models
============

Data models for caching system.
"""

from datetime import datetime
from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum


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
    ttl: Optional[int] = None
    strategy: CacheStrategy = CacheStrategy.TTL


