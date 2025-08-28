"""Quality trend analysis module."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

from .config import DEFAULT_HISTORY_WINDOW

logger = logging.getLogger(__name__)


class QualityTrendAnalyzer:
    """Analyzes historical quality scores for trends."""

    def __init__(self, history_window: int = DEFAULT_HISTORY_WINDOW) -> None:
        self.history_window = history_window
        self.quality_history: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("Quality Trend Analyzer initialized")

    def add_quality_data(self, service_id: str, quality_score: float, timestamp: float | None = None) -> None:
        """Record a quality data point for a service."""
        if timestamp is None:
            timestamp = time.time()
        history = self.quality_history.setdefault(service_id, [])
        history.append({"score": quality_score, "timestamp": timestamp})
        if len(history) > self.history_window:
            self.quality_history[service_id] = history[-self.history_window:]

    def get_quality_trend(self, service_id: str, time_window: float = 3600) -> Dict[str, Any]:
        """Return trend metrics for the specified service."""
        try:
            if service_id not in self.quality_history:
                return {"error": "No quality data available"}
            current_time = time.time()
            cutoff = current_time - time_window
            recent = [p for p in self.quality_history[service_id] if p["timestamp"] >= cutoff]
            if not recent:
                return {"error": "No data in specified time window"}
            scores = [p["score"] for p in recent]
            timestamps = [p["timestamp"] for p in recent]
            return {
                "service_id": service_id,
                "data_points": len(recent),
                "current_score": scores[-1],
                "average_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores),
                "trend_direction": self._calculate_trend_direction(scores),
                "stability_score": self._calculate_stability_score(scores),
                "time_span": timestamps[-1] - timestamps[0],
            }
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to analyze quality trend for %s: %s", service_id, exc)
            return {"error": str(exc)}

    def _calculate_trend_direction(self, scores: List[float]) -> str:
        """Determine whether scores are improving, declining, or stable."""
        if len(scores) < 2:
            return "insufficient_data"
        first_half = scores[: len(scores) // 2]
        second_half = scores[len(scores) // 2 :]
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        if second_avg > first_avg + 0.5:
            return "improving"
        if second_avg < first_avg - 0.5:
            return "declining"
        return "stable"

    def _calculate_stability_score(self, scores: List[float]) -> float:
        """Calculate a simple stability score from variance."""
        if len(scores) < 2:
            return 0.0
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        stability = max(0, 10 - (variance * 10))
        return round(stability, 2)

    def get_system_quality_summary(self) -> Dict[str, Any]:
        """Summarize overall quality across services."""
        try:
            summary = {
                "total_services": len(self.quality_history),
                "services_with_data": 0,
                "overall_average_score": 0.0,
                "trend_summary": {"improving": 0, "stable": 0, "declining": 0},
            }
            total_score = 0.0
            service_count = 0
            for service_id, data in self.quality_history.items():
                if data:
                    service_count += 1
                    latest_score = data[-1]["score"]
                    total_score += latest_score
                    trend = self.get_quality_trend(service_id)
                    direction = trend.get("trend_direction")
                    if direction in summary["trend_summary"]:
                        summary["trend_summary"][direction] += 1
            summary["services_with_data"] = service_count
            if service_count:
                summary["overall_average_score"] = round(total_score / service_count, 2)
            return summary
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to get system quality summary: %s", exc)
            return {"error": str(exc)}


__all__ = ["QualityTrendAnalyzer"]
