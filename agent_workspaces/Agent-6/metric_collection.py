import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import psutil


class MetricCollector:
    """Collects raw system metrics used during optimization."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".MetricCollector")

    def collect_all(self) -> Dict[str, Any]:
        """Collect a snapshot of CPU, memory, disk and network metrics."""
        snapshot = {
            "cpu": self.collect_cpu_metrics(),
            "memory": self.collect_memory_metrics(),
            "disk": self.collect_disk_metrics(),
            "network": self.collect_network_metrics(),
            "timestamp": datetime.now().isoformat(),
        }
        self.logger.debug("Collected metric snapshot: %s", snapshot)
        return snapshot

    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive CPU metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            return {
                "usage_percent": cpu_percent,
                "core_count": cpu_count,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "load_average": self._get_load_average(),
            }
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to collect CPU metrics: %s", exc)
            return {"error": str(exc)}

    def collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive memory metrics."""
        try:
            memory = psutil.virtual_memory()
            return {
                "total_gb": memory.total / (1024 ** 3),
                "available_gb": memory.available / (1024 ** 3),
                "used_percent": memory.percent,
            }
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to collect memory metrics: %s", exc)
            return {"error": str(exc)}

    def collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive disk metrics."""
        try:
            disk = psutil.disk_usage("/")
            io = psutil.disk_io_counters()
            return {
                "total_gb": disk.total / (1024 ** 3),
                "used_gb": disk.used / (1024 ** 3),
                "free_percent": (disk.free / disk.total) * 100,
                "read_bytes": io.read_bytes if io else 0,
                "write_bytes": io.write_bytes if io else 0,
            }
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to collect disk metrics: %s", exc)
            return {"error": str(exc)}

    def collect_network_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive network metrics."""
        try:
            network = psutil.net_io_counters()
            return {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv,
            }
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to collect network metrics: %s", exc)
            return {"error": str(exc)}

    def analyze_performance_patterns(self) -> Dict[str, Any]:
        """Return simple static descriptions of performance patterns."""
        # In the original toolkit this performed complex analysis.  For the
        # refactor we keep a lightweight placeholder that still returns
        # structured information used by the orchestrator.
        return {
            "cpu_patterns": "Variable usage with peaks during operations",
            "memory_patterns": "Consistent usage with gradual growth",
            "disk_patterns": "Burst I/O during file operations",
            "network_patterns": "Low baseline with activity spikes",
        }

    def _get_load_average(self) -> Optional[float]:
        try:
            if hasattr(os, "getloadavg"):
                return os.getloadavg()[0]
        except Exception:  # pragma: no cover - platform dependent
            return None
        return None
