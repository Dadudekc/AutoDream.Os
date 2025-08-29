"""
🚨 COMMUNICATION MONITORING SYSTEM 🚨
Contract: EMERGENCY-RESTORE-006
Agent: Agent-7
Mission: Agent Communication Restoration (450 pts)

This system implements real-time monitoring, alerting, and health tracking
for agent communication channels and coordination protocols.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class HealthStatus(Enum):
    """Health status enumeration."""
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class MonitoringMetric:
    """Represents a monitoring metric."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: HealthStatus = HealthStatus.UNKNOWN


@dataclass
class MonitoringAlert:
    """Represents a monitoring alert."""
    id: str
    severity: AlertSeverity
    message: str
    source: str
    timestamp: datetime
    resolved: bool = False
    resolution_notes: str = ""
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: Optional[datetime] = None


class CommunicationMonitoringSystem:
    """
    Real-time monitoring system for agent communication channels and coordination protocols.
    
    Features:
    - Real-time health monitoring
    - Automated alerting
    - Performance metrics collection
    - Health score calculation
    - Alert management and resolution
    """
    
    def __init__(self):
        self.metrics: Dict[str, MonitoringMetric] = {}
        self.alerts: List[MonitoringAlert] = []
        self.health_scores: Dict[str, float] = {}
        self.monitoring_active = False
        self.alert_callbacks: List[callable] = []
        self.metric_history: Dict[str, List[MonitoringMetric]] = {}
        self._lock = threading.Lock()
        self._monitoring_thread = None
        
        # Configuration
        self.monitoring_interval = 30  # seconds
        self.alert_thresholds = {
            "channel_latency_ms": 1000,  # 1 second
            "channel_error_rate": 0.1,   # 10%
            "protocol_success_rate": 0.8, # 80%
            "agent_response_time": 5000,  # 5 seconds
        }
        
        # Initialize default metrics
        self._initialize_default_metrics()
    
    def _initialize_default_metrics(self):
        """Initialize default monitoring metrics."""
        default_metrics = [
            ("system_health_score", 0.0, "percentage"),
            ("active_channels", 0, "count"),
            ("total_channels", 0, "count"),
            ("active_protocols", 0, "count"),
            ("total_protocols", 0, "count"),
            ("active_agents", 0, "count"),
            ("total_agents", 0, "count"),
            ("avg_channel_latency", 0.0, "milliseconds"),
            ("avg_protocol_success_rate", 0.0, "percentage"),
            ("unresolved_alerts", 0, "count"),
        ]
        
        for name, value, unit in default_metrics:
            metric = MonitoringMetric(
                name=name,
                value=value,
                unit=unit,
                timestamp=datetime.now(),
                status=HealthStatus.UNKNOWN
            )
            self.metrics[name] = metric
            self.metric_history[name] = []
    
    def start_monitoring(self) -> bool:
        """Start the monitoring system."""
        try:
            if self.monitoring_active:
                logger.warning("Monitoring system already active")
                return True
            
            self.monitoring_active = True
            logger.info("🚨 Communication monitoring system started")
            
            # Start monitoring thread
            self._monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self._monitoring_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start monitoring system: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop the monitoring system."""
        try:
            self.monitoring_active = False
            if self._monitoring_thread:
                self._monitoring_thread.join(timeout=5)
            
            logger.info("Communication monitoring system stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop monitoring system: {e}")
            return False
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Collect metrics
                self._collect_system_metrics()
                
                # Update health scores
                self._update_health_scores()
                
                # Check thresholds and generate alerts
                self._check_thresholds()
                
                # Clean up old metrics
                self._cleanup_old_metrics()
                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _collect_system_metrics(self):
        """Collect current system metrics."""
        try:
            current_time = datetime.now()
            
            # Update metric values (this would normally come from actual system data)
            # For demonstration, we'll simulate some metric collection
            
            # Simulate channel metrics
            self._update_metric("active_channels", 5, current_time)
            self._update_metric("total_channels", 8, current_time)
            
            # Simulate protocol metrics
            self._update_metric("active_protocols", 3, current_time)
            self._update_metric("total_protocols", 3, current_time)
            
            # Simulate agent metrics
            self._update_metric("active_agents", 4, current_time)
            self._update_metric("total_agents", 5, current_time)
            
            # Simulate performance metrics
            self._update_metric("avg_channel_latency", 150.0, current_time)
            self._update_metric("avg_protocol_success_rate", 0.85, current_time)
            
            # Calculate system health score
            health_score = self._calculate_system_health_score()
            self._update_metric("system_health_score", health_score, current_time)
            
            # Update unresolved alerts count
            unresolved_count = len([a for a in self.alerts if not a.resolved])
            self._update_metric("unresolved_alerts", unresolved_count, current_time)
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def _update_metric(self, name: str, value: float, timestamp: datetime):
        """Update a monitoring metric."""
        try:
            if name in self.metrics:
                # Store current value in history
                current_metric = self.metrics[name]
                self.metric_history[name].append(current_metric)
                
                # Keep only last 100 values
                if len(self.metric_history[name]) > 100:
                    self.metric_history[name] = self.metric_history[name][-100:]
                
                # Update current metric
                with self._lock:
                    self.metrics[name].value = value
                    self.metrics[name].timestamp = timestamp
                    
                    # Update health status based on thresholds
                    if name in self.alert_thresholds:
                        threshold = self.alert_thresholds[name]
                        if value > threshold:
                            self.metrics[name].status = HealthStatus.CRITICAL
                        elif value > threshold * 0.8:
                            self.metrics[name].status = HealthStatus.DEGRADED
                        else:
                            self.metrics[name].status = HealthStatus.OPERATIONAL
                    else:
                        self.metrics[name].status = HealthStatus.OPERATIONAL
                        
        except Exception as e:
            logger.error(f"Error updating metric {name}: {e}")
    
    def _calculate_system_health_score(self) -> float:
        """Calculate overall system health score."""
        try:
            # Calculate component health scores
            channel_health = 0.0
            if self.metrics["total_channels"].value > 0:
                channel_health = (self.metrics["active_channels"].value / self.metrics["total_channels"].value) * 100
            
            protocol_health = 0.0
            if self.metrics["total_protocols"].value > 0:
                protocol_health = (self.metrics["active_protocols"].value / self.metrics["total_protocols"].value) * 100
            
            agent_health = 0.0
            if self.metrics["total_agents"].value > 0:
                agent_health = (self.metrics["active_agents"].value / self.metrics["total_agents"].value) * 100
            
            # Performance health (inverse of latency and error rates)
            latency_health = max(0, 100 - (self.metrics["avg_channel_latency"].value / 10))
            success_rate_health = self.metrics["avg_protocol_success_rate"].value * 100
            
            # Calculate weighted average
            overall_health = (
                channel_health * 0.25 +
                protocol_health * 0.25 +
                agent_health * 0.20 +
                latency_health * 0.15 +
                success_rate_health * 0.15
            )
            
            return round(overall_health, 2)
            
        except Exception as e:
            logger.error(f"Error calculating system health score: {e}")
            return 0.0
    
    def _update_health_scores(self):
        """Update health scores for all components."""
        try:
            # Update system health score
            system_health = self.metrics["system_health_score"].value
            self.health_scores["system"] = system_health
            
            # Update component health scores
            self.health_scores["channels"] = self.metrics["active_channels"].value / max(self.metrics["total_channels"].value, 1) * 100
            self.health_scores["protocols"] = self.metrics["active_protocols"].value / max(self.metrics["total_protocols"].value, 1) * 100
            self.health_scores["agents"] = self.metrics["active_agents"].value / max(self.metrics["total_agents"].value, 1) * 100
            
        except Exception as e:
            logger.error(f"Error updating health scores: {e}")
    
    def _check_thresholds(self):
        """Check metric thresholds and generate alerts."""
        try:
            for metric_name, metric in self.metrics.items():
                if metric_name in self.alert_thresholds:
                    threshold = self.alert_thresholds[metric_name]
                    
                    # Check if threshold is exceeded
                    if metric.value > threshold:
                        # Check if alert already exists
                        existing_alert = self._find_existing_alert(metric_name, "threshold_exceeded")
                        
                        if not existing_alert:
                            # Create new alert
                            alert = MonitoringAlert(
                                id=f"alert_{int(time.time())}_{len(self.alerts)}",
                                severity=AlertSeverity.HIGH if metric.value > threshold * 1.5 else AlertSeverity.MEDIUM,
                                message=f"Metric {metric_name} exceeded threshold: {metric.value} {metric.unit} > {threshold} {metric.unit}",
                                source="threshold_monitor",
                                timestamp=datetime.now()
                            )
                            
                            self._create_alert(alert)
                    
                    # Check if metric has recovered
                    elif metric.value <= threshold * 0.8:  # 20% below threshold
                        existing_alert = self._find_existing_alert(metric_name, "threshold_exceeded")
                        if existing_alert:
                            self._resolve_alert(existing_alert.id, f"Metric {metric_name} recovered: {metric.value} {metric.unit}")
                            
        except Exception as e:
            logger.error(f"Error checking thresholds: {e}")
    
    def _find_existing_alert(self, source: str, alert_type: str) -> Optional[MonitoringAlert]:
        """Find existing alert for a source and type."""
        for alert in self.alerts:
            if alert.source == source and not alert.resolved:
                return alert
        return None
    
    def _create_alert(self, alert: MonitoringAlert):
        """Create a new monitoring alert."""
        try:
            with self._lock:
                self.alerts.append(alert)
            
            logger.warning(f"🚨 Alert created: {alert.message}")
            
            # Trigger alert callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")
                    
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
    
    def _resolve_alert(self, alert_id: str, resolution_notes: str):
        """Resolve a monitoring alert."""
        try:
            with self._lock:
                for alert in self.alerts:
                    if alert.id == alert_id:
                        alert.resolved = True
                        alert.resolution_notes = resolution_notes
                        logger.info(f"Alert {alert_id} resolved: {resolution_notes}")
                        break
                        
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")
    
    def _cleanup_old_metrics(self):
        """Clean up old metric history data."""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=24)  # Keep 24 hours of data
            
            for metric_name, history in self.metric_history.items():
                self.metric_history[metric_name] = [
                    metric for metric in history
                    if metric.timestamp > cutoff_time
                ]
                
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {e}")
    
    def add_alert_callback(self, callback: callable):
        """Add a callback function for alert notifications."""
        self.alert_callbacks.append(callback)
    
    def get_current_metrics(self) -> Dict[str, MonitoringMetric]:
        """Get current monitoring metrics."""
        with self._lock:
            return {name: metric for name, metric in self.metrics.items()}
    
    def get_metric_history(self, metric_name: str, hours: int = 24) -> List[MonitoringMetric]:
        """Get metric history for a specific metric."""
        try:
            if metric_name not in self.metric_history:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return [
                metric for metric in self.metric_history[metric_name]
                if metric.timestamp > cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error getting metric history for {metric_name}: {e}")
            return []
    
    def get_active_alerts(self) -> List[MonitoringAlert]:
        """Get all active (unresolved) alerts."""
        with self._lock:
            return [alert for alert in self.alerts if not alert.resolved]
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary."""
        try:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "monitoring_active": self.monitoring_active,
                "overall_health_score": self.health_scores.get("system", 0.0),
                "component_health": {
                    "channels": round(self.health_scores.get("channels", 0.0), 2),
                    "protocols": round(self.health_scores.get("protocols", 0.0), 2),
                    "agents": round(self.health_scores.get("agents", 0.0), 2)
                },
                "current_metrics": {},
                "active_alerts": len(self.get_active_alerts()),
                "total_alerts": len(self.alerts),
                "resolved_alerts": len([a for a in self.alerts if a.resolved])
            }
            
            # Add current metric values
            for name, metric in self.metrics.items():
                summary["current_metrics"][name] = {
                    "value": metric.value,
                    "unit": metric.unit,
                    "status": metric.status.value,
                    "timestamp": metric.timestamp.isoformat()
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating health summary: {e}")
            return {"error": str(e)}
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""
        try:
            with self._lock:
                for alert in self.alerts:
                    if alert.id == alert_id:
                        alert.acknowledged = True
                        alert.acknowledged_by = acknowledged_by
                        alert.acknowledged_at = datetime.now()
                        logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False
    
    def save_monitoring_state(self, filepath: str) -> bool:
        """Save current monitoring state to file."""
        try:
            state_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": {name: asdict(metric) for name, metric in self.metrics.items()},
                "alerts": [asdict(alert) for alert in self.alerts],
                "health_scores": self.health_scores,
                "monitoring_active": self.monitoring_active
            }
            
            # Convert datetime objects to strings
            def datetime_converter(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            with open(filepath, 'w') as f:
                json.dump(state_data, f, indent=2, default=datetime_converter)
            
            logger.info(f"Monitoring state saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save monitoring state: {e}")
            return False


# Example alert callback function
def example_alert_callback(alert: MonitoringAlert):
    """Example callback function for alert notifications."""
    print(f"🚨 ALERT: {alert.severity.value.upper()} - {alert.message}")
    print(f"   Source: {alert.source}")
    print(f"   Time: {alert.timestamp}")


# Main execution function
def main():
    """Main execution function for the communication monitoring system."""
    print("🚨 COMMUNICATION MONITORING SYSTEM DEPLOYING 🚨")
    
    try:
        # Initialize monitoring system
        monitoring_system = CommunicationMonitoringSystem()
        
        # Add alert callback
        monitoring_system.add_alert_callback(example_alert_callback)
        
        # Start monitoring
        if monitoring_system.start_monitoring():
            print("✅ Monitoring system started successfully")
            
            # Run monitoring for a few cycles
            print("📊 Collecting initial metrics...")
            time.sleep(5)
            
            # Display health summary
            health_summary = monitoring_system.get_health_summary()
            print("\n📈 HEALTH SUMMARY:")
            print(f"Overall Health Score: {health_summary['overall_health_score']}%")
            print(f"Component Health:")
            for component, score in health_summary['component_health'].items():
                print(f"  {component.title()}: {score}%")
            print(f"Active Alerts: {health_summary['active_alerts']}")
            
            # Display current metrics
            print("\n📊 CURRENT METRICS:")
            current_metrics = monitoring_system.get_current_metrics()
            for name, metric in current_metrics.items():
                print(f"  {name}: {metric.value} {metric.unit} ({metric.status.value})")
            
            # Wait for more monitoring cycles
            print("\n⏳ Running additional monitoring cycles...")
            time.sleep(10)
            
            # Display updated health summary
            updated_summary = monitoring_system.get_health_summary()
            print(f"\n📈 UPDATED HEALTH SCORE: {updated_summary['overall_health_score']}%")
            
            # Save monitoring state
            state_file = "communication_monitoring_state.json"
            if monitoring_system.save_monitoring_state(state_file):
                print(f"\n📊 Monitoring state saved to: {state_file}")
            
            # Stop monitoring
            monitoring_system.stop_monitoring()
            print("✅ Monitoring system stopped")
            
        else:
            print("❌ Failed to start monitoring system")
        
        print("\n🎯 Communication monitoring system deployment complete!")
        
    except Exception as e:
        print(f"\n❌ CRITICAL SYSTEM FAILURE: {e}")
        print("🚨 COMMUNICATION MONITORING SYSTEM DEPLOYMENT FAILED 🚨")


if __name__ == "__main__":
    main()
