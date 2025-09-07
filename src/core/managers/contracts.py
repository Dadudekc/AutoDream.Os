"""
Manager Contracts - Phase-2 Manager Consolidation
================================================

Defines core manager protocols and interfaces for DIP compliance.
Consolidates 16+ managers into 5 core managers following SOLID principles.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Callable
from datetime import datetime


@dataclass(frozen=True)
class ManagerContext:
    """SSOT: shared context object for all managers (DIP)."""

    config: Dict[str, Any]
    logger: Callable[[str], None]
    metrics: Dict[str, Any]
    timestamp: datetime


@dataclass
class ManagerResult:
    """Standard result object for all manager operations."""

    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    error: Optional[str] = None


class Manager(Protocol):
    """Base manager protocol - stable contract (LSP)."""

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize manager with context."""
        ...

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute manager operation."""
        ...

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup manager resources."""
        ...

    def get_status(self) -> Dict[str, Any]:
        """Get manager status."""
        ...


class ResourceManager(Manager, Protocol):
    """Resource management protocol - files, locks, contexts."""

    def create_resource(
        self, context: ManagerContext, resource_type: str, data: Dict[str, Any]
    ) -> ManagerResult:
        """Create a resource."""
        ...

    def get_resource(self, context: ManagerContext, resource_id: str) -> ManagerResult:
        """Get a resource."""
        ...

    def update_resource(
        self, context: ManagerContext, resource_id: str, updates: Dict[str, Any]
    ) -> ManagerResult:
        """Update a resource."""
        ...

    def delete_resource(
        self, context: ManagerContext, resource_id: str
    ) -> ManagerResult:
        """Delete a resource."""
        ...


class ConfigurationManager(Manager, Protocol):
    """Configuration management protocol - all config operations."""

    def load_config(self, context: ManagerContext, config_key: str) -> ManagerResult:
        """Load configuration."""
        ...

    def save_config(
        self, context: ManagerContext, config_key: str, config_data: Dict[str, Any]
    ) -> ManagerResult:
        """Save configuration."""
        ...

    def validate_config(
        self, context: ManagerContext, config_data: Dict[str, Any]
    ) -> ManagerResult:
        """Validate configuration."""
        ...


class ExecutionManager(Manager, Protocol):
    """Execution management protocol - tasks, protocols, execution."""

    def execute_task(
        self, context: ManagerContext, task_id: str, task_data: Dict[str, Any]
    ) -> ManagerResult:
        """Execute a task."""
        ...

    def register_protocol(
        self, context: ManagerContext, protocol_name: str, protocol_data: Dict[str, Any]
    ) -> ManagerResult:
        """Register a protocol."""
        ...

    def get_execution_status(
        self, context: ManagerContext, execution_id: str
    ) -> ManagerResult:
        """Get execution status."""
        ...


class MonitoringManager(Manager, Protocol):
    """Monitoring management protocol - alerts, metrics, widgets."""

    def create_alert(
        self, context: ManagerContext, alert_data: Dict[str, Any]
    ) -> ManagerResult:
        """Create an alert."""
        ...

    def record_metric(
        self, context: ManagerContext, metric_name: str, metric_value: Any
    ) -> ManagerResult:
        """Record a metric."""
        ...

    def create_widget(
        self, context: ManagerContext, widget_data: Dict[str, Any]
    ) -> ManagerResult:
        """Create a widget."""
        ...


class ServiceManager(Manager, Protocol):
    """Service management protocol - onboarding, recovery, results."""

    def onboard_agent(
        self, context: ManagerContext, agent_data: Dict[str, Any]
    ) -> ManagerResult:
        """Onboard an agent."""
        ...

    def recover_from_error(
        self, context: ManagerContext, error_data: Dict[str, Any]
    ) -> ManagerResult:
        """Recover from error."""
        ...

    def process_results(
        self, context: ManagerContext, results_data: Dict[str, Any]
    ) -> ManagerResult:
        """Process results."""
        ...


# Manager type registry for dynamic instantiation
MANAGER_TYPES = {
    "resource": ResourceManager,
    "configuration": ConfigurationManager,
    "execution": ExecutionManager,
    "monitoring": MonitoringManager,
    "service": ServiceManager,
    # Specialized service managers
    "onboarding": "CoreOnboardingManager",
    "recovery": "CoreRecoveryManager",
    "results": "CoreResultsManager",
    "service_coordinator": "CoreServiceCoordinator",
}
