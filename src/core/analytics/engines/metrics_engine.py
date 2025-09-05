#!/usr/bin/env python3
"""
Metrics Engine - V2 Compliance Module
===================================

Handles analytics metrics collection and performance monitoring.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Performance metrics collection
- Analytics metrics tracking
- Performance monitoring
- Metrics reporting

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import time
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque

from ..vector_analytics_models import AnalyticsMetrics


class MetricsEngine:
    """
    Analytics metrics collection and monitoring engine.
    
    Provides comprehensive metrics tracking for analytics processing
    with performance monitoring and reporting capabilities.
    """
    
    def __init__(self, config):
        """Initialize metrics engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core metrics
        self.metrics = AnalyticsMetrics()
        
        # Performance tracking
        self.performance_history = deque(maxlen=1000)
        self.error_history = deque(maxlen=100)
        
        # Processing time tracking
        self.processing_times = defaultdict(list)
        self.batch_times = []
        
        # Initialize metrics
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Initialize metrics collection."""
        self.metrics.last_update = datetime.now()
        self.logger.info("Metrics engine initialized")
    
    def record_processing_time(self, processing_time: float, success: bool, operation_type: str = "general"):
        """Record processing time for an operation."""
        try:
            # Update core metrics
            if success:
                self.metrics.processed_insights += 1
            else:
                self.metrics.error_count += 1
            
            # Record processing time
            self.processing_times[operation_type].append(processing_time)
            
            # Update average processing time
            self._update_average_processing_time(processing_time)
            
            # Record in performance history
            self.performance_history.append({
                'timestamp': datetime.now(),
                'processing_time': processing_time,
                'success': success,
                'operation_type': operation_type
            })
            
            # Update success rate
            self.metrics.update_success_rate()
            self.metrics.last_update = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error recording processing time: {e}")
    
    def record_batch_processing(self, batch_size: int, results_count: int, processing_time: float):
        """Record batch processing metrics."""
        try:
            # Update core metrics
            self.metrics.processed_insights += results_count
            self.metrics.error_count += (batch_size - results_count)
            
            # Record batch time
            self.batch_times.append(processing_time)
            
            # Update average processing time per item
            time_per_item = processing_time / batch_size if batch_size > 0 else 0
            self._update_average_processing_time(time_per_item)
            
            # Update success rate
            self.metrics.update_success_rate()
            self.metrics.last_update = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error recording batch processing: {e}")
    
    def record_pattern_generation(self, pattern_count: int):
        """Record pattern generation metrics."""
        try:
            self.metrics.generated_patterns += pattern_count
            self.metrics.last_update = datetime.now()
        except Exception as e:
            self.logger.error(f"Error recording pattern generation: {e}")
    
    def record_prediction_made(self):
        """Record prediction generation metrics."""
        try:
            self.metrics.predictions_made += 1
            self.metrics.last_update = datetime.now()
        except Exception as e:
            self.logger.error(f"Error recording prediction: {e}")
    
    def record_anomaly_detected(self):
        """Record anomaly detection metrics."""
        try:
            self.metrics.anomalies_detected += 1
            self.metrics.last_update = datetime.now()
        except Exception as e:
            self.logger.error(f"Error recording anomaly: {e}")
    
    def record_optimization_cycle(self):
        """Record optimization cycle metrics."""
        try:
            self.metrics.optimization_cycles += 1
            self.metrics.last_update = datetime.now()
        except Exception as e:
            self.logger.error(f"Error recording optimization cycle: {e}")
    
    def record_error(self, error_type: str, error_message: str):
        """Record error metrics."""
        try:
            self.metrics.error_count += 1
            
            # Record in error history
            self.error_history.append({
                'timestamp': datetime.now(),
                'error_type': error_type,
                'error_message': error_message
            })
            
            # Update success rate
            self.metrics.update_success_rate()
            self.metrics.last_update = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error recording error metrics: {e}")
    
    def _update_average_processing_time(self, processing_time: float):
        """Update average processing time using exponential moving average."""
        try:
            if self.metrics.average_processing_time == 0:
                self.metrics.average_processing_time = processing_time
            else:
                # Exponential moving average
                alpha = 0.1
                self.metrics.average_processing_time = (
                    alpha * processing_time + 
                    (1 - alpha) * self.metrics.average_processing_time
                )
        except Exception as e:
            self.logger.error(f"Error updating average processing time: {e}")
    
    def get_metrics(self) -> AnalyticsMetrics:
        """Get current analytics metrics."""
        return self.metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics."""
        try:
            # Calculate performance statistics
            recent_performance = list(self.performance_history)[-100:]  # Last 100 operations
            
            if not recent_performance:
                return {'message': 'No performance data available'}
            
            processing_times = [p['processing_time'] for p in recent_performance]
            success_count = sum(1 for p in recent_performance if p['success'])
            
            return {
                'total_operations': len(recent_performance),
                'successful_operations': success_count,
                'success_rate': success_count / len(recent_performance) if recent_performance else 0,
                'average_processing_time': sum(processing_times) / len(processing_times) if processing_times else 0,
                'min_processing_time': min(processing_times) if processing_times else 0,
                'max_processing_time': max(processing_times) if processing_times else 0,
                'last_update': self.metrics.last_update.isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {'error': str(e)}
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary statistics."""
        try:
            recent_errors = list(self.error_history)[-50:]  # Last 50 errors
            
            if not recent_errors:
                return {'message': 'No error data available'}
            
            error_types = defaultdict(int)
            for error in recent_errors:
                error_types[error['error_type']] += 1
            
            return {
                'total_errors': len(recent_errors),
                'error_types': dict(error_types),
                'recent_errors': recent_errors[-10:],  # Last 10 errors
                'last_update': self.metrics.last_update.isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting error summary: {e}")
            return {'error': str(e)}
    
    def get_processing_time_breakdown(self) -> Dict[str, Any]:
        """Get processing time breakdown by operation type."""
        try:
            breakdown = {}
            for operation_type, times in self.processing_times.items():
                if times:
                    breakdown[operation_type] = {
                        'count': len(times),
                        'average_time': sum(times) / len(times),
                        'min_time': min(times),
                        'max_time': max(times)
                    }
            
            return breakdown
        except Exception as e:
            self.logger.error(f"Error getting processing time breakdown: {e}")
            return {'error': str(e)}
    
    def reset_metrics(self):
        """Reset all metrics to initial state."""
        try:
            self.metrics = AnalyticsMetrics()
            self.performance_history.clear()
            self.error_history.clear()
            self.processing_times.clear()
            self.batch_times.clear()
            self.logger.info("Metrics reset successfully")
        except Exception as e:
            self.logger.error(f"Error resetting metrics: {e}")
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export comprehensive metrics data."""
        try:
            return {
                'core_metrics': {
                    'processed_insights': self.metrics.processed_insights,
                    'generated_patterns': self.metrics.generated_patterns,
                    'predictions_made': self.metrics.predictions_made,
                    'anomalies_detected': self.metrics.anomalies_detected,
                    'optimization_cycles': self.metrics.optimization_cycles,
                    'error_count': self.metrics.error_count,
                    'success_rate': self.metrics.success_rate,
                    'average_processing_time': self.metrics.average_processing_time,
                    'last_update': self.metrics.last_update.isoformat()
                },
                'performance_summary': self.get_performance_summary(),
                'error_summary': self.get_error_summary(),
                'processing_breakdown': self.get_processing_time_breakdown()
            }
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
            return {'error': str(e)}
