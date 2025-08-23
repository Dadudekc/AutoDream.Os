"""
Performance Monitoring Smoke Tests for Agent_Cellphone_V2_Repository
Lightweight smoke tests to verify basic functionality and integration.
"""

import asyncio
import json
import os
import sys
import tempfile
import time
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent.parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def test_basic_imports():
    """Test that all performance monitoring modules can be imported."""
    print("🧪 Testing Basic Imports")
    print("=" * 40)

    try:
        from services.performance_monitor import (
            PerformanceMonitor,
            MetricType,
            MetricData,
            MetricSeries,
            PerformanceAlert,
            AlertSeverity,
            AlertCondition,
        )

        print("✅ Performance monitor imported successfully")

        from services.metrics_collector import (
            SystemMetricsCollector,
            ApplicationMetricsCollector,
            NetworkMetricsCollector,
            CustomMetricsCollector,
        )

        print("✅ Metrics collectors imported successfully")

        from services.dashboard_backend import (
            DashboardBackend,
            DashboardAPI,
            DashboardWebSocket,
        )

        print("✅ Dashboard backend imported successfully")

        from src.services.dashboard import (
            DashboardFrontend,
            DashboardWidget,
            ChartType,
        )

        print("✅ Dashboard frontend imported successfully")

        from services.performance_alerting import (
            AlertingSystem,
            EmailAlertChannel,
            SlackAlertChannel,
        )

        print("✅ Performance alerting imported successfully")

        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_performance_monitor_basic():
    """Test basic performance monitor functionality."""
    print("\n🎯 Testing Performance Monitor Basic Functionality")
    print("=" * 50)

    try:
        from services.performance_monitor import (
            PerformanceMonitor,
            MetricData,
            MetricType,
        )

        # Create performance monitor
        monitor = PerformanceMonitor()
        print("✅ Performance monitor created")

        # Test metric recording
        metric = MetricData(
            metric_name="test_metric",
            metric_type=MetricType.GAUGE,
            value=42.0,
            timestamp=time.time(),
            tags={"test": "true"},
            unit="units",
        )
        monitor.record_metric(metric)
        print("✅ Metric recorded successfully")

        # Test metric retrieval
        series = monitor.get_metric_series("test_metric")
        if series and len(series.data_points) == 1:
            print("✅ Metric retrieved successfully")
        else:
            print("❌ Metric retrieval failed")
            return False

        # Test aggregation
        avg_value = monitor.aggregate_metrics("test_metric", "avg")
        if avg_value == 42.0:
            print("✅ Metric aggregation working")
        else:
            print("❌ Metric aggregation failed")
            return False

        # Test system status
        status = monitor.get_system_status()
        if isinstance(status, dict) and "running" in status:
            print("✅ System status retrieved")
        else:
            print("❌ System status failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Performance monitor test failed: {e}")
        return False


async def test_metrics_collectors():
    """Test metrics collectors functionality."""
    print("\n📊 Testing Metrics Collectors")
    print("=" * 35)

    try:
        from services.metrics_collector import (
            SystemMetricsCollector,
            ApplicationMetricsCollector,
            NetworkMetricsCollector,
            CustomMetricsCollector,
        )

        # Test system metrics collector
        system_collector = SystemMetricsCollector(collection_interval=1)
        metrics = await system_collector.collect_metrics()

        if metrics and len(metrics) > 0:
            print(f"✅ System collector: {len(metrics)} metrics collected")
        else:
            print("❌ System collector failed")
            return False

        # Test application metrics collector
        app_collector = ApplicationMetricsCollector(collection_interval=1)
        app_metrics = await app_collector.collect_metrics()

        if app_metrics and len(app_metrics) > 0:
            print(f"✅ Application collector: {len(app_metrics)} metrics collected")
        else:
            print("❌ Application collector failed")
            return False

        # Test network metrics collector
        network_collector = NetworkMetricsCollector(collection_interval=1)
        network_metrics = await network_collector.collect_metrics()

        if network_metrics and len(network_metrics) > 0:
            print(f"✅ Network collector: {len(network_metrics)} metrics collected")
        else:
            print("❌ Network collector failed")
            return False

        # Test custom metrics collector
        custom_collector = CustomMetricsCollector(collection_interval=1)
        custom_collector.add_custom_metric("test_custom", lambda: 100.0)
        custom_metrics = await custom_collector.collect_metrics()

        if custom_metrics and len(custom_metrics) == 1:
            print("✅ Custom collector working")
        else:
            print("❌ Custom collector failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Metrics collectors test failed: {e}")
        return False


