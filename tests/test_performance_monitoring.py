"""
Performance Monitoring Test Suite for Agent_Cellphone_V2_Repository
Comprehensive testing of performance monitoring and dashboard components following TDD principles.
"""

import pytest
import asyncio
import json
import time
import threading
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import tempfile
import shutil
from datetime import datetime, timedelta

# Import the components we're testing (will be created)
try:
    from src.services.performance_monitor import (
        PerformanceMonitor,
        MetricType,
        MetricData,
        MetricSeries,
        PerformanceAlert,
        AlertSeverity,
        AlertCondition,
    )
    from src.services.metrics_collector import (
        MetricsCollector,
        SystemMetricsCollector,
        ApplicationMetricsCollector,
        NetworkMetricsCollector,
        CustomMetricsCollector,
    )
    from src.services.dashboard_backend import (
        DashboardBackend,
        DashboardAPI,
        DashboardWebSocket,
        DashboardEndpoint,
        DashboardRoute,
    )
    from src.services.dashboard_frontend import (
        DashboardFrontend,
        DashboardWidget,
        ChartType,
        DashboardLayout,
        RealTimeUpdater,
    )
    from src.services.performance_alerting import (
        AlertingSystem,
        AlertRule,
        AlertChannel,
        PerformanceAlertManager,
        EmailAlertChannel,
        SlackAlertChannel,
        WebhookAlertChannel,
    )
except ImportError:
    # These will be created during implementation
    pass


class TestPerformanceMonitor:
    """Test suite for the Performance Monitor component."""

    @pytest.fixture
    def performance_monitor(self):
        """Create a fresh performance monitor for each test."""
        return PerformanceMonitor()

    @pytest.fixture
    def sample_metric_data(self):
        """Create sample metric data for testing."""
        return MetricData(
            metric_name="cpu_usage",
            metric_type=MetricType.GAUGE,
            value=75.5,
            timestamp=time.time(),
            tags={"host": "localhost", "service": "api"},
            unit="percent",
        )

    def test_performance_monitor_initialization(self, performance_monitor):
        """Test that performance monitor initializes correctly."""
        assert performance_monitor.metrics_storage == {}
        assert performance_monitor.alert_rules == []
        assert performance_monitor.collectors == []
        assert not performance_monitor.running

    def test_add_metrics_collector(self, performance_monitor):
        """Test adding metrics collectors."""
        collector = Mock()
        performance_monitor.add_collector(collector)

        assert len(performance_monitor.collectors) == 1
        assert performance_monitor.collectors[0] == collector

    def test_record_metric(self, performance_monitor, sample_metric_data):
        """Test recording a metric."""
        performance_monitor.record_metric(sample_metric_data)

        assert "cpu_usage" in performance_monitor.metrics_storage
        metrics = performance_monitor.metrics_storage["cpu_usage"]
        assert len(metrics.data_points) == 1
        assert metrics.data_points[0].value == 75.5

    def test_get_metric_series(self, performance_monitor, sample_metric_data):
        """Test retrieving metric series."""
        performance_monitor.record_metric(sample_metric_data)

        series = performance_monitor.get_metric_series("cpu_usage")
        assert series is not None
        assert len(series.data_points) == 1
        assert series.metric_name == "cpu_usage"

    def test_get_metric_series_with_time_range(self, performance_monitor):
        """Test retrieving metric series with time range."""
        # Add multiple metrics with different timestamps
        base_time = time.time()
        for i in range(5):
            metric = MetricData(
                metric_name="memory_usage",
                metric_type=MetricType.GAUGE,
                value=50.0 + i * 10,
                timestamp=base_time + i * 60,  # 1 minute apart
                tags={"host": "localhost"},
                unit="percent",
            )
            performance_monitor.record_metric(metric)

        # Query for metrics in the last 3 minutes
        start_time = base_time + 120  # 2 minutes after first metric
        end_time = base_time + 300  # 5 minutes after first metric

        series = performance_monitor.get_metric_series(
            "memory_usage", start_time=start_time, end_time=end_time
        )

        assert len(series.data_points) == 3  # Should get 3 metrics in range

    def test_aggregate_metrics(self, performance_monitor):
        """Test metric aggregation functionality."""
        # Add multiple CPU usage metrics
        base_time = time.time()
        values = [60.0, 70.0, 80.0, 90.0, 75.0]

        for i, value in enumerate(values):
            metric = MetricData(
                metric_name="cpu_usage",
                metric_type=MetricType.GAUGE,
                value=value,
                timestamp=base_time + i * 10,
                tags={"host": "localhost"},
                unit="percent",
            )
            performance_monitor.record_metric(metric)

        # Test aggregation
        avg_value = performance_monitor.aggregate_metrics("cpu_usage", "avg")
        max_value = performance_monitor.aggregate_metrics("cpu_usage", "max")
        min_value = performance_monitor.aggregate_metrics("cpu_usage", "min")

        assert avg_value == 75.0  # Average of the values
        assert max_value == 90.0  # Maximum value
        assert min_value == 60.0  # Minimum value

    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, performance_monitor):
        """Test starting and stopping the monitoring system."""
        assert not performance_monitor.running

        await performance_monitor.start()
        assert performance_monitor.running

        await performance_monitor.stop()
        assert not performance_monitor.running

    def test_create_alert_rule(self, performance_monitor):
        """Test creating performance alert rules."""
        alert_rule = AlertRule(
            name="High CPU Usage",
            metric_name="cpu_usage",
            condition=AlertCondition.GREATER_THAN,
            threshold=80.0,
            severity=AlertSeverity.WARNING,
            description="CPU usage is above 80%",
        )

        performance_monitor.add_alert_rule(alert_rule)
        assert len(performance_monitor.alert_rules) == 1
        assert performance_monitor.alert_rules[0].name == "High CPU Usage"

    def test_trigger_alert(self, performance_monitor):
        """Test triggering alerts based on metrics."""
        # Add alert rule
        alert_rule = AlertRule(
            name="High CPU Usage",
            metric_name="cpu_usage",
            condition=AlertCondition.GREATER_THAN,
            threshold=80.0,
            severity=AlertSeverity.WARNING,
        )
        performance_monitor.add_alert_rule(alert_rule)

        # Record metric that should trigger alert
        high_cpu_metric = MetricData(
            metric_name="cpu_usage",
            metric_type=MetricType.GAUGE,
            value=85.0,
            timestamp=time.time(),
            tags={"host": "localhost"},
            unit="percent",
        )

        alerts = performance_monitor.check_alerts(high_cpu_metric)
        assert len(alerts) == 1
        assert alerts[0].rule_name == "High CPU Usage"
        assert alerts[0].severity == AlertSeverity.WARNING


