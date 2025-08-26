#!/usr/bin/env python3
"""
Gaming Performance Monitor - Agent Cellphone V2

Monitors gaming system performance and integrates with core performance infrastructure.
Provides real-time gaming metrics, performance tracking, and alert generation.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3C - Gaming Systems Integration
V2 Standards: ≤200 LOC, SRP, OOP principles
"""

import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Core infrastructure imports
from ..core.managers.performance_manager import PerformanceManager
from ..core.performance.alerts import AlertSeverity, AlertType


@dataclass
class GamingPerformanceMetrics:
    """Gaming performance metrics for monitoring"""
    system_id: str
    frame_rate: float
    response_time: float
    memory_usage: float
    cpu_usage: float
    gpu_usage: float
    network_latency: float
    game_state: str
    performance_score: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class GamingPerformanceMonitor:
    """
    Gaming Performance Monitor - TASK 3C
    
    Monitors gaming system performance and integrates with:
    - Core performance monitoring infrastructure
    - Alert management system
    - Performance reporting
    """
    
    def __init__(self, performance_manager: PerformanceManager):
        self.performance_manager = performance_manager
        self.logger = logging.getLogger(f"{__name__}.GamingPerformanceMonitor")
        
        # Performance tracking
        self.performance_history: Dict[str, List[GamingPerformanceMetrics]] = {}
        self.monitoring_active = False
        self.monitoring_interval = 5  # seconds
        
        # Performance thresholds
        self.performance_thresholds = {
            "frame_rate": {"warning": 30.0, "error": 15.0, "critical": 5.0},
            "response_time": {"warning": 100.0, "error": 200.0, "critical": 500.0},
            "memory_usage": {"warning": 2048.0, "error": 4096.0, "critical": 8192.0},
            "cpu_usage": {"warning": 80.0, "error": 90.0, "critical": 95.0},
            "gpu_usage": {"warning": 85.0, "error": 90.0, "critical": 95.0}
        }
        
        self.logger.info("Gaming Performance Monitor initialized for TASK 3C")
    
    def start_monitoring(self):
        """Start gaming performance monitoring"""
        try:
            if self.monitoring_active:
                self.logger.info("Gaming performance monitoring already active")
                return True
            
            self.monitoring_active = True
            
            # Setup performance metrics
            self._setup_performance_metrics()
            
            # Setup alert thresholds
            self._setup_alert_thresholds()
            
            self.logger.info("Gaming performance monitoring started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start gaming performance monitoring: {e}")
            self.monitoring_active = False
            return False
    
    def stop_monitoring(self):
        """Stop gaming performance monitoring"""
        try:
            self.monitoring_active = False
            self.logger.info("Gaming performance monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop gaming performance monitoring: {e}")
            return False
    
    def _setup_performance_metrics(self):
        """Setup performance metrics for gaming systems"""
        try:
            # Add gaming performance metrics to performance manager
            self.performance_manager.add_metric("gaming_frame_rate_avg", 0.0, "fps", "gaming")
            self.performance_manager.add_metric("gaming_response_time_avg", 0.0, "ms", "gaming")
            self.performance_manager.add_metric("gaming_memory_usage_avg", 0.0, "MB", "gaming")
            self.performance_manager.add_metric("gaming_cpu_usage_avg", 0.0, "percent", "gaming")
            self.performance_manager.add_metric("gaming_gpu_usage_avg", 0.0, "percent", "gaming")
            
            self.logger.info("Gaming performance metrics setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup gaming performance metrics: {e}")
    
    def _setup_alert_thresholds(self):
        """Setup alert thresholds for gaming performance"""
        try:
            # Set gaming performance thresholds
            for metric, thresholds in self.performance_thresholds.items():
                for severity, value in thresholds.items():
                    metric_name = f"gaming_{metric}"
                    self.performance_manager.set_alert_threshold(metric_name, severity, value)
            
            self.logger.info("Gaming alert thresholds setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup gaming alert thresholds: {e}")
    
    def update_performance_metrics(self, metrics: GamingPerformanceMetrics):
        """Update gaming performance metrics"""
        try:
            if not self.monitoring_active:
                self.logger.warning("Gaming performance monitoring not active, skipping metrics update")
                return False
            
            # Store metrics in history
            if metrics.system_id not in self.performance_history:
                self.performance_history[metrics.system_id] = []
            
            self.performance_history[metrics.system_id].append(metrics)
            
            # Keep only last 100 metrics per system
            if len(self.performance_history[metrics.system_id]) > 100:
                self.performance_history[metrics.system_id] = self.performance_history[metrics.system_id][-100:]
            
            # Update performance manager
            self._update_performance_manager(metrics)
            
            # Check for performance alerts
            self._check_performance_alerts(metrics)
            
            self.logger.debug(f"Updated performance metrics for {metrics.system_id}: {metrics.performance_score}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update performance metrics: {e}")
            return False
    
    def _update_performance_manager(self, metrics: GamingPerformanceMetrics):
        """Update performance manager with gaming metrics"""
        try:
            # Update individual metrics
            self.performance_manager.add_metric("gaming_frame_rate_avg", metrics.frame_rate, "fps", "gaming")
            self.performance_manager.add_metric("gaming_response_time_avg", metrics.response_time, "ms", "gaming")
            self.performance_manager.add_metric("gaming_memory_usage_avg", metrics.memory_usage, "MB", "gaming")
            self.performance_manager.add_metric("gaming_cpu_usage_avg", metrics.cpu_usage, "percent", "gaming")
            self.performance_manager.add_metric("gaming_gpu_usage_avg", metrics.gpu_usage, "percent", "gaming")
            
        except Exception as e:
            self.logger.error(f"Failed to update performance manager: {e}")
    
    def _check_performance_alerts(self, metrics: GamingPerformanceMetrics):
        """Check performance metrics for alert conditions"""
        try:
            # Check frame rate alerts
            if metrics.frame_rate < self.performance_thresholds["frame_rate"]["critical"]:
                self._create_performance_alert("critical", "gaming_frame_rate", metrics)
            elif metrics.frame_rate < self.performance_thresholds["frame_rate"]["error"]:
                self._create_performance_alert("error", "gaming_frame_rate", metrics)
            elif metrics.frame_rate < self.performance_thresholds["frame_rate"]["warning"]:
                self._create_performance_alert("warning", "gaming_frame_rate", metrics)
            
            # Check response time alerts
            if metrics.response_time > self.performance_thresholds["response_time"]["critical"]:
                self._create_performance_alert("critical", "gaming_response_time", metrics)
            elif metrics.response_time > self.performance_thresholds["response_time"]["error"]:
                self._create_performance_alert("error", "gaming_response_time", metrics)
            elif metrics.response_time > self.performance_thresholds["response_time"]["warning"]:
                self._create_performance_alert("warning", "gaming_response_time", metrics)
            
            # Check memory usage alerts
            if metrics.memory_usage > self.performance_thresholds["memory_usage"]["critical"]:
                self._create_performance_alert("critical", "gaming_memory_usage", metrics)
            elif metrics.memory_usage > self.performance_thresholds["memory_usage"]["error"]:
                self._create_performance_alert("error", "gaming_memory_usage", metrics)
            elif metrics.memory_usage > self.performance_thresholds["memory_usage"]["warning"]:
                self._create_performance_alert("warning", "gaming_memory_usage", metrics)
                
        except Exception as e:
            self.logger.error(f"Failed to check performance alerts: {e}")
    
    def _create_performance_alert(self, severity: str, alert_type: str, metrics: GamingPerformanceMetrics):
        """Create a performance alert"""
        try:
            alert_message = f"Gaming performance alert: {alert_type} {severity} for {metrics.system_id}"
            
            # Create alert in performance manager
            self.performance_manager.add_metric("gaming_performance_alerts", 1, "count", "gaming")
            
            self.logger.warning(f"Created {severity} alert: {alert_message}")
            
        except Exception as e:
            self.logger.error(f"Failed to create performance alert: {e}")
    
    def get_performance_summary(self, system_id: Optional[str] = None) -> Dict[str, Any]:
        """Get gaming performance summary"""
        try:
            if system_id:
                return self._get_system_performance_summary(system_id)
            else:
                return self._get_overall_performance_summary()
                
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}
    
    def _get_system_performance_summary(self, system_id: str) -> Dict[str, Any]:
        """Get performance summary for a specific system"""
        try:
            if system_id not in self.performance_history:
                return {"error": f"System {system_id} not found"}
            
            metrics = self.performance_history[system_id]
            if not metrics:
                return {"error": f"No performance data for {system_id}"}
            
            latest = metrics[-1]
            
            return {
                "system_id": system_id,
                "latest_metrics": {
                    "frame_rate": latest.frame_rate,
                    "response_time": latest.response_time,
                    "memory_usage": latest.memory_usage,
                    "cpu_usage": latest.cpu_usage,
                    "gpu_usage": latest.gpu_usage,
                    "performance_score": latest.performance_score,
                    "game_state": latest.game_state
                },
                "total_metrics": len(metrics),
                "last_update": latest.timestamp
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system performance summary: {e}")
            return {"error": str(e)}
    
    def _get_overall_performance_summary(self) -> Dict[str, Any]:
        """Get overall gaming performance summary"""
        try:
            all_metrics = []
            for system_metrics in self.performance_history.values():
                all_metrics.extend(system_metrics)
            
            if not all_metrics:
                return {"error": "No performance data available"}
            
            # Calculate averages
            avg_frame_rate = sum(m.frame_rate for m in all_metrics) / len(all_metrics)
            avg_response_time = sum(m.response_time for m in all_metrics) / len(all_metrics)
            avg_memory_usage = sum(m.memory_usage for m in all_metrics) / len(all_metrics)
            avg_cpu_usage = sum(m.cpu_usage for m in all_metrics) / len(all_metrics)
            avg_gpu_usage = sum(m.gpu_usage for m in all_metrics) / len(all_metrics)
            avg_performance_score = sum(m.performance_score for m in all_metrics) / len(all_metrics)
            
            return {
                "overall_performance": {
                    "avg_frame_rate": round(avg_frame_rate, 2),
                    "avg_response_time": round(avg_response_time, 2),
                    "avg_memory_usage": round(avg_memory_usage, 2),
                    "avg_cpu_usage": round(avg_cpu_usage, 2),
                    "avg_gpu_usage": round(avg_gpu_usage, 2),
                    "avg_performance_score": round(avg_performance_score, 2)
                },
                "total_systems": len(self.performance_history),
                "total_metrics": len(all_metrics),
                "monitoring_active": self.monitoring_active,
                "last_update": all_metrics[-1].timestamp if all_metrics else None
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get overall performance summary: {e}")
            return {"error": str(e)}