async def test_dashboard_backend():
    """Test dashboard backend functionality."""
    print("\n🌐 Testing Dashboard Backend")
    print("=" * 30)

    try:
        from services.dashboard_backend import DashboardBackend
        from services.performance_monitor import PerformanceMonitor

        # Create components
        monitor = PerformanceMonitor()
        dashboard = DashboardBackend(
            monitor, host="localhost", port=0
        )  # Use port 0 for testing

        print("✅ Dashboard backend created")

        # Test API endpoint registration
        initial_endpoints = len(dashboard.api_endpoints)
        if initial_endpoints > 0:
            print(f"✅ API endpoints registered: {initial_endpoints}")
        else:
            print("❌ No API endpoints registered")
            return False

        # Test metrics endpoint (mock)
        test_params = {
            "metric_name": "test_metric",
            "start_time": str(time.time() - 3600),
            "end_time": str(time.time()),
        }

        response = dashboard.get_metrics_endpoint(test_params)
        if response and response.get("status") == "success":
            print("✅ Metrics endpoint working")
        else:
            print("❌ Metrics endpoint failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Dashboard backend test failed: {e}")
        return False


def test_dashboard_frontend():
    """Test dashboard frontend functionality."""
    print("\n🎨 Testing Dashboard Frontend")
    print("=" * 30)

    try:
        from src.services.dashboard import (
            DashboardFrontend,
            DashboardWidget,
            ChartType,
            DashboardLayout,
        )

        # Create dashboard frontend
        frontend = DashboardFrontend("ws://localhost:8080/ws")
        print("✅ Dashboard frontend created")

        # Test widget creation
        widget = DashboardWidget(
            widget_id="test_widget",
            title="Test Widget",
            chart_type=ChartType.LINE,
            metric_name="test_metric",
        )
        frontend.add_widget(widget)

        if len(frontend.widgets) == 1:
            print("✅ Widget added successfully")
        else:
            print("❌ Widget addition failed")
            return False

        # Test layout configuration
        layout = DashboardLayout(columns=12, rows=8)
        frontend.set_layout(layout)

        if frontend.layout.columns == 12:
            print("✅ Layout configured")
        else:
            print("❌ Layout configuration failed")
            return False

        # Test HTML generation
        html = frontend.generate_html()
        if "<!DOCTYPE html>" in html and "Test Widget" in html:
            print("✅ HTML generation working")
        else:
            print("❌ HTML generation failed")
            return False

        # Test JavaScript generation
        js = frontend.generate_javascript()
        if "websocket" in js.lower() and "chart" in js.lower():
            print("✅ JavaScript generation working")
        else:
            print("❌ JavaScript generation failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Dashboard frontend test failed: {e}")
        return False


async def test_alerting_system():
    """Test alerting system functionality."""
    print("\n🚨 Testing Alerting System")
    print("=" * 25)

    try:
        from services.performance_alerting import (
            AlertingSystem,
            AlertRule,
            EmailAlertChannel,
        )
        from services.performance_monitor import (
            AlertCondition,
            AlertSeverity,
            PerformanceAlert,
        )

        # Create alerting system
        alerting = AlertingSystem()
        print("✅ Alerting system created")

        # Test alert rule creation
        rule = AlertRule(
            name="Test Rule",
            metric_name="test_metric",
            condition=AlertCondition.GREATER_THAN,
            threshold=50.0,
            severity=AlertSeverity.WARNING,
        )
        alerting.add_alert_rule(rule)

        if len(alerting.alert_rules) == 1:
            print("✅ Alert rule added")
        else:
            print("❌ Alert rule addition failed")
            return False

        # Test alert channel creation (mock email)
        email_channel = EmailAlertChannel(
            name="test_email",
            recipients=["test@example.com"],
            smtp_server="localhost",
            smtp_port=25,
        )
        alerting.add_alert_channel(email_channel)

        if len(alerting.alert_channels) == 1:
            print("✅ Alert channel added")
        else:
            print("❌ Alert channel addition failed")
            return False

        # Test alert processing (without actually sending)
        test_alert = PerformanceAlert(
            alert_id="test_001",
            rule_name="Test Rule",
            metric_name="test_metric",
            current_value=75.0,
            threshold=50.0,
            severity=AlertSeverity.WARNING,
            message="Test alert message",
            timestamp=time.time(),
        )

        # Mock the sending to avoid actual email/webhook calls
        email_channel.enabled = False  # Disable for testing
        results = await alerting.process_alert(test_alert)

        print("✅ Alert processing completed")

        return True

    except Exception as e:
        print(f"❌ Alerting system test failed: {e}")
        return False


