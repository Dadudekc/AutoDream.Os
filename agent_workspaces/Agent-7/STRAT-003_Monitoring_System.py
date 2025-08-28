#!/usr/bin/env python3
"""
Optimization Impact Monitoring System

Contract: STRAT-003 - Optimization Impact Monitoring
Agent: Agent-7 (QUALITY ASSURANCE MANAGER)
Date: 2025-01-27
Status: In Progress

This module implements a comprehensive monitoring system for tracking
optimization efforts across all 8-agent systems.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import threading
import queue
import statistics
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics that can be monitored"""
    PERFORMANCE = "performance"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"
    COORDINATION = "coordination"
    SYSTEM = "system"

class MetricStatus(Enum):
    """Status of metric measurements"""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class Metric:
    """Individual metric measurement"""
    name: str
    value: float
    unit: str
    metric_type: MetricType
    timestamp: datetime
    status: MetricStatus
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemMetrics:
    """Collection of metrics for a specific system"""
    system_name: str
    timestamp: datetime
    metrics: List[Metric] = field(default_factory=list)
    overall_status: MetricStatus = MetricStatus.UNKNOWN

@dataclass
class OptimizationImpact:
    """Measurement of optimization impact"""
    metric_name: str
    before_value: float
    after_value: float
    improvement_percentage: float
    impact_level: str  # "low", "medium", "high", "critical"
    confidence_level: float  # 0.0 to 1.0
    timestamp: datetime

