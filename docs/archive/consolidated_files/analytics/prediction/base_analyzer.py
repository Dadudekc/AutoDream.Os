"""Base prediction analyzer utilities.

This module centralizes probability normalization and confidence-level
computations to maintain a single source of truth (SSOT) across prediction
analyzers.

Example:
    >>> from core.analytics.prediction.base_analyzer import BasePredictionAnalyzer
    >>> BasePredictionAnalyzer.confidence_level(0.75)
    'high'
"""

from typing import Any


class BasePredictionAnalyzer:
    """Shared utilities for prediction analyzers (SSOT)."""

    CONFIDENCE_THRESHOLDS = [
        (0.9, "very_high"),
        (0.7, "high"),
        (0.5, "medium"),
        (0.0, "low"),
    ]

    @classmethod
    def normalize_probability(cls, probability: float) -> float:
        """Clamp probability to the [0, 1] range."""
        return max(0.0, min(1.0, probability))

    @classmethod
    def confidence_label(cls, probability: float) -> str:
        """Return text label for confidence level."""
        for threshold, label in cls.CONFIDENCE_THRESHOLDS:
            if probability >= threshold:
                return label
        return "low"

    @classmethod
    def confidence_level(cls, probability: float, mapping: dict[str, Any] | None = None) -> Any:
        """Return confidence level using optional custom mapping."""
        label = cls.confidence_label(probability)
        if mapping:
            return mapping.get(label, label)
        return label


__all__ = ["BasePredictionAnalyzer"]
