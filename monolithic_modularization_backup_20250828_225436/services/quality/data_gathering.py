"""Data gathering utilities for the quality monitoring system."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Dict, Optional

from .analysis import QualityAnalyzer
from .config import DEFAULT_CHECK_INTERVAL

logger = logging.getLogger(__name__)

MetricsProvider = Callable[[], Dict[str, Any]]


class QualityMonitor:
    """Collect metrics and delegate analysis to :class:`QualityAnalyzer`."""

    def __init__(
        self,
        check_interval: float = DEFAULT_CHECK_INTERVAL,
        analyzer: Optional[QualityAnalyzer] = None,
    ) -> None:
        self.check_interval = check_interval
        self.analyzer = analyzer or QualityAnalyzer()
        self.monitored_services: Dict[str, Dict[str, Any]] = {}
        self._monitoring = False
        self._monitor_thread: threading.Thread | None = None
        self._lock = threading.Lock()
        logger.info("Quality Monitor initialized")

    def add_service_monitoring(
        self,
        service_id: str,
        metrics_provider: MetricsProvider,
        thresholds: Dict[str, Any],
    ) -> bool:
        """Register a service for monitoring."""
        try:
            with self._lock:
                self.monitored_services[service_id] = {
                    "provider": metrics_provider,
                    "thresholds": thresholds,
                    "last_check": 0.0,
                }
            logger.info("Service %s added to quality monitoring", service_id)
            return True
        except Exception as exc:
            logger.error(
                "Failed to add service monitoring for %s: %s", service_id, exc
            )
            return False

    def remove_service_monitoring(self, service_id: str) -> bool:
        """Remove a service from monitoring."""
        try:
            with self._lock:
                self.monitored_services.pop(service_id, None)
            logger.info("Service %s removed from quality monitoring", service_id)
            return True
        except Exception as exc:
            logger.error(
                "Failed to remove service monitoring for %s: %s", service_id, exc
            )
            return False

    def start_monitoring(self) -> bool:
        """Start the background monitoring loop."""
        if self._monitoring:
            logger.warning("Quality monitoring already running")
            return False
        try:
            self._monitoring = True
            self._monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True
            )
            self._monitor_thread.start()
            logger.info("Quality monitoring started")
            return True
        except Exception as exc:
            logger.error("Failed to start quality monitoring: %s", exc)
            self._monitoring = False
            return False

    def stop_monitoring(self) -> bool:
        """Stop the background monitoring loop."""
        if not self._monitoring:
            logger.warning("Quality monitoring not running")
            return False
        try:
            self._monitoring = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=5.0)
            logger.info("Quality monitoring stopped")
            return True
        except Exception as exc:
            logger.error("Failed to stop quality monitoring: %s", exc)
            return False

    def _monitor_loop(self) -> None:
        """Periodically gather metrics from services."""
        while self._monitoring:
            try:
                self._check_service_quality()
                time.sleep(self.check_interval)
            except Exception as exc:
                logger.error("Error in monitoring loop: %s", exc)
                time.sleep(self.check_interval)

    def _check_service_quality(self) -> None:
        """Gather metrics and run analysis for monitored services."""
        current_time = time.time()
        with self._lock:
            for service_id, info in self.monitored_services.items():
                if current_time - info["last_check"] >= self.check_interval:
                    metrics = info["provider"]()
                    self.analyzer.evaluate(service_id, metrics, info["thresholds"])
                    info["last_check"] = current_time
