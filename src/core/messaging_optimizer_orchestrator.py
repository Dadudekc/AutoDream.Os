#!/usr/bin/env python3
"""
Messaging Optimizer Orchestrator - V2 Compliance Module
=======================================================

Orchestration logic for messaging integration optimization.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
from typing import Any, Dict, List, Optional
from queue import Queue

from .messaging_optimizer_models import (
    MessagingConfig, MessagingMetrics, OptimizationResult, 
    SystemInfo, ConfigurationInfo
)
from .messaging_optimizer_engines import (
    BatchProcessor, AsyncDeliveryEngine, RetryEngine, 
    ConnectionPoolEngine, MetricsEngine
)

from src.utils.logger import get_logger


class MessagingOptimizationOrchestrator:
    """
    Orchestrates messaging integration optimization operations.
    
    Coordinates all optimization engines and provides unified interface.
    """
    
    def __init__(self, config: Optional[MessagingConfig] = None):
        """Initialize messaging optimization orchestrator."""
        self.logger = get_logger(__name__)
        self.config = config or MessagingConfig()
        
        # Validate configuration
        try:
            self.config.validate()
        except Exception as e:
            self.logger.error(f"Invalid configuration: {e}")
            raise
        
        # System state
        self.is_active = False
        self.start_time = None
        self.optimization_count = 0
        
        # Message processing
        self.message_queue = Queue(maxsize=self.config.queue_size)
        
        # Performance tracking
        self.current_metrics = MessagingMetrics()
        
        # Initialize engines
        self.batch_processor = BatchProcessor(self.config, self.current_metrics)
        self.async_engine = AsyncDeliveryEngine(self.config, self.current_metrics)
        self.retry_engine = RetryEngine(self.config)
        self.connection_engine = ConnectionPoolEngine(self.config, self.current_metrics)
        self.metrics_engine = MetricsEngine(self.config, self.message_queue)
        
        self.logger.info("🚀 Messaging Optimization Orchestrator initialized")
    
    def start_optimizer(self) -> bool:
        """Start messaging optimization system."""
        try:
            if self.is_active:
                self.logger.warning("Optimizer is already active")
                return True
            
            self.is_active = True
            self.start_time = time.time()
            
            # Start monitoring
            asyncio.create_task(self._monitoring_loop())
            
            # Start batch processor if enabled
            if self.config.enable_batching:
                asyncio.create_task(self.batch_processor.batch_processor_loop(
                    lambda: self.is_active
                ))
            
            self.logger.info("Messaging integration optimizer started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start optimizer: {e}")
            return False
    
    def stop_optimizer(self) -> bool:
        """Stop messaging optimization system."""
        try:
            if not self.is_active:
                self.logger.warning("Optimizer is not active")
                return True
            
            self.is_active = False
            
            self.logger.info("Messaging integration optimizer stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop optimizer: {e}")
            return False
    
    async def optimize_messaging(self) -> OptimizationResult:
        """Optimize messaging integration performance."""
        try:
            if not self.is_active:
                return OptimizationResult(
                    status="inactive",
                    execution_time_ms=0.0,
                    optimization_count=self.optimization_count,
                    batch_optimization={"status": "inactive"},
                    async_optimization={"status": "inactive"},
                    retry_optimization={"status": "inactive"},
                    connection_optimization={"status": "inactive"},
                    current_metrics=self.current_metrics.to_dict(),
                    error="Optimizer is not active"
                )
            
            start_time = time.time()
            
            # Run optimization strategies
            batch_optimization = await self.batch_processor.optimize_batching()
            async_optimization = await self.async_engine.optimize_async_delivery()
            retry_optimization = await self.retry_engine.optimize_retry_mechanisms()
            connection_optimization = await self.connection_engine.optimize_connection_pool()
            
            # Update metrics
            execution_time = time.time() - start_time
            self.metrics_engine.update_performance_metrics(self.current_metrics, execution_time)
            
            self.optimization_count += 1
            
            return OptimizationResult(
                status="completed",
                execution_time_ms=execution_time * 1000,
                optimization_count=self.optimization_count,
                batch_optimization=batch_optimization,
                async_optimization=async_optimization,
                retry_optimization=retry_optimization,
                connection_optimization=connection_optimization,
                current_metrics=self.current_metrics.to_dict()
            )
            
        except Exception as e:
            self.logger.error(f"Messaging optimization failed: {e}")
            return OptimizationResult(
                status="failed",
                execution_time_ms=0.0,
                optimization_count=self.optimization_count,
                batch_optimization={"status": "failed"},
                async_optimization={"status": "failed"},
                retry_optimization={"status": "failed"},
                connection_optimization={"status": "failed"},
                current_metrics=self.current_metrics.to_dict(),
                error=str(e)
            )
    
    async def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_active:
            try:
                # Update metrics
                self.metrics_engine.update_performance_metrics(self.current_metrics, 0.001)
                
                # Auto-optimize if performance is low
                if (len(self.metrics_engine.get_metrics_history()) > 0 and 
                    self.current_metrics.messages_per_second < 10):
                    await self.optimize_messaging()
                
                await asyncio.sleep(self.config.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5.0)
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get comprehensive optimization summary."""
        uptime = None
        if self.start_time:
            uptime = time.time() - self.start_time
        
        return {
            "system_info": SystemInfo(
                is_active=self.is_active,
                uptime_seconds=uptime,
                optimization_count=self.optimization_count,
                queue_size=self.message_queue.qsize(),
                batch_queue_size=len(self.batch_processor.batch_queue),
                active_connections=self.connection_engine.active_connections
            ).__dict__,
            "current_metrics": self.current_metrics.to_dict(),
            "configuration": ConfigurationInfo(
                delivery_strategy=self.config.delivery_strategy.value,
                optimization_mode=self.config.optimization_mode.value,
                target_improvement=self.config.target_improvement,
                batching_enabled=self.config.enable_batching,
                async_enabled=self.config.enable_async_delivery
            ).__dict__,
            "metrics_history_size": len(self.metrics_engine.get_metrics_history())
        }
