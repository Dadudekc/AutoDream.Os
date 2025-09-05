#!/usr/bin/env python3
"""
Batch Analytics Engine - V2 Compliance Module
============================================

Handles batch analytics processing with parallel execution capabilities.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Batch processing coordination
- Parallel execution management
- Batch metrics tracking
- Performance optimization

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import time
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from ..vector_analytics_models import VectorAnalyticsConfig


class BatchAnalyticsEngine:
    """
    Batch analytics processing engine.
    
    Handles batch processing of analytics items with parallel execution
    and performance optimization.
    """
    
    def __init__(self, config: VectorAnalyticsConfig, processing_callbacks: Dict[str, Callable]):
        """Initialize batch analytics engine."""
        self.config = config
        self.processing_callbacks = processing_callbacks
        self.logger = logging.getLogger(__name__)
        
        # Processing state
        self.batch_queue = []
        self.batch_active = False
        self.batch_timer = None
        self.processing_lock = threading.Lock()
        
        # Thread pools
        self.thread_pool = ThreadPoolExecutor(max_workers=config.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=config.max_workers) if config.enable_parallel_processing else None
        
        # Metrics
        self.batch_metrics = {
            'batches_processed': 0,
            'items_processed': 0,
            'processing_errors': 0,
            'average_batch_time': 0.0,
            'last_batch_time': None
        }
        
        # Initialize if batch processing is enabled
        if config.analytics_mode.value in ['batch', 'hybrid']:
            self._initialize_batch_processing()
    
    def _initialize_batch_processing(self):
        """Initialize batch processing system."""
        self.batch_active = True
        self.batch_processing_interval = self.config.update_interval * 10  # 10x slower than real-time
        
        # Start batch processing timer
        self._schedule_next_batch()
        self.logger.info("Batch analytics engine initialized")
    
    def _schedule_next_batch(self):
        """Schedule the next batch processing cycle."""
        if self.batch_active:
            self.batch_timer = threading.Timer(
                self.batch_processing_interval, 
                self._batch_processing_cycle
            )
            self.batch_timer.daemon = True
            self.batch_timer.start()
    
    def _batch_processing_cycle(self):
        """Execute batch processing cycle."""
        try:
            if self.batch_queue:
                self.logger.info(f"Starting batch processing cycle with {len(self.batch_queue)} items")
                
                # Process items in batches
                batch_size = self.config.batch_size
                for i in range(0, len(self.batch_queue), batch_size):
                    batch = self.batch_queue[i:i + batch_size]
                    self._process_batch(batch)
                
                # Clear processed items
                with self.processing_lock:
                    self.batch_queue.clear()
            
            # Schedule next cycle
            self._schedule_next_batch()
                
        except Exception as e:
            self.logger.error(f"Error in batch processing cycle: {e}")
            self._schedule_next_batch()
    
    def _process_batch(self, batch: List[Dict[str, Any]]):
        """Process a batch of analytics items."""
        if not batch:
            return
        
        start_time = time.time()
        results = []
        
        try:
            # Use parallel processing if enabled
            if self.process_pool and len(batch) > 1:
                futures = []
                for item in batch:
                    future = self.process_pool.submit(self._process_batch_item, item)
                    futures.append(future)
                
                # Collect results
                for future in as_completed(futures, timeout=self.config.timeout_seconds):
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception as e:
                        self.logger.error(f"Error processing batch item: {e}")
            else:
                # Sequential processing
                for item in batch:
                    result = self._process_batch_item(item)
                    if result:
                        results.append(result)
            
            # Update metrics
            processing_time = time.time() - start_time
            self._update_batch_metrics(len(batch), len(results), processing_time)
            
            # Store results
            for result in results:
                self._store_processing_result(result, 'batch')
                
        except Exception as e:
            self.logger.error(f"Error processing batch: {e}")
    
    def _process_batch_item(self, item: Dict[str, Any]) -> Optional[Any]:
        """Process a single batch item."""
        try:
            item_type = item.get('type')
            data = item.get('data')
            
            callback = self.processing_callbacks.get(item_type)
            if callback:
                return callback(data)
            else:
                self.logger.warning(f"No callback found for item type: {item_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error processing batch item: {e}")
            return None
    
    def add_batch_item(self, item_type: str, data: Any) -> bool:
        """Add item to batch processing queue."""
        try:
            with self.processing_lock:
                item = {
                    'type': item_type, 
                    'data': data, 
                    'timestamp': datetime.now()
                }
                self.batch_queue.append(item)
                return True
        except Exception as e:
            self.logger.error(f"Error adding batch item: {e}")
            return False
    
    def _update_batch_metrics(self, batch_size: int, results_count: int, processing_time: float):
        """Update batch processing metrics."""
        self.batch_metrics['batches_processed'] += 1
        self.batch_metrics['items_processed'] += results_count
        self.batch_metrics['processing_errors'] += (batch_size - results_count)
        
        # Update average batch processing time
        time_per_item = processing_time / batch_size if batch_size > 0 else 0
        if self.batch_metrics['average_batch_time'] == 0:
            self.batch_metrics['average_batch_time'] = time_per_item
        else:
            alpha = 0.1
            self.batch_metrics['average_batch_time'] = (
                alpha * time_per_item + 
                (1 - alpha) * self.batch_metrics['average_batch_time']
            )
        
        self.batch_metrics['last_batch_time'] = datetime.now()
    
    def _store_processing_result(self, result: Any, result_type: str):
        """Store processing result for future use."""
        # Implementation depends on storage backend
        self.logger.debug(f"Processed {result_type} result: {type(result).__name__}")
    
    def get_batch_metrics(self) -> Dict[str, Any]:
        """Get batch processing metrics."""
        return self.batch_metrics.copy()
    
    def get_queue_size(self) -> int:
        """Get current batch queue size."""
        with self.processing_lock:
            return len(self.batch_queue)
    
    def is_processing_active(self) -> bool:
        """Check if batch processing is active."""
        return self.batch_active
    
    def shutdown(self):
        """Shutdown batch processing engine gracefully."""
        self.logger.info("Shutting down batch analytics engine...")
        
        # Stop batch processing
        self.batch_active = False
        if self.batch_timer:
            self.batch_timer.cancel()
        
        # Shutdown thread pools
        self.thread_pool.shutdown(wait=True)
        if self.process_pool:
            self.process_pool.shutdown(wait=True)
        
        self.logger.info("Batch analytics engine shutdown complete")
