#!/usr/bin/env python3
"""
Watchdog Integration Script
==========================

Real-time file monitoring and automated metric refresh integration.
Monitors documentation files and triggers metric updates automatically.

Author: Agent-7 (Web Development Expert / Implementation Specialist)
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import time
from datetime import datetime
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️ Watchdog not available. Install with: pip install watchdog")

from .metric_refresh_system import MetricRefreshSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricRefreshHandler(FileSystemEventHandler):
    """File system event handler for metric refresh triggers."""

    def __init__(self, refresh_system: MetricRefreshSystem):
        self.refresh_system = refresh_system
        self.triggered_files: set[str] = set()
        self.last_trigger = datetime.now()
        logger.info("MetricRefreshHandler initialized")

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process relevant files
        if self._should_trigger_refresh(file_path):
            self._trigger_metric_refresh(file_path)

    def _should_trigger_refresh(self, file_path: Path) -> bool:
        """Determine if file change should trigger metric refresh."""
        relevant_extensions = {".md", ".json", ".py", ".yaml", ".yml"}
        relevant_names = {
            "AGENTS.md",
            "project_analysis.json",
            "quality_gates.py",
            "agent_workspaces",
            "config",
            "docs",
        }

        # Check file extension
        if file_path.suffix.lower() in relevant_extensions:
            return True

        # Check file/directory names
        for name in relevant_names:
            if name in str(file_path):
                return True

        return False

    def _trigger_metric_refresh(self, file_path: Path):
        """Trigger metric refresh for file change."""
        try:
            # Prevent too frequent refreshes (debounce)
            now = datetime.now()
            if (now - self.last_trigger).seconds < 5:
                return

            self.triggered_files.add(str(file_path))
            self.last_trigger = now

            logger.info(f"File change detected: {file_path.name}")
            logger.info("Triggering metric refresh...")

            # Trigger metric refresh
            results = self.refresh_system.refresh_all_metrics()

            if results["success_count"] > 0:
                logger.info("✅ Metric refresh triggered successfully")
            else:
                logger.warning(f"⚠️ Metric refresh had issues: {results['error_count']} errors")

        except Exception as e:
            logger.error(f"Error triggering metric refresh: {e}")


class WatchdogIntegration:
    """Watchdog integration for real-time metric refresh."""

    def __init__(self):
        self.refresh_system = MetricRefreshSystem()
        self.observer = None
        self.is_running = False
        self.watched_directories = [
            "agent_workspaces",
            "config",
            "docs",
            "src",
            "tools",
        ]
        logger.info("WatchdogIntegration initialized")

    def start_monitoring(self) -> dict[str, str]:
        """Start file system monitoring."""
        if not WATCHDOG_AVAILABLE:
            return {
                "status": "error",
                "message": "Watchdog not available. Install with: pip install watchdog",
            }

        try:
            if self.is_running:
                return {"status": "warning", "message": "Monitoring already running"}

            self.observer = Observer()
            handler = MetricRefreshHandler(self.refresh_system)

            # Add watches for relevant directories
            project_root = Path(__file__).parent.parent.parent
            for directory in self.watched_directories:
                watch_path = project_root / directory
                if watch_path.exists():
                    self.observer.schedule(handler, str(watch_path), recursive=True)
                    logger.info(f"Watching directory: {directory}")

            self.observer.start()
            self.is_running = True

            logger.info("File system monitoring started")
            return {
                "status": "success",
                "message": "Monitoring started successfully",
                "watched_directories": str(self.watched_directories),
            }

        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            return {"status": "error", "message": f"Failed to start monitoring: {e}"}

    def stop_monitoring(self) -> dict[str, str]:
        """Stop file system monitoring."""
        try:
            if not self.is_running or not self.observer:
                return {"status": "warning", "message": "Monitoring not running"}

            self.observer.stop()
            self.observer.join()
            self.is_running = False

            logger.info("File system monitoring stopped")
            return {"status": "success", "message": "Monitoring stopped successfully"}

        except Exception as e:
            logger.error(f"Error stopping monitoring: {e}")
            return {"status": "error", "message": f"Failed to stop monitoring: {e}"}

    def get_status(self) -> dict[str, any]:
        """Get current monitoring status."""
        return {
            "is_running": self.is_running,
            "watched_directories": self.watched_directories,
            "watchdog_available": WATCHDOG_AVAILABLE,
            "last_refresh": self.refresh_system.last_refresh.isoformat(),
        }

    def run_continuous_monitoring(self, duration_seconds: int = 300):
        """Run continuous monitoring for specified duration."""
        logger.info(f"Starting continuous monitoring for {duration_seconds} seconds")

        start_result = self.start_monitoring()
        if start_result["status"] != "success":
            logger.error(f"Failed to start monitoring: {start_result['message']}")
            return start_result

        try:
            # Run for specified duration
            time.sleep(duration_seconds)

            # Stop monitoring
            stop_result = self.stop_monitoring()
            logger.info(f"Continuous monitoring completed: {stop_result['message']}")

            return {
                "status": "success",
                "message": f"Monitoring completed for {duration_seconds} seconds",
                "start_result": start_result,
                "stop_result": stop_result,
            }

        except KeyboardInterrupt:
            logger.info("Monitoring interrupted by user")
            self.stop_monitoring()
            return {"status": "interrupted", "message": "Monitoring interrupted by user"}
        except Exception as e:
            logger.error(f"Error during continuous monitoring: {e}")
            self.stop_monitoring()
            return {"status": "error", "message": f"Monitoring error: {e}"}


def main():
    """Main function for watchdog integration."""
    print("👁️ Watchdog Integration for Metric Refresh")
    print("=" * 50)

    if not WATCHDOG_AVAILABLE:
        print("❌ Watchdog not available")
        print("Install with: pip install watchdog")
        return

    integration = WatchdogIntegration()

    # Show status
    status = integration.get_status()
    print(f"📊 Status: {'Running' if status['is_running'] else 'Stopped'}")
    print(f"📁 Watched directories: {len(status['watched_directories'])}")
    print(f"🔄 Last refresh: {status['last_refresh']}")

    # Start monitoring
    print("\n🚀 Starting monitoring...")
    start_result = integration.start_monitoring()
    print(f"Result: {start_result['message']}")

    if start_result["status"] == "success":
        print("✅ Monitoring active. Press Ctrl+C to stop.")
        try:
            # Run for 60 seconds as demo
            integration.run_continuous_monitoring(60)
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitoring...")
            integration.stop_monitoring()


if __name__ == "__main__":
    main()
