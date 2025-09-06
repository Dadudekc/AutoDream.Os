"""
Integration Interfaces
=====================

Abstract interfaces for integration engines and coordinators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .integration_models import IntegrationType, IntegrationMetrics, OptimizationConfig


class IIntegrationEngine(ABC):
    """Interface for integration engines."""

    @abstractmethod
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for this integration."""
        pass

    @abstractmethod
    def optimize(self, **kwargs) -> bool:
        """Apply optimizations to this integration."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current status of this integration."""
        pass


class IIntegrationCoordinator(ABC):
    """Interface for integration coordinators."""

    @abstractmethod
    def get_unified_performance_report(self) -> Dict[str, Any]:
        """Get unified performance report for all integrations."""
        pass

    @abstractmethod
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations based on current metrics."""
        pass

    @abstractmethod
    def optimize_integration(self, integration_type: IntegrationType, **kwargs) -> bool:
        """Optimize specific integration with custom parameters."""
        pass

    @abstractmethod
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current status of all integrations."""
        pass


class IPerformanceMonitor(ABC):
    """Interface for performance monitoring."""

    @abstractmethod
    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        pass

    @abstractmethod
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        pass

    @abstractmethod
    def collect_metrics(self) -> Dict[IntegrationType, IntegrationMetrics]:
        """Collect performance metrics from all integrations."""
        pass

    @abstractmethod
    def analyze_performance(self) -> List[Dict[str, Any]]:
        """Analyze performance and identify optimization opportunities."""
        pass
