#!/usr/bin/env python3
"""
Dashboard Shared Utilities - V2 Compliant
=========================================

Shared utilities for web dashboard functionality.
Consolidates common dashboard operations across multiple dashboard services.

V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DashboardUtilities:
    """Shared utilities for dashboard functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cache: Dict[str, Any] = {}
        self._cache_timeout = 30  # seconds
    
    def generate_chart_data(self, data: List[Dict[str, Any]], chart_type: str = "line") -> Dict[str, Any]:
        """Generate standardized chart data for visualizations.
        
        Args:
            data: Raw data points
            chart_type: Type of chart (line, bar, pie, etc.)
            
        Returns:
            Standardized chart data structure
        """
        try:
            if chart_type == "line":
                return self._generate_line_chart_data(data)
            elif chart_type == "bar":
                return self._generate_bar_chart_data(data)
            elif chart_type == "pie":
                return self._generate_pie_chart_data(data)
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
        except Exception as e:
            self.logger.error(f"Failed to generate chart data: {e}")
            return {"error": str(e)}
    
    def _generate_line_chart_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate line chart data."""
        return {
            "type": "line",
            "data": {
                "labels": [item.get("label", "") for item in data],
                "datasets": [{
                    "label": "Data",
                    "data": [item.get("value", 0) for item in data],
                    "borderColor": "#3b82f6",
                    "backgroundColor": "rgba(59, 130, 246, 0.1)"
                }]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {"beginAtZero": True}
                }
            }
        }
    
    def _generate_bar_chart_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate bar chart data."""
        return {
            "type": "bar",
            "data": {
                "labels": [item.get("label", "") for item in data],
                "datasets": [{
                    "label": "Data",
                    "data": [item.get("value", 0) for item in data],
                    "backgroundColor": "#10b981",
                    "borderColor": "#059669"
                }]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {"beginAtZero": True}
                }
            }
        }
    
    def _generate_pie_chart_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate pie chart data."""
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
        return {
            "type": "pie",
            "data": {
                "labels": [item.get("label", "") for item in data],
                "datasets": [{
                    "data": [item.get("value", 0) for item in data],
                    "backgroundColor": colors[:len(data)]
                }]
            },
            "options": {
                "responsive": True
            }
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics."""
        try:
            import psutil
            
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "timestamp": datetime.now().isoformat()
            }
        except ImportError:
            return {
                "cpu_percent": 0,
                "memory_percent": 0,
                "disk_percent": 0,
                "timestamp": datetime.now().isoformat(),
                "note": "psutil not available"
            }
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load dashboard configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Failed to load config from {config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default dashboard configuration."""
        return {
            "title": "Dashboard",
            "refresh_interval": 30,
            "theme": "light",
            "charts": {
                "default_type": "line",
                "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]
            },
            "alerts": {
                "enabled": True,
                "thresholds": {
                    "cpu": 80,
                    "memory": 85,
                    "disk": 90
                }
            }
        }
    
    def check_alert_conditions(self, metrics: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if alert conditions are met.
        
        Args:
            metrics: Current system metrics
            config: Dashboard configuration
            
        Returns:
            List of active alerts
        """
        alerts = []
        
        if not config.get("alerts", {}).get("enabled", True):
            return alerts
        
        thresholds = config.get("alerts", {}).get("thresholds", {})
        
        # Check CPU threshold
        if metrics.get("cpu_percent", 0) > thresholds.get("cpu", 80):
            alerts.append({
                "type": "warning",
                "message": f"High CPU usage: {metrics['cpu_percent']:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check memory threshold
        if metrics.get("memory_percent", 0) > thresholds.get("memory", 85):
            alerts.append({
                "type": "warning",
                "message": f"High memory usage: {metrics['memory_percent']:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check disk threshold
        if metrics.get("disk_percent", 0) > thresholds.get("disk", 90):
            alerts.append({
                "type": "critical",
                "message": f"High disk usage: {metrics['disk_percent']:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    def cache_data(self, key: str, data: Any, timeout: Optional[int] = None) -> None:
        """Cache data with optional timeout.
        
        Args:
            key: Cache key
            data: Data to cache
            timeout: Cache timeout in seconds
        """
        timeout = timeout or self._cache_timeout
        self._cache[key] = {
            "data": data,
            "timestamp": time.time(),
            "timeout": timeout
        }
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None if expired/not found
        """
        if key not in self._cache:
            return None
        
        cache_entry = self._cache[key]
        if time.time() - cache_entry["timestamp"] > cache_entry["timeout"]:
            del self._cache[key]
            return None
        
        return cache_entry["data"]
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
    
    def format_timestamp(self, timestamp: Optional[datetime] = None) -> str:
        """Format timestamp for display.
        
        Args:
            timestamp: Timestamp to format (defaults to now)
            
        Returns:
            Formatted timestamp string
        """
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")


# Global utility instance
_global_dashboard_utilities: Optional[DashboardUtilities] = None


def get_dashboard_utilities() -> DashboardUtilities:
    """Get or create the global dashboard utilities instance."""
    global _global_dashboard_utilities
    
    if _global_dashboard_utilities is None:
        _global_dashboard_utilities = DashboardUtilities()
    
    return _global_dashboard_utilities


# Convenience functions for backward compatibility
def generate_chart_data(data: List[Dict[str, Any]], chart_type: str = "line") -> Dict[str, Any]:
    """Generate chart data."""
    return get_dashboard_utilities().generate_chart_data(data, chart_type)


def get_system_metrics() -> Dict[str, Any]:
    """Get system metrics."""
    return get_dashboard_utilities().get_system_metrics()


def load_dashboard_config(config_path: str) -> Dict[str, Any]:
    """Load dashboard configuration."""
    return get_dashboard_utilities().load_config(config_path)

