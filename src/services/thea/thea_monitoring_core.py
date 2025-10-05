#!/usr/bin/env python3
"""
Thea Monitoring Core - Core Monitoring Operations
================================================

Core monitoring operations for Thea autonomous system.
Handles system health collection and performance tracking.

V2 Compliance: ≤400 lines, focused monitoring operations module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Event, Thread

import psutil

from .thea_monitoring_models import PerformanceMetrics, SystemHealth


class TheaMonitoringCore:
    """
    Core monitoring operations for Thea autonomous system.

    Handles system health collection and performance tracking.
    """

    def __init__(self, log_dir: str = "logs/thea_monitoring"):
        """Initialize monitoring core."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(f"{__name__}.TheaMonitoringCore")
        self._setup_logging()

        self.monitoring_active = False
        self.stop_event = Event()
        self.monitoring_thread: Thread | None = None

        self.performance_data: list[PerformanceMetrics] = []
        self.system_health_data: list[SystemHealth] = []

        self.max_data_points = 1000
        self.cleanup_interval = 3600  # 1 hour

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_file = self.log_dir / "thea_monitoring.log"

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def start_monitoring(self) -> bool:
        """Start monitoring system."""
        if self.monitoring_active:
            return False

        self.monitoring_active = True
        self.stop_event.clear()

        self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()

        self.logger.info("Thea monitoring system started")
        return True

    def stop_monitoring(self) -> bool:
        """Stop monitoring system."""
        if not self.monitoring_active:
            return False

        self.monitoring_active = False
        self.stop_event.set()

        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

        self.logger.info("Thea monitoring system stopped")
        return True

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while not self.stop_event.is_set():
            try:
                # Collect system health
                health = self._collect_system_health()
                self.system_health_data.append(health)

                # Check for alerts
                self._check_alerts(health)

                # Cleanup old data
                self._cleanup_old_data()

                # Sleep for monitoring interval
                time.sleep(30)  # 30 seconds

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _collect_system_health(self) -> SystemHealth:
        """Collect current system health metrics."""
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Check network connectivity
            network_connected = self._check_network_connectivity()

            # Check browser status
            browser_running = self._check_browser_status()

            # Check cookie status
            cookies_valid = self._check_cookie_status()

            # Determine overall health
            overall_health = self._determine_overall_health(
                cpu_usage,
                memory.percent,
                disk.percent,
                network_connected,
                browser_running,
                cookies_valid,
            )

            return SystemHealth(
                timestamp=datetime.utcnow().isoformat(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_connected=network_connected,
                browser_running=browser_running,
                cookies_valid=cookies_valid,
                overall_health=overall_health,
            )

        except Exception as e:
            self.logger.error(f"Error collecting system health: {e}")
            return SystemHealth(
                timestamp=datetime.utcnow().isoformat(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_connected=False,
                browser_running=False,
                cookies_valid=False,
                overall_health="error",
            )

    def _check_network_connectivity(self) -> bool:
        """Check network connectivity."""
        try:
            import socket

            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def _check_browser_status(self) -> bool:
        """Check if browser is running."""
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                if "chrome" in proc.info["name"].lower():
                    return True
            return False
        except Exception:
            return False

    def _check_cookie_status(self) -> bool:
        """Check cookie file status."""
        try:
            cookie_file = Path.home() / ".config" / "google-chrome" / "Default" / "Cookies"
            return cookie_file.exists() and cookie_file.stat().st_size > 0
        except Exception:
            return False

    def _determine_overall_health(
        self, cpu: float, memory: float, disk: float, network: bool, browser: bool, cookies: bool
    ) -> str:
        """Determine overall system health."""
        if not network or not browser or not cookies:
            return "critical"
        elif cpu > 90 or memory > 90 or disk > 90:
            return "warning"
        elif cpu > 70 or memory > 70 or disk > 70:
            return "degraded"
        else:
            return "healthy"

    def _check_alerts(self, health: SystemHealth) -> None:
        """Check for alert conditions."""
        alerts = []

        if health.cpu_usage > 90:
            alerts.append(f"High CPU usage: {health.cpu_usage}%")
        if health.memory_usage > 90:
            alerts.append(f"High memory usage: {health.memory_usage}%")
        if health.disk_usage > 90:
            alerts.append(f"High disk usage: {health.disk_usage}%")
        if not health.network_connected:
            alerts.append("Network connectivity lost")
        if not health.browser_running:
            alerts.append("Browser not running")
        if not health.cookies_valid:
            alerts.append("Cookie file invalid")

        if alerts:
            health.alerts = alerts
            for alert in alerts:
                self.logger.warning(f"ALERT: {alert}")

    def _cleanup_old_data(self) -> None:
        """Cleanup old monitoring data."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=24)

            # Cleanup performance data
            self.performance_data = [
                data
                for data in self.performance_data
                if datetime.fromisoformat(data.timestamp) > cutoff_time
            ]

            # Cleanup system health data
            self.system_health_data = [
                data
                for data in self.system_health_data
                if datetime.fromisoformat(data.timestamp) > cutoff_time
            ]

        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {e}")

    def log_operation(
        self,
        operation: str,
        duration: float,
        success: bool,
        response_length: int = 0,
        error_message: str = None,
    ) -> None:
        """Log operation performance."""
        try:
            metrics = PerformanceMetrics(
                timestamp=datetime.utcnow().isoformat(),
                operation=operation,
                duration=duration,
                success=success,
                memory_usage=psutil.virtual_memory().percent,
                cpu_usage=psutil.cpu_percent(),
                response_length=response_length,
                error_message=error_message,
            )

            self.performance_data.append(metrics)

            if success:
                self.logger.info(f"Operation completed: {operation} ({duration:.2f}s)")
            else:
                self.logger.error(f"Operation failed: {operation} - {error_message}")

        except Exception as e:
            self.logger.error(f"Error logging operation: {e}")


__all__ = ["TheaMonitoringCore"]
