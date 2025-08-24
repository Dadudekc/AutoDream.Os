import asyncio
import time
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        MetricData = perf_monitor_module.MetricData
        MetricType = perf_monitor_module.MetricType
        AlertSeverity = perf_monitor_module.AlertSeverity

        monitor = PerformanceMonitor()
        print("✅ Performance monitor created successfully")

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

        series = monitor.get_metric_series("test_cpu_usage")
        if series and len(series.data_points) == 1:
            print("✅ Metric retrieved successfully")
            print(f"   - Metric: {series.metric_name}")
            print(f"   - Value: {series.data_points[0].value}")
            print(f"   - Unit: {series.data_points[0].unit}")
        else:
            print("❌ Metric retrieval failed")
            return False

        avg_value = monitor.aggregate_metrics("test_cpu_usage", "avg")
        if avg_value == 75.5:
            print("✅ Metric aggregation working")
            print(f"   - Average: {avg_value}")
        else:
            print("❌ Metric aggregation failed")
            return False

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

        avg_memory = monitor.aggregate_metrics("test_memory_usage", "avg")
        max_memory = monitor.aggregate_metrics("test_memory_usage", "max")
        min_memory = monitor.aggregate_metrics("test_memory_usage", "min")

        print(f"✅ Memory metrics aggregation:")
        print(f"   - Average: {avg_memory}%")
        print(f"   - Maximum: {max_memory}%")
        print(f"   - Minimum: {min_memory}%")

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
        collectors_path = "src/services/metrics_collector.py"
        collectors_module = load_module_from_file("metrics_collector", collectors_path)

        SystemMetricsCollector = collectors_module.SystemMetricsCollector
        system_collector = SystemMetricsCollector(collection_interval=1)

        print("1. Testing System Metrics Collector...")
        system_metrics = await system_collector.collect_metrics()

        if system_metrics and len(system_metrics) > 0:
            print(f"✅ System collector: {len(system_metrics)} metrics collected")
            for metric in system_metrics[:3]:
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ System collector failed")
            return False

        ApplicationMetricsCollector = collectors_module.ApplicationMetricsCollector
        app_collector = ApplicationMetricsCollector(collection_interval=1)

        print("\n2. Testing Application Metrics Collector...")
        app_metrics = await app_collector.collect_metrics()

        if app_metrics and len(app_metrics) > 0:
            print(f"✅ Application collector: {len(app_metrics)} metrics collected")
            for metric in app_metrics[:3]:
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ Application collector failed")
            return False

        NetworkMetricsCollector = collectors_module.NetworkMetricsCollector
        network_collector = NetworkMetricsCollector(collection_interval=1)

        print("\n3. Testing Network Metrics Collector...")
        network_metrics = await network_collector.collect_metrics()

        if network_metrics and len(network_metrics) > 0:
            print(f"✅ Network collector: {len(network_metrics)} metrics collected")
            for metric in network_metrics[:3]:
                print(f"   - {metric.metric_name}: {metric.value} {metric.unit}")
        else:
            print("❌ Network collector failed")
            return False

        CustomMetricsCollector = collectors_module.CustomMetricsCollector
        custom_collector = CustomMetricsCollector(collection_interval=1)

        print("\n4. Testing Custom Metrics Collector...")
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
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        dashboard_path = "src/services/dashboard_backend.py"
        dashboard_module = load_module_from_file("dashboard_backend", dashboard_path)

        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        DashboardBackend = dashboard_module.DashboardBackend

        monitor = PerformanceMonitor()
        dashboard = DashboardBackend(monitor, host="localhost", port=0)

        print("✅ Dashboard backend created successfully")

        if len(dashboard.api_endpoints) > 0:
            print(f"✅ API endpoints registered: {len(dashboard.api_endpoints)}")
            for endpoint in dashboard.api_endpoints:
                print(f"   - {endpoint.method} {endpoint.path}: {endpoint.description}")
        else:
            print("❌ No API endpoints registered")
            return False

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
