import os
import time


def print_startup_summary(launcher):
    """Print startup summary information."""
    uptime = time.time() - launcher.startup_time
    print("\n" + "=" * 60)
    print("🚀 Performance Monitoring System Started")
    print("=" * 60)

    if launcher.performance_monitor:
        print("✅ Performance Monitor: Running")
        print(f"   - Collectors: {len(launcher.performance_monitor.collectors)}")
        print(f"   - Alert Rules: {len(launcher.performance_monitor.alert_rules)}")
        print(
            f"   - Collection Interval: {launcher.performance_monitor.collection_interval}s"
        )

    if launcher.dashboard_backend:
        print("✅ Dashboard Backend: Running")
        print(f"   - Host: {launcher.dashboard_backend.host}")
        print(f"   - Port: {launcher.dashboard_backend.port}")
        print(
            f"   - URL: http://{launcher.dashboard_backend.host}:{launcher.dashboard_backend.port}"
        )

    if launcher.dashboard_frontend:
        print("✅ Dashboard Frontend: Ready")
        print(f"   - Widgets: {len(launcher.dashboard_frontend.widgets)}")
        print(f"   - Theme: {launcher.dashboard_frontend.layout.theme}")
        print(f"   - Auto Refresh: {launcher.dashboard_frontend.layout.auto_refresh}")

    if launcher.alerting_system:
        print("✅ Alerting System: Active")
        print(f"   - Channels: {len(launcher.alerting_system.alert_channels)}")
        print(f"   - Rules: {len(launcher.alerting_system.alert_rules)}")

    print(f"\n📊 System Status:")
    print(f"   - Startup Time: {uptime:.2f}s")
    print(f"   - Configuration: {launcher.config_file}")
    print(f"   - Process ID: {os.getpid()}")

    print("\n💡 Usage:")
    if launcher.dashboard_backend:
        print(
            f"   - Dashboard: http://{launcher.dashboard_backend.host}:{launcher.dashboard_backend.port}"
        )
        print(
            f"   - Health Check: http://{launcher.dashboard_backend.host}:{launcher.dashboard_backend.port}/api/health"
        )
        print(
            f"   - Metrics API: http://{launcher.dashboard_backend.host}:{launcher.dashboard_backend.port}/api/metrics"
        )

    print("   - Press Ctrl+C to stop gracefully")
    print("   - Monitor logs for real-time status")
    print("   - Access dashboard for visual monitoring")
    print("=" * 60 + "\n")


def get_system_status(launcher) -> dict:
    """Get current system status."""
    status = {
        "running": launcher.running,
        "uptime": time.time() - launcher.startup_time,
        "components": {},
    }
    if launcher.performance_monitor:
        status["components"]["performance_monitor"] = launcher.performance_monitor.get_system_status()
    if launcher.dashboard_backend:
        status["components"]["dashboard_backend"] = {
            "running": launcher.dashboard_backend.running,
            "host": launcher.dashboard_backend.host,
            "port": launcher.dashboard_backend.port,
            "websocket_connections": len(
                launcher.dashboard_backend.websocket_handler.connections
            ),
        }
    if launcher.alerting_system:
        status["components"]["alerting_system"] = {
            "channels": len(launcher.alerting_system.alert_channels),
            "rules": len(launcher.alerting_system.alert_rules),
            "active_alerts": len(launcher.alerting_system.active_alerts),
        }
    return status


def get_health_status(launcher) -> dict:
    """Get health check status."""
    health = {
        "status": "healthy" if launcher.running else "unhealthy",
        "timestamp": time.time(),
        "uptime": time.time() - launcher.startup_time,
        "checks": {},
    }
    if launcher.performance_monitor:
        health["checks"]["performance_monitor"] = {
            "status": "healthy" if launcher.performance_monitor.running else "unhealthy",
            "collectors": len(launcher.performance_monitor.collectors),
            "metrics_count": len(
                launcher.performance_monitor.metrics_storage.get_all_metric_names()
            ),
        }
    if launcher.dashboard_backend:
        health["checks"]["dashboard_backend"] = {
            "status": "healthy" if launcher.dashboard_backend.running else "unhealthy",
            "port": launcher.dashboard_backend.port,
            "connections": len(
                launcher.dashboard_backend.websocket_handler.connections
            ),
        }
    if launcher.alerting_system:
        health["checks"]["alerting_system"] = {
            "status": "healthy",
            "channels": len(launcher.alerting_system.alert_channels),
            "active_alerts": len(launcher.alerting_system.active_alerts),
        }
    return health