class TestMetricsCollector:
    """Test suite for the Metrics Collector components."""

    @pytest.fixture
    def metrics_collector(self):
        """Create a fresh metrics collector for each test."""
        return MetricsCollector()

    @pytest.fixture
    def system_metrics_collector(self):
        """Create a system metrics collector for testing."""
        return SystemMetricsCollector()

    def test_metrics_collector_initialization(self, metrics_collector):
        """Test that metrics collector initializes correctly."""
        assert metrics_collector.collection_interval == 60  # Default 1 minute
        assert metrics_collector.enabled == True
        assert not metrics_collector.running

    @pytest.mark.asyncio
    async def test_collect_metrics_interface(self, metrics_collector):
        """Test the abstract collect_metrics interface."""
        # This should be implemented by subclasses
        with pytest.raises(NotImplementedError):
            await metrics_collector.collect_metrics()

    def test_system_metrics_collector_initialization(self, system_metrics_collector):
        """Test system metrics collector initialization."""
        assert system_metrics_collector.collect_cpu == True
        assert system_metrics_collector.collect_memory == True
        assert system_metrics_collector.collect_disk == True
        assert system_metrics_collector.collect_network == True

    @pytest.mark.asyncio
    async def test_system_metrics_collection(self, system_metrics_collector):
        """Test system metrics collection."""
        metrics = await system_metrics_collector.collect_metrics()

        assert isinstance(metrics, list)
        assert len(metrics) > 0

        # Check that we have expected metric types
        metric_names = [m.metric_name for m in metrics]
        assert "cpu_usage_percent" in metric_names
        assert "memory_usage_percent" in metric_names
        assert "disk_usage_percent" in metric_names

    @pytest.mark.asyncio
    async def test_application_metrics_collection(self):
        """Test application metrics collection."""
        app_collector = ApplicationMetricsCollector()
        metrics = await app_collector.collect_metrics()

        assert isinstance(metrics, list)
        # Should collect metrics like request_count, response_time, etc.

    @pytest.mark.asyncio
    async def test_network_metrics_collection(self):
        """Test network metrics collection."""
        network_collector = NetworkMetricsCollector()
        metrics = await network_collector.collect_metrics()

        assert isinstance(metrics, list)
        # Should collect metrics like bytes_sent, bytes_received, etc.

    @pytest.mark.asyncio
    async def test_custom_metrics_collection(self):
        """Test custom metrics collection."""
        custom_collector = CustomMetricsCollector()

        # Add a custom metric function
        def get_queue_size():
            return 42

        custom_collector.add_custom_metric("queue_size", get_queue_size)
        metrics = await custom_collector.collect_metrics()

        assert len(metrics) == 1
        assert metrics[0].metric_name == "queue_size"
        assert metrics[0].value == 42


