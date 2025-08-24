import asyncio
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


def test_dashboard_frontend_standalone():
    """Test dashboard frontend in standalone mode."""
    print("\n🎨 Testing Dashboard Frontend Standalone")
    print("=" * 40)

    try:
        frontend_path = "src/services/dashboard"
        frontend_module = load_module_from_file("dashboard_frontend", frontend_path)

        DashboardFrontend = frontend_module.DashboardFrontend
        DashboardWidget = frontend_module.DashboardWidget
        ChartType = frontend_module.ChartType
        DashboardLayout = frontend_module.DashboardLayout

        frontend = DashboardFrontend("ws://localhost:8080/ws")
        print("✅ Dashboard frontend created")

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

        html = frontend.generate_html()
        if "<!DOCTYPE html>" in html and "CPU Usage" in html and "Memory Usage" in html:
            print("✅ HTML generation working")
            print(f"   - HTML size: {len(html)} characters")
            print(f"   - Contains dashboard title: {'Agent Cellphone V2' in html}")
        else:
            print("❌ HTML generation failed")
            return False

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


async def test_integration_workflow_standalone():
    """Test end-to-end integration workflow."""
    print("\n🔄 Testing Integration Workflow Standalone")
    print("=" * 45)

    try:
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

        PerformanceMonitor = perf_monitor_module.PerformanceMonitor
        SystemMetricsCollector = collectors_module.SystemMetricsCollector
        DashboardBackend = dashboard_module.DashboardBackend
        AlertingSystem = alerting_module.AlertingSystem

        print("✅ All modules loaded successfully")

        monitor = PerformanceMonitor()
        collector = SystemMetricsCollector(collection_interval=1)
        dashboard = DashboardBackend(monitor, host="localhost", port=0)
        alerting = AlertingSystem()

        print("✅ All components initialized")

        monitor.add_collector(collector)
        monitor.alert_callbacks.append(alerting.process_alert)

        print("✅ Components connected")

        await monitor.start()
        print("✅ Monitoring started")

        print("⏳ Collecting metrics for 3 seconds...")
        await asyncio.sleep(3)

        metric_names = monitor.metrics_storage.get_all_metric_names()
        if metric_names:
            print(f"✅ Metrics collected: {len(metric_names)} metric types")
            for metric_name in metric_names[:5]:
                series = monitor.get_metric_series(metric_name)
                if series and series.data_points:
                    latest = series.data_points[-1]
                    print(f"   - {metric_name}: {latest.value} {latest.unit}")
        else:
            print("❌ No metrics collected")
            return False

        test_params = {"metric_name": metric_names[0] if metric_names else "test"}
        response = dashboard.get_metrics_endpoint(test_params)
        if response.get("status") == "success":
            print("✅ Dashboard can access collected metrics")
        else:
            print("❌ Dashboard cannot access metrics")
            return False

        status = monitor.get_system_status()
        print("✅ System status check:")
        print(f"   - Running: {status['running']}")
        print(f"   - Collectors: {status['collectors_count']}")
        print(f"   - Metrics: {len(status['metric_names'])}")

        await monitor.stop()
        print("✅ Monitoring stopped gracefully")

        return True

    except Exception as e:
        print(f"❌ Integration workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False
