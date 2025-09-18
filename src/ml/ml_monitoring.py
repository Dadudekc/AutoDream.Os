import os
import json
import logging
import asyncio
import time
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, deque

class MetricType(Enum):
    """Enumeration for different metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class AlertSeverity(Enum):
    """Enumeration for alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class MetricData:
    """Data class for metric information."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Optional[Dict[str, str]] = None
    model_name: Optional[str] = None
    version: Optional[str] = None

@dataclass
class Alert:
    """Data class for alert information."""
    alert_id: str
    name: str
    description: str
    severity: AlertSeverity
    metric_name: str
    threshold: float
    current_value: float
    triggered_at: datetime
    status: str = "active"
    resolved_at: Optional[datetime] = None

class MLMonitoring:
    """
    Provides comprehensive ML model monitoring, metrics collection, and alerting.
    Tracks model performance, data drift, and system health metrics.
    """

    def __init__(self, metrics_path: str = "/app/metrics", retention_days: int = 30):
        """
        Initializes the MLMonitoring system.

        Args:
            metrics_path: Path to store metrics data.
            retention_days: Number of days to retain metrics data.
        """
        if not metrics_path:
            raise ValueError("Metrics path cannot be empty.")
        if retention_days <= 0:
            raise ValueError("Retention days must be positive.")

        self.metrics_path = metrics_path
        self.retention_days = retention_days
        self.logger = logging.getLogger(__name__)
        
        # Metrics storage
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        
        # Monitoring configuration
        self.monitoring_enabled = True
        self.alert_callbacks: List[Callable[[Alert], None]] = []

        # Ensure directories exist
        os.makedirs(metrics_path, exist_ok=True)

        # Load existing metrics and alerts
        self._load_metrics()
        self._load_alerts()

    def _load_metrics(self) -> None:
        """Loads metrics from disk."""
        metrics_file = os.path.join(self.metrics_path, "metrics.json")
        if os.path.exists(metrics_file):
            try:
                with open(metrics_file, 'r') as f:
                    data = json.load(f)
                
                for metric_name, metric_list in data.items():
                    for metric_data in metric_list:
                        metric_data['timestamp'] = datetime.fromisoformat(metric_data['timestamp'])
                        metric_data['metric_type'] = MetricType(metric_data['metric_type'])
                        metric = MetricData(**metric_data)
                        self.metrics[metric_name].append(metric)
                
                self.logger.info(f"Loaded metrics for {len(self.metrics)} metric types")
            except Exception as e:
                self.logger.error(f"Failed to load metrics: {e}")

    def _save_metrics(self) -> None:
        """Saves metrics to disk."""
        try:
            metrics_file = os.path.join(self.metrics_path, "metrics.json")
            data = {}
            
            for metric_name, metric_deque in self.metrics.items():
                data[metric_name] = []
                for metric in metric_deque:
                    metric_dict = asdict(metric)
                    metric_dict['timestamp'] = metric.timestamp.isoformat()
                    metric_dict['metric_type'] = metric.metric_type.value
                    data[metric_name].append(metric_dict)
            
            with open(metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info("Metrics saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save metrics: {e}")

    def _load_alerts(self) -> None:
        """Loads alerts from disk."""
        alerts_file = os.path.join(self.metrics_path, "alerts.json")
        if os.path.exists(alerts_file):
            try:
                with open(alerts_file, 'r') as f:
                    data = json.load(f)
                
                for alert_id, alert_data in data.items():
                    alert_data['triggered_at'] = datetime.fromisoformat(alert_data['triggered_at'])
                    alert_data['severity'] = AlertSeverity(alert_data['severity'])
                    if alert_data.get('resolved_at'):
                        alert_data['resolved_at'] = datetime.fromisoformat(alert_data['resolved_at'])
                    self.alerts[alert_id] = Alert(**alert_data)
                
                self.logger.info(f"Loaded {len(self.alerts)} alerts")
            except Exception as e:
                self.logger.error(f"Failed to load alerts: {e}")

    def _save_alerts(self) -> None:
        """Saves alerts to disk."""
        try:
            alerts_file = os.path.join(self.metrics_path, "alerts.json")
            data = {}
            
            for alert_id, alert in self.alerts.items():
                alert_dict = asdict(alert)
                alert_dict['triggered_at'] = alert.triggered_at.isoformat()
                alert_dict['severity'] = alert.severity.value
                if alert.resolved_at:
                    alert_dict['resolved_at'] = alert.resolved_at.isoformat()
                data[alert_id] = alert_dict
            
            with open(alerts_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info("Alerts saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save alerts: {e}")

    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     labels: Optional[Dict[str, str]] = None,
                     model_name: Optional[str] = None,
                     version: Optional[str] = None) -> None:
        """
        Records a metric value.

        Args:
            name: Name of the metric.
            value: Metric value.
            metric_type: Type of the metric.
            labels: Optional labels for the metric.
            model_name: Optional model name.
            version: Optional model version.
        """
        if not name:
            raise ValueError("Metric name cannot be empty.")
        if not isinstance(value, (int, float)):
            raise ValueError("Metric value must be numeric.")

        metric = MetricData(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.utcnow(),
            labels=labels,
            model_name=model_name,
            version=version
        )

        self.metrics[name].append(metric)
        
        # Check for alerts
        self._check_alerts(name, value)
        
        self.logger.debug(f"Recorded metric: {name} = {value}")

    def record_prediction_metrics(self, model_name: str, version: str, 
                                prediction_time: float, confidence: float,
                                input_size: int, output_size: int) -> None:
        """
        Records prediction-related metrics.

        Args:
            model_name: Name of the model.
            version: Model version.
            prediction_time: Time taken for prediction in seconds.
            confidence: Prediction confidence score.
            input_size: Size of input data.
            output_size: Size of output data.
        """
        labels = {"model": model_name, "version": version}
        
        self.record_metric("prediction_time", prediction_time, MetricType.HISTOGRAM, labels)
        self.record_metric("prediction_confidence", confidence, MetricType.GAUGE, labels)
        self.record_metric("input_size", input_size, MetricType.GAUGE, labels)
        self.record_metric("output_size", output_size, MetricType.GAUGE, labels)
        self.record_metric("predictions_total", 1, MetricType.COUNTER, labels)

    def record_training_metrics(self, model_name: str, version: str,
                              loss: float, accuracy: float, epoch: int) -> None:
        """
        Records training-related metrics.

        Args:
            model_name: Name of the model.
            version: Model version.
            loss: Training loss value.
            accuracy: Training accuracy value.
            epoch: Training epoch number.
        """
        labels = {"model": model_name, "version": version, "epoch": str(epoch)}
        
        self.record_metric("training_loss", loss, MetricType.GAUGE, labels)
        self.record_metric("training_accuracy", accuracy, MetricType.GAUGE, labels)

    def record_data_drift_metrics(self, model_name: str, version: str,
                                drift_score: float, feature_name: str) -> None:
        """
        Records data drift metrics.

        Args:
            model_name: Name of the model.
            version: Model version.
            drift_score: Drift score (0-1).
            feature_name: Name of the feature.
        """
        labels = {"model": model_name, "version": version, "feature": feature_name}
        self.record_metric("data_drift_score", drift_score, MetricType.GAUGE, labels)

    def get_metric_history(self, metric_name: str, hours: int = 24) -> List[MetricData]:
        """
        Gets metric history for a specific time range.

        Args:
            metric_name: Name of the metric.
            hours: Number of hours to look back.

        Returns:
            List of MetricData objects.
        """
        if not metric_name:
            raise ValueError("Metric name cannot be empty.")
        if hours <= 0:
            raise ValueError("Hours must be positive.")

        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [metric for metric in self.metrics[metric_name] 
                if metric.timestamp >= cutoff_time]

    def get_metric_statistics(self, metric_name: str, hours: int = 24) -> Dict[str, float]:
        """
        Gets statistical summary for a metric.

        Args:
            metric_name: Name of the metric.
            hours: Number of hours to analyze.

        Returns:
            Dictionary with statistical measures.
        """
        history = self.get_metric_history(metric_name, hours)
        if not history:
            return {}

        values = [metric.value for metric in history]
        return {
            "count": len(values),
            "mean": np.mean(values),
            "median": np.median(values),
            "std": np.std(values),
            "min": np.min(values),
            "max": np.max(values),
            "p95": np.percentile(values, 95),
            "p99": np.percentile(values, 99)
        }

    def create_alert_rule(self, name: str, metric_name: str, threshold: float,
                         condition: str, severity: AlertSeverity,
                         description: str) -> str:
        """
        Creates an alert rule.

        Args:
            name: Name of the alert rule.
            metric_name: Name of the metric to monitor.
            threshold: Threshold value for the alert.
            condition: Condition ('gt', 'lt', 'eq', 'gte', 'lte').
            severity: Alert severity level.
            description: Description of the alert.

        Returns:
            Alert rule ID.
        """
        if not name or not metric_name or not condition:
            raise ValueError("Name, metric name, and condition are required.")
        if condition not in ['gt', 'lt', 'eq', 'gte', 'lte']:
            raise ValueError("Condition must be one of: gt, lt, eq, gte, lte.")

        rule_id = f"{name}_{metric_name}_{int(time.time())}"
        self.alert_rules[rule_id] = {
            "name": name,
            "metric_name": metric_name,
            "threshold": threshold,
            "condition": condition,
            "severity": severity,
            "description": description,
            "created_at": datetime.utcnow().isoformat()
        }

        self.logger.info(f"Created alert rule: {rule_id}")
        return rule_id

    def _check_alerts(self, metric_name: str, value: float) -> None:
        """
        Checks if any alert rules are triggered.

        Args:
            metric_name: Name of the metric.
            value: Current metric value.
        """
        for rule_id, rule in self.alert_rules.items():
            if rule["metric_name"] != metric_name:
                continue

            condition = rule["condition"]
            threshold = rule["threshold"]
            triggered = False

            if condition == "gt" and value > threshold:
                triggered = True
            elif condition == "lt" and value < threshold:
                triggered = True
            elif condition == "eq" and value == threshold:
                triggered = True
            elif condition == "gte" and value >= threshold:
                triggered = True
            elif condition == "lte" and value <= threshold:
                triggered = True

            if triggered:
                self._trigger_alert(rule_id, rule, value)

    def _trigger_alert(self, rule_id: str, rule: Dict[str, Any], current_value: float) -> None:
        """
        Triggers an alert.

        Args:
            rule_id: ID of the alert rule.
            rule: Alert rule configuration.
            current_value: Current metric value.
        """
        alert_id = f"{rule_id}_{int(time.time())}"
        
        # Check if alert already exists and is active
        existing_alerts = [alert for alert in self.alerts.values() 
                          if alert.name == rule["name"] and alert.status == "active"]
        if existing_alerts:
            return  # Don't create duplicate alerts

        alert = Alert(
            alert_id=alert_id,
            name=rule["name"],
            description=rule["description"],
            severity=rule["severity"],
            metric_name=rule["metric_name"],
            threshold=rule["threshold"],
            current_value=current_value,
            triggered_at=datetime.utcnow()
        )

        self.alerts[alert_id] = alert
        self._save_alerts()

        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Alert callback failed: {e}")

        self.logger.warning(f"Alert triggered: {alert.name} - {alert.description}")

    def resolve_alert(self, alert_id: str) -> bool:
        """
        Resolves an alert.

        Args:
            alert_id: ID of the alert to resolve.

        Returns:
            True if successfully resolved, False otherwise.
        """
        if alert_id not in self.alerts:
            return False

        alert = self.alerts[alert_id]
        alert.status = "resolved"
        alert.resolved_at = datetime.utcnow()
        
        self._save_alerts()
        self.logger.info(f"Alert resolved: {alert_id}")
        return True

    def get_active_alerts(self) -> List[Alert]:
        """
        Gets all active alerts.

        Returns:
            List of active Alert objects.
        """
        return [alert for alert in self.alerts.values() if alert.status == "active"]

    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """
        Adds an alert callback function.

        Args:
            callback: Function to call when an alert is triggered.
        """
        self.alert_callbacks.append(callback)

    def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """
        Gets data for the monitoring dashboard.

        Returns:
            Dictionary containing dashboard data.
        """
        active_alerts = self.get_active_alerts()
        alert_counts = defaultdict(int)
        for alert in active_alerts:
            alert_counts[alert.severity.value] += 1

        # Get recent metrics
        recent_metrics = {}
        for metric_name in ["prediction_time", "prediction_confidence", "training_loss", "training_accuracy"]:
            if metric_name in self.metrics:
                recent_metrics[metric_name] = self.get_metric_statistics(metric_name, 1)

        return {
            "active_alerts": len(active_alerts),
            "alert_severity_counts": dict(alert_counts),
            "recent_metrics": recent_metrics,
            "total_metrics": len(self.metrics),
            "total_alert_rules": len(self.alert_rules),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def cleanup_old_metrics(self) -> None:
        """
        Cleans up old metrics based on retention policy.
        """
        cutoff_time = datetime.utcnow() - timedelta(days=self.retention_days)
        
        for metric_name, metric_deque in self.metrics.items():
            # Remove old metrics
            while metric_deque and metric_deque[0].timestamp < cutoff_time:
                metric_deque.popleft()
        
        self._save_metrics()
        self.logger.info("Cleaned up old metrics")
