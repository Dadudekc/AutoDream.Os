#!/usr/bin/env python3
"""
V2 Authentication Performance Monitor
====================================

Real-time performance monitoring and analysis for V2 authentication services.
Provides detailed metrics, alerts, and performance optimization recommendations.
"""

import sys
import os
import time
import logging
import threading
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from collections import deque, defaultdict
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from auth_service import AuthService, AuthStatus
    PERFORMANCE_MONITORING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Performance monitoring components not available: {e}")
    PERFORMANCE_MONITORING_AVAILABLE = False

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    context: Dict[str, Any]

@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    alert_id: str
    timestamp: datetime
    alert_type: str  # "warning", "critical", "info"
    message: str
    metric_name: str
    current_value: float
    threshold: float
    severity: int  # 1-5, higher is more severe

@dataclass
class PerformanceReport:
    """Performance report data structure"""
    report_id: str
    timestamp: datetime
    time_period: str
    summary: Dict[str, Any]
    detailed_metrics: List[PerformanceMetric]
    alerts: List[PerformanceAlert]
    recommendations: List[str]

class AuthPerformanceMonitor:
    """
    V2 Authentication Performance Monitor
    Real-time monitoring and analysis of authentication performance
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.logger = self._setup_logging()
        self.config = config or self._default_config()
        
        # Performance tracking
        self.metrics_history = defaultdict(lambda: deque(maxlen=self.config["max_metrics_history"]))
        self.alerts_history = deque(maxlen=self.config["max_alerts_history"])
        self.performance_thresholds = self.config["performance_thresholds"]
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread = None
        self.monitoring_interval = self.config["monitoring_interval"]
        
        # Alert counters
        self.alert_counts = defaultdict(int)
        self.last_alert_time = defaultdict(datetime.now)
        
        # Performance baselines
        self.baselines = {}
        self.baseline_calculated = False
        
        self.logger.info("V2 Authentication Performance Monitor initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the performance monitor"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for performance monitoring"""
        return {
            "monitoring_interval": 5.0,  # 5 seconds
            "max_metrics_history": 1000,
            "max_alerts_history": 100,
            "enable_real_time_monitoring": True,
            "enable_performance_alerts": True,
            "enable_baseline_calculation": True,
            "baseline_calculation_period": 300,  # 5 minutes
            "performance_thresholds": {
                "auth_duration": {
                    "warning": 0.5,    # 500ms
                    "critical": 1.0    # 1 second
                },
                "success_rate": {
                    "warning": 0.95,   # 95%
                    "critical": 0.90   # 90%
                },
                "concurrent_auths": {
                    "warning": 50,     # 50 concurrent
                    "critical": 100    # 100 concurrent
                },
                "error_rate": {
                    "warning": 0.05,   # 5%
                    "critical": 0.10   # 10%
                }
            },
            "alert_cooldown": 300,  # 5 minutes between similar alerts
            "performance_optimization": {
                "enable_auto_optimization": False,
                "optimization_threshold": 0.8,  # 80% of threshold
                "max_optimization_attempts": 3
            }
        }
    
    def start_monitoring(self, auth_service: AuthService):
        """Start real-time performance monitoring"""
        if self.is_monitoring:
            self.logger.warning("Performance monitoring already active")
            return
        
        if not PERFORMANCE_MONITORING_AVAILABLE:
            self.logger.error("Performance monitoring components not available")
            return
        
        self.auth_service = auth_service
        self.is_monitoring = True
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info("🚀 Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time performance monitoring"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        
        self.logger.info("🛑 Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect current metrics
                self._collect_performance_metrics()
                
                # Analyze performance
                self._analyze_performance()
                
                # Check for alerts
                if self.config["enable_performance_alerts"]:
                    self._check_performance_alerts()
                
                # Calculate baselines if needed
                if self.config["enable_baseline_calculation"] and not self.baseline_calculated:
                    self._calculate_performance_baselines()
                
                # Sleep until next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_performance_metrics(self):
        """Collect current performance metrics from auth service"""
        try:
            if not hasattr(self, 'auth_service') or not self.auth_service:
                return
            
            # Get performance metrics from auth service
            metrics = self.auth_service.get_performance_metrics()
            
            # Record key metrics
            current_time = datetime.now()
            
            # Authentication duration
            if "auth_duration" in metrics:
                self._record_metric("auth_duration", metrics["auth_duration"], "seconds", {
                    "source": "auth_service",
                    "metric_type": "timing"
                })
            
            # Success rate
            if "success_rate" in metrics:
                self._record_metric("success_rate", metrics["success_rate"], "percentage", {
                    "source": "auth_service",
                    "metric_type": "ratio"
                })
            
            # Authentication throughput
            if "auth_per_second" in metrics:
                self._record_metric("auth_per_second", metrics["auth_per_second"], "auths/sec", {
                    "source": "auth_service",
                    "metric_type": "throughput"
                })
            
            # Total attempts
            if "total_attempts" in metrics:
                self._record_metric("total_attempts", metrics["total_attempts"], "count", {
                    "source": "auth_service",
                    "metric_type": "counter"
                })
            
            # Uptime
            if "uptime_seconds" in metrics:
                self._record_metric("uptime_seconds", metrics["uptime_seconds"], "seconds", {
                    "source": "auth_service",
                    "metric_type": "uptime"
                })
                
        except Exception as e:
            self.logger.error(f"Failed to collect performance metrics: {e}")
    
    def _record_metric(self, metric_name: str, value: float, unit: str, context: Dict[str, Any]):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            unit=unit,
            context=context
        )
        
        self.metrics_history[metric_name].append(metric)
    
    def _analyze_performance(self):
        """Analyze current performance metrics"""
        try:
            for metric_name, metrics in self.metrics_history.items():
                if len(metrics) < 2:  # Need at least 2 data points for analysis
                    continue
                
                # Calculate current performance indicators
                current_value = metrics[-1].value
                recent_values = [m.value for m in list(metrics)[-10:]]  # Last 10 values
                
                # Trend analysis
                if len(recent_values) >= 2:
                    trend = self._calculate_trend(recent_values)
                    
                    # Store trend information
                    self._record_metric(f"{metric_name}_trend", trend, "slope", {
                        "source": "performance_analyzer",
                        "metric_type": "trend",
                        "base_metric": metric_name
                    })
                
                # Performance degradation detection
                if self.baseline_calculated and metric_name in self.baselines:
                    baseline = self.baselines[metric_name]
                    degradation = self._detect_performance_degradation(current_value, baseline, metric_name)
                    
                    if degradation:
                        self._record_metric(f"{metric_name}_degradation", degradation, "percentage", {
                            "source": "performance_analyzer",
                            "metric_type": "degradation",
                            "base_metric": metric_name
                        })
                        
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend slope from values"""
        if len(values) < 2:
            return 0.0
        
        try:
            # Simple linear regression slope
            n = len(values)
            x_values = list(range(n))
            
            # Calculate means
            x_mean = sum(x_values) / n
            y_mean = sum(values) / n
            
            # Calculate slope
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
            denominator = sum((x - x_mean) ** 2 for x in x_values)
            
            if denominator == 0:
                return 0.0
            
            return numerator / denominator
            
        except Exception:
            return 0.0
    
    def _detect_performance_degradation(self, current_value: float, baseline: Dict[str, Any], metric_name: str) -> Optional[float]:
        """Detect performance degradation compared to baseline"""
        try:
            baseline_value = baseline.get("value", 0)
            baseline_std = baseline.get("std_dev", 0)
            
            if baseline_std == 0:
                return None
            
            # Calculate z-score
            z_score = abs(current_value - baseline_value) / baseline_std
            
            # Consider degradation if z-score > 2 (2 standard deviations)
            if z_score > 2:
                degradation = ((current_value - baseline_value) / baseline_value) * 100
                return degradation
            
            return None
            
        except Exception:
            return None
    
    def _calculate_performance_baselines(self):
        """Calculate performance baselines from historical data"""
        try:
            self.logger.info("📊 Calculating performance baselines...")
            
            for metric_name, metrics in self.metrics_history.items():
                if len(metrics) < 10:  # Need sufficient data
                    continue
                
                values = [m.value for m in metrics]
                
                baseline = {
                    "value": statistics.mean(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "min_value": min(values),
                    "max_value": max(values),
                    "sample_count": len(values),
                    "calculated_at": datetime.now()
                }
                
                self.baselines[metric_name] = baseline
                
                self.logger.info(f"✅ Baseline calculated for {metric_name}: {baseline['value']:.3f} ± {baseline['std_dev']:.3f}")
            
            self.baseline_calculated = True
            self.logger.info("✅ Performance baselines calculated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to calculate performance baselines: {e}")
    
    def _check_performance_alerts(self):
        """Check for performance alerts based on thresholds"""
        try:
            for metric_name, thresholds in self.performance_thresholds.items():
                if metric_name not in self.metrics_history or not self.metrics_history[metric_name]:
                    continue
                
                current_value = self.metrics_history[metric_name][-1].value
                
                # Check warning threshold
                if "warning" in thresholds and current_value > thresholds["warning"]:
                    self._create_alert("warning", metric_name, current_value, thresholds["warning"])
                
                # Check critical threshold
                if "critical" in thresholds and current_value > thresholds["critical"]:
                    self._create_alert("critical", metric_name, current_value, thresholds["critical"])
                    
        except Exception as e:
            self.logger.error(f"Performance alert checking failed: {e}")
    
    def _create_alert(self, alert_type: str, metric_name: str, current_value: float, threshold: float):
        """Create a performance alert"""
        # Check alert cooldown
        alert_key = f"{alert_type}_{metric_name}"
        current_time = datetime.now()
        
        if (current_time - self.last_alert_time[alert_key]).total_seconds() < self.config["alert_cooldown"]:
            return
        
        # Create alert
        alert = PerformanceAlert(
            alert_id=f"alert_{int(time.time())}_{alert_type}_{metric_name}",
            timestamp=current_time,
            alert_type=alert_type,
            message=f"Performance {alert_type}: {metric_name} = {current_value:.3f} (threshold: {threshold:.3f})",
            metric_name=metric_name,
            current_value=current_value,
            threshold=threshold,
            severity=3 if alert_type == "warning" else 5
        )
        
        # Store alert
        self.alerts_history.append(alert)
        self.alert_counts[alert_key] += 1
        self.last_alert_time[alert_key] = current_time
        
        # Log alert
        alert_icon = "⚠️" if alert_type == "warning" else "🚨"
        self.logger.warning(f"{alert_icon} {alert.message}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary"""
        try:
            summary = {
                "monitoring_active": self.is_monitoring,
                "metrics_tracked": len(self.metrics_history),
                "total_alerts": len(self.alerts_history),
                "baseline_calculated": self.baseline_calculated,
                "current_metrics": {},
                "recent_alerts": [],
                "performance_indicators": {}
            }
            
            # Current metrics
            for metric_name, metrics in self.metrics_history.items():
                if metrics:
                    latest = metrics[-1]
                    summary["current_metrics"][metric_name] = {
                        "value": latest.value,
                        "unit": latest.unit,
                        "timestamp": latest.timestamp.isoformat()
                    }
            
            # Recent alerts
            recent_alerts = list(self.alerts_history)[-5:]  # Last 5 alerts
            summary["recent_alerts"] = [
                {
                    "type": alert.alert_type,
                    "message": alert.message,
                    "severity": alert.severity,
                    "timestamp": alert.timestamp.isoformat()
                }
                for alert in recent_alerts
            ]
            
            # Performance indicators
            summary["performance_indicators"] = self._calculate_performance_indicators()
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance summary: {e}")
            return {"error": str(e)}
    
    def _calculate_performance_indicators(self) -> Dict[str, Any]:
        """Calculate key performance indicators"""
        indicators = {}
        
        try:
            # Authentication success rate
            if "success_rate" in self.metrics_history and self.metrics_history["success_rate"]:
                success_rates = [m.value for m in self.metrics_history["success_rate"]]
                indicators["current_success_rate"] = success_rates[-1] if success_rates else 0
                indicators["avg_success_rate"] = statistics.mean(success_rates) if len(success_rates) > 1 else 0
            
            # Authentication duration
            if "auth_duration" in self.metrics_history and self.metrics_history["auth_duration"]:
                durations = [m.value for m in self.metrics_history["auth_duration"]]
                indicators["current_auth_duration"] = durations[-1] if durations else 0
                indicators["avg_auth_duration"] = statistics.mean(durations) if len(durations) > 1 else 0
                indicators["min_auth_duration"] = min(durations) if durations else 0
                indicators["max_auth_duration"] = max(durations) if durations else 0
            
            # Throughput
            if "auth_per_second" in self.metrics_history and self.metrics_history["auth_per_second"]:
                throughputs = [m.value for m in self.metrics_history["auth_per_second"]]
                indicators["current_throughput"] = throughputs[-1] if throughputs else 0
                indicators["avg_throughput"] = statistics.mean(throughputs) if len(throughputs) > 1 else 0
            
            # System health
            indicators["system_health"] = self._calculate_system_health()
            
        except Exception as e:
            self.logger.error(f"Failed to calculate performance indicators: {e}")
            indicators["error"] = str(e)
        
        return indicators
    
    def _calculate_system_health(self) -> str:
        """Calculate overall system health score"""
        try:
            health_score = 100
            health_factors = []
            
            # Check success rate
            if "success_rate" in self.metrics_history and self.metrics_history["success_rate"]:
                current_success = self.metrics_history["success_rate"][-1].value
                if current_success < 0.95:
                    health_score -= 20
                    health_factors.append("Low success rate")
            
            # Check response time
            if "auth_duration" in self.metrics_history and self.metrics_history["auth_duration"]:
                current_duration = self.metrics_history["auth_duration"][-1].value
                if current_duration > 1.0:
                    health_score -= 15
                    health_factors.append("High response time")
            
            # Check alert count
            recent_alerts = [a for a in self.alerts_history if 
                           (datetime.now() - a.timestamp).total_seconds() < 300]  # Last 5 minutes
            if len(recent_alerts) > 5:
                health_score -= 25
                health_factors.append("High alert frequency")
            
            # Determine health status
            if health_score >= 90:
                return "excellent"
            elif health_score >= 75:
                return "good"
            elif health_score >= 60:
                return "fair"
            else:
                return "poor"
                
        except Exception:
            return "unknown"
    
    def generate_performance_report(self, time_period: str = "current") -> PerformanceReport:
        """Generate comprehensive performance report"""
        try:
            report_id = f"perf_report_{int(time.time())}"
            timestamp = datetime.now()
            
            # Generate summary
            summary = self.get_performance_summary()
            
            # Collect detailed metrics
            detailed_metrics = []
            for metric_name, metrics in self.metrics_history.items():
                if metrics:
                    detailed_metrics.extend(list(metrics)[-10:])  # Last 10 metrics
            
            # Get recent alerts
            alerts = list(self.alerts_history)[-20:]  # Last 20 alerts
            
            # Generate recommendations
            recommendations = self._generate_recommendations(summary)
            
            report = PerformanceReport(
                report_id=report_id,
                timestamp=timestamp,
                time_period=time_period,
                summary=summary,
                detailed_metrics=detailed_metrics,
                alerts=alerts,
                recommendations=recommendations
            )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            # Return minimal error report
            return PerformanceReport(
                report_id=f"error_report_{int(time.time())}",
                timestamp=datetime.now(),
                time_period=time_period,
                summary={"error": str(e)},
                detailed_metrics=[],
                alerts=[],
                recommendations=["Investigate system errors"]
            )
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        try:
            # Check success rate
            if "current_success_rate" in summary.get("performance_indicators", {}):
                success_rate = summary["performance_indicators"]["current_success_rate"]
                if success_rate < 0.95:
                    recommendations.append("Investigate authentication failures to improve success rate")
            
            # Check response time
            if "current_auth_duration" in summary.get("performance_indicators", {}):
                auth_duration = summary["performance_indicators"]["current_auth_duration"]
                if auth_duration > 0.5:
                    recommendations.append("Optimize authentication process to reduce response time")
            
            # Check alert frequency
            if len(summary.get("recent_alerts", [])) > 3:
                recommendations.append("Review system configuration to reduce alert frequency")
            
            # Check system health
            system_health = summary.get("performance_indicators", {}).get("system_health", "unknown")
            if system_health in ["fair", "poor"]:
                recommendations.append("Perform system health assessment and optimization")
            
            # Add general recommendations
            if not recommendations:
                recommendations.append("System performance is within acceptable parameters")
                recommendations.append("Continue monitoring for performance trends")
            
        except Exception as e:
            recommendations.append(f"Unable to generate recommendations: {str(e)}")
        
        return recommendations
    
    def cleanup(self):
        """Cleanup performance monitor resources"""
        try:
            self.stop_monitoring()
            self.logger.info("✅ Performance monitor resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"❌ Performance monitor cleanup failed: {e}")
