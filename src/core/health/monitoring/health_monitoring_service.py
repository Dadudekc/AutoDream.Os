#!/usr/bin/env python3
"""
🐝 AGENT-2 COMPREHENSIVE SYSTEM HEALTH MONITORING SERVICE
Core Architecture Consolidation - System Health & Alerting Platform

This service provides a unified health monitoring platform that integrates:
- Service availability monitoring
- Performance metrics collection
- Error rate tracking
- Resource usage monitoring
- Automated health checks
- Failure notification system
- Web dashboard integration
"""

from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

import psutil

try:
    from ..automated_health_check_system import (
        AutomatedHealthCheckSystem,
        HealthCheckResult,
        HealthStatus
    )
    from ..performance_monitoring_dashboard import (
        PerformanceMonitoringDashboard,
        DashboardMetric,
        MetricType
    )
    from ..unified_monitoring_coordinator import (
        UnifiedMonitoringCoordinator,
        MonitoringAlert
    )
except ImportError:
    # Fallback for direct imports
    try:
        from automated_health_check_system import (
            AutomatedHealthCheckSystem,
            HealthCheckResult,
            HealthStatus
        )
        from performance_monitoring_dashboard import (
            PerformanceMonitoringDashboard,
            DashboardMetric,
            MetricType
        )
        from unified_monitoring_coordinator import (
            UnifiedMonitoringCoordinator,
            MonitoringAlert
        )
    except ImportError:
        # Create mock classes if components not available
        class MockHealthStatus:
            HEALTHY = "healthy"
            WARNING = "warning"
            CRITICAL = "critical"
            UNKNOWN = "unknown"

        HealthStatus = MockHealthStatus

        class MockHealthCheckResult:
            pass

        HealthCheckResult = MockHealthCheckResult

        AutomatedHealthCheckSystem = None
        PerformanceMonitoringDashboard = None
        UnifiedMonitoringCoordinator = None
        MonitoringAlert = None

logger = logging.getLogger(__name__)


class ServiceType(Enum):
    """Types of services being monitored."""
    CORE_SERVICE = "core_service"
    WEB_SERVICE = "web_service"
    DATABASE_SERVICE = "database_service"
    MESSAGING_SERVICE = "messaging_service"
    API_SERVICE = "api_service"
    BACKGROUND_SERVICE = "background_service"


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ServiceEndpoint:
    """Represents a service endpoint for monitoring."""
    name: str
    url: str
    service_type: ServiceType
    expected_response_time_ms: int = 1000
    timeout_seconds: int = 10
    health_check_path: str = "/health"
    enabled: bool = True


