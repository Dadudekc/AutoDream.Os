#!/usr/bin/env python3
"""
System Utils Coordinator - Unified System Utilities Interface

This module coordinates the focused system utility modules.
Follows Single Responsibility Principle - only coordinates other modules.
Architecture: Single Responsibility Principle - coordination only
LOC: 60 lines (under 200 limit)
"""

from typing import Dict, Any, List, Optional
from .system_info import SystemInfo
from src.core.performance.monitoring.performance_monitor import PerformanceMonitor
from .logging_setup import LoggingSetup
from .dependency_checker import DependencyChecker


class SystemUtilsCoordinator:
    """Coordinates all system utility modules"""

    def __init__(self):
        self.system_info = SystemInfo()
        self.performance_monitor = PerformanceMonitor()
        self.logging_setup = LoggingSetup()
        self.dependency_checker = DependencyChecker()

    def get_comprehensive_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status from all modules"""
        try:
            status = {
                "system_info": SystemInfo.get_system_info(),
                "performance": self.performance_monitor.get_performance_metrics(),
                "dependencies": self.dependency_checker.check_dependencies(),
                "environment_ready": self.dependency_checker.validate_environment()[
                    "environment_ready"
                ],
            }
            return status
        except Exception as e:
            return {"error": str(e)}

    def setup_system_logging(
        self, log_level: str = "INFO", log_file: Optional[str] = None
    ) -> bool:
        """Setup system logging"""
        return self.logging_setup.setup_logging(log_level, log_file)

    def get_performance_summary(self, time_window_minutes: int = 5) -> Dict[str, Any]:
        """Get performance summary over time window"""
        return self.performance_monitor.get_average_metrics(time_window_minutes)

    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        try:
            # Check dependencies
            deps = self.dependency_checker.check_dependencies()
            critical_deps = ["psutil", "yaml"]
            missing_critical = [
                dep for dep in critical_deps if not deps.get(dep, False)
            ]

            # Get performance metrics
            perf = self.performance_monitor.get_performance_metrics()

            # Determine health status
            health_status = "healthy"
            if missing_critical:
                health_status = "critical"
            elif perf.get("memory", {}).get("percent", 0) > 90:
                health_status = "warning"

            return {
                "status": health_status,
                "missing_critical_deps": missing_critical,
                "memory_usage_percent": perf.get("memory", {}).get("percent", 0),
                "cpu_usage_percent": perf.get("cpu", {}).get("cpu_percent", 0),
                "dependencies_ok": len(missing_critical) == 0,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}


def run_smoke_test():
    """Run basic functionality test for SystemUtilsCoordinator"""
    print("🧪 Running SystemUtilsCoordinator Smoke Test...")

    try:
        coordinator = SystemUtilsCoordinator()

        # Test comprehensive status
        status = coordinator.get_comprehensive_system_status()
        assert "system_info" in status

        # Test system health
        health = coordinator.check_system_health()
        assert "status" in health

        # Test logging setup
        success = coordinator.setup_system_logging("INFO")
        assert success

        print("✅ SystemUtilsCoordinator Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ SystemUtilsCoordinator Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for SystemUtilsCoordinator testing"""
    import argparse

    parser = argparse.ArgumentParser(description="System Utils Coordinator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--status", action="store_true", help="Get comprehensive system status"
    )
    parser.add_argument("--health", action="store_true", help="Check system health")
    parser.add_argument(
        "--performance", type=int, default=5, help="Get performance summary (minutes)"
    )
    parser.add_argument("--setup-logging", help="Setup logging with level")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    coordinator = SystemUtilsCoordinator()

    if args.status:
        status = coordinator.get_comprehensive_system_status()
        print("System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    elif args.health:
        health = coordinator.check_system_health()
        print("System Health:")
        for key, value in health.items():
            print(f"  {key}: {value}")
    elif args.performance:
        summary = coordinator.get_performance_summary(args.performance)
        print(f"Performance Summary (last {args.performance} minutes):")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    elif args.setup_logging:
        success = coordinator.setup_system_logging(args.setup_logging)
        print(f"Logging setup: {'✅ Success' if success else '❌ Failed'}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
