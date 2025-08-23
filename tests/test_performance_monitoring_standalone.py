#!/usr/bin/env python3
"""
Standalone Performance Monitoring Integration Test
Tests the performance monitoring system independently of the main project imports.
"""

import asyncio
import json
import os
import sys
import tempfile
import time
from pathlib import Path
import importlib.util


def load_module_from_file(module_name: str, file_path: str):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_performance_monitor_standalone():
    """Test performance monitor in standalone mode."""
    print("\n🎯 Testing Performance Monitor Standalone")
    print("=" * 45)

    try:
        # Load performance monitor module directly
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        # Test class creation
        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        MetricData = perf_monitor_module.MetricData
        MetricType = perf_monitor_module.MetricType
        AlertSeverity = perf_monitor_module.AlertSeverity

        # Create performance monitor
        monitor = PerformanceMonitor()
        print("✅ Performance monitor created successfully")

        # Test metric recording
        metric = MetricData(
            metric_name="test_cpu_usage",
            metric_type=MetricType.GAUGE,
            value=75.5,
            timestamp=time.time(),
            tags={"host": "test", "service": "test"},
            unit="percent",
        )
        monitor.record_metric(metric)
        print("✅ Metric recorded successfully")

        # Test metric retrieval
        series = monitor.get_metric_series("test_cpu_usage")
        if series and len(series.data_points) == 1:
            print("✅ Metric retrieved successfully")
            print(f"   - Metric: {series.metric_name}")
            print(f"   - Value: {series.data_points[0].value}")
            print(f"   - Unit: {series.data_points[0].unit}")
        else:
            print("❌ Metric retrieval failed")
            return False

        # Test aggregation
        avg_value = monitor.aggregate_metrics("test_cpu_usage", "avg")
        if avg_value == 75.5:
            print("✅ Metric aggregation working")
            print(f"   - Average: {avg_value}")
        else:
            print("❌ Metric aggregation failed")
            return False

        # Test multiple metrics for aggregation
        for i in range(5):
            metric = MetricData(
                metric_name="test_memory_usage",
                metric_type=MetricType.GAUGE,
                value=60.0 + i * 5,
                timestamp=time.time() + i,
                tags={"host": "test"},
                unit="percent",
            )
            monitor.record_metric(metric)

        # Test different aggregations
        avg_memory = monitor.aggregate_metrics("test_memory_usage", "avg")
        max_memory = monitor.aggregate_metrics("test_memory_usage", "max")
        min_memory = monitor.aggregate_metrics("test_memory_usage", "min")

        print(f"✅ Memory metrics aggregation:")
        print(f"   - Average: {avg_memory}%")
        print(f"   - Maximum: {max_memory}%")
        print(f"   - Minimum: {min_memory}%")

        # Test system status
        status = monitor.get_system_status()
        print("✅ System status retrieved:")
        print(f"   - Running: {status['running']}")
        print(f"   - Collectors: {status['collectors_count']}")
        print(f"   - Alert Rules: {status['alert_rules_count']}")
        print(f"   - Metric Names: {len(status['metric_names'])}")

        return True

    except Exception as e:
        print(f"❌ Performance monitor test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_metrics_collectors_standalone():
    """Test metrics collectors in standalone mode."""
    print("\n📊 Testing Metrics Collectors Standalone")
    print("=" * 40)

    try:
        # Load metrics collector module
        collectors_path = "src/services/metrics_collector.py"
        collectors_module = load_module_from_file("metrics_collector", collectors_path)

        # Test system metrics collector
        SystemMetricsCollector = collectors_module.SystemMetricsCollector
        system_collector = SystemMetricsCollector(collection_interval=1)

        print("1. Testing System Metrics Collector...")
        system_metrics = await system_collector.collect_metrics()

        if system_metrics and len(system_metrics) > 0:
            print(f"✅ System collector: {len(system_metrics)} metrics collected")

            # Show some example metrics
            for metric in system_metrics[:3]:  # Show first 3
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ System collector failed")
            return False

        # Test application metrics collector
        ApplicationMetricsCollector = collectors_module.ApplicationMetricsCollector
        app_collector = ApplicationMetricsCollector(collection_interval=1)

        print("\n2. Testing Application Metrics Collector...")
        app_metrics = await app_collector.collect_metrics()

        if app_metrics and len(app_metrics) > 0:
            print(f"✅ Application collector: {len(app_metrics)} metrics collected")

            # Show some example metrics
            for metric in app_metrics[:3]:  # Show first 3
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ Application collector failed")
            return False

        # Test network metrics collector
        NetworkMetricsCollector = collectors_module.NetworkMetricsCollector
        network_collector = NetworkMetricsCollector(collection_interval=1)

        print("\n3. Testing Network Metrics Collector...")
        network_metrics = await network_collector.collect_metrics()

        if network_metrics and len(network_metrics) > 0:
            print(f"✅ Network collector: {len(network_metrics)} metrics collected")

            # Show some example metrics
            for metric in network_metrics[:3]:  # Show first 3
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ Network collector failed")
            return False

        # Test custom metrics collector
        CustomMetricsCollector = collectors_module.CustomMetricsCollector
        custom_collector = CustomMetricsCollector(collection_interval=1)

        print("\n4. Testing Custom Metrics Collector...")

        # Add custom metrics
        custom_collector.add_custom_metric("active_users", lambda: 42)
        custom_collector.add_custom_metric("queue_depth", lambda: 15)
        custom_collector.add_custom_metric("cache_hit_rate", lambda: 87.5)

        custom_metrics = await custom_collector.collect_metrics()

        if custom_metrics and len(custom_metrics) == 3:
            print(f"✅ Custom collector: {len(custom_metrics)} metrics collected")

            for metric in custom_metrics:
                print(f"   - {metric.metric_name}: {metric.value}")
        else:
            print("❌ Custom collector failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Metrics collectors test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_dashboard_backend_standalone():
    """Test dashboard backend in standalone mode."""
    print("\n🌐 Testing Dashboard Backend Standalone")
    print("=" * 40)

    try:
        # Load required modules
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        dashboard_path = "src/services/dashboard_backend.py"
        dashboard_module = load_module_from_file("dashboard_backend", dashboard_path)

        # Create components
        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        DashboardBackend = dashboard_module.DashboardBackend

        monitor = PerformanceMonitor()
        dashboard = DashboardBackend(
            monitor, host="localhost", port=0
        )  # Port 0 for testing

        print("✅ Dashboard backend created successfully")

        # Test API endpoints
        if len(dashboard.api_endpoints) > 0:
            print(f"✅ API endpoints registered: {len(dashboard.api_endpoints)}")
            for endpoint in dashboard.api_endpoints:
                print(f"   - {endpoint.method} {endpoint.path}: {endpoint.description}")
        else:
            print("❌ No API endpoints registered")
            return False

        # Test metrics endpoint functionality
        test_params = {
            "metric_name": "test_metric",
            "start_time": str(time.time() - 3600),
            "end_time": str(time.time()),
        }

        response = dashboard.get_metrics_endpoint(test_params)
        if response and response.get("status") == "success":
            print("✅ Metrics endpoint working")
            print(f"   - Response status: {response['status']}")
        else:
            print("❌ Metrics endpoint failed")
            return False

        # Test WebSocket handler
        if dashboard.websocket_handler:
            print("✅ WebSocket handler initialized")
            print(
                f"   - Active connections: {len(dashboard.websocket_handler.connections)}"
            )
        else:
            print("❌ WebSocket handler not initialized")
            return False

        return True

    except Exception as e:
        print(f"❌ Dashboard backend test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_dashboard_frontend_standalone():
    """Test dashboard frontend in standalone mode."""
    print("\n🎨 Testing Dashboard Frontend Standalone")
    print("=" * 40)

    try:
        # Load dashboard frontend module
        frontend_path = "src/services/dashboard_frontend.py"
        frontend_module = load_module_from_file("dashboard_frontend", frontend_path)

        DashboardFrontend = frontend_module.DashboardFrontend
        DashboardWidget = frontend_module.DashboardWidget
        ChartType = frontend_module.ChartType
        DashboardLayout = frontend_module.DashboardLayout

        # Create dashboard frontend
        frontend = DashboardFrontend("ws://localhost:8080/ws")
        print("✅ Dashboard frontend created")

        # Test widget creation and addition
        widgets = [
            DashboardWidget(
                widget_id="cpu_widget",
                title="CPU Usage",
                chart_type=ChartType.LINE,
                metric_name="cpu_usage_percent",
            ),
            DashboardWidget(
                widget_id="memory_widget",
                title="Memory Usage",
                chart_type=ChartType.GAUGE,
                metric_name="memory_usage_percent",
            ),
            DashboardWidget(
                widget_id="disk_widget",
                title="Disk Usage",
                chart_type=ChartType.BAR,
                metric_name="disk_usage_percent",
            ),
        ]

        for widget in widgets:
            frontend.add_widget(widget)

        if len(frontend.widgets) == 3:
            print(f"✅ Widgets added successfully: {len(frontend.widgets)}")
            for widget in frontend.widgets:
                print(f"   - {widget.title} ({widget.chart_type.value})")
        else:
            print("❌ Widget addition failed")
            return False

        # Test layout configuration
        layout = DashboardLayout(
            columns=12, rows=8, theme="dark", auto_refresh=True, refresh_interval=5
        )
        frontend.set_layout(layout)

        if frontend.layout.columns == 12 and frontend.layout.theme == "dark":
            print("✅ Layout configured successfully")
            print(f"   - Grid: {layout.columns}x{layout.rows}")
            print(f"   - Theme: {layout.theme}")
            print(f"   - Auto refresh: {layout.auto_refresh}")
        else:
            print("❌ Layout configuration failed")
            return False

        # Test HTML generation
        html = frontend.generate_html()
        if "<!DOCTYPE html>" in html and "CPU Usage" in html and "Memory Usage" in html:
            print("✅ HTML generation working")
            print(f"   - HTML size: {len(html)} characters")
            print(f"   - Contains dashboard title: {'Agent Cellphone V2' in html}")
        else:
            print("❌ HTML generation failed")
            return False

        # Test JavaScript generation
        js = frontend.generate_javascript()
        if (
            "websocket" in js.lower()
            and "chart" in js.lower()
            and "cpu_usage_percent" in js
        ):
            print("✅ JavaScript generation working")
            print(f"   - JavaScript size: {len(js)} characters")
            print(f"   - Contains WebSocket logic: {'WebSocket' in js}")
            print(f"   - Contains chart logic: {'Chart' in js}")
        else:
            print("❌ JavaScript generation failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Dashboard frontend test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_alerting_system_standalone():
    """Test alerting system in standalone mode."""
    print("\n🚨 Testing Alerting System Standalone")
    print("=" * 35)

    try:
        # Load required modules
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        alerting_path = "src/services/performance_alerting.py"
        alerting_module = load_module_from_file("performance_alerting", alerting_path)

        # Get classes
        AlertingSystem = alerting_module.AlertingSystem
        AlertRule = alerting_module.AlertRule
        EmailAlertChannel = alerting_module.EmailAlertChannel
        SlackAlertChannel = alerting_module.SlackAlertChannel
        WebhookAlertChannel = alerting_module.WebhookAlertChannel

        AlertCondition = perf_monitor_module.AlertCondition
        AlertSeverity = perf_monitor_module.AlertSeverity
        PerformanceAlert = perf_monitor_module.PerformanceAlert

        # Create alerting system
        alerting = AlertingSystem()
        print("✅ Alerting system created")

        # Test alert rule creation
        rules = [
            AlertRule(
                name="High CPU Usage",
                metric_name="cpu_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=85.0,
                severity=AlertSeverity.WARNING,
                description="CPU usage is above 85%",
            ),
            AlertRule(
                name="Critical Memory Usage",
                metric_name="memory_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=95.0,
                severity=AlertSeverity.CRITICAL,
                description="Memory usage is critically high",
            ),
            AlertRule(
                name="Low Disk Space",
                metric_name="disk_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=90.0,
                severity=AlertSeverity.WARNING,
                description="Disk space is running low",
            ),
        ]

        for rule in rules:
            alerting.add_alert_rule(rule)

        if len(alerting.alert_rules) == 3:
            print(f"✅ Alert rules added: {len(alerting.alert_rules)}")
            for rule in alerting.alert_rules:
                print(
                    f"   - {rule.name}: {rule.metric_name} {rule.condition.value} {rule.threshold}"
                )
        else:
            print("❌ Alert rule addition failed")
            return False

        # Test alert channels (mock configurations)
        channels = [
            EmailAlertChannel(
                name="test_email",
                recipients=["admin@example.com"],
                smtp_server="localhost",
                smtp_port=25,
            ),
            SlackAlertChannel(
                name="test_slack",
                webhook_url="https://hooks.slack.com/services/test",
                channel="#alerts",
            ),
            WebhookAlertChannel(
                name="test_webhook",
                webhook_url="https://api.example.com/alerts",
                method="POST",
            ),
        ]

        for channel in channels:
            channel.enabled = False  # Disable for testing to avoid actual sends
            alerting.add_alert_channel(channel)

        if len(alerting.alert_channels) == 3:
            print(f"✅ Alert channels added: {len(alerting.alert_channels)}")
            for channel in alerting.alert_channels:
                print(f"   - {channel.name}: {channel.__class__.__name__}")
        else:
            print("❌ Alert channel addition failed")
            return False

        # Test alert processing (without sending)
        test_alert = PerformanceAlert(
            alert_id="test_001",
            rule_name="High CPU Usage",
            metric_name="cpu_usage_percent",
            current_value=87.5,
            threshold=85.0,
            severity=AlertSeverity.WARNING,
            message="CPU usage is 87.5%, which exceeds the threshold of 85%",
            timestamp=time.time(),
            tags={"host": "test-server", "service": "test"},
        )

        # Process alert (channels are disabled so no actual sending occurs)
        results = await alerting.process_alert(test_alert)

        print("✅ Alert processing completed")
        print(f"   - Alert ID: {test_alert.alert_id}")
        print(f"   - Rule: {test_alert.rule_name}")
        print(f"   - Severity: {test_alert.severity.value}")
        print(f"   - Processing results: {results}")

        # Test alert manager functionality
        if alerting.alert_manager:
            history = alerting.alert_manager.get_alert_history(limit=5)
            print(f"✅ Alert history: {len(history)} alerts")

            active_channels = alerting.alert_manager.get_active_channels()
            print(f"✅ Active channels: {len(active_channels)} channels")

        return True

    except Exception as e:
        print(f"❌ Alerting system test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_configuration_standalone():
    """Test configuration loading."""
    print("\n⚙️ Testing Configuration Loading")
    print("=" * 30)

    try:
        config_file = "config/performance_monitoring_config.json"

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
            print("✅ Configuration file loaded successfully")

            # Validate configuration structure
            perf_config = config.get("performance_monitoring", {})
            if perf_config:
                print("✅ Performance monitoring configuration found")

                # Check key sections
                sections = ["collectors", "dashboard", "alerting"]
                for section in sections:
                    if section in perf_config:
                        print(f"   - {section}: ✅")
                    else:
                        print(f"   - {section}: ❌")

                # Show configuration summary
                print(f"\nConfiguration Summary:")
                print(f"   - Version: {perf_config.get('version', 'N/A')}")
                print(
                    f"   - Collection Interval: {perf_config.get('collection_interval', 'N/A')}s"
                )
                print(
                    f"   - Retention Period: {perf_config.get('retention_period', 'N/A')}s"
                )

                # Dashboard config
                dashboard_config = perf_config.get("dashboard", {})
                print(f"   - Dashboard Port: {dashboard_config.get('port', 'N/A')}")
                print(f"   - Dashboard Theme: {dashboard_config.get('theme', 'N/A')}")

                # Alerting config
                alerting_config = perf_config.get("alerting", {})
                rules = alerting_config.get("rules", [])
                channels = alerting_config.get("channels", {})
                print(f"   - Alert Rules: {len(rules)}")
                print(f"   - Alert Channels: {len(channels)}")

            else:
                print("❌ Performance monitoring configuration missing")
                return False

            return True
        else:
            print(f"⚠️ Configuration file not found: {config_file}")
            return False

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False


async def test_integration_workflow_standalone():
    """Test end-to-end integration workflow."""
    print("\n🔄 Testing Integration Workflow Standalone")
    print("=" * 45)

    try:
        # Load all required modules
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        collectors_path = "src/services/metrics_collector.py"
        collectors_module = load_module_from_file("metrics_collector", collectors_path)

        dashboard_path = "src/services/dashboard_backend.py"
        dashboard_module = load_module_from_file("dashboard_backend", dashboard_path)

        alerting_path = "src/services/performance_alerting.py"
        alerting_module = load_module_from_file("performance_alerting", alerting_path)

        # Get classes
        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        SystemMetricsCollector = collectors_module.SystemMetricsCollector
        DashboardBackend = dashboard_module.DashboardBackend
        AlertingSystem = alerting_module.AlertingSystem

        print("✅ All modules loaded successfully")

        # Initialize components
        monitor = PerformanceMonitor()
        collector = SystemMetricsCollector(collection_interval=1)
        dashboard = DashboardBackend(monitor, host="localhost", port=0)
        alerting = AlertingSystem()

        print("✅ All components initialized")

        # Connect components
        monitor.add_collector(collector)
        monitor.alert_callbacks.append(alerting.process_alert)

        print("✅ Components connected")

        # Start monitoring (briefly)
        await monitor.start()
        print("✅ Monitoring started")

        # Wait for metrics collection
        print("⏳ Collecting metrics for 3 seconds...")
        await asyncio.sleep(3)

        # Check metrics collection
        metric_names = monitor.metrics_storage.get_all_metric_names()
        if metric_names:
            print(f"✅ Metrics collected: {len(metric_names)} metric types")

            # Show some collected metrics
            for metric_name in metric_names[:5]:  # Show first 5
                series = monitor.get_metric_series(metric_name)
                if series and series.data_points:
                    latest = series.data_points[-1]
                    print(f"   - {metric_name}: {latest.value} {latest.unit}")
        else:
            print("❌ No metrics collected")
            return False

        # Test dashboard functionality
        test_params = {"metric_name": metric_names[0] if metric_names else "test"}
        response = dashboard.get_metrics_endpoint(test_params)
        if response.get("status") == "success":
            print("✅ Dashboard can access collected metrics")
        else:
            print("❌ Dashboard cannot access metrics")
            return False

        # Test system status
        status = monitor.get_system_status()
        print("✅ System status check:")
        print(f"   - Running: {status['running']}")
        print(f"   - Collectors: {status['collectors_count']}")
        print(f"   - Metrics: {len(status['metric_names'])}")

        # Stop monitoring
        await monitor.stop()
        print("✅ Monitoring stopped gracefully")

        return True

    except Exception as e:
        print(f"❌ Integration workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_launcher_script_standalone():
    """Test launcher script availability and structure."""
    print("\n🚀 Testing Launcher Script Standalone")
    print("=" * 35)

    try:
        launcher_path = "scripts/launch_performance_monitoring.py"

        if os.path.exists(launcher_path):
            print("✅ Launcher script found")

            # Read and analyze script
            with open(launcher_path, "r") as f:
                content = f.read()

            # Check for key components
            checks = [
                ("Main launcher class", "PerformanceMonitoringLauncher" in content),
                ("CLI interface", "argparse" in content),
                ("Async support", "asyncio" in content),
                ("Configuration loading", "load_config" in content),
                ("Component setup", "setup_performance_monitor" in content),
                ("Dashboard setup", "setup_dashboard" in content),
                ("Alerting setup", "setup_alerting_system" in content),
                ("Signal handling", "signal_handler" in content),
                ("Main entry point", "if __name__" in content),
            ]

            all_passed = True
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   - {check_name}: {status}")
                if not check_result:
                    all_passed = False

            if all_passed:
                print("✅ Launcher script structure is complete")
            else:
                print("❌ Launcher script missing some components")
                return False

            # Check script size (should be substantial)
            lines = len(content.split("\n"))
            print(f"✅ Launcher script size: {lines} lines")

            return True
        else:
            print("❌ Launcher script not found")
            return False

    except Exception as e:
        print(f"❌ Launcher script test failed: {e}")
        return False


async def main():
    """Main test runner."""
    print("🚀 Performance Monitoring Standalone Integration Test")
    print("=" * 60)

    # Change to project directory
    os.chdir(Path(__file__).parent)

    tests = [
        ("Performance Monitor", test_performance_monitor_standalone),
        ("Metrics Collectors", test_metrics_collectors_standalone),
        ("Dashboard Backend", test_dashboard_backend_standalone),
        ("Dashboard Frontend", test_dashboard_frontend_standalone),
        ("Alerting System", test_alerting_system_standalone),
        ("Configuration", test_configuration_standalone),
        ("Integration Workflow", test_integration_workflow_standalone),
        ("Launcher Script", test_launcher_script_standalone),
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

    print(f"\nTotal Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")

    if failed == 0:
        print("\n🎉 All integration tests passed!")
        print("Performance monitoring system is fully functional and ready for use.")

        print("\n🔗 Next Steps:")
        print(
            "1. Start the system: python scripts/launch_performance_monitoring.py start"
        )
        print("2. Access dashboard: http://localhost:8080")
        print("3. Check API health: http://localhost:8080/api/health")
        print("4. View metrics: http://localhost:8080/api/metrics")

        return 0
    else:
        print(f"\n❌ {failed} integration tests failed.")
        print("Please review the errors above before proceeding.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
