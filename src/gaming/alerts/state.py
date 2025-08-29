"""State tracking for gaming alerts."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from src.core.health_models import AlertSeverity


@dataclass
class GamingAlert:
    """Represents a single gaming alert instance."""

    alert_id: str
    metric: str
    severity: AlertSeverity
    value: float
    threshold: float
    system_id: str
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())


class AlertState:
    """Tracks active and historical gaming alerts."""

    def __init__(self) -> None:
        self.active: Dict[str, GamingAlert] = {}
        self.history: List[GamingAlert] = []

    def add(self, alert: GamingAlert) -> None:
        self.active[alert.alert_id] = alert
        self.history.append(alert)
