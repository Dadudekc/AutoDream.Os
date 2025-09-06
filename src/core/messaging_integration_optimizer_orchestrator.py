#!/usr/bin/env python3
"""
Messaging Integration Optimizer Orchestrator - V2 Compliance Module
===================================================================

Streamlined messaging integration optimization system for V2 compliance.
Refactored into modular architecture for maintainability and scalability.

Responsibilities:
- High-performance messaging integration optimization
- Intelligent batching and async delivery mechanisms
- Retry strategies and connection pooling
- Performance monitoring and throughput optimization
- Unified interface for messaging optimization

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Any, Dict, Optional

# Import modular components
from .messaging_optimizer_models import (
    MessagingConfig,
    MessagingMetrics,
    DeliveryStrategy,
    OptimizationMode,
)
from .messaging_optimizer_orchestrator import MessagingOptimizationOrchestrator


class MessagingIntegrationOptimizer:
    """Streamlined messaging integration optimizer for V2 compliance.

    Provides comprehensive messaging optimization capabilities while maintaining all
    original functionality through efficient modular design.

    This class serves as a backward-compatible wrapper around the new modular
    architecture for seamless integration.
    """

    def __init__(self, config: Optional[MessagingConfig] = None):
        """Initialize messaging integration optimizer."""
        self._orchestrator = MessagingOptimizationOrchestrator(config)

    def start_optimizer(self) -> bool:
        """Start messaging optimization system."""
        return self._orchestrator.start_optimizer()

    def stop_optimizer(self) -> bool:
        """Stop messaging optimization system."""
        return self._orchestrator.stop_optimizer()

    async def optimize_messaging(self) -> Dict[str, Any]:
        """Optimize messaging integration performance."""
        result = await self._orchestrator.optimize_messaging()

        # Convert OptimizationResult to legacy format for backward compatibility
        if result.error:
            return {"status": result.status, "error": result.error}

        return {
            "status": result.status,
            "optimization_count": result.optimization_count,
            "execution_time_ms": result.execution_time_ms,
            "batch_optimization": result.batch_optimization,
            "async_optimization": result.async_optimization,
            "retry_optimization": result.retry_optimization,
            "connection_optimization": result.connection_optimization,
            "current_metrics": result.current_metrics,
        }

    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get comprehensive optimization summary."""
        return self._orchestrator.get_optimization_summary()

    # Backward compatibility properties
    @property
    def is_active(self) -> bool:
        """Check if optimizer is active."""
        return self._orchestrator.is_active

    @property
    def config(self) -> MessagingConfig:
        """Get current configuration."""
        return self._orchestrator.config

    @property
    def current_metrics(self) -> MessagingMetrics:
        """Get current metrics."""
        return self._orchestrator.current_metrics


# Global instance for backward compatibility
_global_optimizer = None


def get_messaging_integration_optimizer() -> MessagingIntegrationOptimizer:
    """Get global messaging integration optimizer instance."""
    global _global_optimizer

    if _global_optimizer is None:
        _global_optimizer = MessagingIntegrationOptimizer()

    return _global_optimizer
