#!/usr/bin/env python3
"""
Discord Commander Performance Optimization
==========================================

Performance optimization utilities for the Discord Commander system.
V2 Compliance: ≤400 lines, focused optimization functionality.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from collections import deque
import weakref

logger = logging.getLogger(__name__)


@dataclass
class DiscordPerformanceMetrics:
    """Performance metrics for Discord Commander."""
    
    message_processing_time: float
    command_execution_time: float
    event_handling_time: float
    memory_usage: float
    messages_per_second: float
    commands_per_second: float
    error_rate: float
    uptime_seconds: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "message_processing_time": self.message_processing_time,
            "command_execution_time": self.command_execution_time,
            "event_handling_time": self.event_handling_time,
            "memory_usage": self.memory_usage,
            "messages_per_second": self.messages_per_second,
            "commands_per_second": self.commands_per_second,
            "error_rate": self.error_rate,
            "uptime_seconds": self.uptime_seconds
        }


class DiscordPerformanceMonitor:
    """Monitors Discord Commander performance."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.message_times: deque = deque(maxlen=window_size)
        self.command_times: deque = deque(maxlen=window_size)
        self.event_times: deque = deque(maxlen=window_size)
        self.error_count = 0
        self.total_requests = 0
        self.start_time = datetime.now()
        self.lock = threading.RLock()
    
    def record_message_processing(self, processing_time: float):
        """Record message processing time."""
        with self.lock:
            self.message_times.append(processing_time)
            self.total_requests += 1
    
    def record_command_execution(self, execution_time: float):
        """Record command execution time."""
        with self.lock:
            self.command_times.append(execution_time)
    
    def record_event_handling(self, handling_time: float):
        """Record event handling time."""
        with self.lock:
            self.event_times.append(handling_time)
    
    def record_error(self):
        """Record an error."""
        with self.lock:
            self.error_count += 1
    
    def get_current_metrics(self) -> DiscordPerformanceMetrics:
        """Get current performance metrics."""
        with self.lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            # Calculate averages
            avg_message_time = sum(self.message_times) / len(self.message_times) if self.message_times else 0
            avg_command_time = sum(self.command_times) / len(self.command_times) if self.command_times else 0
            avg_event_time = sum(self.event_times) / len(self.event_times) if self.event_times else 0
            
            # Calculate rates
            messages_per_second = len(self.message_times) / uptime if uptime > 0 else 0
            commands_per_second = len(self.command_times) / uptime if uptime > 0 else 0
            
            # Calculate error rate
            error_rate = self.error_count / self.total_requests if self.total_requests > 0 else 0
            
            return DiscordPerformanceMetrics(
                message_processing_time=avg_message_time,
                command_execution_time=avg_command_time,
                event_handling_time=avg_event_time,
                memory_usage=0.0,  # Will be set by system monitor
                messages_per_second=messages_per_second,
                commands_per_second=commands_per_second,
                error_rate=error_rate,
                uptime_seconds=uptime
            )


class DiscordCommandCache:
    """Caching system for Discord commands."""
    
    def __init__(self, max_size: int = 500):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.access_times: Dict[str, datetime] = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
    
    def get_command_result(self, command_key: str) -> Optional[Any]:
        """Get cached command result."""
        with self.lock:
            if command_key in self.cache:
                self.access_times[command_key] = datetime.now()
                self.hit_count += 1
                return self.cache[command_key]
            
            self.miss_count += 1
            return None
    
    def cache_command_result(self, command_key: str, result: Any, ttl_seconds: int = 300):
        """Cache command result with TTL."""
        with self.lock:
            # Evict expired entries
            self._evict_expired()
            
            # Evict oldest if cache is full
            if len(self.cache) >= self.max_size:
                self._evict_oldest()
            
            self.cache[command_key] = {
                "result": result,
                "expires_at": datetime.now() + timedelta(seconds=ttl_seconds)
            }
            self.access_times[command_key] = datetime.now()
    
    def _evict_expired(self):
        """Evict expired cache entries."""
        now = datetime.now()
        expired_keys = [
            key for key, data in self.cache.items()
            if data["expires_at"] < now
        ]
        
        for key in expired_keys:
            del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
    
    def _evict_oldest(self):
        """Evict oldest cache entry."""
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
    
    def clear(self):
        """Clear cache."""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total_requests if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class DiscordRateLimiter:
    """Rate limiting for Discord commands."""
    
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests = max_requests_per_minute
        self.request_times: deque = deque()
        self.lock = threading.RLock()
    
    def can_execute_command(self, user_id: str) -> bool:
        """Check if user can execute command."""
        with self.lock:
            now = datetime.now()
            
            # Remove old requests (older than 1 minute)
            while self.request_times and (now - self.request_times[0]).total_seconds() > 60:
                self.request_times.popleft()
            
            # Check if under rate limit
            if len(self.request_times) < self.max_requests:
                self.request_times.append(now)
                return True
            
            return False
    
    def get_wait_time(self) -> float:
        """Get time to wait before next request."""
        with self.lock:
            if not self.request_times:
                return 0.0
            
            oldest_request = self.request_times[0]
            wait_time = 60 - (datetime.now() - oldest_request).total_seconds()
            return max(0.0, wait_time)


