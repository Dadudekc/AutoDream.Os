#!/usr/bin/env python3
"""
Caching Strategies Implementation
Contract: V2-COMPLIANCE-005 - Performance Optimization Implementation
Agent: Agent-6 (Performance Optimization Manager)
Description: Comprehensive caching strategies for performance optimization
"""

import time
import json
import logging
import threading
import weakref
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import pickle
import functools
from collections import OrderedDict, defaultdict
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Individual cache entry"""
    key: str
    value: Any
    timestamp: float
    access_count: int
    size_bytes: int
    ttl: Optional[float] = None
    last_accessed: float = 0.0

@dataclass
class CacheStats:
    """Cache performance statistics"""
    total_entries: int
    total_size_bytes: int
    hit_count: int
    miss_count: int
    hit_rate: float
    eviction_count: int
    memory_usage_percent: float
    timestamp: str

class LRUCache:
    """Least Recently Used (LRU) Cache Implementation"""
    
    def __init__(self, max_size: int = 100, max_memory_mb: Optional[float] = None):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024 if max_memory_mb else None
        self.cache = OrderedDict()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        self.lock = threading.RLock()
        
        logger.info(f"LRU Cache initialized: max_size={max_size}, max_memory={max_memory_mb}MB")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.stats['hits'] += 1
                return value
            else:
                self.stats['misses'] += 1
                return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache"""
        with self.lock:
            # Remove if key already exists
            if key in self.cache:
                self.cache.pop(key)
            
            # Check if we need to evict
            while len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
                self.stats['evictions'] += 1
            
            self.cache[key] = value
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            logger.info("LRU Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_entries': len(self.cache),
            'max_size': self.max_size,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'hit_rate': hit_rate
        }

class TTLCache:
    """Time-To-Live (TTL) Cache Implementation"""
    
    def __init__(self, default_ttl: float = 300):  # 5 minutes default
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'expirations': 0
        }
        self.lock = threading.RLock()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        
        logger.info(f"TTL Cache initialized: default_ttl={default_ttl}s")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache, checking TTL"""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                
                # Check if expired
                if entry.ttl and time.time() > entry.timestamp + entry.ttl:
                    del self.cache[key]
                    self.stats['expirations'] += 1
                    return None
                
                # Update access info
                entry.last_accessed = time.time()
                entry.access_count += 1
                self.stats['hits'] += 1
                return entry.value
            else:
                self.stats['misses'] += 1
                return None
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Put value in cache with optional TTL"""
        if ttl is None:
            ttl = self.default_ttl
        
        with self.lock:
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=time.time(),
                access_count=1,
                size_bytes=len(pickle.dumps(value)),
                ttl=ttl,
                last_accessed=time.time()
            )
            self.cache[key] = entry
    
    def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            time.sleep(60)  # Check every minute
            self._cleanup_expired()
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = []
        
        with self.lock:
            for key, entry in self.cache.items():
                if entry.ttl and current_time > entry.timestamp + entry.ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
                self.stats['expirations'] += 1
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            logger.info("TTL Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_entries': len(self.cache),
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'expirations': self.stats['expirations'],
            'hit_rate': hit_rate
        }

class FunctionCache:
    """Function result caching with multiple strategies"""
    
    def __init__(self, strategy: str = 'lru', **kwargs):
        self.strategy = strategy
        
        if strategy == 'lru':
            self.cache = LRUCache(**kwargs)
        elif strategy == 'ttl':
            self.cache = TTLCache(**kwargs)
        else:
            raise ValueError(f"Unknown caching strategy: {strategy}")
        
        self.function_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'calls': 0,
            'cache_hits': 0,
            'cache_misses': 0
        })
        
        logger.info(f"Function Cache initialized with {strategy} strategy")
    
    def cached(self, ttl: Optional[float] = None, key_func: Optional[Callable] = None):
        """Decorator for caching function results"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    # Default key generation
                    key_parts = [func.__name__]
                    key_parts.extend([str(arg) for arg in args])
                    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
                    cache_key = hashlib.md5('|'.join(key_parts).encode()).hexdigest()
                
                # Try to get from cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    self.function_stats[func.__name__]['cache_hits'] += 1
                    return cached_result
                
                # Cache miss - execute function
                self.function_stats[func.__name__]['cache_misses'] += 1
                result = func(*args, **kwargs)
                
                # Store in cache
                if self.strategy == 'ttl':
                    self.cache.put(cache_key, result, ttl=ttl)
                else:
                    self.cache.put(cache_key, result)
                
                return result
            
            return wrapper
        return decorator
    
    def get_function_stats(self, function_name: str) -> Dict[str, Any]:
        """Get statistics for a specific function"""
        if function_name not in self.function_stats:
            return {'error': 'Function not found'}
        
        stats = self.function_stats[function_name]
        total_calls = stats['calls'] + stats['cache_hits'] + stats['cache_misses']
        cache_hit_rate = (stats['cache_hits'] / total_calls * 100) if total_calls > 0 else 0
        
        return {
            'function_name': function_name,
            'total_calls': total_calls,
            'cache_hits': stats['cache_hits'],
            'cache_misses': stats['cache_misses'],
            'cache_hit_rate': cache_hit_rate
        }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall cache statistics"""
        cache_stats = self.cache.get_stats()
        
        return {
            'strategy': self.strategy,
            'cache_stats': cache_stats,
            'function_stats': dict(self.function_stats)
        }

