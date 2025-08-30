"""Common utilities for Agent-7 QA tools."""

import logging
from dataclasses import dataclass
from typing import Any, List


def setup_logging(name: str) -> logging.Logger:
    """Configure and return a logger with the given name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


@dataclass
class QualityMetric:
    """Represents a single quality metric measurement."""
    metric_name: str
    value: Any
    threshold: Any
    status: str  # PASS, FAIL, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    recommendations: List[str]


@dataclass
class StallDetectionMetric:
    """Represents stall detection and prevention metrics."""
    metric_name: str
    value: Any
    threshold: Any
    status: str  # PASS, FAIL, WARNING, STALL_DETECTED
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    stall_risk_level: str  # NONE, LOW, MEDIUM, HIGH, CRITICAL
    prevention_actions: List[str]
    recommendations: List[str]
