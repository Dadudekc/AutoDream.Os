#!/usr/bin/env python3
"""
Vector Database Monitoring V2
=============================

V2 compliant monitoring system for vector database operations.
"""

import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """A single metric data point."""
    timestamp: float
    value: float
    tags: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'value': self.value,
            'tags': self.tags
        }


@dataclass
class HealthStatus:
    """Health status information."""
    healthy: bool
    timestamp: float
    details: Dict[str, Any]
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'healthy': self.healthy,
            'timestamp': self.timestamp,
            'details': self.details,
            'error_message': self.error_message
        }


class MetricsCollector:
    """Collects and stores metrics."""
    
    def __init__(self, max_metrics: int = 1000):
        self.max_metrics = max_metrics
        self.metrics: List[MetricPoint] = []
    
    def add_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        """Add a metric point."""
        metric = MetricPoint(
            timestamp=time.time(),
            value=value,
            tags={'metric': name, **(tags or {})}
        )
        
        self.metrics.append(metric)
        
        # Keep only recent metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
    
    def get_metrics(self, metric_name: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metrics, optionally filtered by name."""
        filtered_metrics = self.metrics
        
        if metric_name:
            filtered_metrics = [
                m for m in self.metrics 
                if m.tags.get('metric') == metric_name
            ]
        
        return [m.to_dict() for m in filtered_metrics[-limit:]]


class VectorDatabaseMonitoring:
    """V2 compliant vector database monitoring system."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.health_checks = []
        self.start_time = time.time()
        logger.info("VectorDatabaseMonitoring V2 initialized")
    
    def record_operation_metric(
        self, 
        operation_type: str, 
        duration: float, 
        success: bool
    ):
        """Record operation metrics."""
        self.metrics_collector.add_metric(
            'operation_duration',
            duration,
            {
                'operation_type': operation_type,
                'success': str(success)
            }
        )
        
        self.metrics_collector.add_metric(
            'operation_count',
            1,
            {
                'operation_type': operation_type,
                'success': str(success)
            }
        )
    
    def record_connection_metric(self, active_connections: int):
        """Record connection metrics."""
        self.metrics_collector.add_metric(
            'active_connections',
            float(active_connections)
        )
    
    def record_query_metric(self, query_type: str, result_count: int, duration: float):
        """Record query metrics."""
        self.metrics_collector.add_metric(
            'query_result_count',
            float(result_count),
            {'query_type': query_type}
        )
        
        self.metrics_collector.add_metric(
            'query_duration',
            duration,
            {'query_type': query_type}
        )
    
    def add_health_check(self, name: str, status: HealthStatus):
        """Add a health check result."""
        health_data = {
            'name': name,
            'status': status.to_dict(),
            'timestamp': time.time()
        }
        self.health_checks.append(health_data)
        
        # Keep only recent health checks
        if len(self.health_checks) > 100:
            self.health_checks = self.health_checks[-100:]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        uptime = time.time() - self.start_time
        
        all_metrics = self.metrics_collector.get_metrics()
        
        # Calculate summary statistics
        operation_metrics = self.metrics_collector.get_metrics('operation_duration')
        avg_duration = 0.0
        if operation_metrics:
            avg_duration = sum(m['value'] for m in operation_metrics) / len(operation_metrics)
        
        return {
            'uptime_seconds': uptime,
            'total_metrics': len(all_metrics),
            'health_checks': len(self.health_checks),
            'average_operation_duration': avg_duration,
            'metrics_collected': len(all_metrics)
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status."""
        if not self.health_checks:
            return {
                'overall_healthy': True,
                'checks': [],
                'message': 'No health checks performed yet'
            }
        
        recent_checks = self.health_checks[-10:]  # Last 10 checks
        healthy_count = sum(
            1 for check in recent_checks 
            if check['status']['healthy']
        )
        
        overall_healthy = healthy_count == len(recent_checks)
        
        return {
            'overall_healthy': overall_healthy,
            'healthy_checks': healthy_count,
            'total_checks': len(recent_checks),
            'recent_checks': recent_checks
        }
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed metrics data."""
        return {
            'summary': self.get_metrics_summary(),
            'health': self.get_health_status(),
            'recent_metrics': self.metrics_collector.get_metrics(limit=50)
        }
