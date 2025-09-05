#!/usr/bin/env python3
"""
Vector Analytics Processor V2 - Modular Architecture
===================================================

V2 Compliant modular vector analytics processing engine.
Refactored from monolithic vector_analytics_processor.py for V2 compliance.

Architecture:
- Analytics Engines: Realtime, Batch, Caching, Metrics
- Processors: Insight, Pattern, Prediction
- Coordinators: Analytics, Processing
- Backward compatible API

V2 Compliance: < 300 lines, modular design, single responsibility.

Author: Agent-7 - Web Development
License: MIT
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .vector_analytics_models import (
    AnalyticsInsight, PatternMatch, PredictionResult, VectorAnalyticsConfig,
    AnalyticsMode, AnalyticsMetrics, create_insight
)
from .vector_analytics_intelligence import VectorAnalyticsIntelligence
from .coordinators import AnalyticsCoordinator


class VectorAnalyticsProcessor:
    """
    V2 Compliant modular vector analytics processing engine.
    
    Provides backward-compatible API while using modular architecture
    for improved maintainability and performance.
    """
    
    def __init__(self, config: VectorAnalyticsConfig, intelligence: VectorAnalyticsIntelligence):
        """Initialize V2 analytics processor."""
        self.config = config
        self.intelligence = intelligence
        self.logger = logging.getLogger(__name__)
        
        # Initialize modular coordinator
        self.coordinator = AnalyticsCoordinator(config, intelligence)
        
        # Backward compatibility attributes
        self.processing_queue = self.coordinator.batch_engine.batch_queue
        self.active_tasks = {}
        self.metrics = self.coordinator.metrics_engine.get_metrics()
        self.cache_stats = self.coordinator.caching_engine.get_cache_stats()
        
        # Threading and processing (backward compatibility)
        self.thread_pool = self.coordinator.batch_engine.thread_pool
        self.process_pool = self.coordinator.batch_engine.process_pool
        self.processing_lock = self.coordinator.batch_engine.processing_lock
        
        # Processing modes (backward compatibility)
        self.realtime_processor = self.coordinator.realtime_engine
        self.batch_processor = self.coordinator.batch_engine
        
        self.logger.info(f"V2 Analytics processor initialized with {config.analytics_mode.value} mode")
    
    # Backward compatibility methods
    def _setup_caching_system(self):
        """Setup intelligent caching system (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _initialize_processing_systems(self):
        """Initialize processing systems (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _setup_realtime_processing(self):
        """Setup real-time analytics processing (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _setup_batch_processing(self):
        """Setup batch processing system (backward compatibility)."""
        # Handled by coordinator
        pass
    
    async def _realtime_processing_loop(self):
        """Real-time processing loop (backward compatibility)."""
        # Handled by coordinator
        pass
    
    async def _process_realtime_item(self, item: Dict[str, Any]):
        """Process a single real-time analytics item (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _batch_processing_cycle(self):
        """Execute batch processing cycle (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _process_batch(self, batch: List[Dict[str, Any]]):
        """Process a batch of analytics items (backward compatibility)."""
        # Handled by coordinator
        pass
    
    def _process_batch_item(self, item: Dict[str, Any]) -> Optional[Any]:
        """Process a single batch item (backward compatibility)."""
        # Handled by coordinator
        pass
    
    # Core processing methods (backward compatibility)
    def _process_insight_uncached(self, data: Dict[str, Any]) -> Optional[AnalyticsInsight]:
        """Process analytics insight without caching (backward compatibility)."""
        return self.coordinator._process_insight_callback(data)
    
    def _detect_patterns_uncached(self, data: List[Any]) -> List[PatternMatch]:
        """Detect patterns without caching (backward compatibility)."""
        return self.coordinator._process_pattern_callback(data)
    
    def _generate_prediction_uncached(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Generate prediction without caching (backward compatibility)."""
        return self.coordinator._process_prediction_callback(data)
    
    # Async versions for real-time processing (backward compatibility)
    async def _process_insight_async(self, data: Dict[str, Any]) -> Optional[AnalyticsInsight]:
        """Async version of insight processing (backward compatibility)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, self._process_insight_uncached, data)
    
    async def _detect_patterns_async(self, data: List[Any]) -> List[PatternMatch]:
        """Async version of pattern detection (backward compatibility)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, self._detect_patterns_uncached, data)
    
    async def _generate_prediction_async(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Async version of prediction generation (backward compatibility)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, self._generate_prediction_uncached, data)
    
    # Public interface methods (backward compatibility)
    def add_realtime_item(self, item_type: str, data: Any) -> bool:
        """Add item to real-time processing queue (backward compatibility)."""
        return self.coordinator.add_realtime_item(item_type, data)
    
    def add_batch_item(self, item_type: str, data: Any) -> bool:
        """Add item to batch processing queue (backward compatibility)."""
        return self.coordinator.add_batch_item(item_type, data)
    
    def _update_processing_metrics(self, processing_time: float, success: bool):
        """Update processing performance metrics (backward compatibility)."""
        self.coordinator.metrics_engine.record_processing_time(processing_time, success, 'general')
    
    def _update_batch_metrics(self, batch_size: int, results_count: int, processing_time: float):
        """Update batch processing metrics (backward compatibility)."""
        self.coordinator.metrics_engine.record_batch_processing(batch_size, results_count, processing_time)
    
    def _store_processing_result(self, result: Any, result_type: str):
        """Store processing result for future use (backward compatibility)."""
        # Implementation depends on storage backend
        self.logger.debug(f"Processed {result_type} result: {type(result).__name__}")
    
    def get_processing_metrics(self) -> AnalyticsMetrics:
        """Get current processing metrics (backward compatibility)."""
        return self.coordinator.get_analytics_metrics()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get caching performance statistics (backward compatibility)."""
        return self.coordinator.caching_engine.get_cache_stats()
    
    def shutdown(self):
        """Shutdown processing engine gracefully (backward compatibility)."""
        self.coordinator.shutdown()
    
    # New V2 methods
    async def start_processing(self):
        """Start analytics processing systems."""
        await self.coordinator.start_analytics_processing()
    
    async def stop_processing(self):
        """Stop analytics processing systems."""
        await self.coordinator.stop_analytics_processing()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return self.coordinator.get_system_status()
    
    def get_processing_metrics_detailed(self) -> Dict[str, Any]:
        """Get detailed processing metrics."""
        return self.coordinator.get_processing_metrics()
    
    def optimize_system(self):
        """Optimize system performance."""
        self.coordinator.optimize_system()
    
    def process_insight(self, data: Dict[str, Any]) -> Optional[AnalyticsInsight]:
        """Process insight directly (new V2 method)."""
        return self.coordinator.processing_coordinator.process_insight(data)
    
    def process_patterns(self, data: List[Any]) -> List[PatternMatch]:
        """Process patterns directly (new V2 method)."""
        return self.coordinator.processing_coordinator.process_patterns(data)
    
    def process_prediction(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Process prediction directly (new V2 method)."""
        return self.coordinator.processing_coordinator.process_prediction(data)
    
    def process_batch(self, items: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """Process batch directly (new V2 method)."""
        return self.coordinator.processing_coordinator.process_batch(items)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status (new V2 method)."""
        return self.coordinator.processing_coordinator.get_health_status()