class MonitoringSystem:
    """Core monitoring system for optimization impact tracking"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "monitoring_config.json"
        self.metrics_history: List[SystemMetrics] = []
        self.impact_history: List[OptimizationImpact] = []
        self.alert_callbacks: List[Callable] = []
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.metrics_queue = queue.Queue()
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize metric collectors
        self.collectors = self._initialize_collectors()
        
        # Performance thresholds
        self.thresholds = {
            "response_time": {"warning": 100, "critical": 500},  # ms
            "throughput": {"warning": 1000, "critical": 500},   # ops/sec
            "cpu_usage": {"warning": 80, "critical": 95},       # %
            "memory_usage": {"warning": 85, "critical": 95},    # %
            "error_rate": {"warning": 5, "critical": 15},       # %
            "test_coverage": {"warning": 80, "critical": 70},   # %
            "code_quality": {"warning": 75, "critical": 60},    # %
        }
        
        logger.info("Monitoring system initialized successfully")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load monitoring configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                return {
                    "monitoring_interval": 30,  # seconds
                    "metrics_retention_days": 30,
                    "alert_enabled": True,
                    "systems_to_monitor": [
                        "messaging_system",
                        "contract_system", 
                        "quality_system",
                        "coordination_system"
                    ]
                }
        except Exception as e:
            logger.warning(f"Could not load config: {e}, using defaults")
            return self._load_config.__defaults__[0]
    
    def _initialize_collectors(self) -> Dict[str, Callable]:
        """Initialize metric collection functions"""
        return {
            "system_performance": self._collect_system_performance,
            "quality_metrics": self._collect_quality_metrics,
            "coordination_metrics": self._collect_coordination_metrics,
            "efficiency_metrics": self._collect_efficiency_metrics
        }
    
    def start_monitoring(self):
        """Start the monitoring system"""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        logger.info("Monitoring system started")
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Monitoring system stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect metrics from all systems
                system_metrics = self._collect_all_metrics()
                
                # Store metrics
                self.metrics_history.append(system_metrics)
                
                # Analyze for alerts
                self._check_alerts(system_metrics)
                
                # Calculate optimization impact
                self._calculate_optimization_impact(system_metrics)
                
                # Clean up old metrics
                self._cleanup_old_metrics()
                
                # Wait for next collection cycle
                time.sleep(self.config.get("monitoring_interval", 30))
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _collect_all_metrics(self) -> SystemMetrics:
        """Collect metrics from all monitored systems"""
        metrics = []
        timestamp = datetime.now()
        
        # Collect from each collector
        for collector_name, collector_func in self.collectors.items():
            try:
                collector_metrics = collector_func()
                metrics.extend(collector_metrics)
            except Exception as e:
                logger.error(f"Error collecting from {collector_name}: {e}")
        
        # Create system metrics object
        system_metrics = SystemMetrics(
            system_name="8_agent_system",
            timestamp=timestamp,
            metrics=metrics
        )
        
        # Determine overall status
        system_metrics.overall_status = self._calculate_overall_status(metrics)
        
        return system_metrics
    
    def _collect_system_performance(self) -> List[Metric]:
        """Collect system performance metrics"""
        metrics = []
        timestamp = datetime.now()
        
        # Simulate performance metrics collection
        # In a real implementation, these would come from actual system monitoring
        
        # Response time simulation
        response_time = 50 + (time.time() % 100)  # Simulate varying response time
        status = self._evaluate_threshold("response_time", response_time)
        metrics.append(Metric(
            name="response_time",
            value=response_time,
            unit="ms",
            metric_type=MetricType.PERFORMANCE,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["response_time"]["warning"],
            threshold_critical=self.thresholds["response_time"]["critical"]
        ))
        
        # Throughput simulation
        throughput = 1500 + (time.time() % 500)
        status = self._evaluate_threshold("throughput", throughput)
        metrics.append(Metric(
            name="throughput",
            value=throughput,
            unit="ops/sec",
            metric_type=MetricType.PERFORMANCE,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["throughput"]["warning"],
            threshold_critical=self.thresholds["throughput"]["critical"]
        ))
        
        # CPU usage simulation
        cpu_usage = 60 + (time.time() % 30)
        status = self._evaluate_threshold("cpu_usage", cpu_usage)
        metrics.append(Metric(
            name="cpu_usage",
            value=cpu_usage,
            unit="%",
            metric_type=MetricType.SYSTEM,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["cpu_usage"]["warning"],
            threshold_critical=self.thresholds["cpu_usage"]["critical"]
        ))
        
        return metrics
    
    def _collect_quality_metrics(self) -> List[Metric]:
        """Collect quality-related metrics"""
        metrics = []
        timestamp = datetime.now()
        
        # Test coverage simulation
        test_coverage = 85 + (time.time() % 10)
        status = self._evaluate_threshold("test_coverage", test_coverage)
        metrics.append(Metric(
            name="test_coverage",
            value=test_coverage,
            unit="%",
            metric_type=MetricType.QUALITY,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["test_coverage"]["warning"],
            threshold_critical=self.thresholds["test_coverage"]["critical"]
        ))
        
        # Code quality simulation
        code_quality = 80 + (time.time() % 15)
        status = self._evaluate_threshold("code_quality", code_quality)
        metrics.append(Metric(
            name="code_quality",
            value=code_quality,
            unit="%",
            metric_type=MetricType.QUALITY,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["code_quality"]["warning"],
            threshold_critical=self.thresholds["code_quality"]["critical"]
        ))
        
        return metrics
    
    def _collect_coordination_metrics(self) -> List[Metric]:
        """Collect coordination-related metrics"""
        metrics = []
        timestamp = datetime.now()
        
        # Task handoff time simulation
        handoff_time = 3 + (time.time() % 4)  # 3-7 minutes
        status = MetricStatus.NORMAL if handoff_time < 5 else MetricStatus.WARNING
        metrics.append(Metric(
            name="task_handoff_time",
            value=handoff_time,
            unit="minutes",
            metric_type=MetricType.COORDINATION,
            timestamp=timestamp,
            status=status,
            threshold_warning=5,
            threshold_critical=10
        ))
        
        # Communication latency simulation
        latency = 1.5 + (time.time() % 1)  # 1.5-2.5 seconds
        status = MetricStatus.NORMAL if latency < 2 else MetricStatus.WARNING
        metrics.append(Metric(
            name="communication_latency",
            value=latency,
            unit="seconds",
            metric_type=MetricType.COORDINATION,
            timestamp=timestamp,
            status=status,
            threshold_warning=2,
            threshold_critical=5
        ))
        
        return metrics
    
    def _collect_efficiency_metrics(self) -> List[Metric]:
        """Collect efficiency-related metrics"""
        metrics = []
        timestamp = datetime.now()
        
        # Automation coverage simulation
        automation_coverage = 75 + (time.time() % 20)
        metrics.append(Metric(
            name="automation_coverage",
            value=automation_coverage,
            unit="%",
            metric_type=MetricType.EFFICIENCY,
            timestamp=timestamp,
            status=MetricStatus.NORMAL
        ))
        
        # Error rate simulation
        error_rate = 2 + (time.time() % 3)
        status = self._evaluate_threshold("error_rate", error_rate)
        metrics.append(Metric(
            name="error_rate",
            value=error_rate,
            unit="%",
            metric_type=MetricType.EFFICIENCY,
            timestamp=timestamp,
            status=status,
            threshold_warning=self.thresholds["error_rate"]["warning"],
            threshold_critical=self.thresholds["error_rate"]["critical"]
        ))
        
        return metrics
    
    def _evaluate_threshold(self, metric_name: str, value: float) -> MetricStatus:
        """Evaluate metric value against thresholds"""
        if metric_name not in self.thresholds:
            return MetricStatus.UNKNOWN
        
        thresholds = self.thresholds[metric_name]
        
        if value >= thresholds["critical"]:
            return MetricStatus.CRITICAL
        elif value >= thresholds["warning"]:
            return MetricStatus.WARNING
        else:
            return MetricStatus.NORMAL
    
    def _calculate_overall_status(self, metrics: List[Metric]) -> MetricStatus:
        """Calculate overall system status from individual metrics"""
        if not metrics:
            return MetricStatus.UNKNOWN
        
        # Count metrics by status
        status_counts = {
            MetricStatus.CRITICAL: 0,
            MetricStatus.WARNING: 0,
            MetricStatus.NORMAL: 0,
            MetricStatus.UNKNOWN: 0
        }
        
        for metric in metrics:
            status_counts[metric.status] += 1
        
        # Determine overall status
        if status_counts[MetricStatus.CRITICAL] > 0:
            return MetricStatus.CRITICAL
        elif status_counts[MetricStatus.WARNING] > 0:
            return MetricStatus.WARNING
        elif status_counts[MetricStatus.NORMAL] > 0:
            return MetricStatus.NORMAL
        else:
            return MetricStatus.UNKNOWN
    
    def _check_alerts(self, system_metrics: SystemMetrics):
        """Check for alert conditions and trigger callbacks"""
        if not self.config.get("alert_enabled", True):
            return
        
        for metric in system_metrics.metrics:
            if metric.status in [MetricStatus.WARNING, MetricStatus.CRITICAL]:
                alert_message = {
                    "timestamp": datetime.now().isoformat(),
                    "system": system_metrics.system_name,
                    "metric": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "status": metric.status.value,
                    "threshold_warning": metric.threshold_warning,
                    "threshold_critical": metric.threshold_critical
                }
                
                # Trigger alert callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert_message)
                    except Exception as e:
                        logger.error(f"Error in alert callback: {e}")
                
                logger.warning(f"Alert triggered: {alert_message}")
    
    def _calculate_optimization_impact(self, current_metrics: SystemMetrics):
        """Calculate optimization impact by comparing with historical data"""
        if len(self.metrics_history) < 2:
            return
        
        # Get previous metrics for comparison
        previous_metrics = self.metrics_history[-2]
        
        for current_metric in current_metrics.metrics:
            # Find corresponding previous metric
            previous_metric = next(
                (m for m in previous_metrics.metrics if m.name == current_metric.name),
                None
            )
            
            if previous_metric and previous_metric.value != 0:
                # Calculate improvement
                improvement = ((current_metric.value - previous_metric.value) / 
                             abs(previous_metric.value)) * 100
                
                # Determine impact level
                if abs(improvement) < 5:
                    impact_level = "low"
                elif abs(improvement) < 15:
                    impact_level = "medium"
                elif abs(improvement) < 30:
                    impact_level = "high"
                else:
                    impact_level = "critical"
                
                # Create impact record
                impact = OptimizationImpact(
                    metric_name=current_metric.name,
                    before_value=previous_metric.value,
                    after_value=current_metric.value,
                    improvement_percentage=improvement,
                    impact_level=impact_level,
                    confidence_level=0.8,  # Simplified confidence calculation
                    timestamp=datetime.now()
                )
                
                self.impact_history.append(impact)
    
    def _cleanup_old_metrics(self):
        """Remove old metrics based on retention policy"""
        retention_days = self.config.get("metrics_retention_days", 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Clean up metrics history
        self.metrics_history = [
            metrics for metrics in self.metrics_history
            if metrics.timestamp > cutoff_date
        ]
        
        # Clean up impact history
        self.impact_history = [
            impact for impact in self.impact_history
            if impact.timestamp > cutoff_date
        ]
    
    def add_alert_callback(self, callback: Callable):
        """Add a callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current system status summary"""
        if not self.metrics_history:
            return {"status": "no_data", "message": "No metrics collected yet"}
        
        latest_metrics = self.metrics_history[-1]
        
        # Calculate summary statistics
        status_summary = {
            "timestamp": latest_metrics.timestamp.isoformat(),
            "overall_status": latest_metrics.overall_status.value,
            "total_metrics": len(latest_metrics.metrics),
            "metrics_by_status": {},
            "metrics_by_type": {},
            "recent_alerts": [],
            "optimization_impact": {}
        }
        
        # Count metrics by status
        for metric in latest_metrics.metrics:
            status = metric.status.value
            status_summary["metrics_by_status"][status] = \
                status_summary["metrics_by_status"].get(status, 0) + 1
            
            metric_type = metric.metric_type.value
            status_summary["metrics_by_type"][metric_type] = \
                status_summary["metrics_by_type"].get(metric_type, 0) + 1
        
        # Get recent alerts (last 10)
        recent_impacts = sorted(
            self.impact_history, 
            key=lambda x: x.timestamp, 
            reverse=True
        )[:10]
        
        for impact in recent_impacts:
            status_summary["optimization_impact"][impact.metric_name] = {
                "improvement_percentage": impact.improvement_percentage,
                "impact_level": impact.impact_level,
                "confidence_level": impact.confidence_level,
                "timestamp": impact.timestamp.isoformat()
            }
        
        return status_summary
    
    def get_metrics_history(self, hours: int = 24) -> List[SystemMetrics]:
        """Get metrics history for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            metrics for metrics in self.metrics_history
            if metrics.timestamp > cutoff_time
        ]
    
    def export_metrics(self, filepath: str, format: str = "json"):
        """Export metrics to file"""
        try:
            if format.lower() == "json":
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "metrics_history": [
                        {
                            "system_name": m.system_name,
                            "timestamp": m.timestamp.isoformat(),
                            "overall_status": m.overall_status.value,
                            "metrics": [
                                {
                                    "name": metric.name,
                                    "value": metric.value,
                                    "unit": metric.unit,
                                    "metric_type": metric.metric_type.value,
                                    "status": metric.status.value,
                                    "timestamp": metric.timestamp.isoformat()
                                }
                                for metric in m.metrics
                            ]
                        }
                        for m in self.metrics_history
                    ],
                    "impact_history": [
                        {
                            "metric_name": impact.metric_name,
                            "before_value": impact.before_value,
                            "after_value": impact.after_value,
                            "improvement_percentage": impact.improvement_percentage,
                            "impact_level": impact.impact_level,
                            "confidence_level": impact.confidence_level,
                            "timestamp": impact.timestamp.isoformat()
                        }
                        for impact in self.impact_history
                    ]
                }
                
                with open(filepath, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                logger.info(f"Metrics exported to {filepath}")
                return True
                
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return False

def main():
    """Main function for testing the monitoring system"""
    # Create monitoring system
    monitor = MonitoringSystem()
    
    # Add simple alert callback
    def alert_callback(alert_data):
        print(f"🚨 ALERT: {alert_data['metric']} = {alert_data['value']} {alert_data['unit']} ({alert_data['status']})")
    
    monitor.add_alert_callback(alert_callback)
    
    # Start monitoring
    print("🚀 Starting Optimization Impact Monitoring System...")
    monitor.start_monitoring()
    
    try:
        # Run for a few cycles to collect data
        print("📊 Collecting metrics...")
        time.sleep(90)  # Wait for 3 monitoring cycles
        
        # Get status
        status = monitor.get_current_status()
        print("\n📈 Current System Status:")
        print(json.dumps(status, indent=2))
        
        # Export metrics
        monitor.export_metrics("optimization_metrics_export.json")
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping monitoring...")
    finally:
        monitor.stop_monitoring()
        print("✅ Monitoring stopped")

if __name__ == "__main__":
    main()
