#!/usr/bin/env python3
"""
Performance Tracker - Validation System Performance Monitoring

This module provides performance tracking functionality for the validation system,
extracted from the main unified validation system to achieve V2 compliance.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance - File size optimization
"""

import time
import psutil
from typing import Dict, Any
from datetime import datetime


class PerformanceTracker:
    """
    Performance tracking for validation operations.
    
    This class provides comprehensive performance monitoring
    while maintaining V2 compliance through focused responsibility.
    """
    
    def __init__(self):
        """Initialize the performance tracker."""
        self.total_validations = 0
        self.total_validation_time = 0.0
        self.start_time = time.time()
    
    def start_validation(self) -> Dict[str, Any]:
        """
        Start performance tracking for a validation operation.
        
        Returns:
            Dictionary with start metrics
        """
        return {
            'start_time': time.time(),
            'start_memory_kb': psutil.Process().memory_info().rss / 1024
        }
    
    def end_validation(self, start_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        End performance tracking for a validation operation.
        
        Args:
            start_metrics: Metrics from start_validation()
            
        Returns:
            Dictionary with performance metrics
        """
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024  # KB
        
        validation_time_ms = (end_time - start_metrics['start_time']) * 1000
        memory_usage_kb = end_memory - start_metrics['start_memory_kb']
        
        # Update tracking
        self.total_validations += 1
        self.total_validation_time += validation_time_ms
        
        return {
            'validation_time_ms': validation_time_ms,
            'memory_usage_kb': memory_usage_kb,
            'total_validations': self.total_validations,
            'total_validation_time_ms': self.total_validation_time
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        avg_time = (self.total_validation_time / self.total_validations 
                   if self.total_validations > 0 else 0)
        
        return {
            'total_validations': self.total_validations,
            'total_validation_time_ms': self.total_validation_time,
            'average_validation_time_ms': avg_time,
            'uptime_seconds': time.time() - self.start_time
        }
    
    def reset_performance_stats(self) -> None:
        """Reset performance statistics."""
        self.total_validations = 0
        self.total_validation_time = 0.0
        self.start_time = time.time()
    
    def log_performance_metrics(self, result: Any, metrics: Dict[str, Any]) -> None:
        """
        Log performance metrics to validation result.
        
        Args:
            result: Validation result object
            metrics: Performance metrics from end_validation()
        """
        if hasattr(result, 'validation_time_ms'):
            result.validation_time_ms = metrics['validation_time_ms']
        if hasattr(result, 'memory_usage_kb'):
            result.memory_usage_kb = metrics['memory_usage_kb']
        if hasattr(result, 'validator_version'):
            result.validator_version = "2.0.0"
