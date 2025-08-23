"""
Performance Monitor for Agent_Cellphone_V2_Repository
Core performance monitoring system with metrics collection, storage, and alerting.
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
import uuid
from datetime import datetime, timedelta
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics that can be collected."""

    GAUGE = "gauge"  # Current value (e.g., CPU usage)
    COUNTER = "counter"  # Incrementing value (e.g., request count)
    HISTOGRAM = "histogram"  # Distribution of values
    TIMER = "timer"  # Timing measurements
    SET = "set"  # Unique values count


class AlertSeverity(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertCondition(Enum):
    """Alert trigger conditions."""

    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"


@dataclass
class MetricData:
    """Individual metric data point."""

    metric_name: str
    metric_type: MetricType
    value: Union[float, int]
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""
    description: str = ""


@dataclass
class MetricSeries:
    """Series of metric data points."""

    metric_name: str
    metric_type: MetricType
    data_points: List[MetricData] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""
    description: str = ""


@dataclass
class AlertRule:
    """Performance alert rule definition."""

    name: str
    metric_name: str
    condition: AlertCondition
    threshold: Union[float, int]
    severity: AlertSeverity
    description: str = ""
    enabled: bool = True
    tags_filter: Dict[str, str] = field(default_factory=dict)
    cooldown_period: int = 300  # 5 minutes default
    consecutive_violations: int = 1


@dataclass
class PerformanceAlert:
    """Performance alert instance."""

    alert_id: str
    rule_name: str
    metric_name: str
    current_value: Union[float, int]
    threshold: Union[float, int]
    severity: AlertSeverity
    message: str
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)
    resolved: bool = False
    resolved_timestamp: Optional[float] = None


