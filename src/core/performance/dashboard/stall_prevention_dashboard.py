#!/usr/bin/env python3
"""
Stall Prevention Performance Monitoring Dashboard - Agent Cellphone V2
===================================================================

Comprehensive performance monitoring dashboard for stall prevention systems.
Provides real-time metrics, health monitoring, and optimization recommendations.

Author: Agent-6 - Performance Optimization Manager
License: MIT
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StallSeverity(Enum):
    """Stall severity levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SystemHealth(Enum):
    """System health status"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class StallPreventionMetric:
    """Individual stall prevention metric"""
    name: str
    value: float
    unit: str
    timestamp: datetime
    threshold: float
    status: StallSeverity
    trend: str  # "improving", "stable", "degrading"


@dataclass
class SystemHealthMetric:
    """System health metric"""
    component: str
    health_score: float
    status: SystemHealth
    last_check: datetime
    issues: List[str]
    recommendations: List[str]


@dataclass
class PerformanceAlert:
    """Performance alert"""
    id: str
    severity: StallSeverity
    message: str
    component: str
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None


class StallPreventionDashboard:
    """
    Comprehensive stall prevention performance monitoring dashboard.
    
    Features:
    - Real-time stall prevention metrics
    - System health monitoring
    - Performance optimization recommendations
    - Automated alerting and notifications
    - Historical trend analysis
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/system/stall_prevention_dashboard.json"
        self.config = self._load_config()
        
        # Dashboard state
        self.running = False
        self.refresh_interval = self.config.get("refresh_interval_seconds", 5)
        self.metrics_retention_hours = self.config.get("metrics_retention_hours", 24)
        
        # Data storage
        self.stall_metrics: List[StallPreventionMetric] = []
        self.health_metrics: Dict[str, SystemHealthMetric] = {}
        self.alerts: List[PerformanceAlert] = []
        self.performance_history: List[Dict[str, Any]] = []
        
        # Threading
        self.dashboard_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()
        
        # Callbacks
        self.update_callbacks: List[Callable] = []
        self.alert_callbacks: List[Callable] = []
        
        # Performance tracking
        self.start_time = datetime.now()
        self.total_checks = 0
        self.stall_events = 0
        self.recovery_events = 0
        
        # Initialize components
        self._initialize_health_monitoring()
        self._setup_performance_tracking()
        
        logger.info("Stall Prevention Dashboard initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load dashboard configuration"""
        default_config = {
            "refresh_interval_seconds": 5,
            "metrics_retention_hours": 24,
            "alert_thresholds": {
                "response_time_ms": 1000,
                "stall_detection_rate": 0.1,
                "recovery_time_ms": 5000,
                "system_health_score": 0.7
            },
            "health_weights": {
                "cpu_usage": 0.25,
                "memory_usage": 0.25,
                "response_time": 0.3,
                "error_rate": 0.2
            }
        }
        
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
        except Exception as e:
            logger.warning(f"Could not load config, using defaults: {e}")
        
        return default_config
    
    def _initialize_health_monitoring(self):
        """Initialize system health monitoring"""
        self.health_metrics = {
            "stall_prevention_service": SystemHealthMetric(
                component="Stall Prevention Service",
                health_score=1.0,
                status=SystemHealth.EXCELLENT,
                last_check=datetime.now(),
                issues=[],
                recommendations=[]
            ),
            "agent_coordination": SystemHealthMetric(
                component="Agent Coordination",
                health_score=1.0,
                status=SystemHealth.EXCELLENT,
                last_check=datetime.now(),
                issues=[],
                recommendations=[]
            ),
            "system_resources": SystemHealthMetric(
                component="System Resources",
                health_score=1.0,
                status=SystemHealth.EXCELLENT,
                last_check=datetime.now(),
                issues=[],
                recommendations=[]
            ),
            "communication_channels": SystemHealthMetric(
                component="Communication Channels",
                health_score=1.0,
                status=SystemHealth.EXCELLENT,
                last_check=datetime.now(),
                issues=[],
                recommendations=[]
            )
        }
    
    def _setup_performance_tracking(self):
        """Setup performance tracking integration"""
        try:
            # Try to integrate with existing stall prevention service
            from src.services.agent_stall_prevention_service import AgentStallPreventionService
            self.stall_service = AgentStallPreventionService()
            logger.info("Integrated with existing stall prevention service")
        except ImportError:
            logger.warning("Stall prevention service not available, using standalone mode")
            self.stall_service = None
    
    def start(self):
        """Start the dashboard"""
        if self.running:
            logger.warning("Dashboard already running")
            return
        
        self.running = True
        self.dashboard_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        self.dashboard_thread.start()
        logger.info("Stall Prevention Dashboard started")
    
    def stop(self):
        """Stop the dashboard"""
        self.running = False
        if self.dashboard_thread and self.dashboard_thread.is_alive():
            self.dashboard_thread.join(timeout=5)
        logger.info("Stall Prevention Dashboard stopped")
    
    def _dashboard_loop(self):
        """Main dashboard update loop"""
        while self.running:
            try:
                # Update metrics
                self._update_stall_metrics()
                self._update_health_metrics()
                self._check_performance_alerts()
                
                # Cleanup old data
                self._cleanup_old_data()
                
                # Notify callbacks
                self._notify_update_callbacks()
                
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                logger.error(f"Error in dashboard loop: {e}")
                time.sleep(10)
    
    def _update_stall_metrics(self):
        """Update stall prevention metrics"""
        try:
            current_time = datetime.now()
            
            # Get system performance metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Calculate response time (simulated for demo)
            response_time = self._calculate_response_time()
            
            # Create stall prevention metrics
            metrics = [
                StallPreventionMetric(
                    name="cpu_usage",
                    value=cpu_percent,
                    unit="percent",
                    timestamp=current_time,
                    threshold=80.0,
                    status=self._get_stall_severity(cpu_percent, 80.0),
                    trend=self._get_trend("cpu_usage", cpu_percent)
                ),
                StallPreventionMetric(
                    name="memory_usage",
                    value=memory.percent,
                    unit="percent",
                    timestamp=current_time,
                    threshold=85.0,
                    status=self._get_stall_severity(memory.percent, 85.0),
                    trend=self._get_trend("memory_usage", memory.percent)
                ),
                StallPreventionMetric(
                    name="response_time",
                    value=response_time,
                    unit="ms",
                    timestamp=current_time,
                    threshold=1000.0,
                    status=self._get_stall_severity(response_time, 1000.0),
                    trend=self._get_trend("response_time", response_time)
                ),
                StallPreventionMetric(
                    name="stall_detection_rate",
                    value=self._calculate_stall_rate(),
                    unit="events/minute",
                    timestamp=current_time,
                    threshold=0.1,
                    status=self._get_stall_severity(self._calculate_stall_rate(), 0.1),
                    trend=self._get_trend("stall_detection_rate", self._calculate_stall_rate())
                )
            ]
            
            with self.lock:
                self.stall_metrics.extend(metrics)
                self.total_checks += 1
                
        except Exception as e:
            logger.error(f"Error updating stall metrics: {e}")
    
    def _update_health_metrics(self):
        """Update system health metrics"""
        try:
            current_time = datetime.now()
            
            # Update stall prevention service health
            if self.stall_service:
                service_health = self._assess_service_health()
                self.health_metrics["stall_prevention_service"].health_score = service_health
                self.health_metrics["stall_prevention_service"].last_check = current_time
                self.health_metrics["stall_prevention_service"].status = self._get_health_status(service_health)
            
            # Update agent coordination health
            coordination_health = self._assess_coordination_health()
            self.health_metrics["agent_coordination"].health_score = coordination_health
            self.health_metrics["agent_coordination"].last_check = current_time
            self.health_metrics["agent_coordination"].status = self._get_health_status(coordination_health)
            
            # Update system resources health
            resources_health = self._assess_resources_health()
            self.health_metrics["system_resources"].health_score = resources_health
            self.health_metrics["system_resources"].last_check = current_time
            self.health_metrics["system_resources"].status = self._get_health_status(resources_health)
            
            # Update communication channels health
            communication_health = self._assess_communication_health()
            self.health_metrics["communication_channels"].health_score = communication_health
            self.health_metrics["communication_channels"].last_check = current_time
            self.health_metrics["communication_channels"].status = self._get_health_status(communication_health)
            
        except Exception as e:
            logger.error(f"Error updating health metrics: {e}")
    
    def _assess_service_health(self) -> float:
        """Assess stall prevention service health"""
        try:
            if not self.stall_service:
                return 0.8  # Default health score
            
            # Check if service is running
            if not self.stall_service.is_running:
                return 0.0
            
            # Check last activity
            if self.stall_service.last_check_time:
                time_since_check = (datetime.now() - self.stall_service.last_check_time).total_seconds()
                if time_since_check > 300:  # 5 minutes
                    return 0.3
            
            return 0.9
            
        except Exception as e:
            logger.error(f"Error assessing service health: {e}")
            return 0.5
    
    def _assess_coordination_health(self) -> float:
        """Assess agent coordination health"""
        try:
            # Simulate coordination health based on metrics
            response_time_health = max(0, 1 - (self._get_latest_metric("response_time", 1000) / 1000))
            stall_rate_health = max(0, 1 - (self._get_latest_metric("stall_detection_rate", 0.1) / 0.1))
            
            return (response_time_health + stall_rate_health) / 2
            
        except Exception as e:
            logger.error(f"Error assessing coordination health: {e}")
            return 0.7
    
    def _assess_resources_health(self) -> float:
        """Assess system resources health"""
        try:
            cpu_health = max(0, 1 - (psutil.cpu_percent() / 100))
            memory_health = max(0, 1 - (psutil.virtual_memory().percent / 100))
            disk_health = max(0, 1 - (psutil.disk_usage('/').percent / 100))
            
            return (cpu_health + memory_health + disk_health) / 3
            
        except Exception as e:
            logger.error(f"Error assessing resources health: {e}")
            return 0.6
    
    def _assess_communication_health(self) -> float:
        """Assess communication channels health"""
        try:
            # Simulate communication health
            # In a real implementation, this would check network connectivity, message queues, etc.
            return 0.85
            
        except Exception as e:
            logger.error(f"Error assessing communication health: {e}")
            return 0.7
    
    def _calculate_response_time(self) -> float:
        """Calculate system response time"""
        try:
            start_time = time.time()
            # Simulate a simple operation
            time.sleep(0.001)  # 1ms
            return (time.time() - start_time) * 1000  # Convert to ms
            
        except Exception as e:
            logger.error(f"Error calculating response time: {e}")
            return 100.0
    
    def _calculate_stall_rate(self) -> float:
        """Calculate current stall detection rate"""
        try:
            # Simulate stall rate based on system load
            cpu_percent = psutil.cpu_percent()
            if cpu_percent > 90:
                return 0.15
            elif cpu_percent > 80:
                return 0.08
            elif cpu_percent > 70:
                return 0.05
            else:
                return 0.02
                
        except Exception as e:
            logger.error(f"Error calculating stall rate: {e}")
            return 0.05
    
    def _get_stall_severity(self, value: float, threshold: float) -> StallSeverity:
        """Get stall severity based on value and threshold"""
        if value <= threshold * 0.5:
            return StallSeverity.NONE
        elif value <= threshold * 0.7:
            return StallSeverity.LOW
        elif value <= threshold * 0.9:
            return StallSeverity.MEDIUM
        elif value <= threshold:
            return StallSeverity.HIGH
        else:
            return StallSeverity.CRITICAL
    
    def _get_health_status(self, health_score: float) -> SystemHealth:
        """Get system health status based on score"""
        if health_score >= 0.9:
            return SystemHealth.EXCELLENT
        elif health_score >= 0.8:
            return SystemHealth.GOOD
        elif health_score >= 0.7:
            return SystemHealth.FAIR
        elif health_score >= 0.6:
            return SystemHealth.POOR
        else:
            return SystemHealth.CRITICAL
    
    def _get_trend(self, metric_name: str, current_value: float) -> str:
        """Get trend for a metric (simplified)"""
        # In a real implementation, this would compare with historical values
        return "stable"
    
    def _get_latest_metric(self, metric_name: str, default_value: float) -> float:
        """Get latest value for a specific metric"""
        try:
            with self.lock:
                for metric in reversed(self.stall_metrics):
                    if metric.name == metric_name:
                        return metric.value
            return default_value
        except Exception as e:
            logger.error(f"Error getting latest metric: {e}")
            return default_value
    
    def _check_performance_alerts(self):
        """Check for performance alerts"""
        try:
            current_time = datetime.now()
            
            # Check CPU usage alerts
            cpu_usage = self._get_latest_metric("cpu_usage", 0)
            if cpu_usage > 90:
                self._create_alert(
                    severity=StallSeverity.CRITICAL,
                    message=f"Critical CPU usage: {cpu_usage:.1f}%",
                    component="System Resources"
                )
            elif cpu_usage > 80:
                self._create_alert(
                    severity=StallSeverity.HIGH,
                    message=f"High CPU usage: {cpu_usage:.1f}%",
                    component="System Resources"
                )
            
            # Check memory usage alerts
            memory_usage = self._get_latest_metric("memory_usage", 0)
            if memory_usage > 90:
                self._create_alert(
                    severity=StallSeverity.CRITICAL,
                    message=f"Critical memory usage: {memory_usage:.1f}%",
                    component="System Resources"
                )
            
            # Check response time alerts
            response_time = self._get_latest_metric("response_time", 0)
            if response_time > 2000:
                self._create_alert(
                    severity=StallSeverity.CRITICAL,
                    message=f"Critical response time: {response_time:.1f}ms",
                    component="Agent Coordination"
                )
            elif response_time > 1000:
                self._create_alert(
                    severity=StallSeverity.HIGH,
                    message=f"High response time: {response_time:.1f}ms",
                    component="Agent Coordination"
                )
                
        except Exception as e:
            logger.error(f"Error checking performance alerts: {e}")
    
    def _create_alert(self, severity: StallSeverity, message: str, component: str):
        """Create a new performance alert"""
        try:
            alert = PerformanceAlert(
                id=f"ALERT-{int(time.time())}",
                severity=severity,
                message=message,
                component=component,
                timestamp=datetime.now()
            )
            
            with self.lock:
                self.alerts.append(alert)
            
            # Notify alert callbacks
            self._notify_alert_callbacks(alert)
            
            logger.warning(f"Performance alert created: {message}")
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old metrics and alerts"""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=self.metrics_retention_hours)
            
            with self.lock:
                # Clean up old metrics
                self.stall_metrics = [
                    metric for metric in self.stall_metrics
                    if metric.timestamp > cutoff_time
                ]
                
                # Clean up old alerts
                self.alerts = [
                    alert for alert in self.alerts
                    if alert.timestamp > cutoff_time
                ]
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def _notify_update_callbacks(self):
        """Notify update callbacks"""
        for callback in self.update_callbacks:
            try:
                callback(self.get_dashboard_data())
            except Exception as e:
                logger.error(f"Error in update callback: {e}")
    
    def _notify_alert_callbacks(self, alert: PerformanceAlert):
        """Notify alert callbacks"""
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get current dashboard data"""
        try:
            with self.lock:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                    "total_checks": self.total_checks,
                    "stall_events": self.stall_events,
                    "recovery_events": self.recovery_events,
                    "stall_metrics": [asdict(metric) for metric in self.stall_metrics[-10:]],  # Last 10
                    "health_metrics": {k: asdict(v) for k, v in self.health_metrics.items()},
                    "alerts": [asdict(alert) for alert in self.alerts[-20:]],  # Last 20
                    "overall_health_score": self._calculate_overall_health_score()
                }
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {}
    
    def _calculate_overall_health_score(self) -> float:
        """Calculate overall system health score"""
        try:
            if not self.health_metrics:
                return 0.5
            
            total_score = sum(metric.health_score for metric in self.health_metrics.values())
            return total_score / len(self.health_metrics)
            
        except Exception as e:
            logger.error(f"Error calculating overall health score: {e}")
            return 0.5
    
    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        
        try:
            # CPU usage recommendations
            cpu_usage = self._get_latest_metric("cpu_usage", 0)
            if cpu_usage > 80:
                recommendations.append("Consider optimizing CPU-intensive operations or scaling horizontally")
            
            # Memory usage recommendations
            memory_usage = self._get_latest_metric("memory_usage", 0)
            if memory_usage > 85:
                recommendations.append("Monitor memory leaks and consider memory optimization")
            
            # Response time recommendations
            response_time = self._get_latest_metric("response_time", 0)
            if response_time > 1000:
                recommendations.append("Investigate response time bottlenecks and optimize critical paths")
            
            # Stall rate recommendations
            stall_rate = self._get_latest_metric("stall_detection_rate", 0)
            if stall_rate > 0.05:
                recommendations.append("Review stall prevention mechanisms and improve error handling")
            
            # Health-based recommendations
            overall_health = self._calculate_overall_health_score()
            if overall_health < 0.7:
                recommendations.append("System health is degrading - review all components and optimize")
            
            if not recommendations:
                recommendations.append("System performance is optimal - continue monitoring")
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate recommendations due to system error")
        
        return recommendations
    
    def add_update_callback(self, callback: Callable):
        """Add dashboard update callback"""
        self.update_callbacks.append(callback)
    
    def add_alert_callback(self, callback: Callable):
        """Add alert callback"""
        self.alert_callbacks.append(callback)
    
    def export_dashboard_data(self, filepath: str):
        """Export dashboard data to file"""
        try:
            data = self.get_dashboard_data()
            data["export_timestamp"] = datetime.now().isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Dashboard data exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting dashboard data: {e}")


def main():
    """Main entry point for testing"""
    print("🚀 Stall Prevention Performance Dashboard - Agent-6")
    print("=" * 60)
    
    # Create dashboard
    dashboard = StallPreventionDashboard()
    
    # Start dashboard
    dashboard.start()
    
    try:
        # Run for a few minutes to demonstrate
        print("Dashboard started. Press Ctrl+C to stop...")
        time.sleep(300)  # 5 minutes
        
    except KeyboardInterrupt:
        print("\nStopping dashboard...")
        dashboard.stop()
        print("Dashboard stopped.")


if __name__ == "__main__":
    main()
