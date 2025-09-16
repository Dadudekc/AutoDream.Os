#!/usr/bin/env python3
"""
Performance Metrics Collector - V2 Compliant Module
==================================================

Extracted metrics collection functionality for V2 compliance.
Reduces performance_orchestrator.py from 304 to ~250 lines.

Author: Agent-2 - Infrastructure Specialist (Phase 2 V2 Compliance)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List

from .models.performance_models import DashboardMetric

logger = logging.getLogger(__name__)


class PerformanceMetricsCollector:
    """Dedicated metrics collection system for V2 compliance."""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.collection_interval = 30

    def start_collection_loop(self) -> None:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.performance.performance_metrics_collector import Performance_Metrics_Collector

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Performance_Metrics_Collector(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

        """Start the metrics collection loop."""
        while self.orchestrator._running:
            try:
                self._collect_system_metrics()
                self.orchestrator._check_alerts()
                self._cleanup_old_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(30)

    def _collect_system_metrics(self) -> None:
        """Collect system performance metrics."""
        try:
            import psutil

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.orchestrator._add_metric("system.cpu.usage", cpu_percent, "%", "system")

            # Memory metrics
            memory = psutil.virtual_memory()
            self.orchestrator._add_metric("system.memory.usage", memory.percent, "%", "system")
            self.orchestrator._add_metric("system.memory.used", memory.used / (1024**3), "GB", "system")

            # Disk metrics
            disk = psutil.disk_usage('/')
            self.orchestrator._add_metric("system.disk.usage", disk.percent, "%", "system")

            logger.debug("System metrics collected")

        except ImportError:
            logger.warning("psutil not available, system metrics collection disabled")
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    def _cleanup_old_metrics(self) -> None:
        """Clean up old metrics to prevent memory bloat."""
        cutoff_time = datetime.now().timestamp() - self.orchestrator.retention_period

        with self.orchestrator._lock:
            for metric_name in list(self.orchestrator.metrics_buffer.keys()):
                self.orchestrator.metrics_buffer[metric_name] = [
                    metric for metric in self.orchestrator.metrics_buffer[metric_name]
                    if metric.timestamp.timestamp() > cutoff_time
                ]

                # Remove empty metric buffers
                if not self.orchestrator.metrics_buffer[metric_name]:
                    del self.orchestrator.metrics_buffer[metric_name]

        logger.debug("Old metrics cleaned up")
