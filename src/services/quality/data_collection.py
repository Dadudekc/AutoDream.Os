"""Quality data collection module."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Dict, List

from .config import DEFAULT_CHECK_INTERVAL

logger = logging.getLogger(__name__)


class QualityMonitor:
    """Collects quality metrics from registered services."""

    def __init__(self, check_interval: float = DEFAULT_CHECK_INTERVAL) -> None:
        self.check_interval = check_interval
        self.monitored_services: Dict[str, Dict[str, Any]] = {}
        self.alert_callbacks: List[Callable] = []
        self._monitoring = False
        self._monitor_thread: threading.Thread | None = None
        self._lock = threading.Lock()
        logger.info("Quality Monitor initialized")

    def add_service_monitoring(self, service_id: str, metrics: List[str], thresholds: Dict[str, Any]) -> bool:
        """Register a service for monitoring."""
        try:
            with self._lock:
                self.monitored_services[service_id] = {
                    "metrics": metrics,
                    "thresholds": thresholds,
                    "last_check": time.time(),
                    "alert_count": 0,
                }
            logger.info("Service %s added to quality monitoring", service_id)
            return True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to add service monitoring for %s: %s", service_id, exc)
            return False

    def remove_service_monitoring(self, service_id: str) -> bool:
        """Stop monitoring the specified service."""
        try:
            with self._lock:
                self.monitored_services.pop(service_id, None)
            logger.info("Service %s removed from quality monitoring", service_id)
            return True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to remove service monitoring for %s: %s", service_id, exc)
            return False

    def add_alert_callback(self, callback: Callable) -> None:
        """Register an alert callback."""
        self.alert_callbacks.append(callback)

    def start_monitoring(self) -> bool:
        """Begin background monitoring."""
        if self._monitoring:
            logger.warning("Quality monitoring already running")
            return False
        try:
            self._monitoring = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            logger.info("Quality monitoring started")
            return True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to start quality monitoring: %s", exc)
            self._monitoring = False
            return False

    def stop_monitoring(self) -> bool:
        """Stop background monitoring."""
        if not self._monitoring:
            logger.warning("Quality monitoring not running")
            return False
        try:
            self._monitoring = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=5.0)
            logger.info("Quality monitoring stopped")
            return True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to stop quality monitoring: %s", exc)
            return False

    def _monitor_loop(self) -> None:
        """Background loop that checks service quality."""
        while self._monitoring:
            try:
                self._check_service_quality()
                time.sleep(self.check_interval)
            except Exception as exc:  # pragma: no cover - defensive
                logger.error("Error in monitoring loop: %s", exc)
                time.sleep(self.check_interval)

    def _check_service_quality(self) -> None:
        """Check quality for all registered services."""
        current_time = time.time()
        with self._lock:
            for service_id, service_info in self.monitored_services.items():
                if current_time - service_info["last_check"] >= self.check_interval:
                    self._evaluate_service_quality(service_id, service_info)
                    service_info["last_check"] = current_time

    def _evaluate_service_quality(self, service_id: str, service_info: Dict[str, Any]) -> None:
        """Evaluate quality for a specific service (placeholder logic)."""
        try:
            logger.debug("Evaluating quality for service %s", service_id)
            # Placeholder for actual quality evaluation logic
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to evaluate quality for %s: %s", service_id, exc)


__all__ = ["QualityMonitor"]