class TestDashboardBackend:
    """Test suite for the Dashboard Backend component."""

    @pytest.fixture
    def dashboard_backend(self):
        """Create a fresh dashboard backend for each test."""
        return DashboardBackend()

    @pytest.fixture
    def sample_metrics_data(self):
        """Create sample metrics data for dashboard testing."""
        return [
            MetricData(
                "cpu_usage",
                MetricType.GAUGE,
                75.0,
                time.time(),
                {"host": "web1"},
                "percent",
            ),
            MetricData(
                "memory_usage",
                MetricType.GAUGE,
                60.0,
                time.time(),
                {"host": "web1"},
                "percent",
            ),
            MetricData(
                "request_count",
                MetricType.COUNTER,
                1500,
                time.time(),
                {"service": "api"},
                "count",
            ),
        ]

    def test_dashboard_backend_initialization(self, dashboard_backend):
        """Test dashboard backend initialization."""
        assert dashboard_backend.api_endpoints == []
        assert dashboard_backend.websocket_connections == []
        assert not dashboard_backend.running

    def test_register_api_endpoint(self, dashboard_backend):
        """Test registering API endpoints."""
        endpoint = DashboardEndpoint(
            path="/api/metrics", method="GET", handler=lambda req: {"status": "ok"}
        )

        dashboard_backend.register_endpoint(endpoint)
        assert len(dashboard_backend.api_endpoints) == 1
        assert dashboard_backend.api_endpoints[0].path == "/api/metrics"

    @pytest.mark.asyncio
    async def test_websocket_connection_management(self, dashboard_backend):
        """Test WebSocket connection management."""
        mock_websocket = Mock()

        await dashboard_backend.add_websocket_connection(mock_websocket)
        assert len(dashboard_backend.websocket_connections) == 1

        await dashboard_backend.remove_websocket_connection(mock_websocket)
        assert len(dashboard_backend.websocket_connections) == 0

    @pytest.mark.asyncio
    async def test_broadcast_metrics_update(
        self, dashboard_backend, sample_metrics_data
    ):
        """Test broadcasting metrics updates to WebSocket clients."""
        # Add mock WebSocket connections
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()

        await dashboard_backend.add_websocket_connection(mock_ws1)
        await dashboard_backend.add_websocket_connection(mock_ws2)

        # Broadcast metrics update
        await dashboard_backend.broadcast_metrics_update(sample_metrics_data)

        # Verify both connections received the update
        mock_ws1.send.assert_called_once()
        mock_ws2.send.assert_called_once()

    def test_get_metrics_api_endpoint(self, dashboard_backend, sample_metrics_data):
        """Test the metrics API endpoint."""
        # Mock the performance monitor
        mock_monitor = Mock()
        mock_monitor.get_metric_series.return_value = MetricSeries(
            metric_name="cpu_usage", data_points=sample_metrics_data[:1]
        )

        dashboard_backend.performance_monitor = mock_monitor

        # Test the API endpoint
        response = dashboard_backend.get_metrics_endpoint(
            {
                "metric_name": "cpu_usage",
                "start_time": str(time.time() - 3600),
                "end_time": str(time.time()),
            }
        )

        assert response["status"] == "success"
        assert "data" in response
        assert len(response["data"]) == 1

    @pytest.mark.asyncio
    async def test_start_stop_dashboard(self, dashboard_backend):
        """Test starting and stopping the dashboard backend."""
        assert not dashboard_backend.running

        await dashboard_backend.start()
        assert dashboard_backend.running

        await dashboard_backend.stop()
        assert not dashboard_backend.running


