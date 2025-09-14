"""
Pattern Analysis Engine - V2 Compliance Refactored
=================================================

Simple pattern analysis for analytics.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .pattern_analysis.anomaly_detector import AnomalyDetector

# Import modular components
from .pattern_analysis.pattern_extractor import PatternExtractor
from .pattern_analysis.trend_analyzer import TrendAnalyzer

logger = logging.getLogger(__name__)


class PatternAnalysisEngine:
    """Simple pattern analysis engine - V2 compliant."""

    def __init__(self, config=None):
        """Initialize pattern analysis engine."""
        self.config = config or {}
        self.logger = logger
        self.analysis_history = []

        # Initialize modular components
        self.pattern_extractor = PatternExtractor()
        self.trend_analyzer = TrendAnalyzer()
        self.anomaly_detector = AnomalyDetector()

    def analyze_patterns(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze patterns in data."""
        try:
            if not data:
                return {"error": "No data provided"}

            # Use modular components for analysis
            patterns = self.pattern_extractor.extract_patterns(data)
            trends = self.trend_analyzer.analyze_trends(data)
            anomalies = self.anomaly_detector.detect_anomalies(data)

            analysis_result = {
                "patterns": patterns,
                "trends": trends,
                "anomalies": anomalies,
                "data_points": len(data),
                "timestamp": datetime.now().isoformat(),
            }

            # Store in history
            self.analysis_history.append(analysis_result)

            return analysis_result
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {e}")
            return {"error": str(e)}

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get analysis summary."""
        try:
            if not self.analysis_history:
                return {"message": "No analysis data available"}

            total_analyses = len(self.analysis_history)
            recent_analysis = self.analysis_history[-1] if self.analysis_history else {}

            return {
                "total_analyses": total_analyses,
                "recent_analysis": recent_analysis,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting analysis summary: {e}")
            return {"error": str(e)}

    def clear_analysis_history(self) -> None:
        """Clear analysis history."""
        self.analysis_history.clear()
        self.logger.info("Analysis history cleared")

    def get_status(self) -> dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "analyses_count": len(self.analysis_history),
            "timestamp": datetime.now().isoformat(),
        }

    # Delegate methods to modular components
    def extract_patterns(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Extract patterns from data."""
        return self.pattern_extractor.extract_patterns(data)

    def analyze_trends(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze trends in data."""
        return self.trend_analyzer.analyze_trends(data)

    def detect_anomalies(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Detect anomalies in data."""
        return self.anomaly_detector.detect_anomalies(data)

    def detect_outliers(self, values: list[float], method: str = "iqr") -> list[dict[str, Any]]:
        """Detect outliers using different methods."""
        return self.anomaly_detector.detect_outliers(values, method)


# Simple factory function
def create_pattern_analysis_engine(config=None) -> PatternAnalysisEngine:
    """Create pattern analysis engine."""
    return PatternAnalysisEngine(config)
