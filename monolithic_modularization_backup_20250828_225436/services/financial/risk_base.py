"""Shared risk management primitives and base class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level classifications."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskType(Enum):
    """Types of financial risk."""

    MARKET_RISK = "MARKET_RISK"
    CREDIT_RISK = "CREDIT_RISK"
    LIQUIDITY_RISK = "LIQUIDITY_RISK"
    OPERATIONAL_RISK = "OPERATIONAL_RISK"
    CONCENTRATION_RISK = "CONCENTRATION_RISK"
    VOLATILITY_RISK = "VOLATILITY_RISK"


@dataclass
class RiskMetric:
    """Individual risk metric data."""

    risk_type: RiskType
    value: float
    threshold: float
    risk_level: RiskLevel
    weight: float
    description: str
    last_updated: datetime | None = None

    def __post_init__(self) -> None:  # pragma: no cover - simple dataclass hook
        if self.last_updated is None:
            self.last_updated = datetime.now()
        self.calculate_risk_level()

    def calculate_risk_level(self) -> None:
        """Calculate risk level based on value vs threshold."""
        if self.value <= self.threshold * 0.5:
            self.risk_level = RiskLevel.LOW
        elif self.value <= self.threshold * 0.8:
            self.risk_level = RiskLevel.MEDIUM
        elif self.value <= self.threshold:
            self.risk_level = RiskLevel.HIGH
        else:
            self.risk_level = RiskLevel.CRITICAL


@dataclass
class RiskAlert:
    """Risk alert notification."""

    alert_id: str
    risk_type: RiskType
    risk_level: RiskLevel
    message: str
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: datetime | None = None


class BaseRiskManager:
    """Shared risk management functionality for services and managers."""

    def __init__(self) -> None:
        self.risk_metrics: Dict[RiskType, RiskMetric] = {}
        self.risk_alerts: List[RiskAlert] = []

        # Default thresholds and weights
        self.risk_thresholds: Dict[RiskType, float] = {
            RiskType.MARKET_RISK: 0.25,
            RiskType.CONCENTRATION_RISK: 0.20,
            RiskType.LIQUIDITY_RISK: 0.15,
            RiskType.VOLATILITY_RISK: 0.30,
        }
        self.risk_weights: Dict[RiskType, float] = {
            RiskType.MARKET_RISK: 0.35,
            RiskType.CONCENTRATION_RISK: 0.25,
            RiskType.LIQUIDITY_RISK: 0.20,
            RiskType.VOLATILITY_RISK: 0.20,
        }

    # ------------------------------------------------------------------
    # Shared helper methods
    # ------------------------------------------------------------------
    def initialize_risk_metrics(self) -> None:
        """Initialize risk metrics with default values."""
        for risk_type, threshold in self.risk_thresholds.items():
            weight = self.risk_weights.get(risk_type, 0.25)
            self.risk_metrics[risk_type] = RiskMetric(
                risk_type=risk_type,
                value=0.0,
                threshold=threshold,
                risk_level=RiskLevel.LOW,
                weight=weight,
                description=self.get_risk_description(risk_type),
            )

    def get_risk_description(self, risk_type: RiskType) -> str:
        """Get human readable description for a risk type."""
        descriptions = {
            RiskType.MARKET_RISK: "Risk of losses due to market movements",
            RiskType.CONCENTRATION_RISK: "Risk of over-concentration in single positions",
            RiskType.LIQUIDITY_RISK: "Risk of inability to exit positions quickly",
            RiskType.VOLATILITY_RISK: "Risk of excessive price volatility",
            RiskType.CREDIT_RISK: "Risk of counterparty default",
            RiskType.OPERATIONAL_RISK: "Risk of failures in processes or systems",
        }
        return descriptions.get(risk_type, "Unknown risk type")
