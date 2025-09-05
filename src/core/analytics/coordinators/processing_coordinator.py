#!/usr/bin/env python3
"""
Processing Coordinator - V2 Compliance Module
===========================================

Coordinates data processing workflows between processors and engines.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Processing workflow coordination
- Processor management
- Data flow orchestration
- Error handling and recovery

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import time
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from ..vector_analytics_models import AnalyticsInsight, PatternMatch, PredictionResult


class ProcessingCoordinator:
    """
    Processing workflow coordinator.
    
    Coordinates data processing workflows between processors and engines
    with comprehensive error handling and performance optimization.
    """
    
    def __init__(self, config, insight_processor, pattern_processor, 
                 prediction_processor, caching_engine, metrics_engine):
        """Initialize processing coordinator."""
        self.config = config
        self.insight_processor = insight_processor
        self.pattern_processor = pattern_processor
        self.prediction_processor = prediction_processor
        self.caching_engine = caching_engine
        self.metrics_engine = metrics_engine
        self.logger = logging.getLogger(__name__)
        
        # Processing state
        self.processing_stats = {
            'total_processed': 0,
            'successful_processed': 0,
            'failed_processed': 0,
            'average_processing_time': 0.0
        }
    
    def process_insight(self, data: Dict[str, Any]) -> Optional[AnalyticsInsight]:
        """Process analytics insight with full workflow coordination."""
        start_time = time.time()
        
        try:
            # Validate input
            if not self._validate_insight_input(data):
                self._record_processing_error('insight', 'Invalid input data')
                return None
            
            # Process insight
            result = self.insight_processor.process_insight(data)
            
            # Record metrics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, result is not None)
            
            if result:
                self.metrics_engine.record_processing_time(processing_time, True, 'insight')
                self.logger.debug(f"Processed insight: {result.insight_id}")
            else:
                self.metrics_engine.record_processing_time(processing_time, False, 'insight')
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._record_processing_error('insight', str(e))
            self.metrics_engine.record_processing_time(processing_time, False, 'insight')
            return None
    
    def process_patterns(self, data: List[Any]) -> List[PatternMatch]:
        """Process pattern detection with full workflow coordination."""
        start_time = time.time()
        
        try:
            # Validate input
            if not self._validate_pattern_input(data):
                self._record_processing_error('pattern', 'Invalid input data')
                return []
            
            # Process patterns
            results = self.pattern_processor.detect_patterns(data)
            
            # Record metrics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, len(results) > 0)
            
            if results:
                self.metrics_engine.record_pattern_generation(len(results))
                self.metrics_engine.record_processing_time(processing_time, True, 'pattern')
                self.logger.debug(f"Detected {len(results)} patterns")
            else:
                self.metrics_engine.record_processing_time(processing_time, False, 'pattern')
            
            return results
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._record_processing_error('pattern', str(e))
            self.metrics_engine.record_processing_time(processing_time, False, 'pattern')
            return []
    
    def process_prediction(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Process prediction generation with full workflow coordination."""
        start_time = time.time()
        
        try:
            # Validate input
            if not self._validate_prediction_input(data):
                self._record_processing_error('prediction', 'Invalid input data')
                return None
            
            # Process prediction
            result = self.prediction_processor.generate_prediction(data)
            
            # Record metrics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, result is not None)
            
            if result:
                self.metrics_engine.record_prediction_made()
                self.metrics_engine.record_processing_time(processing_time, True, 'prediction')
                self.logger.debug(f"Generated prediction: {result.prediction_id}")
            else:
                self.metrics_engine.record_processing_time(processing_time, False, 'prediction')
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._record_processing_error('prediction', str(e))
            self.metrics_engine.record_processing_time(processing_time, False, 'prediction')
            return None
    
    def process_batch(self, items: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """Process a batch of items with workflow coordination."""
        start_time = time.time()
        
        try:
            results = {
                'insights': [],
                'patterns': [],
                'predictions': [],
                'errors': []
            }
            
            for item in items:
                try:
                    item_type = item.get('type')
                    data = item.get('data')
                    
                    if item_type == 'insight':
                        result = self.process_insight(data)
                        if result:
                            results['insights'].append(result)
                    elif item_type == 'pattern':
                        result = self.process_patterns(data)
                        if result:
                            results['patterns'].extend(result)
                    elif item_type == 'prediction':
                        result = self.process_prediction(data)
                        if result:
                            results['predictions'].append(result)
                    else:
                        results['errors'].append(f"Unknown item type: {item_type}")
                        
                except Exception as e:
                    error_msg = f"Error processing item: {str(e)}"
                    results['errors'].append(error_msg)
                    self.logger.error(error_msg)
            
            # Record batch metrics
            processing_time = time.time() - start_time
            total_results = len(results['insights']) + len(results['patterns']) + len(results['predictions'])
            self.metrics_engine.record_batch_processing(len(items), total_results, processing_time)
            
            self.logger.info(f"Processed batch: {len(items)} items, {total_results} results")
            return results
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._record_processing_error('batch', str(e))
            self.metrics_engine.record_processing_time(processing_time, False, 'batch')
            return {'errors': [str(e)]}
    
    def _validate_insight_input(self, data: Dict[str, Any]) -> bool:
        """Validate insight input data."""
        try:
            return (isinstance(data, dict) and 
                    data and 
                    self.insight_processor.validate_insight_data(data))
        except Exception as e:
            self.logger.error(f"Error validating insight input: {e}")
            return False
    
    def _validate_pattern_input(self, data: List[Any]) -> bool:
        """Validate pattern input data."""
        try:
            return (isinstance(data, list) and 
                    len(data) >= 2 and 
                    any(item is not None and item != "" for item in data))
        except Exception as e:
            self.logger.error(f"Error validating pattern input: {e}")
            return False
    
    def _validate_prediction_input(self, data: Dict[str, Any]) -> bool:
        """Validate prediction input data."""
        try:
            return (isinstance(data, dict) and 
                    data and 
                    self.prediction_processor.validate_prediction_data(data))
        except Exception as e:
            self.logger.error(f"Error validating prediction input: {e}")
            return False
    
    def _record_processing_error(self, processing_type: str, error_message: str):
        """Record processing error."""
        self.processing_stats['failed_processed'] += 1
        self.metrics_engine.record_error(processing_type, error_message)
        self.logger.error(f"Processing error ({processing_type}): {error_message}")
    
    def _update_processing_stats(self, processing_time: float, success: bool):
        """Update processing statistics."""
        self.processing_stats['total_processed'] += 1
        
        if success:
            self.processing_stats['successful_processed'] += 1
        else:
            self.processing_stats['failed_processed'] += 1
        
        # Update average processing time
        if self.processing_stats['average_processing_time'] == 0:
            self.processing_stats['average_processing_time'] = processing_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.processing_stats['average_processing_time'] = (
                alpha * processing_time + 
                (1 - alpha) * self.processing_stats['average_processing_time']
            )
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.processing_stats.copy()
    
    def get_processor_stats(self) -> Dict[str, Any]:
        """Get individual processor statistics."""
        return {
            'insight_processor': self.insight_processor.get_processing_stats(),
            'pattern_processor': self.pattern_processor.get_processing_stats(),
            'prediction_processor': self.prediction_processor.get_processing_stats()
        }
    
    def reset_stats(self):
        """Reset all processing statistics."""
        self.processing_stats = {
            'total_processed': 0,
            'successful_processed': 0,
            'failed_processed': 0,
            'average_processing_time': 0.0
        }
        
        # Reset individual processor stats
        self.insight_processor.reset_stats()
        self.pattern_processor.reset_stats()
        self.prediction_processor.reset_stats()
        
        self.logger.info("Processing statistics reset")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get processing health status."""
        try:
            success_rate = 0.0
            if self.processing_stats['total_processed'] > 0:
                success_rate = self.processing_stats['successful_processed'] / self.processing_stats['total_processed']
            
            return {
                'total_processed': self.processing_stats['total_processed'],
                'success_rate': success_rate,
                'average_processing_time': self.processing_stats['average_processing_time'],
                'health_status': 'healthy' if success_rate > 0.8 else 'degraded' if success_rate > 0.5 else 'unhealthy',
                'last_update': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting health status: {e}")
            return {'health_status': 'error', 'error': str(e)}
