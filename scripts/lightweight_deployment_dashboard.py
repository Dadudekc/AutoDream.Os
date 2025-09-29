#!/usr/bin/env python3
"""
Lightweight Deployment Dashboard
================================

Minimal overhead dashboard for monitoring deployed components.
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.monitoring.memory_optimized_monitor import MemoryOptimizedMonitor
from tools.workflow.simple_manager import SimpleWorkflowManager


class LightweightDashboard:
    """Lightweight dashboard with minimal overhead."""

    def __init__(self):
        self.project_root = project_root
        self.components = {}
        self.monitoring_active = False
        self.start_time = time.time()

    def initialize_components(self):
        """Initialize lightweight components only."""
        try:
            # Initialize only essential components
            self.components["simple_workflow_manager"] = SimpleWorkflowManager()
            self.components["lightweight_monitor"] = MemoryOptimizedMonitor(
                self.project_root, max_history=50
            )

            print("Lightweight components initialized successfully!")
            return True

        except Exception as e:
            print(f"Component initialization failed: {e}")
            return False

    def test_component_functionality(self) -> dict[str, bool]:
        """Test functionality with minimal overhead."""
        results = {}

        try:
            # Test simple workflow manager
            manager = self.components["simple_workflow_manager"]
            workflows = manager.list_workflows()
            results["simple_workflow_manager"] = True
            print("Simple Workflow Manager: Functional")

        except Exception as e:
            results["simple_workflow_manager"] = False
            print(f"Simple Workflow Manager: Failed - {e}")

        try:
            # Test lightweight monitor
            monitor = self.components["lightweight_monitor"]
            status = monitor.get_current_status()
            results["lightweight_monitor"] = True
            print("Lightweight Monitor: Functional")

        except Exception as e:
            results["lightweight_monitor"] = False
            print(f"Lightweight Monitor: Failed - {e}")

        return results

    def get_deployment_status(self) -> dict[str, Any]:
        """Get deployment status with minimal processing."""
        status = {
            "deployment_time": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "components": {},
            "overall_status": "healthy",
        }

        # Check component status with minimal overhead
        for name, component in self.components.items():
            try:
                if hasattr(component, "get_current_status"):
                    component_status = component.get_current_status()
                else:
                    component_status = {"status": "initialized"}

                status["components"][name] = {"status": "healthy", "details": component_status}

            except Exception as e:
                status["components"][name] = {"status": "error", "error": str(e)}
                status["overall_status"] = "degraded"

        return status

    def display_dashboard(self):
        """Display lightweight dashboard."""
        print("\n" + "=" * 60)
        print("LIGHTWEIGHT DEPLOYMENT DASHBOARD")
        print("=" * 60)

        # Component status
        print("\nCOMPONENT STATUS:")
        print("-" * 30)

        status = self.get_deployment_status()
        for name, component_status in status["components"].items():
            status_icon = "OK" if component_status["status"] == "healthy" else "ERROR"
            print(
                f"{status_icon} {name.replace('_', ' ').title()}: {component_status['status'].upper()}"
            )

        # Overall status
        overall_icon = "OK" if status["overall_status"] == "healthy" else "WARNING"
        print(f"\n{overall_icon} Overall Status: {status['overall_status'].upper()}")

        # Basic metrics
        print("\nBASIC METRICS:")
        print("-" * 30)

        try:
            monitor = self.components["lightweight_monitor"]
            memory_usage = monitor.get_memory_usage()

            print(f"Process Memory: {memory_usage['process_memory_mb']:.1f}MB")
            print(f"History Objects: {memory_usage['history_objects']}")
            print(f"Estimated Memory: {memory_usage['total_estimated_memory_kb']:.1f}KB")

        except Exception as e:
            print(f"Metrics unavailable: {e}")

        # Monitoring status
        print("\nMONITORING STATUS:")
        print("-" * 30)

        try:
            monitor = self.components["lightweight_monitor"]
            status_info = monitor.get_current_status()

            print(f"Monitoring Active: {status_info['monitoring_active']}")
            print(f"Uptime: {status_info['uptime_seconds']:.1f} seconds")
            print(f"Total Requests: {status_info['total_requests']}")
            print(f"Error Rate: {status_info['error_rate']:.1%}")

        except Exception as e:
            print(f"Monitoring status unavailable: {e}")

        print("\n" + "=" * 60)

    async def start_monitoring(self):
        """Start lightweight monitoring."""
        try:
            monitor = self.components["lightweight_monitor"]
            await monitor.start_monitoring(interval=120)  # 2-minute intervals
            self.monitoring_active = True
            print("Lightweight monitoring started (2-minute intervals)")
        except Exception as e:
            print(f"Failed to start monitoring: {e}")

    async def stop_monitoring(self):
        """Stop lightweight monitoring."""
        try:
            monitor = self.components["lightweight_monitor"]
            await monitor.stop_monitoring()
            self.monitoring_active = False
            print("Lightweight monitoring stopped")
        except Exception as e:
            print(f"Failed to stop monitoring: {e}")

    def save_lightweight_report(self) -> bool:
        """Save lightweight report."""
        try:
            report = {
                "report_time": datetime.now().isoformat(),
                "deployment_status": self.get_deployment_status(),
                "component_tests": self.test_component_functionality(),
                "monitoring_active": self.monitoring_active,
                "uptime_seconds": time.time() - self.start_time,
            }

            report_path = self.project_root / "lightweight_dashboard_report.json"
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)

            print(f"Lightweight report saved: {report_path}")
            return True

        except Exception as e:
            print(f"Failed to save report: {e}")
            return False


async def main():
    """Main lightweight dashboard function."""
    dashboard = LightweightDashboard()

    print("Initializing Lightweight Deployment Dashboard...")

    # Initialize components
    if not dashboard.initialize_components():
        print("Dashboard initialization failed")
        return 1

    # Test component functionality
    print("\nTesting Component Functionality...")
    test_results = dashboard.test_component_functionality()

    # Display dashboard
    dashboard.display_dashboard()

    # Start monitoring
    print("\nStarting Lightweight Monitoring...")
    await dashboard.start_monitoring()

    # Save report
    dashboard.save_lightweight_report()

    print("\nLightweight Deployment Dashboard Ready!")
    print("Press Ctrl+C to stop monitoring and exit")

    try:
        # Keep monitoring running with longer intervals
        while True:
            await asyncio.sleep(120)  # Update every 2 minutes
            dashboard.display_dashboard()

    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        await dashboard.stop_monitoring()
        print("Dashboard stopped successfully")

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
