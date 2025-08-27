#!/usr/bin/env python3
"""
Quality Monitoring System
=========================

Real-time quality monitoring, alerting, and trend analysis for V2 services.
Follows V2 coding standards: ≤300 lines per module.
"""

import time
import logging
import threading
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta

from .core_framework import QualityLevel, QualityMetric, TestResult
from .models import QualityAlert

logger = logging.getLogger(__name__)


class QualityMonitor:
    """Real-time quality monitoring for services"""
    
    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self.monitored_services: Dict[str, Dict[str, Any]] = {}
        self.alert_callbacks: List[Callable] = []
        self._monitoring = False
        self._monitor_thread = None
        self._lock = threading.Lock()
        
        logger.info("Quality Monitor initialized")
        
    def add_service_monitoring(self, service_id: str, metrics: List[str], 
                             thresholds: Dict[str, Any]) -> bool:
        """Add a service for quality monitoring"""
        try:
            with self._lock:
                self.monitored_services[service_id] = {
                    "metrics": metrics,
                    "thresholds": thresholds,
                    "last_check": time.time(),
                    "alert_count": 0
                }
            logger.info(f"Service {service_id} added to quality monitoring")
            return True
        except Exception as e:
            logger.error(f"Failed to add service monitoring for {service_id}: {e}")
            return False
            
    def remove_service_monitoring(self, service_id: str) -> bool:
        """Remove a service from quality monitoring"""
        try:
            with self._lock:
                self.monitored_services.pop(service_id, None)
            logger.info(f"Service {service_id} removed from quality monitoring")
            return True
        except Exception as e:
            logger.error(f"Failed to remove service monitoring for {service_id}: {e}")
            return False
            
    def add_alert_callback(self, callback: Callable) -> None:
        """Add callback function for quality alerts"""
        self.alert_callbacks.append(callback)
        
    def start_monitoring(self) -> bool:
        """Start the quality monitoring system"""
        if self._monitoring:
            logger.warning("Quality monitoring already running")
            return False
            
        try:
            self._monitoring = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            logger.info("Quality monitoring started")
            return True
        except Exception as e:
            logger.error(f"Failed to start quality monitoring: {e}")
            self._monitoring = False
            return False
            
    def stop_monitoring(self) -> bool:
        """Stop the quality monitoring system"""
        if not self._monitoring:
            logger.warning("Quality monitoring not running")
            return False
            
        try:
            self._monitoring = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=5.0)
            logger.info("Quality monitoring stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop quality monitoring: {e}")
            return False
            
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self._monitoring:
            try:
                self._check_service_quality()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)
                
    def _check_service_quality(self) -> None:
        """Check quality for all monitored services"""
        current_time = time.time()
        
        with self._lock:
            for service_id, service_info in self.monitored_services.items():
                # Check if it's time to monitor this service
                if current_time - service_info["last_check"] >= self.check_interval:
                    self._evaluate_service_quality(service_id, service_info)
                    service_info["last_check"] = current_time
                    
    def _evaluate_service_quality(self, service_id: str, service_info: Dict[str, Any]) -> None:
        """Evaluate quality for a specific service"""
        try:
            # This would typically integrate with the quality framework
            # For now, we'll simulate quality checks
            logger.debug(f"Evaluating quality for service {service_id}")
            
            # Check if any thresholds are exceeded
            # This is a placeholder for actual quality evaluation logic
            
        except Exception as e:
            logger.error(f"Failed to evaluate quality for {service_id}: {e}")


