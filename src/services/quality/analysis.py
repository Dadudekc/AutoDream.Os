"""Analysis logic for the quality monitoring system."""

from __future__ import annotations

import logging
from typing import Any, Dict

from .alerting import QualityAlertManager

logger = logging.getLogger(__name__)


class QualityAnalyzer:
    """Evaluate metrics against thresholds and trigger alerts."""

    def __init__(self, alert_manager: QualityAlertManager | None = None) -> None:
        self.alert_manager = alert_manager or QualityAlertManager()

    def evaluate(
        self, service_id: str, metrics: Dict[str, Any], thresholds: Dict[str, Any]
    ) -> None:
        """Compare metrics with thresholds and create alerts when violated."""
        for metric, threshold in thresholds.items():
            value = metrics.get(metric)
            if value is None:
                continue
            if value < threshold:
                self.alert_manager.create_alert(service_id, metric, value, threshold)
