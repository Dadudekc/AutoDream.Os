#!/usr/bin/env python3
"""
Realtime Analytics Engine - V2 Compliance Module
===============================================

Handles real-time analytics processing with async capabilities.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Real-time analytics processing
- Async queue management
- Real-time metrics tracking
- Performance optimization

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import asyncio
import time
import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from collections import deque

from ..vector_analytics_models import (
    AnalyticsInsight, PatternMatch, PredictionResult, VectorAnalyticsConfig
)


class RealtimeAnalyticsEngine:
    """
    Real-time analytics processing engine.
    
    Handles async processing of analytics items with queue management
    and performance optimization.
    """
    
    def __init__(self, config: VectorAnalyticsConfig, processing_callbacks: Dict[str, Callable]):
        """Initialize real-time analytics engine."""
        self.config = config
        self.processing_callbacks = processing_callbacks
        self.logger = logging.getLogger(__name__)
        
        # Processing state
        self.realtime_queue = None
        self.realtime_active = False
        self.realtime_task = None
        self.processing_metrics = {
            'items_processed': 0,
            'processing_errors': 0,
            'average_processing_time': 0.0,
            'last_processing_time': None
        }
        
        # Initialize if real-time is enabled
        if config.enable_realtime_analytics:
            self._initialize_realtime_processing()
    
    def _initialize_realtime_processing(self):
        """Initialize real-time processing system."""
        self.realtime_active = True
        self.logger.info("Real-time analytics engine initialized")
    
    async def start_realtime_processing(self):
        """Start the real-time processing loop."""
        if not self.config.enable_realtime_analytics:
            return
        
        try:
            # Create async queue if not exists
            if self.realtime_queue is None:
                self.realtime_queue = asyncio.Queue(maxsize=1000)
            
            # Start processing loop
            self.realtime_task = asyncio.create_task(self._realtime_processing_loop())
            self.logger.info("Real-time processing loop started")
            
        except Exception as e:
            self.logger.error(f"Error starting real-time processing: {e}")
    
    async def stop_realtime_processing(self):
        """Stop the real-time processing loop."""
        self.realtime_active = False
        
        if self.realtime_task:
            self.realtime_task.cancel()
            try:
                await self.realtime_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Real-time processing loop stopped")
    
    async def _realtime_processing_loop(self):
        """Main real-time processing loop."""
        while self.realtime_active:
            try:
                # Wait for items with timeout
                try:
                    item = await asyncio.wait_for(self.realtime_queue.get(), timeout=1.0)
                    await self._process_realtime_item(item)
                    self.realtime_queue.task_done()
                except asyncio.TimeoutError:
                    continue  # No items, continue loop
                
            except Exception as e:
                self.logger.error(f"Error in real-time processing loop: {e}")
                await asyncio.sleep(1.0)
    
    async def _process_realtime_item(self, item: Dict[str, Any]):
        """Process a single real-time analytics item."""
        try:
            start_time = time.time()
            
            # Get processing callback based on item type
            item_type = item.get('type')
            callback = self.processing_callbacks.get(item_type)
            
            if not callback:
                self.logger.warning(f"No callback found for item type: {item_type}")
                return
            
            # Process item
            result = await callback(item['data'])
            
            # Update metrics
            processing_time = time.time() - start_time
            self._update_processing_metrics(processing_time, True)
            
            # Store result if needed
            if result:
                self._store_processing_result(result, item_type)
                
        except Exception as e:
            self.logger.error(f"Error processing real-time item: {e}")
            self._update_processing_metrics(0, False)
    
    def add_realtime_item(self, item_type: str, data: Any) -> bool:
        """Add item to real-time processing queue."""
        if not self.config.enable_realtime_analytics:
            return False
        
        try:
            # Initialize async queue if not already done
            if self.realtime_queue is None:
                try:
                    self.realtime_queue = asyncio.Queue(maxsize=1000)
                except RuntimeError:
                    # No event loop available
                    return False
            
            item = {
                'type': item_type, 
                'data': data, 
                'timestamp': datetime.now()
            }
            self.realtime_queue.put_nowait(item)
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding real-time item: {e}")
            return False
    
    def _update_processing_metrics(self, processing_time: float, success: bool):
        """Update real-time processing metrics."""
        if success:
            self.processing_metrics['items_processed'] += 1
            
            # Update average processing time
            if self.processing_metrics['average_processing_time'] == 0:
                self.processing_metrics['average_processing_time'] = processing_time
            else:
                # Exponential moving average
                alpha = 0.1
                self.processing_metrics['average_processing_time'] = (
                    alpha * processing_time + 
                    (1 - alpha) * self.processing_metrics['average_processing_time']
                )
        else:
            self.processing_metrics['processing_errors'] += 1
        
        self.processing_metrics['last_processing_time'] = datetime.now()
    
    def _store_processing_result(self, result: Any, result_type: str):
        """Store processing result for future use."""
        # Implementation depends on storage backend
        self.logger.debug(f"Processed {result_type} result: {type(result).__name__}")
    
    def get_processing_metrics(self) -> Dict[str, Any]:
        """Get real-time processing metrics."""
        return self.processing_metrics.copy()
    
    def is_processing_active(self) -> bool:
        """Check if real-time processing is active."""
        return self.realtime_active and self.realtime_queue is not None
    
    def get_queue_size(self) -> int:
        """Get current queue size."""
        if self.realtime_queue:
            return self.realtime_queue.qsize()
        return 0