class TestDashboardFrontend:
    """Test suite for the Dashboard Frontend component."""

    @pytest.fixture
    def dashboard_frontend(self):
        """Create a fresh dashboard frontend for each test."""
        return DashboardFrontend()

    def test_dashboard_frontend_initialization(self, dashboard_frontend):
        """Test dashboard frontend initialization."""
        assert dashboard_frontend.widgets == []
        assert dashboard_frontend.layout is not None
        assert dashboard_frontend.websocket_url is None

    def test_create_dashboard_widget(self, dashboard_frontend):
        """Test creating dashboard widgets."""
        widget = DashboardWidget(
            widget_id="cpu_chart",
            title="CPU Usage",
            chart_type=ChartType.LINE,
            metric_name="cpu_usage",
            refresh_interval=5,
        )

        dashboard_frontend.add_widget(widget)
        assert len(dashboard_frontend.widgets) == 1
        assert dashboard_frontend.widgets[0].title == "CPU Usage"

    def test_dashboard_layout_configuration(self, dashboard_frontend):
        """Test dashboard layout configuration."""
        layout = DashboardLayout(columns=3, rows=2, widget_spacing=10, responsive=True)

        dashboard_frontend.set_layout(layout)
        assert dashboard_frontend.layout.columns == 3
        assert dashboard_frontend.layout.rows == 2
        assert dashboard_frontend.layout.responsive == True

    def test_generate_dashboard_html(self, dashboard_frontend):
        """Test generating dashboard HTML."""
        # Add some widgets
        cpu_widget = DashboardWidget("cpu", "CPU Usage", ChartType.LINE, "cpu_usage")
        memory_widget = DashboardWidget(
            "memory", "Memory Usage", ChartType.GAUGE, "memory_usage"
        )

        dashboard_frontend.add_widget(cpu_widget)
        dashboard_frontend.add_widget(memory_widget)

        html = dashboard_frontend.generate_html()

        assert "<html>" in html
        assert "CPU Usage" in html
        assert "Memory Usage" in html
        assert "chart" in html.lower()

    def test_generate_dashboard_javascript(self, dashboard_frontend):
        """Test generating dashboard JavaScript."""
        # Add a widget
        widget = DashboardWidget("test", "Test Chart", ChartType.LINE, "test_metric")
        dashboard_frontend.add_widget(widget)

        js_code = dashboard_frontend.generate_javascript()

        assert "websocket" in js_code.lower()
        assert "chart" in js_code.lower()
        assert "test_metric" in js_code

    @pytest.mark.asyncio
    async def test_real_time_updater(self):
        """Test real-time dashboard updates."""
        updater = RealTimeUpdater()

        # Mock WebSocket connection
        mock_websocket = AsyncMock()
        updater.websocket = mock_websocket

        # Test sending update
        update_data = {"metric": "cpu_usage", "value": 75.0, "timestamp": time.time()}
        await updater.send_update(update_data)

        mock_websocket.send.assert_called_once()


