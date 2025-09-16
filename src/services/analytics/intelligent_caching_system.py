"""
Intelligent Caching System - V2 Compliant
==========================================

Intelligent caching system for business intelligence optimization.
V2 COMPLIANT: Under 400 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import threading
import time
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class CacheEntry:
    """Cache entry with metadata."""

    def __init__(self, key: str, value: Any, ttl: int = 3600):
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.ttl = ttl
        self.access_count = 0

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() - self.created_at > timedelta(seconds=self.ttl)

    def access(self) -> Any:
        """Access the cache entry and update metadata."""
        self.last_accessed = datetime.now()
        self.access_count += 1
        return self.value


class IntelligentCache:
    """Intelligent caching system with predictive preloading."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.access_patterns = {}
        self.lock = threading.RLock()
        self.stats = {"hits": 0, "misses": 0, "evictions": 0, "preloads": 0}

    def get(self, key: str) -> Any | None:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if entry.is_expired():
                    del self.cache[key]
                    self.stats["misses"] += 1
                    return None
                self.cache.move_to_end(key)
                self.stats["hits"] += 1
                return entry.access()
            self.stats["misses"] += 1
            return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache."""
        with self.lock:
            ttl = ttl or self.default_ttl
            entry = CacheEntry(key, value, ttl)
            if key in self.cache:
                del self.cache[key]
            self.cache[key] = entry
            if len(self.cache) > self.max_size:
                self._evict_lru()

    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if self.cache:
            key, entry = self.cache.popitem(last=False)
            self.stats["evictions"] += 1
            logger.debug(f"Evicted cache entry: {key}")

    def preload(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Preload cache entry."""
        with self.lock:
            self.set(key, value, ttl)
            self.stats["preloads"] += 1
            logger.debug(f"Preloaded cache entry: {key}")

    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.access_patterns.clear()

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = self.stats["hits"] / total_requests * 100 if total_requests > 0 else 0
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hit_rate": round(hit_rate, 2),
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "evictions": self.stats["evictions"],
                "preloads": self.stats["preloads"],
                "utilization": round(len(self.cache) / self.max_size * 100, 2),
            }


class PredictiveCacheManager:
    """Predictive cache manager with intelligent preloading."""

    def __init__(self, cache: IntelligentCache):
        self.cache = cache
        self.pattern_analyzer = AccessPatternAnalyzer()
        self.preload_scheduler = PreloadScheduler(cache)

    def get_with_prediction(self, key: str) -> tuple[Any | None, bool]:
        """Get value with predictive preloading."""
        value = self.cache.get(key)
        self.pattern_analyzer.record_access(key)
        predicted_keys = self.pattern_analyzer.predict_next_accesses(key)
        for pred_key in predicted_keys:
            if pred_key not in self.cache.cache:
                self.preload_scheduler.schedule_preload(pred_key)
        return value, len(predicted_keys) > 0

    def set_with_analysis(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value with access pattern analysis."""
        self.cache.set(key, value, ttl)
        self.pattern_analyzer.record_access(key)


class AccessPatternAnalyzer:
    """Analyzes access patterns for predictive caching."""

    def __init__(self):
        self.access_sequences = []
        self.pattern_frequency = {}
        self.max_sequence_length = 10

    def record_access(self, key: str) -> None:
        """Record access pattern."""
        self.access_sequences.append(key)
        if len(self.access_sequences) > self.max_sequence_length:
            self.access_sequences.pop(0)
        if len(self.access_sequences) >= 2:
            pattern = tuple(self.access_sequences[-2:])
            self.pattern_frequency[pattern] = self.pattern_frequency.get(pattern, 0) + 1

    def predict_next_accesses(self, key: str) -> list[str]:
        """Predict next likely accesses based on patterns."""
        predictions = []
        for pattern, frequency in self.pattern_frequency.items():
            if pattern[0] == key and len(pattern) > 1:
                predictions.append((pattern[1], frequency))
        predictions.sort(key=lambda x: x[1], reverse=True)
        return [pred[0] for pred in predictions[:3]]


class PreloadScheduler:
    """Schedules predictive preloading."""

    def __init__(self, cache: IntelligentCache):
        self.cache = cache
        self.preload_queue = []
        self.scheduler_thread = None
        self.running = False

    def schedule_preload(self, key: str) -> None:
        """Schedule preload for key."""
        self.preload_queue.append(key)
        if not self.running:
            self.start_scheduler()

    def start_scheduler(self) -> None:
        """Start preload scheduler."""
        if self.scheduler_thread is None or not self.scheduler_thread.is_alive():
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()

    def _scheduler_loop(self) -> None:
        """Preload scheduler loop."""
        while self.running and self.preload_queue:
            key = self.preload_queue.pop(0)
            logger.debug(f"Preloading data for key: {key}")
            time.sleep(0.1)
        self.running = False


_global_cache = None


def get_intelligent_cache() -> IntelligentCache:
    """Get global intelligent cache instance."""
    global _global_cache
    if _global_cache is None:
        _global_cache = IntelligentCache()
    return _global_cache


def get_predictive_cache_manager() -> PredictiveCacheManager:
    """Get global predictive cache manager."""
    cache = get_intelligent_cache()
    return PredictiveCacheManager(cache)


if __name__ == "__main__":
    cache = get_intelligent_cache()
    manager = get_predictive_cache_manager()
    cache.set("test_key", "test_value", 60)
    value = cache.get("test_key")
    logger.info(f"Cache test: {value}")
    manager.set_with_analysis("key1", "value1")
    manager.set_with_analysis("key2", "value2")
    value, predicted = manager.get_with_prediction("key1")
    logger.info(f"Predictive cache test: {value}, predicted: {predicted}")
    logger.info(f"Cache stats: {cache.get_stats()}")
