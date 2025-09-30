#!/usr/bin/env python3
"""
Optimization Utils - Discord Commander optimization utilities
=========================================================

Optimization utilities extracted from optimization.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """Performance optimization utilities for Discord Commander."""

    def __init__(self):
        """Initialize performance optimizer."""
        self.optimization_enabled = True
        self.cache_enabled = True
        self.rate_limiting_enabled = True

    def enable_optimizations(self, cache: bool = True, rate_limiting: bool = True):
        """Enable performance optimizations."""
        self.cache_enabled = cache
        self.rate_limiting_enabled = rate_limiting
        self.optimization_enabled = True
        logger.info("Performance optimizations enabled")

    def disable_optimizations(self):
        """Disable performance optimizations."""
        self.optimization_enabled = False
        self.cache_enabled = False
        self.rate_limiting_enabled = False
        logger.info("Performance optimizations disabled")

    def measure_execution_time(self, func: Callable) -> Callable:
        """Decorator to measure function execution time."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
                raise

        return wrapper

    async def measure_async_execution_time(self, func: Callable) -> Callable:
        """Decorator to measure async function execution time."""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
                raise

        return wrapper


class RateLimiter:
    """Rate limiter for Discord Commander operations."""

    def __init__(self, max_requests: int = 100, time_window: float = 60.0):
        """Initialize rate limiter."""
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()

    async def is_allowed(self) -> bool:
        """Check if request is allowed under rate limit."""
        async with self._lock:
            current_time = time.time()

            # Remove old requests outside time window
            self.requests = [
                req_time for req_time in self.requests if current_time - req_time < self.time_window
            ]

            # Check if we're under the limit
            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True

            return False

    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        if not await self.is_allowed():
            # Calculate wait time
            oldest_request = min(self.requests)
            wait_time = self.time_window - (time.time() - oldest_request)

            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)

            # Try again
            await self.wait_if_needed()


class MessageCache:
    """Cache for frequently accessed messages and data."""

    def __init__(self, max_size: int = 1000, ttl: float = 300.0):
        """Initialize message cache."""
        self.max_size = max_size
        self.ttl = ttl
        self.cache: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        async with self._lock:
            if key in self.cache:
                entry = self.cache[key]
                if time.time() - entry["timestamp"] < self.ttl:
                    return entry["value"]
                else:
                    # Expired, remove it
                    del self.cache[key]
            return None

    async def set(self, key: str, value: Any):
        """Set value in cache."""
        async with self._lock:
            # Remove oldest entries if cache is full
            while len(self.cache) >= self.max_size:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
                del self.cache[oldest_key]

            self.cache[key] = {"value": value, "timestamp": time.time()}

    async def clear(self):
        """Clear all cache entries."""
        async with self._lock:
            self.cache.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        async with self._lock:
            current_time = time.time()
            active_entries = sum(
                1 for entry in self.cache.values() if current_time - entry["timestamp"] < self.ttl
            )

            return {
                "total_entries": len(self.cache),
                "active_entries": active_entries,
                "max_size": self.max_size,
                "ttl_seconds": self.ttl,
            }


class BatchProcessor:
    """Process multiple operations in batches for efficiency."""

    def __init__(self, batch_size: int = 10, max_wait_time: float = 1.0):
        """Initialize batch processor."""
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.pending_operations = []
        self._lock = asyncio.Lock()
        self._processing = False

    async def add_operation(self, operation: Callable, *args, **kwargs):
        """Add operation to batch."""
        async with self._lock:
            self.pending_operations.append((operation, args, kwargs))

            # Process if batch is full
            if len(self.pending_operations) >= self.batch_size:
                await self._process_batch()

    async def _process_batch(self):
        """Process current batch of operations."""
        if self._processing or not self.pending_operations:
            return

        self._processing = True

        try:
            # Get current batch
            batch = self.pending_operations[: self.batch_size]
            self.pending_operations = self.pending_operations[self.batch_size :]

            # Process operations concurrently
            tasks = []
            for operation, args, kwargs in batch:
                if asyncio.iscoroutinefunction(operation):
                    tasks.append(operation(*args, **kwargs))
                else:
                    # Run sync operation in thread pool
                    tasks.append(
                        asyncio.get_event_loop().run_in_executor(None, operation, *args, **kwargs)
                    )

            await asyncio.gather(*tasks, return_exceptions=True)

        finally:
            self._processing = False

    async def force_process(self):
        """Force process all pending operations."""
        async with self._lock:
            while self.pending_operations:
                await self._process_batch()

    async def get_pending_count(self) -> int:
        """Get number of pending operations."""
        async with self._lock:
            return len(self.pending_operations)


class ResourceManager:
    """Manage system resources and cleanup."""

    def __init__(self):
        """Initialize resource manager."""
        self.resources = []
        self._lock = asyncio.Lock()

    async def register_resource(self, resource: Any, cleanup_func: Callable):
        """Register a resource with cleanup function."""
        async with self._lock:
            self.resources.append((resource, cleanup_func))

    async def cleanup_all(self):
        """Cleanup all registered resources."""
        async with self._lock:
            for resource, cleanup_func in self.resources:
                try:
                    if asyncio.iscoroutinefunction(cleanup_func):
                        await cleanup_func()
                    else:
                        cleanup_func()
                except Exception as e:
                    logger.error(f"Error cleaning up resource {resource}: {e}")

            self.resources.clear()

    async def get_resource_count(self) -> int:
        """Get number of registered resources."""
        async with self._lock:
            return len(self.resources)
