#!/usr/bin/env python3
"""
Messaging Optimizer Engines - V2 Compliance Module
==================================================

Core processing engines for messaging integration optimization.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
from typing import Any, Dict, List
from queue import Queue, Empty

from .messaging_optimizer_models import (
    MessagingConfig, MessagingMetrics, OptimizationResult
)

from src.utils.logger import get_logger


class BatchProcessor:
    """Handles message batching operations."""
    
    def __init__(self, config: MessagingConfig, metrics: MessagingMetrics):
        self.config = config
        self.metrics = metrics
        self.logger = get_logger(__name__)
        self.batch_queue = []
        self.last_batch_time = time.time()
    
    async def optimize_batching(self) -> Dict[str, Any]:
        """Optimize message batching strategy."""
        try:
            if not self.config.enable_batching:
                return {"status": "disabled"}
            
            # Process any pending batches
            processed_batches = 0
            if len(self.batch_queue) > 0:
                await self._process_batch(self.batch_queue)
                processed_batches = 1
                self.batch_queue = []
            
            # Calculate batch efficiency
            optimal_batch_size = min(self.config.batch_size, 200)
            batch_efficiency = len(self.batch_queue) / optimal_batch_size if optimal_batch_size > 0 else 1.0
            self.metrics.batch_efficiency = batch_efficiency
            
            return {
                "status": "optimized",
                "processed_batches": processed_batches,
                "current_batch_size": len(self.batch_queue),
                "optimal_batch_size": optimal_batch_size,
                "batch_efficiency": batch_efficiency
            }
            
        except Exception as e:
            self.logger.error(f"Batch optimization failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _process_batch(self, batch: List[Any]) -> bool:
        """Process a batch of messages."""
        try:
            # Simulate batch processing
            await asyncio.sleep(0.01 * len(batch))  # Simulate processing time
            
            self.metrics.messages_processed += len(batch)
            return True
            
        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")
            return False
    
    async def batch_processor_loop(self, is_active_callback):
        """Main batch processing loop."""
        while is_active_callback():
            try:
                current_time = time.time()
                
                # Check if batch should be processed
                batch_timeout_reached = (current_time - self.last_batch_time) * 1000 >= self.config.batch_timeout_ms
                batch_size_reached = len(self.batch_queue) >= self.config.batch_size
                
                if (batch_timeout_reached or batch_size_reached) and len(self.batch_queue) > 0:
                    await self._process_batch(self.batch_queue)
                    self.batch_queue = []
                    self.last_batch_time = current_time
                
                await asyncio.sleep(0.1)  # Check every 100ms
                
            except Exception as e:
                self.logger.error(f"Error in batch processor: {e}")
                await asyncio.sleep(1.0)


class AsyncDeliveryEngine:
    """Handles async delivery optimization."""
    
    def __init__(self, config: MessagingConfig, metrics: MessagingMetrics):
        self.config = config
        self.metrics = metrics
        self.logger = get_logger(__name__)
        self.pending_deliveries = 0
    
    async def optimize_async_delivery(self) -> Dict[str, Any]:
        """Optimize async delivery mechanisms."""
        try:
            if not self.config.enable_async_delivery:
                return {"status": "disabled"}
            
            # Simulate async delivery optimization
            optimal_concurrent = min(self.config.max_concurrent_deliveries, 100)
            current_load = self.pending_deliveries / optimal_concurrent if optimal_concurrent > 0 else 0
            
            return {
                "status": "optimized",
                "max_concurrent": optimal_concurrent,
                "current_pending": self.pending_deliveries,
                "load_factor": current_load
            }
            
        except Exception as e:
            self.logger.error(f"Async delivery optimization failed: {e}")
            return {"status": "failed", "error": str(e)}


class RetryEngine:
    """Handles retry mechanism optimization."""
    
    def __init__(self, config: MessagingConfig):
        self.config = config
        self.logger = get_logger(__name__)
    
    async def optimize_retry_mechanisms(self) -> Dict[str, Any]:
        """Optimize retry strategies."""
        try:
            # Calculate optimal retry settings
            optimal_retries = min(self.config.max_retries, 5)
            optimal_delay = max(self.config.retry_delay_ms, 50.0)
            
            return {
                "status": "optimized",
                "max_retries": optimal_retries,
                "retry_delay_ms": optimal_delay,
                "backoff_multiplier": self.config.backoff_multiplier
            }
            
        except Exception as e:
            self.logger.error(f"Retry optimization failed: {e}")
            return {"status": "failed", "error": str(e)}


class ConnectionPoolEngine:
    """Handles connection pool optimization."""
    
    def __init__(self, config: MessagingConfig, metrics: MessagingMetrics):
        self.config = config
        self.metrics = metrics
        self.logger = get_logger(__name__)
        self.active_connections = 0
    
    async def optimize_connection_pool(self) -> Dict[str, Any]:
        """Optimize connection pool performance."""
        try:
            # Optimize connection pool
            optimal_pool_size = min(self.config.connection_pool_size, 20)
            self.active_connections = min(self.active_connections, optimal_pool_size)
            
            pool_usage = self.active_connections / optimal_pool_size if optimal_pool_size > 0 else 0
            self.metrics.connection_pool_usage = pool_usage
            
            return {
                "status": "optimized",
                "pool_size": optimal_pool_size,
                "active_connections": self.active_connections,
                "usage_rate": pool_usage
            }
            
        except Exception as e:
            self.logger.error(f"Connection pool optimization failed: {e}")
            return {"status": "failed", "error": str(e)}


class MetricsEngine:
    """Handles performance metrics calculation and updates."""
    
    def __init__(self, config: MessagingConfig, message_queue: Queue):
        self.config = config
        self.message_queue = message_queue
        self.logger = get_logger(__name__)
        self.metrics_history: List[MessagingMetrics] = []
    
    def update_performance_metrics(self, metrics: MessagingMetrics, execution_time: float):
        """Update performance metrics."""
        metrics.timestamp = time.time()
        
        # Update throughput metrics
        if execution_time > 0:
            metrics.messages_per_second = 1.0 / execution_time
        
        metrics.average_latency_ms = execution_time * 1000
        
        # Calculate success rate (simulated)
        metrics.success_rate = 0.95  # 95% success rate
        metrics.retry_rate = 0.05   # 5% retry rate
        
        # Queue utilization
        if self.config.queue_size > 0:
            metrics.queue_utilization = self.message_queue.qsize() / self.config.queue_size
        
        # Store in history
        metrics_copy = MessagingMetrics(
            timestamp=metrics.timestamp,
            messages_processed=metrics.messages_processed,
            messages_per_second=metrics.messages_per_second,
            average_latency_ms=metrics.average_latency_ms,
            success_rate=metrics.success_rate,
            retry_rate=metrics.retry_rate,
            batch_efficiency=metrics.batch_efficiency,
            queue_utilization=metrics.queue_utilization,
            connection_pool_usage=metrics.connection_pool_usage
        )
        
        self.metrics_history.append(metrics_copy)
        
        # Limit history size
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-50:]
    
    def get_metrics_history(self) -> List[MessagingMetrics]:
        """Get metrics history."""
        return self.metrics_history.copy()