class TestPerformanceAlerting:
    """Test suite for the Performance Alerting component."""

    @pytest.fixture
    def alerting_system(self):
        """Create a fresh alerting system for each test."""
        return AlertingSystem()

    @pytest.fixture
    def sample_alert(self):
        """Create a sample alert for testing."""
        return PerformanceAlert(
            alert_id="alert_001",
            rule_name="High CPU Usage",
            metric_name="cpu_usage",
            current_value=85.0,
            threshold=80.0,
            severity=AlertSeverity.WARNING,
            message="CPU usage is 85%, which exceeds the threshold of 80%",
            timestamp=time.time(),
            tags={"host": "web1", "service": "api"},
        )

    def test_alerting_system_initialization(self, alerting_system):
        """Test alerting system initialization."""
        assert alerting_system.alert_rules == []
        assert alerting_system.alert_channels == []
        assert alerting_system.active_alerts == {}

    def test_add_alert_rule(self, alerting_system):
        """Test adding alert rules."""
        rule = AlertRule(
            name="High Memory Usage",
            metric_name="memory_usage",
            condition=AlertCondition.GREATER_THAN,
            threshold=90.0,
            severity=AlertSeverity.CRITICAL,
        )

        alerting_system.add_alert_rule(rule)
        assert len(alerting_system.alert_rules) == 1
        assert alerting_system.alert_rules[0].name == "High Memory Usage"

    def test_add_alert_channel(self, alerting_system):
        """Test adding alert channels."""
        email_channel = EmailAlertChannel(
            name="admin_email",
            recipients=["admin@example.com"],
            smtp_server="smtp.example.com",
        )

        alerting_system.add_alert_channel(email_channel)
        assert len(alerting_system.alert_channels) == 1
        assert alerting_system.alert_channels[0].name == "admin_email"

    @pytest.mark.asyncio
    async def test_send_alert(self, alerting_system, sample_alert):
        """Test sending alerts through channels."""
        # Add mock alert channel
        mock_channel = Mock()
        mock_channel.send_alert = AsyncMock()

        alerting_system.add_alert_channel(mock_channel)

        # Send alert
        await alerting_system.send_alert(sample_alert)

        # Verify alert was sent
        mock_channel.send_alert.assert_called_once_with(sample_alert)

    def test_email_alert_channel(self):
        """Test email alert channel."""
        channel = EmailAlertChannel(
            name="email_alerts",
            recipients=["admin@example.com", "ops@example.com"],
            smtp_server="smtp.example.com",
            smtp_port=587,
        )

        assert channel.name == "email_alerts"
        assert len(channel.recipients) == 2
        assert channel.smtp_server == "smtp.example.com"

    def test_slack_alert_channel(self):
        """Test Slack alert channel."""
        channel = SlackAlertChannel(
            name="slack_alerts",
            webhook_url="https://hooks.slack.com/services/...",
            channel="#alerts",
            username="AlertBot",
        )

        assert channel.name == "slack_alerts"
        assert channel.channel == "#alerts"
        assert channel.username == "AlertBot"

    def test_webhook_alert_channel(self):
        """Test webhook alert channel."""
        channel = WebhookAlertChannel(
            name="webhook_alerts",
            webhook_url="https://api.example.com/alerts",
            method="POST",
            headers={"Authorization": "Bearer token123"},
        )

        assert channel.name == "webhook_alerts"
        assert channel.method == "POST"
        assert "Authorization" in channel.headers

    @pytest.mark.asyncio
    async def test_alert_deduplication(self, alerting_system, sample_alert):
        """Test alert deduplication functionality."""
        # Send the same alert twice
        await alerting_system.process_alert(sample_alert)
        await alerting_system.process_alert(sample_alert)

        # Should only have one active alert
        assert len(alerting_system.active_alerts) == 1

    @pytest.mark.asyncio
    async def test_alert_escalation(self, alerting_system):
        """Test alert escalation based on severity."""
        # Create critical alert
        critical_alert = PerformanceAlert(
            alert_id="critical_001",
            rule_name="System Down",
            metric_name="system_availability",
            current_value=0.0,
            threshold=1.0,
            severity=AlertSeverity.CRITICAL,
            message="System is down",
            timestamp=time.time(),
        )

        # Add channels with different severities
        email_channel = Mock()
        email_channel.min_severity = AlertSeverity.WARNING
        slack_channel = Mock()
        slack_channel.min_severity = AlertSeverity.CRITICAL

        alerting_system.add_alert_channel(email_channel)
        alerting_system.add_alert_channel(slack_channel)

        # Process critical alert
        channels = alerting_system.get_channels_for_alert(critical_alert)

        # Both channels should receive critical alert
        assert len(channels) == 2