def test_configuration_loading():
    """Test configuration file loading."""
    print("\n⚙️ Testing Configuration Loading")
    print("=" * 35)

    try:
        config_file = "config/system/performance.json"
        config_path = Path(config_file)

        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
            print("✅ Configuration file loaded")

            # Check required sections
            perf_config = config.get("performance_monitoring", {})
            if perf_config:
                print("✅ Performance monitoring config found")
            else:
                print("❌ Performance monitoring config missing")
                return False

            # Check collectors config
            collectors = perf_config.get("collectors", {})
            if collectors:
                print(f"✅ Collectors config found: {len(collectors)} collectors")
            else:
                print("❌ Collectors config missing")
                return False

            # Check dashboard config
            dashboard = perf_config.get("dashboard", {})
            if dashboard:
                print("✅ Dashboard config found")
            else:
                print("❌ Dashboard config missing")
                return False

            return True
        else:
            print(f"⚠️ Configuration file not found: {config_file}")
            return False

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False


async def test_integration_workflow():
    """Test end-to-end integration workflow."""
    print("\n🔄 Testing Integration Workflow")
    print("=" * 35)

    try:
        from services.performance_monitor import (
            PerformanceMonitor,
            MetricData,
            MetricType,
        )
        from services.metrics_collector import SystemMetricsCollector
        from services.dashboard_backend import DashboardBackend
        from services.performance_alerting import AlertingSystem, AlertRule

        # Initialize components
        monitor = PerformanceMonitor()
        collector = SystemMetricsCollector(collection_interval=1)
        dashboard = DashboardBackend(monitor, host="localhost", port=0)
        alerting = AlertingSystem()

        print("✅ All components initialized")

        # Add collector to monitor
        monitor.add_collector(collector)
        print("✅ Collector added to monitor")

        # Connect alerting to monitor
        monitor.alert_callbacks.append(alerting.process_alert)
        print("✅ Alerting connected to monitor")

        # Start monitoring (briefly)
        await monitor.start()
        print("✅ Monitoring started")

        # Wait for some metrics collection
        await asyncio.sleep(2)

        # Check if metrics were collected
        metric_names = monitor.metrics_storage.get_all_metric_names()
        if metric_names:
            print(f"✅ Metrics collected: {len(metric_names)} metric types")
        else:
            print("❌ No metrics collected")
            return False

        # Stop monitoring
        await monitor.stop()
        print("✅ Monitoring stopped")

        # Test dashboard functionality
        if metric_names:
            first_metric = metric_names[0]
            series = monitor.get_metric_series(first_metric)
            if series and series.data_points:
                print(
                    f"✅ Dashboard can access metrics: {len(series.data_points)} data points"
                )
            else:
                print("❌ Dashboard cannot access metrics")
                return False

        return True

    except Exception as e:
        print(f"❌ Integration workflow test failed: {e}")
        return False


def test_launcher_script():
    """Test launcher script availability."""
    print("\n🚀 Testing Launcher Script")
    print("=" * 25)

    try:
        launcher_path = Path("scripts/launch_performance_monitoring.py")

        if launcher_path.exists():
            print("✅ Launcher script found")

            # Check if script is executable/readable
            with open(launcher_path, "r") as f:
                content = f.read()

            if "PerformanceMonitoringLauncher" in content:
                print("✅ Launcher script contains main class")
            else:
                print("❌ Launcher script missing main class")
                return False

            if "argparse" in content:
                print("✅ Launcher script has CLI interface")
            else:
                print("❌ Launcher script missing CLI interface")
                return False

            return True
        else:
            print("❌ Launcher script not found")
            return False

    except Exception as e:
        print(f"❌ Launcher script test failed: {e}")
        return False


async def main():
    """Main smoke test runner."""
    print("🚀 Performance Monitoring Smoke Test Suite")
    print("=" * 50)

    tests = [
        ("Basic Imports", test_basic_imports),
        ("Performance Monitor", test_performance_monitor_basic),
        ("Metrics Collectors", test_metrics_collectors),
        ("Dashboard Backend", test_dashboard_backend),
        ("Dashboard Frontend", test_dashboard_frontend),
        ("Alerting System", test_alerting_system),
        ("Configuration Loading", test_configuration_loading),
        ("Integration Workflow", test_integration_workflow),
        ("Launcher Script", test_launcher_script),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False

    # Print summary
    print("\n📊 Test Summary")
    print("=" * 20)

    passed = 0
    failed = 0

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\nTotal: {len(tests)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print(
            "\n🎉 All smoke tests passed! Performance monitoring system is working correctly."
        )
        return 0
    else:
        print(f"\n❌ {failed} smoke tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