class MemoryAwareCache:
    """Memory-aware cache that monitors system memory usage"""
    
    def __init__(self, max_memory_percent: float = 80.0, cleanup_threshold: float = 70.0):
        self.max_memory_percent = max_memory_percent
        self.cleanup_threshold = cleanup_threshold
        self.cache: Dict[str, CacheEntry] = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'memory_cleanups': 0
        }
        self.lock = threading.RLock()
        
        # Start memory monitoring thread
        self.monitor_thread = threading.Thread(target=self._memory_monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Memory-Aware Cache initialized: max_memory={max_memory_percent}%, cleanup_threshold={cleanup_threshold}%")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                entry.last_accessed = time.time()
                entry.access_count += 1
                self.stats['hits'] += 1
                return entry.value
            else:
                self.stats['misses'] += 1
                return None
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Put value in cache"""
        with self.lock:
            # Check memory usage before adding
            if self._should_evict():
                self._evict_entries()
            
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=time.time(),
                access_count=1,
                size_bytes=len(pickle.dumps(value)),
                ttl=ttl,
                last_accessed=time.time()
            )
            self.cache[key] = entry
    
    def _should_evict(self) -> bool:
        """Check if we should evict entries"""
        memory_percent = psutil.virtual_memory().percent
        return memory_percent > self.cleanup_threshold
    
    def _evict_entries(self):
        """Evict least recently used entries"""
        if not self.cache:
            return
        
        # Sort by last accessed time and access count
        sorted_entries = sorted(
            self.cache.items(),
            key=lambda x: (x[1].last_accessed, -x[1].access_count)
        )
        
        # Remove 20% of entries
        evict_count = max(1, len(sorted_entries) // 5)
        evicted_keys = [entry[0] for entry in sorted_entries[:evict_count]]
        
        for key in evicted_keys:
            del self.cache[key]
            self.stats['evictions'] += 1
        
        self.stats['memory_cleanups'] += 1
        logger.info(f"Evicted {evict_count} entries due to memory pressure")
    
    def _memory_monitor_loop(self):
        """Background memory monitoring loop"""
        while True:
            time.sleep(30)  # Check every 30 seconds
            memory_percent = psutil.virtual_memory().percent
            
            if memory_percent > self.max_memory_percent:
                with self.lock:
                    self._evict_entries()
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            logger.info("Memory-Aware Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        current_memory = psutil.virtual_memory().percent
        
        return {
            'total_entries': len(self.cache),
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'memory_cleanups': self.stats['memory_cleanups'],
            'hit_rate': hit_rate,
            'current_memory_percent': current_memory,
            'max_memory_percent': self.max_memory_percent
        }

class CachingStrategies:
    """
    Main caching strategies orchestrator
    
    Features:
    - Multiple caching strategies (LRU, TTL, Memory-aware)
    - Function result caching
    - Performance monitoring
    - V2 compliance optimization
    """
    
    def __init__(self, output_dir: str = "caching_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.caches: Dict[str, Any] = {}
        self.function_caches: Dict[str, FunctionCache] = {}
        self.performance_metrics: List[Dict[str, Any]] = []
        
        logger.info("Caching Strategies system initialized")
    
    def create_cache(self, name: str, strategy: str = 'lru', **kwargs) -> Any:
        """Create a new cache with specified strategy"""
        if strategy == 'lru':
            cache = LRUCache(**kwargs)
        elif strategy == 'ttl':
            cache = TTLCache(**kwargs)
        elif strategy == 'memory_aware':
            cache = MemoryAwareCache(**kwargs)
        else:
            raise ValueError(f"Unknown caching strategy: {strategy}")
        
        self.caches[name] = cache
        logger.info(f"Created {strategy} cache: {name}")
        return cache
    
    def create_function_cache(self, name: str, strategy: str = 'lru', **kwargs) -> FunctionCache:
        """Create a function cache with specified strategy"""
        function_cache = FunctionCache(strategy=strategy, **kwargs)
        self.function_caches[name] = function_cache
        logger.info(f"Created function cache: {name} with {strategy} strategy")
        return function_cache
    
    def benchmark_cache_performance(self, cache_name: str, 
                                  test_data: List[Tuple[str, Any]], 
                                  iterations: int = 100) -> Dict[str, Any]:
        """Benchmark cache performance"""
        if cache_name not in self.caches:
            return {'error': f'Cache {cache_name} not found'}
        
        cache = self.caches[cache_name]
        
        # Warm up cache
        for key, value in test_data:
            cache.put(key, value)
        
        # Benchmark reads
        start_time = time.time()
        for _ in range(iterations):
            for key, _ in test_data:
                cache.get(key)
        read_time = time.time() - start_time
        
        # Benchmark writes
        start_time = time.time()
        for _ in range(iterations):
            for key, value in test_data:
                cache.put(key, value)
        write_time = time.time() - start_time
        
        # Get cache stats
        cache_stats = cache.get_stats()
        
        benchmark_result = {
            'cache_name': cache_name,
            'iterations': iterations,
            'read_time': read_time,
            'write_time': write_time,
            'read_ops_per_second': (iterations * len(test_data)) / read_time if read_time > 0 else 0,
            'write_ops_per_second': (iterations * len(test_data)) / write_time if write_time > 0 else 0,
            'cache_stats': cache_stats,
            'timestamp': datetime.now().isoformat()
        }
        
        self.performance_metrics.append(benchmark_result)
        logger.info(f"Cache performance benchmark completed for {cache_name}")
        
        return benchmark_result
    
    def generate_caching_report(self) -> str:
        """Generate comprehensive caching report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"caching_report_{timestamp}.json"
        
        report_data = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'caching_system_version': '1.0.0',
                'total_caches': len(self.caches),
                'total_function_caches': len(self.function_caches)
            },
            'caches': {name: cache.get_stats() for name, cache in self.caches.items()},
            'function_caches': {name: cache.get_overall_stats() for name, cache in self.function_caches.items()},
            'performance_metrics': self.performance_metrics
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Caching report generated: {output_file}")
        return str(output_file)
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get overall caching system summary"""
        total_entries = sum(cache.get_stats().get('total_entries', 0) for cache in self.caches.values())
        total_hits = sum(cache.get_stats().get('hits', 0) for cache in self.caches.values())
        total_misses = sum(cache.get_stats().get('misses', 0) for cache in self.caches.values())
        
        overall_hit_rate = (total_hits / (total_hits + total_misses) * 100) if (total_hits + total_misses) > 0 else 0
        
        return {
            'total_caches': len(self.caches),
            'total_function_caches': len(self.function_caches),
            'total_entries': total_entries,
            'total_hits': total_hits,
            'total_misses': total_misses,
            'overall_hit_rate': overall_hit_rate,
            'performance_benchmarks': len(self.performance_metrics)
        }


if __name__ == "__main__":
    # Example usage
    caching_system = CachingStrategies()
    
    # Create different types of caches
    lru_cache = caching_system.create_cache("test_lru", "lru", max_size=50)
    ttl_cache = caching_system.create_cache("test_ttl", "ttl", default_ttl=60)
    memory_cache = caching_system.create_cache("test_memory", "memory_aware", max_memory_percent=75)
    
    # Create function cache
    function_cache = caching_system.create_function_cache("math_functions", "lru", max_size=100)
    
    # Test data for benchmarking
    test_data = [(f"key_{i}", f"value_{i}") for i in range(100)]
    
    # Benchmark cache performance
    lru_benchmark = caching_system.benchmark_cache_performance("test_lru", test_data, iterations=50)
    ttl_benchmark = caching_system.benchmark_cache_performance("test_ttl", test_data, iterations=50)
    
    # Generate report
    report_file = caching_system.generate_caching_report()
    print(f"Caching report generated: {report_file}")
    
    # Show system summary
    summary = caching_system.get_system_summary()
    print(f"Caching system summary: {summary}")