class TestIntegrationEndToEnd:
    """End-to-end integration tests for the performance monitoring system."""

    @pytest.mark.asyncio
    async def test_full_performance_monitoring_workflow(self):
        """Test the complete performance monitoring workflow."""
        # Initialize all components
        monitor = PerformanceMonitor()
        collector = SystemMetricsCollector()
        dashboard = DashboardBackend()
        alerting = AlertingSystem()

        # Add collector to monitor
        monitor.add_collector(collector)

        # Add alert rule
        alert_rule = AlertRule(
            name="High CPU",
            metric_name="cpu_usage",
            condition=AlertCondition.GREATER_THAN,
            threshold=80.0,
            severity=AlertSeverity.WARNING,
        )
        alerting.add_alert_rule(alert_rule)

        # Start monitoring
        await monitor.start()
        await dashboard.start()

        # Simulate metric collection
        await collector.collect_metrics()

        # Verify system is running
        assert monitor.running
        assert dashboard.running

        # Stop systems
        await monitor.stop()
        await dashboard.stop()

        assert not monitor.running
        assert not dashboard.running

    @pytest.mark.asyncio
    async def test_dashboard_real_time_updates(self):
        """Test real-time dashboard updates with WebSocket."""
        dashboard = DashboardBackend()
        monitor = PerformanceMonitor()

        # Start systems
        await dashboard.start()
        await monitor.start()

        # Mock WebSocket connection
        mock_websocket = AsyncMock()
        await dashboard.add_websocket_connection(mock_websocket)

        # Record a metric
        metric = MetricData(
            metric_name="cpu_usage",
            metric_type=MetricType.GAUGE,
            value=75.0,
            timestamp=time.time(),
            tags={"host": "localhost"},
            unit="percent",
        )

        monitor.record_metric(metric)

        # Trigger dashboard update
        await dashboard.broadcast_metrics_update([metric])

        # Verify WebSocket received update
        mock_websocket.send.assert_called()

        # Cleanup
        await dashboard.stop()
        await monitor.stop()

    def test_configuration_loading(self):
        """Test loading performance monitoring configuration."""
        config_data = {
            "performance_monitoring": {
                "collection_interval": 30,
                "retention_period": 86400,
                "dashboard_port": 8080,
                "alert_channels": [
                    {"type": "email", "recipients": ["admin@example.com"]}
                ],
            }
        }

        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name

        try:
            # Test configuration loading (implementation will handle this)
            monitor = PerformanceMonitor(config_file=config_file)
            assert monitor.collection_interval == 30
            assert monitor.retention_period == 86400
        finally:
            Path(config_file).unlink()


class TestPerformanceAndLoad:
    """Performance and load testing for the monitoring system."""

    @pytest.mark.asyncio
    async def test_high_volume_metrics_processing(self):
        """Test processing high volume of metrics."""
        monitor = PerformanceMonitor()

        # Generate large number of metrics
        start_time = time.time()
        num_metrics = 1000

        for i in range(num_metrics):
            metric = MetricData(
                metric_name=f"test_metric_{i % 10}",
                metric_type=MetricType.GAUGE,
                value=float(i),
                timestamp=time.time(),
                tags={"index": str(i)},
                unit="count",
            )
            monitor.record_metric(metric)

        end_time = time.time()
        processing_time = end_time - start_time

        # Should process 1000 metrics in reasonable time (< 1 second)
        assert processing_time < 1.0
        assert len(monitor.metrics_storage) == 10  # 10 different metric names

    @pytest.mark.asyncio
    async def test_concurrent_dashboard_connections(self):
        """Test handling multiple concurrent dashboard connections."""
        dashboard = DashboardBackend()
        await dashboard.start()

        # Add multiple WebSocket connections
        connections = []
        for i in range(50):
            mock_ws = AsyncMock()
            await dashboard.add_websocket_connection(mock_ws)
            connections.append(mock_ws)

        assert len(dashboard.websocket_connections) == 50

        # Broadcast update to all connections
        test_data = [
            MetricData("test", MetricType.GAUGE, 100.0, time.time(), {}, "units")
        ]
        await dashboard.broadcast_metrics_update(test_data)

        # Verify all connections received the update
        for connection in connections:
            connection.send.assert_called_once()

        await dashboard.stop()

    def test_memory_usage_with_large_dataset(self):
        """Test memory usage with large metric datasets."""
        monitor = PerformanceMonitor()

        # Record metrics for 24 hours (every minute)
        num_metrics = 24 * 60  # 1440 metrics
        base_time = time.time() - 86400  # 24 hours ago

        for i in range(num_metrics):
            metric = MetricData(
                metric_name="cpu_usage",
                metric_type=MetricType.GAUGE,
                value=50.0 + (i % 50),  # Varying values
                timestamp=base_time + (i * 60),  # Every minute
                tags={"host": "test"},
                unit="percent",
            )
            monitor.record_metric(metric)

        # Verify all metrics are stored
        series = monitor.get_metric_series("cpu_usage")
        assert len(series.data_points) == num_metrics

        # Test memory cleanup for old metrics
        monitor.cleanup_old_metrics(retention_hours=12)

        # Should have removed half the metrics (older than 12 hours)
        series_after_cleanup = monitor.get_metric_series("cpu_usage")
        assert len(series_after_cleanup.data_points) < num_metrics
