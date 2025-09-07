# Performance optimized version of launch_performance_monitoring.py
# Original file: .\scripts\launchers\launch_performance_monitoring.py

import argparse, asyncio, logging, sys
from pathlib import Path
from launch_performance_core import PerformanceMonitoringLauncher

#!/usr/bin/env python3
"""Orchestrator for the performance monitoring system."""

# Ensure src is on the path for service imports
CURRENT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = CURRENT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


async def main():
    parser = argparse.ArgumentParser(
        description="Performance Monitoring System for Agent_Cellphone_V2_Repository"
    )
    parser.add_argument(
        "action",
        choices=["start", "stop", "restart", "status", "health"],
        help="Action to perform",
    )
    parser.add_argument(
        "--config",
        default="config/system/performance.json",
        help="Configuration file path (default: config/system/performance.json)",
    )
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    launcher = PerformanceMonitoringLauncher(args.config)

    if args.action == "start":
        if not launcher.load_config():
            sys.exit(1)
        if not launcher.setup_performance_monitor():
            sys.exit(1)
        if not launcher.setup_alerting_system():
            sys.exit(1)
        if not launcher.setup_dashboard():
            sys.exit(1)
        if not await launcher.start_system():
            sys.exit(1)
        await launcher.run_main_loop()
    elif args.action == "status":
        print("Performance Monitoring System Status")
        print("=" * 40)
        print("Status: Not implemented for remote status check")
        print("Use the dashboard or health endpoint for live status")
    elif args.action == "health":
        print("Performance Monitoring System Health")
        print("=" * 40)
        print("Health: Not implemented for remote health check")
        print("Use the /api/health endpoint for live health status")
    else:
        print(f"Action '{args.action}' not implemented")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Interrupted by user")
    except Exception as e:
        logging.getLogger(__name__).error("Fatal error: %s", e)
        sys.exit(1)