@dataclass
class HealthMetric:
    """Represents a health metric."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    category: str
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemHealthSnapshot:
    """Complete snapshot of system health."""
    timestamp: datetime
    services: Dict[str, HealthStatus] = field(default_factory=dict)
    metrics: Dict[str, HealthMetric] = field(default_factory=dict)
    alerts: List[MonitoringAlert] = field(default_factory=list)
    overall_status: HealthStatus = HealthStatus.UNKNOWN
    uptime_seconds: float = 0.0


class HealthMonitoringService:
    """
    Comprehensive system health monitoring and alerting service.

    Provides unified monitoring across:
    - Service availability and health checks
    - Performance metrics and resource usage
    - Error rates and failure tracking
    - Automated alerting and notifications
    - Web dashboard integration
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/health_monitoring.json"
        self.data_directory = Path("data/health_monitoring")
        self.data_directory.mkdir(parents=True, exist_ok=True)

        # Core monitoring components
        self.health_check_system = None
        self.performance_dashboard = None
        self.monitoring_coordinator = None

        # Service monitoring
        self.service_endpoints: Dict[str, ServiceEndpoint] = {}
        self.service_health_history: Dict[str, List[HealthStatus]] = {}

        # Metrics collection
        self.metrics_buffer: List[HealthMetric] = []
        self.metrics_retention_hours = 24

        # Alerting system
        self.active_alerts: Dict[str, MonitoringAlert] = {}
        self.alert_history: List[MonitoringAlert] = []
        self.alert_handlers: List[Callable[[MonitoringAlert], None]] = []

        # Monitoring control
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.collection_interval_seconds = 30

        # Initialize components
        self._initialize_components()
        self._load_configuration()
        self._setup_default_services()

    def _initialize_components(self) -> None:
        """Initialize core monitoring components."""
        try:
            self.health_check_system = AutomatedHealthCheckSystem()
            logger.info("✅ Automated health check system initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize health check system: {e}")

        try:
            self.performance_dashboard = PerformanceMonitoringDashboard()
            logger.info("✅ Performance monitoring dashboard initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize performance dashboard: {e}")

        try:
            self.monitoring_coordinator = UnifiedMonitoringCoordinator()
            logger.info("✅ Unified monitoring coordinator initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize monitoring coordinator: {e}")

    def _load_configuration(self) -> None:
        """Load configuration from file."""
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)

                self.collection_interval_seconds = config.get('collection_interval_seconds', 30)
                self.metrics_retention_hours = config.get('metrics_retention_hours', 24)

                # Load service endpoints
                for service_config in config.get('services', []):
                    endpoint = ServiceEndpoint(
                        name=service_config['name'],
                        url=service_config['url'],
                        service_type=ServiceType(service_config['type']),
                        expected_response_time_ms=service_config.get('expected_response_time_ms', 1000),
                        timeout_seconds=service_config.get('timeout_seconds', 10),
                        health_check_path=service_config.get('health_check_path', '/health'),
                        enabled=service_config.get('enabled', True)
                    )
                    self.service_endpoints[endpoint.name] = endpoint

                logger.info(f"✅ Configuration loaded from {config_file}")

            except Exception as e:
                logger.warning(f"⚠️ Failed to load configuration: {e}")
                self._create_default_configuration()

    def _create_default_configuration(self) -> None:
        """Create default configuration."""
        default_config = {
            "collection_interval_seconds": 30,
            "metrics_retention_hours": 24,
            "services": [
                {
                    "name": "core_service",
                    "url": "http://localhost:8000",
                    "type": "core_service",
                    "expected_response_time_ms": 1000,
                    "timeout_seconds": 10,
                    "health_check_path": "/health",
                    "enabled": True
                }
            ]
        }

        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)

        logger.info(f"✅ Default configuration created at {config_file}")

    def _setup_default_services(self) -> None:
        """Setup default service endpoints if none configured."""
        if not self.service_endpoints:
            # Core system services
            default_services = [
                ServiceEndpoint(
                    name="core_messaging",
                    url="http://localhost:8000",
                    service_type=ServiceType.CORE_SERVICE,
                    expected_response_time_ms=500
                ),
                ServiceEndpoint(
                    name="web_interface",
                    url="http://localhost:3000",
                    service_type=ServiceType.WEB_SERVICE,
                    expected_response_time_ms=1000
                )
            ]

            for service in default_services:
                self.service_endpoints[service.name] = service
                self.service_health_history[service.name] = []

    def start_monitoring(self) -> None:
        """Start the health monitoring service."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="HealthMonitoringService"
        )
        self.monitoring_thread.start()

        # Start component monitoring
        if self.health_check_system:
            self.health_check_system.start_monitoring()

        logger.info("✅ Health monitoring service started")

    def stop_monitoring(self) -> None:
        """Stop the health monitoring service."""
        self.monitoring_active = False

        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=10)

        # Stop component monitoring
        if self.health_check_system:
            self.health_check_system.stop_monitoring()

        logger.info("🛑 Health monitoring service stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                start_time = time.time()

                # Collect service health
                self._collect_service_health()

                # Collect system metrics
                self._collect_system_metrics()

                # Process alerts
                self._process_alerts()

                # Cleanup old data
                self._cleanup_old_data()

                # Calculate sleep time to maintain interval
                elapsed = time.time() - start_time
                sleep_time = max(0, self.collection_interval_seconds - elapsed)
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                time.sleep(5)

    def _collect_service_health(self) -> None:
        """Collect health status for all service endpoints."""
        for endpoint in self.service_endpoints.values():
            if not endpoint.enabled:
                continue

            try:
                health_status = self._check_service_health(endpoint)
                self.service_health_history[endpoint.name].append(health_status)

                # Keep only last 100 status entries
                if len(self.service_health_history[endpoint.name]) > 100:
                    self.service_health_history[endpoint.name] = \
                        self.service_health_history[endpoint.name][-100:]

                # Create metric
                availability_metric = HealthMetric(
                    name=f"{endpoint.name}_availability",
                    value=1.0 if health_status == HealthStatus.HEALTHY else 0.0,
                    unit="percent",
                    timestamp=datetime.now(),
                    category="service_availability"
                )
                self.metrics_buffer.append(availability_metric)

            except Exception as e:
                logger.warning(f"⚠️ Failed to check service {endpoint.name}: {e}")

    def _check_service_health(self, endpoint: ServiceEndpoint) -> HealthStatus:
        """Check health of a service endpoint."""
        try:
            import requests

            health_url = f"{endpoint.url.rstrip('/')}{endpoint.health_check_path}"
            response = requests.get(
                health_url,
                timeout=endpoint.timeout_seconds,
                headers={'User-Agent': 'HealthMonitor/1.0'}
            )

            if response.status_code == 200:
                response_time = response.elapsed.total_seconds() * 1000
                if response_time <= endpoint.expected_response_time_ms:
                    return HealthStatus.HEALTHY
                else:
                    return HealthStatus.WARNING
            else:
                return HealthStatus.CRITICAL

        except requests.exceptions.RequestException:
            return HealthStatus.CRITICAL
        except Exception:
            return HealthStatus.UNKNOWN

    def _collect_system_metrics(self) -> None:
        """Collect system performance metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_metric = HealthMetric(
                name="cpu_usage",
                value=cpu_percent,
                unit="percent",
                timestamp=datetime.now(),
                category="system_performance",
                threshold_warning=70.0,
                threshold_critical=85.0
            )
            self.metrics_buffer.append(cpu_metric)

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_metric = HealthMetric(
                name="memory_usage",
                value=memory.percent,
                unit="percent",
                timestamp=datetime.now(),
                category="system_performance",
                threshold_warning=75.0,
                threshold_critical=90.0
            )
            self.metrics_buffer.append(memory_metric)

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_metric = HealthMetric(
                name="disk_usage",
                value=disk.percent,
                unit="percent",
                timestamp=datetime.now(),
                category="system_performance",
                threshold_warning=80.0,
                threshold_critical=95.0
            )
            self.metrics_buffer.append(disk_metric)

            # Network metrics (simplified)
            network_metric = HealthMetric(
                name="network_status",
                value=1.0,  # Assume healthy unless proven otherwise
                unit="status",
                timestamp=datetime.now(),
                category="system_performance"
            )
            self.metrics_buffer.append(network_metric)

        except Exception as e:
            logger.warning(f"⚠️ Failed to collect system metrics: {e}")

    def _process_alerts(self) -> None:
        """Process and generate alerts based on current state."""
        # Check service availability
        for name, history in self.service_health_history.items():
            if len(history) >= 3:
                recent_statuses = history[-3:]
                if all(status == HealthStatus.CRITICAL for status in recent_statuses):
                    self._generate_alert(
                        component=name,
                        severity=AlertSeverity.CRITICAL,
                        message=f"Service {name} is consistently unavailable",
                        metadata={"consecutive_failures": 3}
                    )

        # Check metric thresholds
        for metric in self.metrics_buffer[-10:]:  # Check recent metrics
            if metric.threshold_critical and metric.value >= metric.threshold_critical:
                self._generate_alert(
                    component=metric.category,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Critical threshold exceeded: {metric.name} = {metric.value}{metric.unit}",
                    metadata={"metric": metric.name, "value": metric.value, "threshold": metric.threshold_critical}
                )
            elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                self._generate_alert(
                    component=metric.category,
                    severity=AlertSeverity.WARNING,
                    message=f"Warning threshold exceeded: {metric.name} = {metric.value}{metric.unit}",
                    metadata={"metric": metric.name, "value": metric.value, "threshold": metric.threshold_warning}
                )

    def _generate_alert(self, component: str, severity: AlertSeverity,
                       message: str, metadata: Dict[str, Any]) -> None:
        """Generate a monitoring alert."""
        alert_id = f"alert_{int(time.time())}_{component}_{severity.value}"

        alert = MonitoringAlert(
            alert_id=alert_id,
            component=getattr(SwarmComponent, component.upper(), SwarmComponent.MESSAGING_SYSTEM),
            level=getattr(MonitoringAlertLevel, severity.value.upper(), MonitoringAlertLevel.WARNING),
            message=message,
            timestamp=datetime.now(),
            metadata=metadata
        )

        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)

        # Notify alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.warning(f"⚠️ Alert handler failed: {e}")

        logger.warning(f"🚨 {severity.value.upper()}: {message}")

    def _cleanup_old_data(self) -> None:
        """Clean up old metrics and alerts."""
        cutoff_time = datetime.now() - timedelta(hours=self.metrics_retention_hours)

        # Clean old metrics
        self.metrics_buffer = [
            m for m in self.metrics_buffer
            if m.timestamp > cutoff_time
        ]

        # Clean old alerts (keep last 1000)
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

        # Clean resolved alerts older than 1 hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        self.active_alerts = {
            alert_id: alert for alert_id, alert in self.active_alerts.items()
            if not alert.resolved or alert.resolved_at > one_hour_ago
        }

    def add_alert_handler(self, handler: Callable[[MonitoringAlert], None]) -> None:
        """Add an alert notification handler."""
        self.alert_handlers.append(handler)

    def _initialize_health_check_system(self) -> None:
        """Initialize the automated health check system."""
        if AutomatedHealthCheckSystem:
            self.health_check_system = AutomatedHealthCheckSystem()

    def _initialize_performance_dashboard(self) -> None:
        """Initialize the performance monitoring dashboard."""
        if PerformanceMonitoringDashboard:
            self.performance_dashboard = PerformanceMonitoringDashboard()

    def _initialize_monitoring_coordinator(self) -> None:
        """Initialize the unified monitoring coordinator."""
        if UnifiedMonitoringCoordinator:
            self.monitoring_coordinator = UnifiedMonitoringCoordinator()

    def get_health_snapshot(self) -> SystemHealthSnapshot:
        """Get current system health snapshot."""
        # Calculate overall status
        all_statuses = []
        for history in self.service_health_history.values():
            if history:
                all_statuses.append(history[-1])

        for metric in self.metrics_buffer[-10:]:
            if metric.threshold_critical and metric.value >= metric.threshold_critical:
                all_statuses.append(HealthStatus.CRITICAL)
            elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                all_statuses.append(HealthStatus.WARNING)
            else:
                all_statuses.append(HealthStatus.HEALTHY)

        if HealthStatus.CRITICAL in all_statuses:
            overall_status = HealthStatus.CRITICAL
        elif HealthStatus.WARNING in all_statuses:
            overall_status = HealthStatus.WARNING
        elif all_statuses:
            overall_status = HealthStatus.HEALTHY
        else:
            overall_status = HealthStatus.UNKNOWN

        return SystemHealthSnapshot(
            timestamp=datetime.now(),
            services={name: history[-1] if history else HealthStatus.UNKNOWN
                     for name, history in self.service_health_history.items()},
            metrics={m.name: m for m in self.metrics_buffer[-50:]},
            alerts=list(self.active_alerts.values()),
            overall_status=overall_status,
            uptime_seconds=time.time()  # Simplified uptime
        )

    def export_health_data(self, filepath: Optional[str] = None) -> str:
        """Export current health data to JSON file."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(self.data_directory / f"health_snapshot_{timestamp}.json")

        snapshot = self.get_health_snapshot()
        data = {
            "timestamp": snapshot.timestamp.isoformat(),
            "overall_status": snapshot.overall_status.value,
            "services": {k: v.value for k, v in snapshot.services.items()},
            "metrics": {k: {
                "value": v.value,
                "unit": v.unit,
                "timestamp": v.timestamp.isoformat(),
                "category": v.category
            } for k, v in snapshot.metrics.items()},
            "active_alerts": [{
                "alert_id": getattr(a, 'alert_id', f'alert_{i}'),
                "component": getattr(a, 'component', {}).value if hasattr(getattr(a, 'component', {}), 'value') else 'unknown',
                "level": getattr(a, 'level', {}).value if hasattr(getattr(a, 'level', {}), 'value') else 'unknown',
                "message": getattr(a, 'message', 'Unknown alert'),
                "timestamp": getattr(a, 'timestamp', datetime.now()).isoformat(),
                "resolved": getattr(a, 'resolved', False)
            } for i, a in enumerate(snapshot.alerts)],
            "uptime_seconds": snapshot.uptime_seconds
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Health data exported to {filepath}")
        return filepath
