#!/usr/bin/env python3
"""
Decision Metrics Manager - Agent Cellphone V2

Manages decision performance tracking, analytics, and reporting.
Handles metrics collection, analysis, and performance optimization.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Large File Modularization
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .decision_models import DecisionMetrics, DecisionType, DecisionPriority, DecisionStatus


@dataclass
class MetricsSnapshot:
    """Snapshot of decision metrics at a point in time"""
    snapshot_id: str
    timestamp: str
    total_decisions: int
    successful_decisions: int
    failed_decisions: int
    average_decision_time: float
    success_rate: float
    performance_score: float
    metrics_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAlert:
    """Performance alert for decision metrics"""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    threshold_value: float
    current_value: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    acknowledged: bool = False
    resolved: bool = False


class DecisionMetricsManager:
    """
    Decision Metrics Manager - TASK 3A
    
    Manages decision performance tracking, analytics, and reporting.
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DecisionMetricsManager")
        
        # Metrics storage
        self.metrics: Dict[str, DecisionMetrics] = {}
        self.metrics_history: List[MetricsSnapshot] = []
        self.performance_alerts: List[PerformanceAlert] = []
        
        # Performance tracking
        self.total_decisions_tracked = 0
        self.successful_decisions_tracked = 0
        self.failed_decisions_tracked = 0
        self.total_decision_time = 0.0
        
        # Configuration
        self.snapshot_interval_minutes = 15
        self.last_snapshot_time: Optional[datetime] = None
        self.alert_thresholds = {
            "success_rate": 0.8,
            "average_decision_time": 5.0,
            "performance_score": 0.7
        }
        
        # Status
        self.initialized = False
        
        self.logger.info("DecisionMetricsManager initialized")

    def initialize(self):
        """Initialize the metrics manager"""
        try:
            if self.initialized:
                self.logger.info("Metrics manager already initialized")
                return
            
            # Initialize default metrics
            self._initialize_default_metrics()
            
            # Initialize first snapshot
            self._create_metrics_snapshot()
            
            self.initialized = True
            self.logger.info("Metrics manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize metrics manager: {e}")

    def shutdown(self):
        """Shutdown the metrics manager"""
        try:
            self.initialized = False
            self.metrics.clear()
            self.metrics_history.clear()
            self.performance_alerts.clear()
            self.logger.info("Metrics manager shutdown successfully")
            
        except Exception as e:
            self.logger.error(f"Error during metrics manager shutdown: {e}")

    def is_initialized(self) -> bool:
        """Check if the manager is initialized"""
        return self.initialized

    def _initialize_default_metrics(self):
        """Initialize default decision metrics"""
        try:
            # Overall decision metrics
            overall_metrics = DecisionMetrics(
                metrics_id="overall_decisions",
                name="Overall Decision Metrics",
                description="Aggregate metrics for all decisions",
                metrics_type=DecisionType.RULE_BASED,
                current_value=0.0,
                target_value=1.0,
                unit="score",
                is_active=True
            )
            self.metrics["overall_decisions"] = overall_metrics
            
            # Success rate metrics
            success_metrics = DecisionMetrics(
                metrics_id="success_rate",
                name="Decision Success Rate",
                description="Percentage of successful decisions",
                metrics_type=DecisionType.RULE_BASED,
                current_value=0.0,
                target_value=0.9,
                unit="percentage",
                is_active=True
            )
            self.metrics["success_rate"] = success_metrics
            
            # Decision time metrics
            time_metrics = DecisionMetrics(
                metrics_id="decision_time",
                name="Average Decision Time",
                description="Average time to make decisions",
                metrics_type=DecisionType.RULE_BASED,
                current_value=0.0,
                target_value=2.0,
                unit="seconds",
                is_active=True
            )
            self.metrics["decision_time"] = time_metrics
            
            # Performance score metrics
            performance_metrics = DecisionMetrics(
                metrics_id="performance_score",
                name="Decision Performance Score",
                description="Overall performance score for decisions",
                metrics_type=DecisionType.RULE_BASED,
                current_value=0.0,
                target_value=0.8,
                unit="score",
                is_active=True
            )
            self.metrics["performance_score"] = performance_metrics
            
            self.logger.info(f"Initialized {len(self.metrics)} default metrics")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default metrics: {e}")

    def register_metrics(self, metrics: DecisionMetrics) -> bool:
        """Register new decision metrics"""
        try:
            if not self.initialized:
                self.logger.warning("Metrics manager not initialized, skipping registration")
                return False
            
            metrics_id = metrics.metrics_id
            if metrics_id in self.metrics:
                self.logger.warning(f"Metrics {metrics_id} already registered, updating")
            
            self.metrics[metrics_id] = metrics
            
            self.logger.info(f"Registered metrics: {metrics_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register metrics: {e}")
            return False

    def unregister_metrics(self, metrics_id: str) -> bool:
        """Unregister decision metrics"""
        try:
            if metrics_id not in self.metrics:
                self.logger.warning(f"Metrics {metrics_id} not found")
                return False
            
            del self.metrics[metrics_id]
            
            self.logger.info(f"Unregistered metrics: {metrics_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister metrics {metrics_id}: {e}")
            return False

    def get_metrics(self, metrics_id: str) -> Optional[DecisionMetrics]:
        """Get decision metrics by ID"""
        try:
            return self.metrics.get(metrics_id)
        except Exception as e:
            self.logger.error(f"Failed to get metrics {metrics_id}: {e}")
            return None

    def list_metrics(self) -> List[str]:
        """List all available metrics IDs"""
        try:
            return list(self.metrics.keys())
        except Exception as e:
            self.logger.error(f"Failed to list metrics: {e}")
            return []

    def update_metrics(self):
        """Update all decision metrics"""
        try:
            if not self.initialized:
                self.logger.warning("Metrics manager not initialized, skipping update")
                return
            
            # Calculate current metrics values
            self._calculate_current_metrics()
            
            # Check if snapshot is needed
            if self._should_create_snapshot():
                self._create_metrics_snapshot()
            
            # Check for performance alerts
            self._check_performance_alerts()
            
            self.logger.debug("Metrics updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update metrics: {e}")

    def _calculate_current_metrics(self):
        """Calculate current values for all metrics"""
        try:
            # Calculate success rate
            if self.total_decisions_tracked > 0:
                success_rate = self.successful_decisions_tracked / self.total_decisions_tracked
                if "success_rate" in self.metrics:
                    self.metrics["success_rate"].current_value = success_rate
            
            # Calculate average decision time
            if self.successful_decisions_tracked > 0:
                avg_decision_time = self.total_decision_time / self.successful_decisions_tracked
                if "decision_time" in self.metrics:
                    self.metrics["decision_time"].current_value = avg_decision_time
            
            # Calculate performance score
            if "success_rate" in self.metrics and "decision_time" in self.metrics:
                success_score = self.metrics["success_rate"].current_value
                time_score = max(0.0, 1.0 - (self.metrics["decision_time"].current_value / 10.0))
                performance_score = (success_score * 0.7) + (time_score * 0.3)
                
                if "performance_score" in self.metrics:
                    self.metrics["performance_score"].current_value = performance_score
            
            # Update overall metrics
            if "overall_decisions" in self.metrics:
                self.metrics["overall_decisions"].current_value = self.total_decisions_tracked
                
        except Exception as e:
            self.logger.error(f"Failed to calculate current metrics: {e}")

    def _should_create_snapshot(self) -> bool:
        """Check if a new snapshot should be created"""
        try:
            if not self.last_snapshot_time:
                return True
            
            time_since_last = datetime.now() - self.last_snapshot_time
            return time_since_last.total_seconds() >= (self.snapshot_interval_minutes * 60)
            
        except Exception as e:
            self.logger.error(f"Failed to check snapshot timing: {e}")
            return False

    def _create_metrics_snapshot(self):
        """Create a new metrics snapshot"""
        try:
            snapshot = MetricsSnapshot(
                snapshot_id=f"snapshot_{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                total_decisions=self.total_decisions_tracked,
                successful_decisions=self.successful_decisions_tracked,
                failed_decisions=self.failed_decisions_tracked,
                average_decision_time=self.total_decision_time / max(1, self.successful_decisions_tracked),
                success_rate=self.successful_decisions_tracked / max(1, self.total_decisions_tracked),
                performance_score=self.metrics.get("performance_score", {}).get("current_value", 0.0),
                metrics_data={
                    metrics_id: {
                        "current_value": metrics.current_value,
                        "target_value": metrics.target_value,
                        "unit": metrics.unit
                    }
                    for metrics_id, metrics in self.metrics.items()
                }
            )
            
            self.metrics_history.append(snapshot)
            
            # Keep only last 100 snapshots
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            self.last_snapshot_time = datetime.now()
            
            self.logger.info(f"Created metrics snapshot: {snapshot.snapshot_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to create metrics snapshot: {e}")

    def _check_performance_alerts(self):
        """Check for performance alerts based on thresholds"""
        try:
            for metrics_id, metrics in self.metrics.items():
                if not metrics.is_active:
                    continue
                
                current_value = metrics.current_value
                target_value = metrics.target_value
                
                # Check if threshold is exceeded
                if current_value < target_value:
                    alert_type = f"{metrics_id}_below_threshold"
                    severity = "warning" if current_value >= target_value * 0.8 else "critical"
                    
                    # Check if alert already exists
                    existing_alert = next(
                        (alert for alert in self.performance_alerts 
                         if alert.alert_type == alert_type and not alert.resolved),
                        None
                    )
                    
                    if not existing_alert:
                        alert = PerformanceAlert(
                            alert_id=f"alert_{alert_type}_{int(time.time())}",
                            alert_type=alert_type,
                            severity=severity,
                            message=f"{metrics.name} is below threshold: {current_value} < {target_value}",
                            threshold_value=target_value,
                            current_value=current_value
                        )
                        self.performance_alerts.append(alert)
                        
                        self.logger.warning(f"Performance alert created: {alert.message}")
                
                # Check if performance has improved (resolve alerts)
                elif current_value >= target_value:
                    alert_type = f"{metrics_id}_below_threshold"
                    existing_alerts = [
                        alert for alert in self.performance_alerts
                        if alert.alert_type == alert_type and not alert.resolved
                    ]
                    
                    for alert in existing_alerts:
                        alert.resolved = True
                        alert.timestamp = datetime.now().isoformat()
                        
                        self.logger.info(f"Performance alert resolved: {alert.message}")
                        
        except Exception as e:
            self.logger.error(f"Failed to check performance alerts: {e}")

    def record_decision_result(self, decision_id: str, success: bool, execution_time: float):
        """Record the result of a decision"""
        try:
            if not self.initialized:
                self.logger.warning("Metrics manager not initialized, skipping recording")
                return
            
            # Update counters
            self.total_decisions_tracked += 1
            if success:
                self.successful_decisions_tracked += 1
                self.total_decision_time += execution_time
            else:
                self.failed_decisions_tracked += 1
            
            self.logger.debug(f"Recorded decision result: {decision_id}, success: {success}, time: {execution_time}")
            
        except Exception as e:
            self.logger.error(f"Failed to record decision result: {e}")

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        try:
            if not self.initialized:
                return {"error": "Metrics manager not initialized"}
            
            summary = {
                "total_decisions": self.total_decisions_tracked,
                "successful_decisions": self.successful_decisions_tracked,
                "failed_decisions": self.failed_decisions_tracked,
                "success_rate": (self.successful_decisions_tracked / self.total_decisions_tracked * 100) if self.total_decisions_tracked > 0 else 0,
                "average_decision_time": (self.total_decision_time / self.successful_decisions_tracked) if self.successful_decisions_tracked > 0 else 0,
                "metrics": {},
                "last_snapshot": self.last_snapshot_time.isoformat() if self.last_snapshot_time else None,
                "total_snapshots": len(self.metrics_history),
                "active_alerts": len([alert for alert in self.performance_alerts if not alert.resolved])
            }
            
            # Add individual metrics
            for metrics_id, metrics in self.metrics.items():
                summary["metrics"][metrics_id] = {
                    "name": metrics.name,
                    "current_value": metrics.current_value,
                    "target_value": metrics.target_value,
                    "unit": metrics.unit,
                    "is_active": metrics.is_active
                }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get metrics summary: {e}")
            return {"error": str(e)}

    def get_metrics_history(self, hours: int = 24) -> List[MetricsSnapshot]:
        """Get metrics history for the specified time period"""
        try:
            if not self.initialized:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            filtered_snapshots = [
                snapshot for snapshot in self.metrics_history
                if datetime.fromisoformat(snapshot.timestamp) >= cutoff_time
            ]
            
            return filtered_snapshots
            
        except Exception as e:
            self.logger.error(f"Failed to get metrics history: {e}")
            return []

    def get_performance_alerts(self, include_resolved: bool = False) -> List[PerformanceAlert]:
        """Get performance alerts"""
        try:
            if not self.initialized:
                return []
            
            if include_resolved:
                return self.performance_alerts
            else:
                return [alert for alert in self.performance_alerts if not alert.resolved]
                
        except Exception as e:
            self.logger.error(f"Failed to get performance alerts: {e}")
            return []

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a performance alert"""
        try:
            alert = next((a for a in self.performance_alerts if a.alert_id == alert_id), None)
            if not alert:
                self.logger.warning(f"Alert {alert_id} not found")
                return False
            
            alert.acknowledged = True
            self.logger.info(f"Alert {alert_id} acknowledged")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve a performance alert"""
        try:
            alert = next((a for a in self.performance_alerts if a.alert_id == alert_id), None)
            if not alert:
                self.logger.warning(f"Alert {alert_id} not found")
                return False
            
            alert.resolved = True
            alert.timestamp = datetime.now().isoformat()
            self.logger.info(f"Alert {alert_id} resolved")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False

    def clear_old_alerts(self, days: int = 30):
        """Clear old resolved alerts"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            
            # Keep only recent alerts or unresolved alerts
            self.performance_alerts = [
                alert for alert in self.performance_alerts
                if (not alert.resolved or 
                    datetime.fromisoformat(alert.timestamp) >= cutoff_time)
            ]
            
            self.logger.info(f"Cleared old alerts, remaining: {len(self.performance_alerts)}")
            
        except Exception as e:
            self.logger.error(f"Failed to clear old alerts: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get metrics manager status"""
        try:
            return {
                "initialized": self.initialized,
                "total_metrics": len(self.metrics),
                "active_metrics": len([m for m in self.metrics.values() if m.is_active]),
                "total_decisions_tracked": self.total_decisions_tracked,
                "successful_decisions_tracked": self.successful_decisions_tracked,
                "failed_decisions_tracked": self.failed_decisions_tracked,
                "total_snapshots": len(self.metrics_history),
                "active_alerts": len([alert for alert in self.performance_alerts if not alert.resolved]),
                "last_snapshot": self.last_snapshot_time.isoformat() if self.last_snapshot_time else None
            }
        except Exception as e:
            self.logger.error(f"Failed to get metrics manager status: {e}")
            return {"error": str(e)}

