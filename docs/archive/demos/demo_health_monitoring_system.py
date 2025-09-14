#!/usr/bin/env python3
"""
🐝 DEMO: COMPREHENSIVE SYSTEM HEALTH MONITORING SYSTEM
Complete Health Monitoring Platform Demonstration

This script demonstrates the complete health monitoring system including:
- Service availability monitoring
- Performance metrics collection
- Error rate tracking
- Resource usage monitoring
- Automated health checks
- Alerting system
- Web dashboard
- Messaging integration

Run with:
    python demo_health_monitoring_system.py --start --dashboard
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def demo_health_monitoring():
    """Demonstrate the complete health monitoring system."""
    print("🐝 COMPREHENSIVE SYSTEM HEALTH MONITORING DEMO")
    print("=" * 60)

    try:
        # Import the complete system
        from core.health.monitoring.health_monitoring_system import HealthMonitoringSystem

        print("🚀 Initializing Health Monitoring System...")
        monitor = HealthMonitoringSystem()

        print("✅ System initialized successfully")
        print()

        # Show system status
        status = monitor.get_system_status()
        print("📊 INITIAL SYSTEM STATUS:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        print()

        # Start monitoring
        print("🔄 Starting health monitoring...")
        monitor.start()
        print("✅ Monitoring started")
        print()

        # Let it collect some data
        print("📈 Collecting health metrics for 15 seconds...")
        time.sleep(15)

        # Get and display health snapshot
        print("🏥 HEALTH SNAPSHOT:")
        snapshot = monitor.get_health_snapshot()
        if snapshot:
            print(f"  Overall Status: {snapshot.overall_status.value.upper()}")
            print(f"  Services: {len(snapshot.services)}")
            print(f"  Metrics: {len(snapshot.metrics)}")
            print(f"  Active Alerts: {len(snapshot.alerts)}")
            print(f"  Uptime: {snapshot.uptime_seconds:.1f} seconds")
        print()

        # Show component status
        print("🔧 COMPONENT STATUS EXAMPLES:")
        for component in ["cpu", "memory", "messaging"]:
            comp_status = monitor.get_component_status(component)
            if "error" not in comp_status:
                print(
                    f"  {component.upper()}: {comp_status.get('health_status', 'unknown').upper()}"
                )
                if comp_status.get("metrics"):
                    for name, metric in list(comp_status["metrics"].items())[:2]:
                        print(f"    {name}: {metric['value']:.1f}{metric['unit']}")
        print()

        # Show alerting system status
        if hasattr(monitor, "alerting_system") and monitor.alerting_system:
            alert_stats = monitor.alerting_system.get_alert_statistics()
            print("🚨 ALERTING SYSTEM:")
            print(f"  Active Alerts: {alert_stats['active_alerts']}")
            print(f"  Alerts (24h): {alert_stats['alerts_last_24h']}")
            print(f"  Critical Alerts: {alert_stats['critical_alerts_active']}")
            print()

        # Export data
        print("💾 EXPORTING SYSTEM DATA...")
        exports = monitor.export_system_data()
        for data_type, filepath in exports.items():
            print(f"✅ {data_type}: {filepath}")
        print()

        # Start dashboard (brief demo)
        print("🌐 STARTING WEB DASHBOARD (brief demo)...")
        if monitor.start_dashboard("127.0.0.1", 8080):
            print("✅ Dashboard started at http://127.0.0.1:8080")
            print("📝 Dashboard will be accessible in a web browser")
            print("🔍 Check system health, metrics, and alerts in real-time")
            time.sleep(5)  # Let dashboard initialize
            monitor.stop_dashboard()
            print("🛑 Dashboard stopped")
        else:
            print("⚠️ Dashboard not available (Flask may not be installed)")
        print()

        # Show final status
        final_status = monitor.get_system_status()
        print("📊 FINAL SYSTEM STATUS:")
        for key, value in final_status.items():
            print(f"  {key}: {value}")
        print()

        # Cleanup
        print("🧹 Cleaning up...")
        monitor.stop()
        print("✅ Demo completed successfully!")

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install flask requests psutil")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


def demo_quick_start():
    """Quick start demonstration."""
    print("⚡ QUICK START DEMO")
    print("=" * 30)

    try:
        from core.health.monitoring.health_monitoring_system import HealthMonitoringSystem

        # Initialize
        monitor = HealthMonitoringSystem()

        # Start monitoring
        monitor.start()

        # Wait for some data
        print("📊 Monitoring system for 10 seconds...")
        time.sleep(10)

        # Show status
        snapshot = monitor.get_health_snapshot()
        if snapshot:
            print(f"✅ System Health: {snapshot.overall_status.value.upper()}")
            print(f"📈 Metrics Collected: {len(snapshot.metrics)}")
            print(f"🚨 Active Alerts: {len(snapshot.alerts)}")

        # Cleanup
        monitor.stop()

    except Exception as e:
        print(f"❌ Quick demo failed: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Health Monitoring System Demo")
    parser.add_argument("--quick", action="store_true", help="Run quick demo only")
    parser.add_argument("--full", action="store_true", help="Run full comprehensive demo")

    args = parser.parse_args()

    if args.quick:
        demo_quick_start()
    elif args.full:
        demo_health_monitoring()
    else:
        print("🐝 Health Monitoring System Demo")
        print("Usage:")
        print("  python demo_health_monitoring_system.py --quick    # Quick 10-second demo")
        print("  python demo_health_monitoring_system.py --full     # Full comprehensive demo")
        print()
        print("Features Demonstrated:")
        print("✅ Service availability monitoring")
        print("✅ Performance metrics collection")
        print("✅ Error rate and failure tracking")
        print("✅ Resource usage monitoring")
        print("✅ Automated health checks")
        print("✅ Multi-channel alerting system")
        print("✅ Real-time web dashboard")
        print("✅ System health snapshots")
        print("✅ Data export capabilities")