class DiscordAsyncPool:
    """Async task pool for Discord operations."""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.task_counter = 0
        self.lock = asyncio.Lock()
    
    async def execute_async(self, coro: Callable, task_name: str = None) -> Any:
        """Execute async task with concurrency control."""
        async with self.semaphore:
            if task_name is None:
                async with self.lock:
                    self.task_counter += 1
                    task_name = f"task_{self.task_counter}"
            
            # Track active task
            async with self.lock:
                self.active_tasks[task_name] = asyncio.current_task()
            
            try:
                result = await coro
                return result
            finally:
                # Remove from active tasks
                async with self.lock:
                    if task_name in self.active_tasks:
                        del self.active_tasks[task_name]
    
    def get_active_task_count(self) -> int:
        """Get number of active tasks."""
        return len(self.active_tasks)
    
    def get_task_names(self) -> List[str]:
        """Get names of active tasks."""
        return list(self.active_tasks.keys())


class DiscordOptimizer:
    """Main Discord Commander optimization engine."""
    
    def __init__(self):
        self.performance_monitor = DiscordPerformanceMonitor()
        self.command_cache = DiscordCommandCache()
        self.rate_limiter = DiscordRateLimiter()
        self.async_pool = DiscordAsyncPool()
        self.optimization_enabled = True
        self.start_time = datetime.now()
    
    async def optimize_command_execution(self, command_func: Callable, 
                                       ctx: Any, *args, **kwargs) -> Any:
        """Optimize command execution with caching and rate limiting."""
        if not self.optimization_enabled:
            return await self._execute_command_direct(command_func, ctx, *args, **kwargs)
        
        # Check rate limiting
        user_id = str(ctx.author.id) if hasattr(ctx, 'author') else "unknown"
        if not self.rate_limiter.can_execute_command(user_id):
            wait_time = self.rate_limiter.get_wait_time()
            return f"Rate limited. Please wait {wait_time:.1f} seconds."
        
        # Generate cache key
        cache_key = self._generate_cache_key(command_func.__name__, args, kwargs)
        
        # Check cache
        cached_result = self.command_cache.get_command_result(cache_key)
        if cached_result is not None:
            logger.debug(f"Command cache hit: {command_func.__name__}")
            return cached_result["result"]
        
        # Execute command with performance monitoring
        start_time = time.time()
        
        try:
            result = await self.async_pool.execute_async(
                command_func(ctx, *args, **kwargs),
                f"command_{command_func.__name__}"
            )
            
            execution_time = time.time() - start_time
            self.performance_monitor.record_command_execution(execution_time)
            
            # Cache result
            self.command_cache.cache_command_result(cache_key, result)
            
            return result
            
        except Exception as e:
            self.performance_monitor.record_error()
            logger.error(f"Command execution error: {e}")
            raise
    
    async def optimize_message_processing(self, message_handler: Callable, 
                                        message: Any) -> Any:
        """Optimize message processing."""
        if not self.optimization_enabled:
            return await message_handler(message)
        
        start_time = time.time()
        
        try:
            result = await self.async_pool.execute_async(
                message_handler(message),
                f"message_{message.id}"
            )
            
            processing_time = time.time() - start_time
            self.performance_monitor.record_message_processing(processing_time)
            
            return result
            
        except Exception as e:
            self.performance_monitor.record_error()
            logger.error(f"Message processing error: {e}")
            raise
    
    async def optimize_event_handling(self, event_handler: Callable, 
                                    event_name: str, *args, **kwargs) -> Any:
        """Optimize event handling."""
        if not self.optimization_enabled:
            return await event_handler(*args, **kwargs)
        
        start_time = time.time()
        
        try:
            result = await self.async_pool.execute_async(
                event_handler(*args, **kwargs),
                f"event_{event_name}"
            )
            
            handling_time = time.time() - start_time
            self.performance_monitor.record_event_handling(handling_time)
            
            return result
            
        except Exception as e:
            self.performance_monitor.record_error()
            logger.error(f"Event handling error: {e}")
            raise
    
    async def _execute_command_direct(self, command_func: Callable, 
                                    ctx: Any, *args, **kwargs) -> Any:
        """Execute command directly without optimization."""
        return await command_func(ctx, *args, **kwargs)
    
    def _generate_cache_key(self, command_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key for command."""
        # Simple cache key generation
        key_parts = [command_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return "|".join(key_parts)
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        performance_metrics = self.performance_monitor.get_current_metrics()
        cache_stats = self.command_cache.get_stats()
        
        return {
            "performance": performance_metrics.to_dict(),
            "cache": cache_stats,
            "rate_limiter": {
                "max_requests_per_minute": self.rate_limiter.max_requests,
                "current_requests": len(self.rate_limiter.request_times)
            },
            "async_pool": {
                "max_concurrent": self.async_pool.max_concurrent,
                "active_tasks": self.async_pool.get_active_task_count(),
                "active_task_names": self.async_pool.get_task_names()
            },
            "optimization_enabled": self.optimization_enabled,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }
    
    def enable_optimization(self):
        """Enable optimization features."""
        self.optimization_enabled = True
        logger.info("Discord Commander optimization enabled")
    
    def disable_optimization(self):
        """Disable optimization features."""
        self.optimization_enabled = False
        logger.info("Discord Commander optimization disabled")
    
    def clear_cache(self):
        """Clear command cache."""
        self.command_cache.clear()
        logger.info("Discord Commander cache cleared")
    
    def reset_rate_limiter(self):
        """Reset rate limiter."""
        self.rate_limiter.request_times.clear()
        logger.info("Discord Commander rate limiter reset")