class MetricsStorage:
    """Thread-safe metrics storage with time-series support."""

    def __init__(self, max_data_points: int = 10000):
        self.data: Dict[str, MetricSeries] = {}
        self.max_data_points = max_data_points
        self._lock = threading.RLock()

    def store_metric(self, metric_data: MetricData):
        """Store a metric data point."""
        with self._lock:
            metric_name = metric_data.metric_name

            if metric_name not in self.data:
                self.data[metric_name] = MetricSeries(
                    metric_name=metric_name,
                    metric_type=metric_data.metric_type,
                    tags=metric_data.tags.copy(),
                    unit=metric_data.unit,
                    description=metric_data.description,
                )

            series = self.data[metric_name]
            series.data_points.append(metric_data)

            # Maintain max data points limit
            if len(series.data_points) > self.max_data_points:
                series.data_points = series.data_points[-self.max_data_points :]

    def get_series(
        self,
        metric_name: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Optional[MetricSeries]:
        """Get metric series with optional time range filtering."""
        with self._lock:
            if metric_name not in self.data:
                return None

            series = self.data[metric_name]

            if start_time is None and end_time is None:
                return series

            # Filter by time range
            filtered_points = []
            for point in series.data_points:
                if start_time and point.timestamp < start_time:
                    continue
                if end_time and point.timestamp > end_time:
                    continue
                filtered_points.append(point)

            # Create filtered series
            filtered_series = MetricSeries(
                metric_name=series.metric_name,
                metric_type=series.metric_type,
                data_points=filtered_points,
                tags=series.tags.copy(),
                unit=series.unit,
                description=series.description,
            )

            return filtered_series

    def get_all_metric_names(self) -> List[str]:
        """Get all stored metric names."""
        with self._lock:
            return list(self.data.keys())

    def cleanup_old_data(self, retention_seconds: int):
        """Remove data older than retention period."""
        cutoff_time = time.time() - retention_seconds

        with self._lock:
            for metric_name, series in self.data.items():
                series.data_points = [
                    point
                    for point in series.data_points
                    if point.timestamp >= cutoff_time
                ]


class PerformanceMonitor:
    """Main performance monitoring system."""

    def __init__(self, config_file: Optional[str] = None):
        self.metrics_storage = MetricsStorage()
        self.alert_rules: List[AlertRule] = []
        self.collectors: List["MetricsCollector"] = []
        self.running = False
        self.collection_interval = 60  # Default 1 minute
        self.retention_period = 86400  # Default 24 hours

        # Alert tracking
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_cooldowns: Dict[str, float] = {}

        # Event callbacks
        self.metric_callbacks: List[Callable[[MetricData], None]] = []
        self.alert_callbacks: List[Callable[[PerformanceAlert], None]] = []

        # Background tasks
        self._collection_task: Optional[asyncio.Task] = None
        self._cleanup_task: Optional[asyncio.Task] = None

        # Load configuration if provided
        if config_file:
            self.load_config(config_file)

        logger.info("Performance Monitor initialized")

    def load_config(self, config_file: str):
        """Load configuration from file."""
        try:
            with open(config_file, "r") as f:
                config = json.load(f)

            perf_config = config.get("performance_monitoring", {})
            self.collection_interval = perf_config.get("collection_interval", 60)
            self.retention_period = perf_config.get("retention_period", 86400)

            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load config from {config_file}: {e}")

    def add_collector(self, collector: "MetricsCollector"):
        """Add a metrics collector."""
        self.collectors.append(collector)
        collector.performance_monitor = self
        logger.info(f"Added metrics collector: {collector.__class__.__name__}")

    def record_metric(self, metric_data: MetricData):
        """Record a metric data point."""
        self.metrics_storage.store_metric(metric_data)

        # Trigger callbacks
        for callback in self.metric_callbacks:
            try:
                callback(metric_data)
            except Exception as e:
                logger.error(f"Error in metric callback: {e}")

        # Check alert rules
        alerts = self.check_alerts(metric_data)
        for alert in alerts:
            self.process_alert(alert)

    def get_metric_series(
        self,
        metric_name: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Optional[MetricSeries]:
        """Get metric series with optional time range."""
        return self.metrics_storage.get_series(metric_name, start_time, end_time)

    def aggregate_metrics(
        self,
        metric_name: str,
        aggregation: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Optional[float]:
        """Aggregate metrics using specified aggregation function."""
        series = self.get_metric_series(metric_name, start_time, end_time)
        if not series or not series.data_points:
            return None

        values = [point.value for point in series.data_points]

        if aggregation == "avg":
            return sum(values) / len(values)
        elif aggregation == "max":
            return max(values)
        elif aggregation == "min":
            return min(values)
        elif aggregation == "sum":
            return sum(values)
        elif aggregation == "count":
            return len(values)
        else:
            raise ValueError(f"Unknown aggregation function: {aggregation}")

    def add_alert_rule(self, alert_rule: AlertRule):
        """Add an alert rule."""
        self.alert_rules.append(alert_rule)
        logger.info(f"Added alert rule: {alert_rule.name}")

    def check_alerts(self, metric_data: MetricData) -> List[PerformanceAlert]:
        """Check if metric data triggers any alerts."""
        triggered_alerts = []

        for rule in self.alert_rules:
            if not rule.enabled:
                continue

            if rule.metric_name != metric_data.metric_name:
                continue

            # Check tags filter
            if rule.tags_filter:
                if not all(
                    metric_data.tags.get(k) == v for k, v in rule.tags_filter.items()
                ):
                    continue

            # Check cooldown
            cooldown_key = f"{rule.name}_{metric_data.metric_name}"
            if cooldown_key in self.alert_cooldowns:
                if (
                    time.time() - self.alert_cooldowns[cooldown_key]
                    < rule.cooldown_period
                ):
                    continue

            # Evaluate condition
            if self._evaluate_alert_condition(rule, metric_data.value):
                alert = PerformanceAlert(
                    alert_id=str(uuid.uuid4()),
                    rule_name=rule.name,
                    metric_name=metric_data.metric_name,
                    current_value=metric_data.value,
                    threshold=rule.threshold,
                    severity=rule.severity,
                    message=f"{rule.description or rule.name}: {metric_data.metric_name} is {metric_data.value} {metric_data.unit}",
                    timestamp=metric_data.timestamp,
                    tags=metric_data.tags.copy(),
                )

                triggered_alerts.append(alert)
                self.alert_cooldowns[cooldown_key] = time.time()

        return triggered_alerts

    def _evaluate_alert_condition(
        self, rule: AlertRule, value: Union[float, int]
    ) -> bool:
        """Evaluate if a value meets the alert condition."""
        threshold = rule.threshold

        if rule.condition == AlertCondition.GREATER_THAN:
            return value > threshold
        elif rule.condition == AlertCondition.LESS_THAN:
            return value < threshold
        elif rule.condition == AlertCondition.EQUALS:
            return value == threshold
        elif rule.condition == AlertCondition.NOT_EQUALS:
            return value != threshold
        elif rule.condition == AlertCondition.GREATER_THAN_OR_EQUAL:
            return value >= threshold
        elif rule.condition == AlertCondition.LESS_THAN_OR_EQUAL:
            return value <= threshold
        else:
            return False

    def process_alert(self, alert: PerformanceAlert):
        """Process a triggered alert."""
        self.active_alerts[alert.alert_id] = alert

        # Trigger alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

        logger.warning(f"Alert triggered: {alert.message}")

    def resolve_alert(self, alert_id: str):
        """Resolve an active alert."""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_timestamp = time.time()
            del self.active_alerts[alert_id]
            logger.info(f"Alert resolved: {alert.rule_name}")

    async def start(self):
        """Start the performance monitoring system."""
        if self.running:
            logger.warning("Performance monitor is already running")
            return

        self.running = True

        # Start collection task
        self._collection_task = asyncio.create_task(self._collection_loop())

        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

        logger.info("Performance monitor started")

    async def stop(self):
        """Stop the performance monitoring system."""
        if not self.running:
            return

        self.running = False

        # Cancel background tasks
        if self._collection_task:
            self._collection_task.cancel()
            try:
                await self._collection_task
            except asyncio.CancelledError:
                pass

        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        logger.info("Performance monitor stopped")

    async def _collection_loop(self):
        """Background loop for metrics collection."""
        while self.running:
            try:
                # Collect metrics from all collectors
                for collector in self.collectors:
                    if collector.enabled:
                        metrics = await collector.collect_metrics()
                        for metric in metrics:
                            self.record_metric(metric)

                # Wait for next collection interval
                await asyncio.sleep(self.collection_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    async def _cleanup_loop(self):
        """Background loop for data cleanup."""
        cleanup_interval = 3600  # Run cleanup every hour

        while self.running:
            try:
                # Clean up old metrics data
                self.cleanup_old_metrics(
                    self.retention_period / 3600
                )  # Convert to hours

                # Wait for next cleanup
                await asyncio.sleep(cleanup_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    def cleanup_old_metrics(self, retention_hours: int):
        """Clean up old metrics data."""
        retention_seconds = retention_hours * 3600
        self.metrics_storage.cleanup_old_data(retention_seconds)
        logger.debug(f"Cleaned up metrics older than {retention_hours} hours")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "running": self.running,
            "collectors_count": len(self.collectors),
            "alert_rules_count": len(self.alert_rules),
            "active_alerts_count": len(self.active_alerts),
            "metric_names": self.metrics_storage.get_all_metric_names(),
            "collection_interval": self.collection_interval,
            "retention_period": self.retention_period,
        }


# Base class for metrics collectors (will be used by metrics_collector.py)
class MetricsCollector(ABC):
    """Abstract base class for metrics collectors."""

    def __init__(self, collection_interval: int = 60):
        self.collection_interval = collection_interval
        self.enabled = True
        self.running = False
        self.performance_monitor: Optional[PerformanceMonitor] = None

    @abstractmethod
    async def collect_metrics(self) -> List[MetricData]:
        """Collect metrics and return list of MetricData objects."""
        raise NotImplementedError

    def set_enabled(self, enabled: bool):
        """Enable or disable this collector."""
        self.enabled = enabled
        logger.info(
            f"Metrics collector {self.__class__.__name__} {'enabled' if enabled else 'disabled'}"
        )


# Export all classes for use in other modules
__all__ = [
    "MetricType",
    "AlertSeverity",
    "AlertCondition",
    "MetricData",
    "MetricSeries",
    "AlertRule",
    "PerformanceAlert",
    "MetricsStorage",
    "PerformanceMonitor",
    "MetricsCollector",
]
