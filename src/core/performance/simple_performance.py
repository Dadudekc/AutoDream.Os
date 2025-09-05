#!/usr/bin/env python3
"""
Simple Performance Monitor - KISS Compliant
==========================================

Simple performance monitoring utilities.
KISS PRINCIPLE: Keep It Simple, Stupid.

Author: Agent-6 - Coordination & Communication Specialist
License: MIT
"""

import time
import psutil
from datetime import datetime
from typing import Dict, Any


class SimplePerformanceMonitor:
    """Simple performance monitoring."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
    
    def get_cpu_usage(self) -> float:
        """Get CPU usage percentage."""
        return psutil.cpu_percent()
    
    def get_memory_usage(self) -> float:
        """Get memory usage percentage."""
        return psutil.virtual_memory().percent
    
    def get_disk_usage(self) -> float:
        """Get disk usage percentage."""
        return psutil.disk_usage('/').percent
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        return {
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage": self.get_memory_usage(),
            "disk_usage": self.get_disk_usage(),
            "timestamp": datetime.now()
        }
    
    def log_metric(self, name: str, value: Any):
        """Log a performance metric."""
        self.metrics[name] = {
            "value": value,
            "timestamp": datetime.now()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all logged metrics."""
        return self.metrics.copy()
