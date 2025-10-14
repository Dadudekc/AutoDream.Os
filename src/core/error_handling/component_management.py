#!/usr/bin/env python3
"""
Component Management Module
===========================

Component registration and status management for error handling.
Extracted from coordination_error_handler.py for autonomous systems.

Features:
- Circuit breaker registration
- Retry mechanism registration
- Recovery strategy management
- Component status tracking
- Health monitoring integration

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import logging
from typing import Any

from .circuit_breaker import CircuitBreaker
from .error_handling_core import CircuitBreakerConfig, RetryConfig
from .error_intelligence import intelligence_engine
from .recovery_strategies import RecoveryStrategy
from .retry_mechanisms import RetryMechanism

logger = logging.getLogger(__name__)


class ComponentManager:
    """Manages error handling components for autonomous systems."""

    def __init__(self):
        """Initialize component manager."""
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.retry_mechanisms: dict[str, RetryMechanism] = {}
        self.recovery_strategies: list[RecoveryStrategy] = []
        logger.info("ComponentManager initialized")

    def register_circuit_breaker(
        self,
        component: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
    ) -> CircuitBreaker:
        """Register a circuit breaker for a component.

        Args:
            component: Component identifier
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Timeout before attempting recovery (seconds)

        Returns:
            Registered circuit breaker
        """
        config = CircuitBreakerConfig(
            name=component,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )
        circuit_breaker = CircuitBreaker(config)
        self.circuit_breakers[component] = circuit_breaker
        logger.info(f"Circuit breaker registered for {component}")
        return circuit_breaker

    def register_retry_mechanism(
        self,
        component: str,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ) -> RetryMechanism:
        """Register a retry mechanism for a component.

        Args:
            component: Component identifier
            max_attempts: Maximum retry attempts
            base_delay: Initial delay between retries
            max_delay: Maximum delay between retries

        Returns:
            Registered retry mechanism
        """
        config = RetryConfig(
            max_attempts=max_attempts,
            base_delay=base_delay,
            max_delay=max_delay,
        )
        retry_mechanism = RetryMechanism(config)
        self.retry_mechanisms[component] = retry_mechanism
        logger.info(f"Retry mechanism registered for {component}")
        return retry_mechanism

    def add_recovery_strategy(self, strategy: RecoveryStrategy):
        """Add a custom recovery strategy.

        Args:
            strategy: Recovery strategy to add
        """
        self.recovery_strategies.append(strategy)
        logger.info(f"Recovery strategy added: {strategy.name}")

    def get_component_status(self, component: str) -> dict[str, Any]:
        """Get detailed status for a specific component.

        Args:
            component: Component to analyze

        Returns:
            Component status including health and intelligence insights
        """
        try:
            health_report = intelligence_engine.get_component_health(component)
        except Exception as e:
            logger.error(f"Error getting component health: {e}")
            health_report = {"error": str(e)}

        circuit_breaker = self.circuit_breakers.get(component)
        has_retry = component in self.retry_mechanisms

        return {
            "component": component,
            "health": health_report,
            "circuit_breaker": circuit_breaker.state.value if circuit_breaker else "none",
            "retry_enabled": has_retry,
            "strategies_available": len(self.recovery_strategies),
        }

    def get_error_report(self) -> dict[str, Any]:
        """Generate comprehensive error report with intelligence insights.

        Returns:
            Comprehensive error and intelligence report
        """
        try:
            intelligence_report = intelligence_engine.get_system_intelligence_report()

            return {
                "system_health": {
                    "total_errors": intelligence_report["summary"]["total_errors"],
                    "critical_errors": intelligence_report["summary"]["critical_errors"],
                    "components_tracked": intelligence_report["summary"]["components_tracked"],
                    "high_risk_components": len(intelligence_report["high_risk_components"]),
                },
                "intelligence": intelligence_report,
                "circuit_breakers": {
                    name: breaker.state.value for name, breaker in self.circuit_breakers.items()
                },
                "retry_mechanisms": list(self.retry_mechanisms.keys()),
                "recovery_strategies": [s.name for s in self.recovery_strategies],
            }
        except Exception as e:
            logger.error(f"Error generating error report: {e}")
            return {
                "error": str(e),
                "circuit_breakers": list(self.circuit_breakers.keys()),
                "retry_mechanisms": list(self.retry_mechanisms.keys()),
                "recovery_strategies": [s.name for s in self.recovery_strategies],
            }

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component.

        Args:
            component: Component to reset

        Returns:
            True if reset successful
        """
        # Reset circuit breaker
        if component in self.circuit_breakers:
            self.circuit_breakers[component].reset()
            logger.info(f"Circuit breaker reset for {component}")

        logger.info(f"Component {component} error handling state reset")
        return True

    def get_all_components(self) -> list[str]:
        """Get list of all registered components.

        Returns:
            List of component identifiers
        """
        components = set()
        components.update(self.circuit_breakers.keys())
        components.update(self.retry_mechanisms.keys())
        return sorted(list(components))

    def get_component_metrics(self, component: str) -> dict[str, Any]:
        """Get metrics for a specific component.

        Args:
            component: Component to analyze

        Returns:
            Component metrics
        """
        metrics = {
            "component": component,
            "has_circuit_breaker": component in self.circuit_breakers,
            "has_retry_mechanism": component in self.retry_mechanisms,
            "recovery_strategies": len(self.recovery_strategies),
        }

        # Add circuit breaker metrics
        if component in self.circuit_breakers:
            breaker = self.circuit_breakers[component]
            metrics["circuit_breaker_state"] = breaker.state.value
            metrics["circuit_breaker_failures"] = breaker.failure_count

        # Add intelligence metrics
        try:
            health = intelligence_engine.get_component_health(component)
            metrics["intelligence_health"] = health
        except Exception as e:
            logger.debug(f"Could not get intelligence metrics: {e}")

        return metrics


# Global component manager instance
component_manager = ComponentManager()


# Helper functions for quick access
def register_circuit_breaker(component: str, **kwargs) -> CircuitBreaker:
    """Register circuit breaker using global manager."""
    return component_manager.register_circuit_breaker(component, **kwargs)


def register_retry_mechanism(component: str, **kwargs) -> RetryMechanism:
    """Register retry mechanism using global manager."""
    return component_manager.register_retry_mechanism(component, **kwargs)


def add_recovery_strategy(strategy: RecoveryStrategy):
    """Add recovery strategy using global manager."""
    component_manager.add_recovery_strategy(strategy)


def get_component_status(component: str) -> dict[str, Any]:
    """Get component status using global manager."""
    return component_manager.get_component_status(component)


def reset_component(component: str) -> bool:
    """Reset component using global manager."""
    return component_manager.reset_component(component)
