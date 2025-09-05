#!/usr/bin/env python3
"""
Data Optimization Engine - V2 Compliance Module
==============================================

Core business logic for data processing optimization.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union, Iterator
import logging

from .data_optimization_models import (
    ProcessingStrategy,
    OptimizationLevel,
    ProcessingMetrics,
    OptimizationConfig,
    OptimizationResult,
    CacheEntry,
    PerformanceProfile,
)


class DataOptimizationEngine:
    """Core engine for data processing optimization."""

    def __init__(self, config: OptimizationConfig = None):
        """Initialize data optimization engine."""
        self.config = config or OptimizationConfig()
        self.logger = logging.getLogger(__name__)
        
        # Initialize metrics
        self.current_metrics = ProcessingMetrics()
        self.metrics_history: List[ProcessingMetrics] = []
        
        # Initialize cache
        self.cache: Dict[str, CacheEntry] = {}
        
        # Initialize thread pool
        if self.config.enable_parallel_processing:
            self.thread_pool = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # System state
        self.is_active = True
        self.start_time = time.time()
        self.optimization_count = 0

    async def optimize_processing(
        self, 
        data: Any, 
        operation: str, 
        **kwargs
    ) -> OptimizationResult:
        """
        Optimize data processing operation.
        
        Args:
            data: Data to process
            operation: Operation type
            **kwargs: Additional parameters
            
        Returns:
            Optimization result with metrics
        """
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(data, operation, kwargs)
            if self.config.cache_enabled and cache_key in self.cache:
                cache_entry = self.cache[cache_key]
                if not cache_entry.is_expired():
                    self.logger.debug(f"Cache hit for operation: {operation}")
                    return OptimizationResult(
                        success=True,
                        strategy_used="cache",
                        execution_time_ms=0.0,
                        result=cache_entry.value,
                        metrics=self.current_metrics,
                        cache_hit=True
                    )
            
            # Choose processing strategy
            strategy = self._select_optimal_strategy(data, operation)
            
            # Execute processing
            if strategy == ProcessingStrategy.PARALLEL:
                result = await self._process_parallel(data, operation, **kwargs)
            elif strategy == ProcessingStrategy.STREAMING:
                result = await self._process_streaming(data, operation, **kwargs)
            elif strategy == ProcessingStrategy.BATCH:
                result = await self._process_batch(data, operation, **kwargs)
            else:
                result = await self._process_sequential(data, operation, **kwargs)
            
            # Update metrics
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics(execution_time, len(data) if hasattr(data, '__len__') else 1)
            
            # Cache result
            if self.config.cache_enabled:
                self._cache_result(cache_key, result)
            
            self.optimization_count += 1
            
            self.logger.debug(f"Data processing optimized: {strategy.value} strategy, "
                            f"{execution_time:.1f}ms")
            
            return OptimizationResult(
                success=True,
                strategy_used=strategy.value,
                execution_time_ms=execution_time,
                result=result,
                metrics=self.current_metrics,
                cache_hit=False
            )
            
        except Exception as e:
            self.logger.error(f"Error optimizing data processing: {e}")
            return OptimizationResult(
                success=False,
                strategy_used="error",
                execution_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e)
            )

    def _select_optimal_strategy(self, data: Any, operation: str) -> ProcessingStrategy:
        """Select optimal processing strategy based on data and operation."""
        try:
            # Estimate data size
            data_size = self._estimate_data_size(data)
            
            # Select strategy based on size and configuration
            if self.config.strategy == ProcessingStrategy.ADAPTIVE:
                if data_size > 10000 and self.config.enable_parallel_processing:
                    return ProcessingStrategy.PARALLEL
                elif data_size > 1000 and self.config.enable_streaming:
                    return ProcessingStrategy.STREAMING
                elif data_size > 100:
                    return ProcessingStrategy.BATCH
                else:
                    return ProcessingStrategy.SEQUENTIAL
            else:
                return self.config.strategy
                
        except Exception as e:
            self.logger.warning(f"Error selecting strategy, using sequential: {e}")
            return ProcessingStrategy.SEQUENTIAL

    def _estimate_data_size(self, data: Any) -> int:
        """Estimate data size for strategy selection."""
        try:
            if hasattr(data, '__len__'):
                return len(data)
            elif isinstance(data, (list, tuple)):
                return len(data)
            elif isinstance(data, dict):
                return len(data)
            else:
                return 1
        except:
            return 1

    async def _process_sequential(self, data: Any, operation: str, **kwargs) -> Any:
        """Process data sequentially."""
        # Simulate sequential processing
        await asyncio.sleep(0.001)  # Simulate processing time
        return f"Sequential processing result for {operation}"

    async def _process_parallel(self, data: Any, operation: str, **kwargs) -> Any:
        """Process data in parallel."""
        if not self.config.enable_parallel_processing:
            return await self._process_sequential(data, operation, **kwargs)
        
        # Simulate parallel processing
        await asyncio.sleep(0.0005)  # Simulate faster processing
        return f"Parallel processing result for {operation}"

    async def _process_streaming(self, data: Any, operation: str, **kwargs) -> Any:
        """Process data in streaming mode."""
        if not self.config.enable_streaming:
            return await self._process_sequential(data, operation, **kwargs)
        
        # Simulate streaming processing
        chunk_size = self.config.streaming_chunk_size
        if hasattr(data, '__len__') and len(data) > chunk_size:
            # Process in chunks
            results = []
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                result = await self._process_sequential(chunk, operation, **kwargs)
                results.append(result)
            return results
        else:
            return await self._process_sequential(data, operation, **kwargs)

    async def _process_batch(self, data: Any, operation: str, **kwargs) -> Any:
        """Process data in batch mode."""
        # Simulate batch processing
        await asyncio.sleep(0.0008)  # Simulate batch processing time
        return f"Batch processing result for {operation}"

    def _generate_cache_key(self, data: Any, operation: str, kwargs: Dict[str, Any]) -> str:
        """Generate cache key for operation."""
        try:
            # Create a simple hash-based key
            data_str = str(data)[:100] if hasattr(data, '__str__') else str(type(data))
            kwargs_str = str(sorted(kwargs.items()))
            return f"{operation}:{hash(data_str + kwargs_str)}"
        except:
            return f"{operation}:{time.time()}"

    def _cache_result(self, cache_key: str, result: Any) -> None:
        """Cache processing result."""
        if not self.config.cache_enabled:
            return
        
        # Check cache size limit
        if len(self.cache) >= self.config.max_cache_size:
            self._evict_oldest_cache_entry()
        
        # Store result
        self.cache[cache_key] = CacheEntry(
            key=cache_key,
            value=result,
            ttl_seconds=self.config.cache_ttl_seconds
        )

    def _evict_oldest_cache_entry(self) -> None:
        """Evict oldest cache entry."""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].timestamp)
        del self.cache[oldest_key]

    def _update_metrics(self, execution_time_ms: float, records_processed: int) -> None:
        """Update processing metrics."""
        self.current_metrics.operations_processed += 1
        self.current_metrics.processing_time_ms += execution_time_ms
        
        # Calculate throughput
        if execution_time_ms > 0:
            ops_per_sec = 1000 / execution_time_ms
            self.current_metrics.throughput_ops_per_sec = ops_per_sec
        
        # Update cache hit rate
        total_operations = self.current_metrics.operations_processed
        cache_hits = sum(1 for entry in self.cache.values() if not entry.is_expired())
        if total_operations > 0:
            self.current_metrics.cache_hit_rate = cache_hits / total_operations

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        uptime = None
        if self.start_time:
            uptime = time.time() - self.start_time
        
        return {
            "system_info": {
                "is_active": self.is_active,
                "uptime_seconds": uptime,
                "optimization_count": self.optimization_count,
                "cache_size": len(self.cache),
                "max_workers": self.config.max_workers
            },
            "current_metrics": self.current_metrics.to_dict(),
            "configuration": {
                "strategy": self.config.strategy.value,
                "optimization_level": self.config.optimization_level.value,
                "target_improvement": self.config.target_improvement,
                "cache_enabled": self.config.cache_enabled,
                "streaming_enabled": self.config.enable_streaming,
                "parallel_enabled": self.config.enable_parallel_processing
            },
            "metrics_history_size": len(self.metrics_history)
        }

    def clear_cache(self) -> None:
        """Clear all cached results."""
        self.cache.clear()
        self.logger.info("Cache cleared")

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.current_metrics.reset()
        self.metrics_history.clear()
        self.optimization_count = 0
        self.logger.info("Metrics reset")

    def cleanup(self) -> None:
        """Cleanup resources."""
        if hasattr(self, 'thread_pool'):
            self.thread_pool.shutdown(wait=True)
        self.clear_cache()
        self.is_active = False
