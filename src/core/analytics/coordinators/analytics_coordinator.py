#!/usr/bin/env python3
"""
Analytics Coordinator - V2 Compliance Module
==========================================

Main coordinator for vector analytics processing workflow.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Analytics workflow orchestration
- Engine coordination
- Processing coordination
- Performance monitoring

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from ..vector_analytics_models import VectorAnalyticsConfig, AnalyticsMetrics
from ..engines import RealtimeAnalyticsEngine, BatchAnalyticsEngine, CachingEngine, MetricsEngine
from ..processors import InsightProcessor, PatternProcessor, PredictionProcessor


class AnalyticsCoordinator:
    """
    Main coordinator for vector analytics processing.
    
    Orchestrates the entire analytics workflow including real-time and batch
    processing, caching, and metrics collection.
    """
    
    def __init__(self, config: VectorAnalyticsConfig, intelligence_engine=None):
        """Initialize analytics coordinator."""
        self.config = config
        self.intelligence_engine = intelligence_engine
        self.logger = logging.getLogger(__name__)
        
        # Setup processing callbacks first
        self._setup_processing_callbacks()
        
        # Initialize engines
        self._initialize_engines()
        
        # Initialize processors
        self._initialize_processors()
        
        # Initialize processing coordinator
        self._initialize_processing_coordinator()
        
        self.logger.info("Analytics coordinator initialized")
    
    def _initialize_engines(self):
        """Initialize analytics engines."""
        # Caching engine
        self.caching_engine = CachingEngine(self.config)
        
        # Metrics engine
        self.metrics_engine = MetricsEngine(self.config)
        
        # Real-time engine
        self.realtime_engine = RealtimeAnalyticsEngine(
            self.config, 
            self._get_processing_callbacks()
        )
        
        # Batch engine
        self.batch_engine = BatchAnalyticsEngine(
            self.config,
            self._get_processing_callbacks()
        )
    
    def _initialize_processors(self):
        """Initialize analytics processors."""
        self.insight_processor = InsightProcessor(self.config)
        self.pattern_processor = PatternProcessor(self.config, self.intelligence_engine)
        self.prediction_processor = PredictionProcessor(self.config)
    
    def _setup_processing_callbacks(self):
        """Setup processing callbacks for engines."""
        self.processing_callbacks = {
            'insight': self._process_insight_callback,
            'pattern': self._process_pattern_callback,
            'prediction': self._process_prediction_callback
        }
    
    def _get_processing_callbacks(self) -> Dict[str, Callable]:
        """Get processing callbacks for engines."""
        return self.processing_callbacks
    
    def _initialize_processing_coordinator(self):
        """Initialize processing coordinator."""
        from .processing_coordinator import ProcessingCoordinator
        self.processing_coordinator = ProcessingCoordinator(
            self.config,
            self.insight_processor,
            self.pattern_processor,
            self.prediction_processor,
            self.caching_engine,
            self.metrics_engine
        )
    
    async def start_analytics_processing(self):
        """Start analytics processing systems."""
        try:
            # Start real-time processing if enabled
            if self.config.enable_realtime_analytics:
                await self.realtime_engine.start_realtime_processing()
                self.logger.info("Real-time analytics processing started")
            
            # Batch processing starts automatically
            if self.config.analytics_mode.value in ['batch', 'hybrid']:
                self.logger.info("Batch analytics processing active")
            
            self.logger.info("Analytics processing systems started")
            
        except Exception as e:
            self.logger.error(f"Error starting analytics processing: {e}")
            raise
    
    async def stop_analytics_processing(self):
        """Stop analytics processing systems."""
        try:
            # Stop real-time processing
            if self.config.enable_realtime_analytics:
                await self.realtime_engine.stop_realtime_processing()
            
            # Stop batch processing
            self.batch_engine.shutdown()
            
            self.logger.info("Analytics processing systems stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping analytics processing: {e}")
            raise
    
    def add_realtime_item(self, item_type: str, data: Any) -> bool:
        """Add item to real-time processing queue."""
        try:
            # Record metrics
            self.metrics_engine.record_processing_time(0, True, 'realtime_queue')
            
            return self.realtime_engine.add_realtime_item(item_type, data)
        except Exception as e:
            self.logger.error(f"Error adding real-time item: {e}")
            self.metrics_engine.record_error('realtime_queue', str(e))
            return False
    
    def add_batch_item(self, item_type: str, data: Any) -> bool:
        """Add item to batch processing queue."""
        try:
            # Record metrics
            self.metrics_engine.record_processing_time(0, True, 'batch_queue')
            
            return self.batch_engine.add_batch_item(item_type, data)
        except Exception as e:
            self.logger.error(f"Error adding batch item: {e}")
            self.metrics_engine.record_error('batch_queue', str(e))
            return False
    
    def _process_insight_callback(self, data: Dict[str, Any]) -> Optional[Any]:
        """Process insight callback for engines."""
        try:
            # Use caching if enabled
            if self.caching_engine.is_caching_enabled():
                cached_result = self.caching_engine.get_cached_insight(data)
                if cached_result:
                    return cached_result
            
            # Process with insight processor
            result = self.insight_processor.process_insight(data)
            
            # Record metrics
            if result:
                self.metrics_engine.record_processing_time(0, True, 'insight_processing')
            else:
                self.metrics_engine.record_processing_time(0, False, 'insight_processing')
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in insight processing callback: {e}")
            self.metrics_engine.record_error('insight_processing', str(e))
            return None
    
    def _process_pattern_callback(self, data: List[Any]) -> List[Any]:
        """Process pattern callback for engines."""
        try:
            # Use caching if enabled
            if self.caching_engine.is_caching_enabled():
                cached_result = self.caching_engine.get_cached_patterns(data)
                if cached_result:
                    return cached_result
            
            # Process with pattern processor
            result = self.pattern_processor.detect_patterns(data)
            
            # Record metrics
            if result:
                self.metrics_engine.record_pattern_generation(len(result))
                self.metrics_engine.record_processing_time(0, True, 'pattern_processing')
            else:
                self.metrics_engine.record_processing_time(0, False, 'pattern_processing')
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in pattern processing callback: {e}")
            self.metrics_engine.record_error('pattern_processing', str(e))
            return []
    
    def _process_prediction_callback(self, data: Dict[str, Any]) -> Optional[Any]:
        """Process prediction callback for engines."""
        try:
            # Use caching if enabled
            if self.caching_engine.is_caching_enabled():
                cached_result = self.caching_engine.get_cached_prediction(data)
                if cached_result:
                    return cached_result
            
            # Process with prediction processor
            result = self.prediction_processor.generate_prediction(data)
            
            # Record metrics
            if result:
                self.metrics_engine.record_prediction_made()
                self.metrics_engine.record_processing_time(0, True, 'prediction_processing')
            else:
                self.metrics_engine.record_processing_time(0, False, 'prediction_processing')
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in prediction processing callback: {e}")
            self.metrics_engine.record_error('prediction_processing', str(e))
            return None
    
    def get_analytics_metrics(self) -> AnalyticsMetrics:
        """Get comprehensive analytics metrics."""
        return self.metrics_engine.get_metrics()
    
    def get_processing_metrics(self) -> Dict[str, Any]:
        """Get processing performance metrics."""
        return {
            'realtime_engine': self.realtime_engine.get_processing_metrics(),
            'batch_engine': self.batch_engine.get_batch_metrics(),
            'caching_engine': self.caching_engine.get_cache_stats(),
            'insight_processor': self.insight_processor.get_processing_stats(),
            'pattern_processor': self.pattern_processor.get_processing_stats(),
            'prediction_processor': self.prediction_processor.get_processing_stats()
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            'realtime_active': self.realtime_engine.is_processing_active(),
            'batch_active': self.batch_engine.is_processing_active(),
            'caching_enabled': self.caching_engine.is_caching_enabled(),
            'realtime_queue_size': self.realtime_engine.get_queue_size(),
            'batch_queue_size': self.batch_engine.get_queue_size(),
            'last_update': datetime.now().isoformat()
        }
    
    def optimize_system(self):
        """Optimize system performance."""
        try:
            # Optimize caching
            self.caching_engine.optimize_cache()
            
            # Reset metrics if needed
            if self.metrics_engine.get_metrics().error_count > 1000:
                self.logger.info("Resetting metrics due to high error count")
                self.metrics_engine.reset_metrics()
            
            self.logger.info("System optimization completed")
            
        except Exception as e:
            self.logger.error(f"Error optimizing system: {e}")
    
    def shutdown(self):
        """Shutdown analytics coordinator gracefully."""
        try:
            self.logger.info("Shutting down analytics coordinator...")
            
            # Stop real-time processing synchronously
            if hasattr(self, 'realtime_engine') and self.realtime_engine:
                self.realtime_engine.realtime_active = False
            
            # Shutdown engines
            self.batch_engine.shutdown()
            
            self.logger.info("Analytics coordinator shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