class QualityAlertManager:
    """Manages quality alerts and notifications"""
    
    def __init__(self):
        self.alerts: Dict[str, QualityAlert] = {}
        self.alert_history: List[QualityAlert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
        # Default alert rules
        self._setup_default_rules()
        
        logger.info("Quality Alert Manager initialized")
        
    def _setup_default_rules(self) -> None:
        """Setup default alert rules"""
        self.alert_rules = {
            "test_failure": {
                "threshold": 0,
                "severity": "high",
                "message": "Test failures detected"
            },
            "performance_degradation": {
                "threshold": 100.0,
                "severity": "medium",
                "message": "Performance degradation detected"
            },
            "low_coverage": {
                "threshold": 80.0,
                "severity": "medium",
                "message": "Test coverage below threshold"
            }
        }
        
    def create_alert(self, service_id: str, alert_type: str, 
                    metric_value: Any, threshold: Any, 
                    custom_message: str = None) -> str:
        """Create a new quality alert"""
        try:
            alert_id = f"alert_{service_id}_{alert_type}_{int(time.time())}"
            
            rule = self.alert_rules.get(alert_type, {})
            severity = rule.get("severity", "medium")
            message = custom_message or rule.get("message", f"Quality alert: {alert_type}")
            
            alert = QualityAlert(
                alert_id=alert_id,
                service_id=service_id,
                alert_type=alert_type,
                severity=severity,
                message=message,
                timestamp=time.time(),
                metric_value=metric_value,
                threshold=threshold
            )
            
            with self._lock:
                self.alerts[alert_id] = alert
                self.alert_history.append(alert)
                
            logger.warning(f"Quality alert created: {alert_id} - {message}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
            return ""
            
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        try:
            with self._lock:
                if alert_id in self.alerts:
                    self.alerts[alert_id].resolved = True
                    logger.info(f"Alert {alert_id} marked as resolved")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False
            
    def get_active_alerts(self, service_id: str = None) -> List[QualityAlert]:
        """Get active (unresolved) alerts"""
        with self._lock:
            if service_id:
                return [alert for alert in self.alerts.values() 
                       if not alert.resolved and alert.service_id == service_id]
            return [alert for alert in self.alerts.values() if not alert.resolved]
            
    def get_alert_history(self, service_id: str = None, 
                         alert_type: str = None) -> List[QualityAlert]:
        """Get alert history with optional filtering"""
        with self._lock:
            filtered_alerts = self.alert_history
            
            if service_id:
                filtered_alerts = [alert for alert in filtered_alerts 
                                 if alert.service_id == service_id]
            if alert_type:
                filtered_alerts = [alert for alert in filtered_alerts 
                                 if alert.alert_type == alert_type]
                                 
            return filtered_alerts
            
    def add_alert_rule(self, alert_type: str, threshold: Any, 
                       severity: str, message: str) -> bool:
        """Add a new alert rule"""
        try:
            self.alert_rules[alert_type] = {
                "threshold": threshold,
                "severity": severity,
                "message": message
            }
            logger.info(f"Alert rule added: {alert_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to add alert rule: {e}")
            return False


class QualityTrendAnalyzer:
    """Analyzes quality trends over time"""
    
    def __init__(self, history_window: int = 100):
        self.history_window = history_window
        self.quality_history: Dict[str, List[Dict[str, Any]]] = {}
        
        logger.info("Quality Trend Analyzer initialized")
        
    def add_quality_data(self, service_id: str, quality_score: float, 
                        timestamp: float = None) -> None:
        """Add quality data point for trend analysis"""
        if timestamp is None:
            timestamp = time.time()
            
        if service_id not in self.quality_history:
            self.quality_history[service_id] = []
            
        data_point = {
            "score": quality_score,
            "timestamp": timestamp
        }
        
        self.quality_history[service_id].append(data_point)
        
        # Keep only recent history
        if len(self.quality_history[service_id]) > self.history_window:
            self.quality_history[service_id] = self.quality_history[service_id][-self.history_window:]
            
    def get_quality_trend(self, service_id: str, 
                         time_window: float = 3600) -> Dict[str, Any]:
        """Get quality trend analysis for a service"""
        try:
            if service_id not in self.quality_history:
                return {"error": "No quality data available"}
                
            current_time = time.time()
            cutoff_time = current_time - time_window
            
            # Filter data within time window
            recent_data = [
                point for point in self.quality_history[service_id]
                if point["timestamp"] >= cutoff_time
            ]
            
            if not recent_data:
                return {"error": "No data in specified time window"}
                
            # Calculate trend metrics
            scores = [point["score"] for point in recent_data]
            timestamps = [point["timestamp"] for point in recent_data]
            
            trend_analysis = {
                "service_id": service_id,
                "data_points": len(recent_data),
                "current_score": scores[-1],
                "average_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores),
                "trend_direction": self._calculate_trend_direction(scores),
                "stability_score": self._calculate_stability_score(scores),
                "time_span": timestamps[-1] - timestamps[0]
            }
            
            return trend_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze quality trend for {service_id}: {e}")
            return {"error": str(e)}
            
    def _calculate_trend_direction(self, scores: List[float]) -> str:
        """Calculate overall trend direction"""
        if len(scores) < 2:
            return "insufficient_data"
            
        # Simple linear trend calculation
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 0.5:
            return "improving"
        elif second_avg < first_avg - 0.5:
            return "declining"
        else:
            return "stable"
            
    def _calculate_stability_score(self, scores: List[float]) -> float:
        """Calculate stability score based on variance"""
        if len(scores) < 2:
            return 0.0
            
        mean = sum(scores) / len(scores)
        variance = sum((score - mean) ** 2 for score in scores) / len(scores)
        
        # Convert to 0-10 scale where 10 is most stable
        stability = max(0, 10 - (variance * 10))
        return round(stability, 2)
        
    def get_system_quality_summary(self) -> Dict[str, Any]:
        """Get overall system quality summary"""
        try:
            summary = {
                "total_services": len(self.quality_history),
                "services_with_data": 0,
                "overall_average_score": 0.0,
                "trend_summary": {
                    "improving": 0,
                    "stable": 0,
                    "declining": 0
                }
            }
            
            total_score = 0.0
            service_count = 0
            
            for service_id in self.quality_history:
                if self.quality_history[service_id]:
                    service_count += 1
                    latest_score = self.quality_history[service_id][-1]["score"]
                    total_score += latest_score
                    
                    # Get trend for this service
                    trend = self.get_quality_trend(service_id)
                    if "trend_direction" in trend:
                        direction = trend["trend_direction"]
                        if direction in summary["trend_summary"]:
                            summary["trend_summary"][direction] += 1
                            
            summary["services_with_data"] = service_count
            if service_count > 0:
                summary["overall_average_score"] = round(total_score / service_count, 2)
                
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get system quality summary: {e}")
            return {"error": str(e)}
