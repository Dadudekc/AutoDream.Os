#!/usr/bin/env python3
"""
Real-Time System Health Monitor
===============================

V2 Compliant: ≤400 lines, provides real-time system health
monitoring and performance tracking for autonomous development.

This module monitors system health, performance metrics,
and provides proactive issue detection and reporting.

🐝 WE ARE SWARM - Real Initiative Discovery Protocol
"""

import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemHealthMonitor:
    """Real-time system health monitoring."""

    def __init__(self, project_root: str = "."):
        """Initialize system health monitor."""
        self.project_root = Path(project_root)
        self.monitoring_dir = self.project_root / "monitoring"
        self.monitoring_dir.mkdir(exist_ok=True)

        # Health thresholds
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "file_count": 10000,
            "response_time": 5.0
        }

        # Monitoring data
        self.health_data = []
        self.alerts = []
        self.monitoring_active = False

        # Performance metrics
        self.metrics = {
            "cpu_usage": [],
            "memory_usage": [],
            "disk_usage": [],
            "file_count": [],
            "response_time": []
        }

    def start_monitoring(self, interval: int = 30) -> Dict[str, Any]:
        """Start real-time system health monitoring."""
        logger.info("Starting real-time system health monitoring")

        if self.monitoring_active:
            return {
                "status": "ALREADY_ACTIVE",
                "message": "Monitoring already running"
            }

        self.monitoring_active = True

        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,, daemon=True),
            daemon=True
        )
        monitor_thread.start()

        return {
            "status": "STARTED",
            "interval": interval,
            "monitoring_active": self.monitoring_active
        }

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop system health monitoring."""
        logger.info("Stopping system health monitoring")

        self.monitoring_active = False

        return {
            "status": "STOPPED",
            "monitoring_active": self.monitoring_active
        }

    def get_current_health(self) -> Dict[str, Any]:
        """Get current system health status."""
        logger.info("Getting current system health")

        health_status = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": self._get_cpu_usage(),
            "memory_usage": self._get_memory_usage(),
            "disk_usage": self._get_disk_usage(),
            "file_count": self._get_file_count(),
            "response_time": self._get_response_time(),
            "health_score": 0.0,
            "alerts": []
        }

        # Calculate health score
        health_status["health_score"] = self._calculate_health_score(health_status)

        # Check for alerts
        health_status["alerts"] = self._check_health_alerts(health_status)

        return health_status

    def get_health_history(self, hours: int = 24) -> Dict[str, Any]:
        """Get system health history."""
        logger.info(f"Getting health history for last {hours} hours")

        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Filter recent data
        recent_data = [
            data for data in self.health_data
            if datetime.fromisoformat(data["timestamp"]) > cutoff_time
        ]

        return {
            "period_hours": hours,
            "data_points": len(recent_data),
            "health_data": recent_data,
            "average_health_score": self._calculate_average_health_score(recent_data)
        }

    def _monitoring_loop(self, interval: int):
        """Main monitoring loop."""
        logger.info(f"Monitoring loop started with {interval}s interval")

        while self.monitoring_active:
            try:
                # Collect health data
                health_data = self.get_current_health()

                # Store data
                self.health_data.append(health_data)

                # Keep only last 1000 data points
                if len(self.health_data) > 1000:
                    self.health_data = self.health_data[-1000:]

                # Update metrics
                self._update_metrics(health_data)

                # Check for alerts
                if health_data["alerts"]:
                    self._handle_alerts(health_data["alerts"])

                # Save data
                self._save_health_data()

                # Wait for next interval
                time.sleep(interval)

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(interval)

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            logger.error(f"CPU usage error: {e}")
            return 0.0

    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage."""
        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception as e:
            logger.error(f"Memory usage error: {e}")
            return 0.0

    def _get_disk_usage(self) -> float:
        """Get current disk usage percentage."""
        try:
            disk = psutil.disk_usage(self.project_root)
            return (disk.used / disk.total) * 100
        except Exception as e:
            logger.error(f"Disk usage error: {e}")
            return 0.0

    def _get_file_count(self) -> int:
        """Get current project file count."""
        try:
            file_count = 0
            for root, dirs, files in os.walk(self.project_root):
                file_count += len(files)
            return file_count
        except Exception as e:
            logger.error(f"File count error: {e}")
            return 0

    def _get_response_time(self) -> float:
        """Get system response time."""
        try:
            start_time = time.time()
            # Simulate system operation
            self._get_cpu_usage()
            end_time = time.time()
            return end_time - start_time
        except Exception as e:
            logger.error(f"Response time error: {e}")
            return 0.0

    def _calculate_health_score(self, health_data: Dict[str, Any]) -> float:
        """Calculate overall health score (0-100)."""
        try:
            # Normalize metrics (lower is better for most)
            cpu_score = max(0, 100 - health_data["cpu_usage"])
            memory_score = max(0, 100 - health_data["memory_usage"])
            disk_score = max(0, 100 - health_data["disk_usage"])

            # File count score (penalty for excessive files)
            file_count = health_data["file_count"]
            if file_count > self.thresholds["file_count"]:
                file_score = max(0, 100 - ((file_count - self.thresholds["file_count"]) / 100))
            else:
                file_score = 100

            # Response time score
            response_time = health_data["response_time"]
            if response_time > self.thresholds["response_time"]:
                response_score = max(0, 100 - (response_time * 20))
            else:
                response_score = 100

            # Weighted average
            health_score = (
                cpu_score * 0.25 +
                memory_score * 0.25 +
                disk_score * 0.20 +
                file_score * 0.15 +
                response_score * 0.15
            )

            return round(health_score, 2)

        except Exception as e:
            logger.error(f"Health score calculation error: {e}")
            return 0.0

    def _check_health_alerts(self, health_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for health alerts."""
        alerts = []

        # CPU alert
        if health_data["cpu_usage"] > self.thresholds["cpu_usage"]:
            alerts.append({
                "type": "CPU_HIGH",
                "severity": "WARNING",
                "value": health_data["cpu_usage"],
                "threshold": self.thresholds["cpu_usage"]
            })

        # Memory alert
        if health_data["memory_usage"] > self.thresholds["memory_usage"]:
            alerts.append({
                "type": "MEMORY_HIGH",
                "severity": "WARNING",
                "value": health_data["memory_usage"],
                "threshold": self.thresholds["memory_usage"]
            })

        # Disk alert
        if health_data["disk_usage"] > self.thresholds["disk_usage"]:
            alerts.append({
                "type": "DISK_FULL",
                "severity": "CRITICAL",
                "value": health_data["disk_usage"],
                "threshold": self.thresholds["disk_usage"]
            })

        # File count alert
        if health_data["file_count"] > self.thresholds["file_count"]:
            alerts.append({
                "type": "FILE_COUNT_HIGH",
                "severity": "WARNING",
                "value": health_data["file_count"],
                "threshold": self.thresholds["file_count"]
            })

        # Response time alert
        if health_data["response_time"] > self.thresholds["response_time"]:
            alerts.append({
                "type": "RESPONSE_SLOW",
                "severity": "WARNING",
                "value": health_data["response_time"],
                "threshold": self.thresholds["response_time"]
            })

        return alerts

    def _update_metrics(self, health_data: Dict[str, Any]):
        """Update performance metrics."""
        for metric, value in health_data.items():
            if metric in self.metrics and isinstance(value, (int, float)):
                self.metrics[metric].append(value)

                # Keep only last 100 values
                if len(self.metrics[metric]) > 100:
                    self.metrics[metric] = self.metrics[metric][-100:]

    def _handle_alerts(self, alerts: List[Dict[str, Any]]):
        """Handle health alerts."""
        for alert in alerts:
            self.alerts.append({
                "timestamp": datetime.now().isoformat(),
                "alert": alert
            })

            logger.warning(f"Health Alert: {alert['type']} - {alert['value']}")

    def _calculate_average_health_score(self, data: List[Dict[str, Any]]) -> float:
        """Calculate average health score from data."""
        if not data:
            return 0.0

        scores = [item["health_score"] for item in data if "health_score" in item]
        return sum(scores) / len(scores) if scores else 0.0

    def _save_health_data(self):
        """Save health data to file."""
        try:
            data_file = self.monitoring_dir / "health_data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "health_data": self.health_data[-100:],  # Last 100 points
                    "alerts": self.alerts[-50:],  # Last 50 alerts
                    "metrics": self.metrics
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving health data: {e}")

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring status."""
        return {
            "monitoring_active": self.monitoring_active,
            "data_points": len(self.health_data),
            "alerts_count": len(self.alerts),
            "thresholds": self.thresholds,
            "current_health": self.get_current_health() if self.health_data else None
        }

def main():
    """Main execution function."""
    monitor = SystemHealthMonitor()

    # Start monitoring
    start_result = monitor.start_monitoring(interval=30)
    print(f"Monitoring started: {start_result}")

    # Get current health
    health = monitor.get_current_health()
    print(f"Current health score: {health['health_score']}")
    print(f"Alerts: {len(health['alerts'])}")

    # Get status
    status = monitor.get_monitoring_status()
    print(f"Monitoring status: {status}")

if __name__ == "__main__":
    main()
