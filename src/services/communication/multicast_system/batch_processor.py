#!/usr/bin/env python3
"""
Multicast Batch Processor
=========================

Message batching and processing for the multicast routing system.

**Author:** Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
**Contract:** COORD-012 - Advanced Coordination Protocol Implementation
**Status:** MODULARIZED
**Target:** 1000+ msg/sec throughput (10x improvement)
"""

import asyncio
import threading
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import (
    Message, MessageBatch, RoutingStrategy, MessagePriority,
    BatchConfiguration, RoutingMetrics
)

class MessageBatchProcessor:
    """
    Handles message batching and processing for optimal throughput
    
    Features:
    - Intelligent message grouping
    - Dynamic batch sizing
    - Priority-based processing
    - Performance optimization
    """
    
    def __init__(self, config: BatchConfiguration):
        self.config = config
        self.batches: Dict[str, MessageBatch] = {}
        self.active_batches: Set[str] = set()
        self.completed_batches: Set[str] = set()
        self.failed_batches: Set[str] = set()
        
        # Processing state
        self.is_processing = False
        self.total_batches_processed = 0
        self.total_messages_processed = 0
        self.batch_timings: Dict[str, float] = {}
        
        # Performance tracking
        self.start_time: Optional[datetime] = None
        self.throughput_history: List[float] = []
        self.batch_efficiency_history: List[float] = []
        
        # Threading support
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.lock = threading.Lock()
        self.processing_thread: Optional[threading.Thread] = None
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    def create_batch(self, messages: List[Message], strategy: Optional[RoutingStrategy] = None) -> MessageBatch:
        """Create a new message batch"""
        batch_id = str(uuid.uuid4())
        strategy = strategy or self.config.strategy
        
        batch = MessageBatch(
            batch_id=batch_id,
            messages=messages,
            strategy=strategy,
            max_size=self.config.max_batch_size,
            priority_threshold=self.config.priority_threshold,
            time_window=self.config.time_window,
            start_time=datetime.now()
        )
        
        with self.lock:
            self.batches[batch_id] = batch
            self.active_batches.add(batch_id)
        
        self.logger.info(f"Created batch {batch_id} with {len(messages)} messages")
        return batch
    
    def add_message_to_batch(self, message: Message, batch_id: Optional[str] = None) -> str:
        """Add a message to an existing batch or create a new one"""
        if batch_id and batch_id in self.batches:
            batch = self.batches[batch_id]
            if len(batch.messages) < batch.max_size:
                batch.messages.append(message)
                self.logger.debug(f"Added message to existing batch {batch_id}")
                return batch_id
        
        # Create new batch for this message
        new_batch = self.create_batch([message])
        return new_batch.batch_id
    
    def process_batch(self, batch_id: str) -> Dict:
        """Process a specific batch of messages"""
        if batch_id not in self.batches:
            return {'error': f'Batch {batch_id} not found'}
        
        batch = self.batches[batch_id]
        if batch.status != "pending":
            return {'error': f'Batch {batch_id} is not in pending status'}
        
        try:
            start_time = time.time()
            batch.status = "processing"
            
            # Process messages based on strategy
            if batch.strategy == RoutingStrategy.PRIORITY_BASED:
                results = self._process_priority_based(batch)
            elif batch.strategy == RoutingStrategy.LOAD_BALANCED:
                results = self._process_load_balanced(batch)
            else:
                results = self._process_standard(batch)
            
            # Update batch status
            processing_time = time.time() - start_time
            batch.completion_time = datetime.now()
            batch.total_processing_time = processing_time
            batch.throughput = len(batch.messages) / max(processing_time, 0.001)
            batch.status = "completed"
            
            # Update tracking
            with self.lock:
                self.active_batches.discard(batch_id)
                self.completed_batches.add(batch_id)
                self.batch_timings[batch_id] = processing_time
                self.total_batches_processed += 1
                self.total_messages_processed += len(batch.messages)
            
            # Update performance history
            self._update_performance_metrics(batch)
            
            self.logger.info(f"Batch {batch_id} processed successfully in {processing_time:.3f}s")
            return {
                'batch_id': batch_id,
                'status': 'completed',
                'processing_time': processing_time,
                'throughput': batch.throughput,
                'results': results
            }
            
        except Exception as e:
            batch.status = "failed"
            batch.failure_count = len(batch.messages)
            
            with self.lock:
                self.active_batches.discard(batch_id)
                self.failed_batches.add(batch_id)
            
            self.logger.error(f"Error processing batch {batch_id}: {e}")
            return {'error': str(e), 'batch_id': batch_id}
    
    def _process_priority_based(self, batch: MessageBatch) -> Dict:
        """Process batch using priority-based strategy"""
        # Sort messages by priority (highest first)
        sorted_messages = sorted(batch.messages, key=lambda m: m.priority.value, reverse=True)
        
        results = {
            'high_priority': 0,
            'normal_priority': 0,
            'low_priority': 0,
            'total_processed': 0
        }
        
        for message in sorted_messages:
            if message.priority in [MessagePriority.URGENT, MessagePriority.CRITICAL]:
                results['high_priority'] += 1
            elif message.priority in [MessagePriority.HIGH, MessagePriority.NORMAL]:
                results['normal_priority'] += 1
            else:
                results['low_priority'] += 1
            
            results['total_processed'] += 1
            batch.success_count += 1
        
        return results
    
    def _process_load_balanced(self, batch: MessageBatch) -> Dict:
        """Process batch using load-balanced strategy"""
        # Simulate load balancing by processing messages in smaller chunks
        chunk_size = max(1, len(batch.messages) // 4)
        results = {
            'chunks_processed': 0,
            'messages_per_chunk': chunk_size,
            'total_processed': 0
        }
        
        for i in range(0, len(batch.messages), chunk_size):
            chunk = batch.messages[i:i + chunk_size]
            # Process chunk (simulated)
            time.sleep(0.001)  # Simulate processing time
            results['chunks_processed'] += 1
            results['total_processed'] += len(chunk)
            batch.success_count += len(chunk)
        
        return results
    
    def _process_standard(self, batch: MessageBatch) -> Dict:
        """Process batch using standard strategy"""
        results = {
            'total_processed': 0,
            'processing_efficiency': 0.0
        }
        
        for message in batch.messages:
            # Simulate message processing
            time.sleep(0.001)  # Simulate processing time
            batch.success_count += 1
            results['total_processed'] += 1
        
        results['processing_efficiency'] = (results['total_processed'] / len(batch.messages)) * 100
        return results
    
    def _update_performance_metrics(self, batch: MessageBatch) -> None:
        """Update performance tracking metrics"""
        # Update throughput history
        self.throughput_history.append(batch.throughput)
        if len(self.throughput_history) > 100:  # Keep last 100 entries
            self.throughput_history.pop(0)
        
        # Update batch efficiency history
        efficiency = (batch.success_count / len(batch.messages)) * 100
        self.batch_efficiency_history.append(efficiency)
        if len(self.batch_efficiency_history) > 100:
            self.batch_efficiency_history.pop(0)
    
    def get_batch_metrics(self) -> Dict:
        """Get current batch processing metrics"""
        with self.lock:
            total_batches = len(self.batches)
            active_batches = len(self.active_batches)
            completed_batches = len(self.completed_batches)
            failed_batches = len(self.failed_batches)
            
            avg_throughput = 0.0
            if self.throughput_history:
                avg_throughput = sum(self.throughput_history) / len(self.throughput_history)
            
            avg_efficiency = 0.0
            if self.batch_efficiency_history:
                avg_efficiency = sum(self.batch_efficiency_history) / len(self.batch_efficiency_history)
            
            return {
                'total_batches': total_batches,
                'active_batches': active_batches,
                'completed_batches': completed_batches,
                'failed_batches': failed_batches,
                'total_messages_processed': self.total_messages_processed,
                'average_throughput': avg_throughput,
                'average_efficiency': avg_efficiency,
                'success_rate': (completed_batches / max(total_batches, 1)) * 100
            }
    
    def cleanup_completed_batches(self, max_age_hours: int = 24) -> int:
        """Clean up old completed batches to free memory"""
        current_time = datetime.now()
        cleaned_count = 0
        
        with self.lock:
            for batch_id in list(self.completed_batches):
                batch = self.batches[batch_id]
                if batch.completion_time:
                    age_hours = (current_time - batch.completion_time).total_seconds() / 3600
                    if age_hours > max_age_hours:
                        del self.batches[batch_id]
                        self.completed_batches.discard(batch_id)
                        cleaned_count += 1
        
        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} old completed batches")
        
        return cleaned_count
    
    def shutdown(self) -> None:
        """Shutdown the batch processor"""
        self.is_processing = False
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=5.0)
        
        self.executor.shutdown(wait=True)
        
        # Clean up all batches
        self.cleanup_completed_batches(max_age_hours=0)
        
        self.logger.info("Message batch processor shutdown complete")
