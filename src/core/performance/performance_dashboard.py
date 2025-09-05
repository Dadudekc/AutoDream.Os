#!/usr/bin/env python3
"""
Performance Dashboard - V2 Compliance Module
============================================

Real-time performance monitoring dashboard and reporting system.
Provides comprehensive performance insights and analytics.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from .performance_monitoring_system import create_performance_monitoring_system


class PerformanceDashboard:
    """Real-time performance dashboard."""
    
    def __init__(self):
        """Initialize performance dashboard."""
        self.logger = logging.getLogger(__name__)
        self.monitor = create_performance_monitoring_system()
        self.optimizer = None  # Will be implemented later
        
        # Dashboard state
        self.dashboard_active = False
        self.refresh_interval = 5.0  # seconds
        
        # Performance history
        self.performance_history: List[Dict[str, Any]] = []
        self.max_history_size = 1000
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time performance metrics."""
        try:
            # Get current system metrics
            system_summary = self.monitor.get_performance_summary()
            
            # Get optimization summary
            optimization_summary = self.optimizer.get_optimization_summary()
            
            # Get recent metrics summary
            metrics_summary = self.monitor.get_metrics_summary(hours=1)
            
            # Combine all metrics
            real_time_data = {
                "timestamp": datetime.now().isoformat(),
                "system": system_summary,
                "optimization": optimization_summary,
                "metrics": metrics_summary,
                "status": "active" if system_summary.get("status") == "active" else "inactive"
            }
            
            # Store in history
            self._add_to_history(real_time_data)
            
            return real_time_data
            
        except Exception as e:
            self.logger.error(f"Error getting real-time metrics: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def get_performance_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance trends over time."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter history by time
            recent_history = [
                entry for entry in self.performance_history
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_time
            ]
            
            if not recent_history:
                return {"status": "no_data", "message": "No data available for the specified period"}
            
            # Extract trends
            timestamps = [entry["timestamp"] for entry in recent_history]
            cpu_values = [entry.get("system", {}).get("cpu_percent", 0) for entry in recent_history]
            memory_values = [entry.get("system", {}).get("memory_percent", 0) for entry in recent_history]
            
            # Calculate trends
            cpu_trend = self._calculate_trend(cpu_values)
            memory_trend = self._calculate_trend(memory_values)
            
            # Calculate averages
            avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
            avg_memory = sum(memory_values) / len(memory_values) if memory_values else 0
            
            # Calculate peaks
            max_cpu = max(cpu_values) if cpu_values else 0
            max_memory = max(memory_values) if memory_values else 0
            
            return {
                "status": "success",
                "period_hours": hours,
                "data_points": len(recent_history),
                "trends": {
                    "cpu": {
                        "trend": cpu_trend,
                        "average": avg_cpu,
                        "peak": max_cpu,
                        "current": cpu_values[-1] if cpu_values else 0
                    },
                    "memory": {
                        "trend": memory_trend,
                        "average": avg_memory,
                        "peak": max_memory,
                        "current": memory_values[-1] if memory_values else 0
                    }
                },
                "timestamps": timestamps,
                "cpu_values": cpu_values,
                "memory_values": memory_values
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance trends: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_optimization_report(self, hours: int = 24) -> Dict[str, Any]:
        """Get optimization performance report."""
        try:
            optimization_history = self.optimizer.get_optimization_history(hours)
            
            if not optimization_history:
                return {"status": "no_data", "message": "No optimization data available"}
            
            # Analyze optimization results
            successful_optimizations = [opt for opt in optimization_history if opt["success"]]
            failed_optimizations = [opt for opt in optimization_history if not opt["success"]]
            
            # Calculate statistics
            total_optimizations = len(optimization_history)
            success_rate = (len(successful_optimizations) / total_optimizations * 100) if total_optimizations > 0 else 0
            
            avg_improvement = (
                sum(opt["improvement_percent"] for opt in successful_optimizations) / 
                len(successful_optimizations)
            ) if successful_optimizations else 0
            
            # Group by rule
            rule_stats = {}
            for opt in optimization_history:
                rule_name = opt["rule_name"]
                if rule_name not in rule_stats:
                    rule_stats[rule_name] = {
                        "total": 0,
                        "successful": 0,
                        "failed": 0,
                        "avg_improvement": 0
                    }
                
                rule_stats[rule_name]["total"] += 1
                if opt["success"]:
                    rule_stats[rule_name]["successful"] += 1
                else:
                    rule_stats[rule_name]["failed"] += 1
            
            # Calculate average improvement per rule
            for rule_name, stats in rule_stats.items():
                rule_optimizations = [opt for opt in successful_optimizations if opt["rule_name"] == rule_name]
                if rule_optimizations:
                    stats["avg_improvement"] = sum(opt["improvement_percent"] for opt in rule_optimizations) / len(rule_optimizations)
            
            return {
                "status": "success",
                "period_hours": hours,
                "summary": {
                    "total_optimizations": total_optimizations,
                    "successful_optimizations": len(successful_optimizations),
                    "failed_optimizations": len(failed_optimizations),
                    "success_rate": success_rate,
                    "average_improvement": avg_improvement
                },
                "rule_statistics": rule_stats,
                "recent_optimizations": optimization_history[-10:]  # Last 10 optimizations
            }
            
        except Exception as e:
            self.logger.error(f"Error getting optimization report: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get current performance alerts."""
        try:
            alerts = []
            
            # Check system metrics for alerts
            if self.monitor.system_metrics:
                latest = self.monitor.system_metrics[-1]
                
                # CPU alert
                if latest.cpu_percent > 80:
                    alerts.append({
                        "type": "cpu_high",
                        "severity": "high" if latest.cpu_percent > 90 else "medium",
                        "message": f"High CPU usage: {latest.cpu_percent:.1f}%",
                        "value": latest.cpu_percent,
                        "threshold": 80,
                        "timestamp": latest.timestamp.isoformat()
                    })
                
                # Memory alert
                if latest.memory_percent > 85:
                    alerts.append({
                        "type": "memory_high",
                        "severity": "high" if latest.memory_percent > 95 else "medium",
                        "message": f"High memory usage: {latest.memory_percent:.1f}%",
                        "value": latest.memory_percent,
                        "threshold": 85,
                        "timestamp": latest.timestamp.isoformat()
                    })
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting performance alerts: {e}")
            return []
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary."""
        try:
            real_time = self.get_real_time_metrics()
            trends = self.get_performance_trends(hours=1)
            optimization = self.get_optimization_report(hours=1)
            alerts = self.get_performance_alerts()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "real_time_metrics": real_time,
                "performance_trends": trends,
                "optimization_report": optimization,
                "alerts": alerts,
                "dashboard_status": "active"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard summary: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "dashboard_status": "error",
                "error": str(e)
            }
    
    def _add_to_history(self, data: Dict[str, Any]):
        """Add data to performance history."""
        self.performance_history.append(data)
        
        # Keep only recent history
        if len(self.performance_history) > self.max_history_size:
            self.performance_history = self.performance_history[-self.max_history_size:]
    
    def export_performance_data(self, hours: int = 24) -> str:
        """Export performance data as JSON."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_data = [
                entry for entry in self.performance_history
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_time
            ]
            return json.dumps(recent_data, indent=2)
        except Exception as e:
            self.logger.error(f"Error exporting performance data: {e}")
            return json.dumps({"error": str(e)})


# Global dashboard instance
_dashboard: Optional[PerformanceDashboard] = None


def get_performance_dashboard() -> PerformanceDashboard:
    """Get global performance dashboard instance."""
    global _dashboard
    if _dashboard is None:
        _dashboard = PerformanceDashboard()
    return _dashboard
