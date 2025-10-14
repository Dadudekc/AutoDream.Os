"""
Message Queue Analytics Interfaces - V2 Compliance Module
=========================================================

Business Intelligence and analytics interfaces for message queue system.
Enables performance monitoring, predictive analytics, and health scoring.

Created for V2 compliance and BI integration capabilities.

Author: Agent-5 (Business Intelligence & Team Beta Leader)
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class IMessageQueueLogger(Protocol):
    """Interface for message queue logging operations."""

    def info(self, message: str) -> None:
        """Log informational message."""
        ...

    def warning(self, message: str) -> None:
        """Log warning message."""
        ...

    def error(self, message: str) -> None:
        """Log error message."""
        ...


class IQueueAnalytics(ABC):
    """Interface for queue performance analytics.

    Provides Business Intelligence capabilities for queue monitoring,
    performance analysis, and optimization insights.
    """

    @abstractmethod
    def get_performance_metrics(self) -> dict[str, Any]:
        """Get comprehensive queue performance metrics.

        Returns:
            Dictionary containing:
            - throughput: Messages per second
            - latency_avg: Average processing latency
            - latency_p95: 95th percentile latency
            - success_rate: Delivery success rate
            - failure_rate: Delivery failure rate
        """
        pass

    @abstractmethod
    def get_trending_data(self, hours: int = 24) -> dict[str, list]:
        """Get trending performance data over time.

        Args:
            hours: Number of hours of historical data

        Returns:
            Dictionary with time-series data for key metrics
        """
        pass

    @abstractmethod
    def analyze_bottlenecks(self) -> list[dict[str, Any]]:
        """Identify performance bottlenecks.

        Returns:
            List of bottleneck analyses with recommendations
        """
        pass


class IQueueIntelligence(ABC):
    """Interface for predictive queue intelligence.

    Provides machine learning and predictive analytics for queue optimization.
    """

    @abstractmethod
    def predict_queue_load(self, hours_ahead: int = 1) -> dict[str, float]:
        """Predict future queue load.

        Args:
            hours_ahead: Hours to predict ahead

        Returns:
            Predicted queue metrics (size, throughput, latency)
        """
        pass

    @abstractmethod
    def suggest_optimizations(self) -> list[dict[str, Any]]:
        """Suggest queue configuration optimizations.

        Returns:
            List of optimization suggestions with:
            - parameter: Configuration parameter to adjust
            - current_value: Current setting
            - suggested_value: Recommended setting
            - expected_impact: Predicted performance impact
            - confidence: Confidence score (0.0-1.0)
        """
        pass

    @abstractmethod
    def detect_anomalies(self) -> list[dict[str, Any]]:
        """Detect anomalous queue behavior.

        Returns:
            List of detected anomalies with severity and description
        """
        pass


class IQueueHealthMonitor(ABC):
    """Interface for queue health monitoring.

    Provides health scoring and status monitoring for autonomous systems.
    """

    @abstractmethod
    def get_health_score(self) -> float:
        """Calculate overall queue health score.

        Returns:
            Health score (0.0-100.0) where:
            - 90-100: Excellent
            - 70-89: Good
            - 50-69: Fair
            - 30-49: Poor
            - 0-29: Critical
        """
        pass

    @abstractmethod
    def get_health_report(self) -> dict[str, Any]:
        """Get comprehensive health report.

        Returns:
            Dictionary containing:
            - health_score: Overall score
            - status: Health status level
            - issues: List of identified issues
            - recommendations: List of recommended actions
            - trend: Health trend (improving/stable/declining)
        """
        pass

    @abstractmethod
    def check_component_health(self, component: str) -> dict[str, Any]:
        """Check health of specific queue component.

        Args:
            component: Component name (persistence, processor, etc.)

        Returns:
            Component-specific health metrics
        """
        pass
