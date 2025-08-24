#!/usr/bin/env python3
"""
Performance Alert Manager - V2 Core Performance System
======================================================

Handles performance alerting and notification management.
Follows Single Responsibility Principle - alert management only.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import
from ..metrics.collector import PerformanceBenchmark, PerformanceLevel, BenchmarkType


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertType(Enum):
    """Types of performance alerts"""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    TARGET_MISSED = "target_missed"
    SYSTEM_OVERLOAD = "system_overload"
    RELIABILITY_ISSUE = "reliability_issue"
    SCALABILITY_LIMIT = "scalability_limit"
    THRESHOLD_BREACH = "threshold_breach"


@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    benchmark_id: str
    benchmark_type: BenchmarkType
    triggered_at: str
    resolved_at: Optional[str]
    is_resolved: bool
    metadata: Dict[str, Any]


class AlertManager:
    """
    Performance alert management and notification system
    
    Responsibilities:
    - Monitor performance metrics for alert conditions
    - Generate and manage performance alerts
    - Handle alert notifications and escalation
    - Track alert history and resolution
    """
    
    def __init__(self):
        self.alerts: Dict[str, PerformanceAlert] = {}
        self.alert_handlers: Dict[AlertSeverity, List[Callable]] = {
            severity: [] for severity in AlertSeverity
        }
        
        # Alert thresholds
        self.alert_thresholds = {
            BenchmarkType.RESPONSE_TIME: {
                "critical": 500,  # 500ms
                "high": 200,      # 200ms
                "medium": 150,    # 150ms
            },
            BenchmarkType.THROUGHPUT: {
                "critical": 100,  # 100 ops/sec
                "high": 500,      # 500 ops/sec
                "medium": 750,    # 750 ops/sec
            },
            BenchmarkType.RELIABILITY: {
                "critical": 95.0,  # 95%
                "high": 98.0,      # 98%
                "medium": 99.0,    # 99%
            },
            BenchmarkType.SCALABILITY: {
                "critical": 30.0,  # 30% scalability score
                "high": 50.0,      # 50% scalability score
                "medium": 70.0,    # 70% scalability score
            },
            BenchmarkType.LATENCY: {
                "critical": 200,   # 200ms
                "high": 100,       # 100ms
                "medium": 75,      # 75ms
            },
        }
        
        self.logger = logging.getLogger(f"{__name__}.AlertManager")
    
    def check_benchmark_for_alerts(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check a benchmark result for alert conditions"""
        try:
            alerts = []
            
            # Check performance level alerts
            if benchmark.performance_level == PerformanceLevel.NOT_READY:
                alert = self._create_performance_level_alert(benchmark, AlertSeverity.CRITICAL)
                alerts.append(alert)
            elif benchmark.performance_level == PerformanceLevel.DEVELOPMENT_READY:
                alert = self._create_performance_level_alert(benchmark, AlertSeverity.HIGH)
                alerts.append(alert)
            
            # Check threshold breaches
            threshold_alerts = self._check_threshold_breaches(benchmark)
            alerts.extend(threshold_alerts)
            
            # Check for specific benchmark type issues
            type_specific_alerts = self._check_type_specific_issues(benchmark)
            alerts.extend(type_specific_alerts)
            
            # Store and trigger alerts
            for alert in alerts:
                self._store_and_trigger_alert(alert)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check benchmark for alerts: {e}")
            return []
    
    def register_alert_handler(self, severity: AlertSeverity, handler: Callable[[PerformanceAlert], None]) -> None:
        """Register an alert handler for a specific severity level"""
        try:
            self.alert_handlers[severity].append(handler)
            self.logger.info(f"Registered alert handler for {severity.value} alerts")
            
        except Exception as e:
            self.logger.error(f"Failed to register alert handler: {e}")
    
    def trigger_alert(self, alert: PerformanceAlert) -> bool:
        """Trigger an alert and notify handlers"""
        try:
            # Call registered handlers for this severity level
            handlers = self.alert_handlers.get(alert.severity, [])
            
            for handler in handlers:
                try:
                    handler(alert)
                except Exception as e:
                    self.logger.error(f"Alert handler failed: {e}")
            
            # Also call handlers for higher severity levels if this is critical
            if alert.severity == AlertSeverity.CRITICAL:
                for severity in [AlertSeverity.HIGH, AlertSeverity.MEDIUM, AlertSeverity.LOW]:
                    for handler in self.alert_handlers.get(severity, []):
                        try:
                            handler(alert)
                        except Exception as e:
                            self.logger.error(f"Escalated alert handler failed: {e}")
            
            self.logger.info(f"Triggered alert: {alert.alert_id} ({alert.severity.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to trigger alert: {e}")
            return False
    
    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """Mark an alert as resolved"""
        try:
            alert = self.alerts.get(alert_id)
            if not alert:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert.is_resolved = True
            alert.resolved_at = datetime.now().isoformat()
            alert.metadata["resolution_note"] = resolution_note
            
            self.logger.info(f"Resolved alert: {alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve alert: {e}")
            return False
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get all active (unresolved) alerts"""
        return [alert for alert in self.alerts.values() if not alert.is_resolved]
    
    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[PerformanceAlert]:
        """Get alerts filtered by severity"""
        return [alert for alert in self.alerts.values() if alert.severity == severity]
    
    def get_alerts_by_type(self, alert_type: AlertType) -> List[PerformanceAlert]:
        """Get alerts filtered by type"""
        return [alert for alert in self.alerts.values() if alert.alert_type == alert_type]
    
    def get_recent_alerts(self, hours: int = 24) -> List[PerformanceAlert]:
        """Get alerts from the last N hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff_time.isoformat()
            
            return [
                alert for alert in self.alerts.values()
                if alert.triggered_at >= cutoff_str
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get recent alerts: {e}")
            return []
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts"""
        try:
            total_alerts = len(self.alerts)
            active_alerts = len(self.get_active_alerts())
            
            # Count by severity
            severity_counts = {}
            for severity in AlertSeverity:
                severity_counts[severity.value] = len(self.get_alerts_by_severity(severity))
            
            # Count by type
            type_counts = {}
            for alert_type in AlertType:
                type_counts[alert_type.value] = len(self.get_alerts_by_type(alert_type))
            
            # Recent activity
            recent_alerts = len(self.get_recent_alerts(24))
            
            return {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "resolved_alerts": total_alerts - active_alerts,
                "alerts_by_severity": severity_counts,
                "alerts_by_type": type_counts,
                "recent_alerts_24h": recent_alerts,
                "alert_rate": recent_alerts / 24.0,  # alerts per hour
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get alert summary: {e}")
            return {"error": str(e)}
    
    def _create_performance_level_alert(self, benchmark: PerformanceBenchmark, 
                                      severity: AlertSeverity) -> PerformanceAlert:
        """Create an alert for performance level issues"""
        alert_id = str(uuid.uuid4())
        
        title = f"Performance Level Alert: {benchmark.test_name}"
        message = (
            f"Benchmark '{benchmark.test_name}' achieved {benchmark.performance_level.value} "
            f"performance level, which is below acceptable standards."
        )
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.PERFORMANCE_DEGRADATION,
            severity=severity,
            title=title,
            message=message,
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "performance_level": benchmark.performance_level.value,
                "duration": benchmark.duration,
                "recommendations": benchmark.optimization_recommendations,
            }
        )
    
    def _check_threshold_breaches(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check for threshold breaches in benchmark metrics"""
        alerts = []
        
        try:
            thresholds = self.alert_thresholds.get(benchmark.benchmark_type, {})
            if not thresholds:
                return alerts
            
            # Get primary metric for this benchmark type
            primary_metric = self._get_primary_metric_value(benchmark)
            if primary_metric is None:
                return alerts
            
            # Check thresholds (from most severe to least)
            for severity_name in ["critical", "high", "medium"]:
                threshold = thresholds.get(severity_name)
                if threshold is None:
                    continue
                
                if self._is_threshold_breached(benchmark.benchmark_type, primary_metric, threshold):
                    severity = AlertSeverity(severity_name.upper())
                    alert = self._create_threshold_alert(benchmark, severity, primary_metric, threshold)
                    alerts.append(alert)
                    break  # Only create one threshold alert per benchmark
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check threshold breaches: {e}")
            return []
    
    def _check_type_specific_issues(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check for benchmark type specific issues"""
        alerts = []
        
        try:
            if benchmark.benchmark_type == BenchmarkType.RELIABILITY:
                alerts.extend(self._check_reliability_issues(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.SCALABILITY:
                alerts.extend(self._check_scalability_issues(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.THROUGHPUT:
                alerts.extend(self._check_throughput_issues(benchmark))
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check type specific issues: {e}")
            return []
    
    def _check_reliability_issues(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check for reliability specific issues"""
        alerts = []
        
        success_rate = benchmark.metrics.get("success_rate_percent", 100)
        failed_ops = benchmark.metrics.get("failed_operations", 0)
        
        if failed_ops > 0:
            alert_id = str(uuid.uuid4())
            severity = AlertSeverity.HIGH if success_rate < 99.0 else AlertSeverity.MEDIUM
            
            alert = PerformanceAlert(
                alert_id=alert_id,
                alert_type=AlertType.RELIABILITY_ISSUE,
                severity=severity,
                title=f"Reliability Issue: {benchmark.test_name}",
                message=f"Detected {failed_ops} failed operations with {success_rate:.1f}% success rate",
                benchmark_id=benchmark.benchmark_id,
                benchmark_type=benchmark.benchmark_type,
                triggered_at=datetime.now().isoformat(),
                resolved_at=None,
                is_resolved=False,
                metadata={
                    "failed_operations": failed_ops,
                    "success_rate": success_rate,
                }
            )
            alerts.append(alert)
        
        return alerts
    
    def _check_scalability_issues(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check for scalability specific issues"""
        alerts = []
        
        scalability_score = benchmark.metrics.get("scalability_score", 100)
        
        if scalability_score < 50:
            alert_id = str(uuid.uuid4())
            
            alert = PerformanceAlert(
                alert_id=alert_id,
                alert_type=AlertType.SCALABILITY_LIMIT,
                severity=AlertSeverity.HIGH,
                title=f"Scalability Limit: {benchmark.test_name}",
                message=f"Poor scalability score: {scalability_score:.1f}%",
                benchmark_id=benchmark.benchmark_id,
                benchmark_type=benchmark.benchmark_type,
                triggered_at=datetime.now().isoformat(),
                resolved_at=None,
                is_resolved=False,
                metadata={
                    "scalability_score": scalability_score,
                }
            )
            alerts.append(alert)
        
        return alerts
    
    def _check_throughput_issues(self, benchmark: PerformanceBenchmark) -> List[PerformanceAlert]:
        """Check for throughput specific issues"""
        alerts = []
        
        throughput = benchmark.metrics.get("throughput_ops_per_sec", 0)
        
        if throughput < 100:  # Very low throughput
            alert_id = str(uuid.uuid4())
            
            alert = PerformanceAlert(
                alert_id=alert_id,
                alert_type=AlertType.SYSTEM_OVERLOAD,
                severity=AlertSeverity.CRITICAL,
                title=f"System Overload: {benchmark.test_name}",
                message=f"Extremely low throughput: {throughput:.1f} ops/sec",
                benchmark_id=benchmark.benchmark_id,
                benchmark_type=benchmark.benchmark_type,
                triggered_at=datetime.now().isoformat(),
                resolved_at=None,
                is_resolved=False,
                metadata={
                    "throughput": throughput,
                }
            )
            alerts.append(alert)
        
        return alerts
    
    def _create_threshold_alert(self, benchmark: PerformanceBenchmark, severity: AlertSeverity,
                              actual_value: float, threshold: float) -> PerformanceAlert:
        """Create a threshold breach alert"""
        alert_id = str(uuid.uuid4())
        
        title = f"Threshold Breach: {benchmark.test_name}"
        message = (
            f"Metric exceeded {severity.value} threshold: "
            f"actual={actual_value:.2f}, threshold={threshold:.2f}"
        )
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.THRESHOLD_BREACH,
            severity=severity,
            title=title,
            message=message,
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "actual_value": actual_value,
                "threshold": threshold,
                "breach_percentage": ((actual_value - threshold) / threshold) * 100 if threshold > 0 else 0,
            }
        )
    
    def _get_primary_metric_value(self, benchmark: PerformanceBenchmark) -> Optional[float]:
        """Get the primary metric value for a benchmark type"""
        metric_mappings = {
            BenchmarkType.RESPONSE_TIME: "average_response_time",
            BenchmarkType.THROUGHPUT: "throughput_ops_per_sec",
            BenchmarkType.SCALABILITY: "scalability_score",
            BenchmarkType.RELIABILITY: "success_rate_percent",
            BenchmarkType.LATENCY: "average_latency",
        }
        
        primary_key = metric_mappings.get(benchmark.benchmark_type)
        return benchmark.metrics.get(primary_key) if primary_key else None
    
    def _is_threshold_breached(self, benchmark_type: BenchmarkType, 
                             actual_value: float, threshold: float) -> bool:
        """Check if a threshold is breached based on benchmark type"""
        # For response time and latency, higher values are worse
        if benchmark_type in {BenchmarkType.RESPONSE_TIME, BenchmarkType.LATENCY}:
            return actual_value > threshold
        
        # For throughput, reliability, and scalability, lower values are worse
        else:
            return actual_value < threshold
    
    def _store_and_trigger_alert(self, alert: PerformanceAlert) -> None:
        """Store an alert and trigger notifications"""
        try:
            self.alerts[alert.alert_id] = alert
            self.trigger_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Failed to store and trigger alert: {e}")
    
    def clear_alerts(self) -> None:
        """Clear all stored alerts"""
        self.alerts.clear()
        self.logger.info("Cleared all alerts")
    
    def clear_resolved_alerts(self) -> int:
        """Clear resolved alerts and return count of cleared alerts"""
        try:
            resolved_count = 0
            alert_ids_to_remove = []
            
            for alert_id, alert in self.alerts.items():
                if alert.is_resolved:
                    alert_ids_to_remove.append(alert_id)
                    resolved_count += 1
            
            for alert_id in alert_ids_to_remove:
                del self.alerts[alert_id]
            
            self.logger.info(f"Cleared {resolved_count} resolved alerts")
            return resolved_count
            
        except Exception as e:
            self.logger.error(f"Failed to clear resolved alerts: {e}")
            return 0
