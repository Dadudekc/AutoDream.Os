"""
Protocol Initializer Handler
=============================

Initializes default emergency protocols.
Extracted from protocols.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from ..models import (
    EmergencyInterventionModels,
    EmergencySeverity,
    EmergencyType,
    InterventionAction,
)
from .protocol_registry import ProtocolRegistry


class ProtocolInitializer:
    """Initializes default emergency protocols."""

    def __init__(self, registry: ProtocolRegistry):
        """Initialize with protocol registry."""
        self.registry = registry

    def initialize_default_protocols(self) -> None:
        """Initialize all default emergency protocols."""
        self._initialize_system_failure_protocols()
        self._initialize_security_protocols()
        self._initialize_performance_protocols()
        self._initialize_data_protocols()
        self._initialize_network_protocols()
        self._initialize_resource_protocols()

    def _initialize_system_failure_protocols(self) -> None:
        """Initialize system failure protocols."""
        # System Failure - Medium Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.SYSTEM_FAILURE,
                severity_threshold=EmergencySeverity.MEDIUM,
                actions=[
                    InterventionAction.RESTART_SERVICE,
                    InterventionAction.SCALE_RESOURCES,
                    InterventionAction.NOTIFY_ADMIN,
                ],
                priority=1,
                timeout_seconds=300,
                auto_execute=True,
            )
        )

        # System Failure - High Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.SYSTEM_FAILURE,
                severity_threshold=EmergencySeverity.HIGH,
                actions=[
                    InterventionAction.IMMEDIATE_SHUTDOWN,
                    InterventionAction.BACKUP_RESTORE,
                    InterventionAction.ESCALATE_TO_HUMAN,
                    InterventionAction.NOTIFY_ADMIN,
                ],
                priority=0,
                timeout_seconds=120,
                auto_execute=True,
            )
        )

    def _initialize_security_protocols(self) -> None:
        """Initialize security breach protocols."""
        # Security Breach - Any Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.SECURITY_BREACH,
                severity_threshold=EmergencySeverity.LOW,
                actions=[
                    InterventionAction.ISOLATE_SYSTEM,
                    InterventionAction.LOG_INCIDENT,
                    InterventionAction.ESCALATE_TO_HUMAN,
                    InterventionAction.NOTIFY_ADMIN,
                ],
                priority=0,
                timeout_seconds=60,
                auto_execute=True,
            )
        )

    def _initialize_performance_protocols(self) -> None:
        """Initialize performance degradation protocols."""
        # Performance Degradation - Medium Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.PERFORMANCE_DEGRADATION,
                severity_threshold=EmergencySeverity.MEDIUM,
                actions=[
                    InterventionAction.SCALE_RESOURCES,
                    InterventionAction.OPTIMIZE_QUERIES,
                    InterventionAction.CLEAR_CACHE,
                ],
                priority=2,
                timeout_seconds=180,
                auto_execute=True,
            )
        )

        # Performance Degradation - High Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.PERFORMANCE_DEGRADATION,
                severity_threshold=EmergencySeverity.HIGH,
                actions=[
                    InterventionAction.RESTART_SERVICE,
                    InterventionAction.SCALE_RESOURCES,
                    InterventionAction.NOTIFY_ADMIN,
                ],
                priority=1,
                timeout_seconds=120,
                auto_execute=True,
            )
        )

    def _initialize_data_protocols(self) -> None:
        """Initialize data corruption protocols."""
        # Data Corruption - Any Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.DATA_CORRUPTION,
                severity_threshold=EmergencySeverity.LOW,
                actions=[
                    InterventionAction.BACKUP_RESTORE,
                    InterventionAction.VALIDATE_DATA,
                    InterventionAction.LOG_INCIDENT,
                    InterventionAction.ESCALATE_TO_HUMAN,
                ],
                priority=0,
                timeout_seconds=300,
                auto_execute=False,  # Require human approval for data operations
            )
        )

    def _initialize_network_protocols(self) -> None:
        """Initialize network failure protocols."""
        # Network Failure - Medium Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.NETWORK_FAILURE,
                severity_threshold=EmergencySeverity.MEDIUM,
                actions=[
                    InterventionAction.RETRY_CONNECTION,
                    InterventionAction.SWITCH_ENDPOINT,
                    InterventionAction.LOG_INCIDENT,
                ],
                priority=2,
                timeout_seconds=60,
                auto_execute=True,
            )
        )

        # Network Failure - High Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.NETWORK_FAILURE,
                severity_threshold=EmergencySeverity.HIGH,
                actions=[
                    InterventionAction.ISOLATE_SYSTEM,
                    InterventionAction.ACTIVATE_BACKUP,
                    InterventionAction.NOTIFY_ADMIN,
                ],
                priority=1,
                timeout_seconds=120,
                auto_execute=True,
            )
        )

    def _initialize_resource_protocols(self) -> None:
        """Initialize resource exhaustion protocols."""
        # Resource Exhaustion - Medium Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.RESOURCE_EXHAUSTION,
                severity_threshold=EmergencySeverity.MEDIUM,
                actions=[
                    InterventionAction.SCALE_RESOURCES,
                    InterventionAction.CLEAR_CACHE,
                    InterventionAction.OPTIMIZE_QUERIES,
                ],
                priority=2,
                timeout_seconds=180,
                auto_execute=True,
            )
        )

        # Resource Exhaustion - High Severity
        self.registry.register_protocol(
            EmergencyInterventionModels.create_intervention_protocol(
                emergency_type=EmergencyType.RESOURCE_EXHAUSTION,
                severity_threshold=EmergencySeverity.HIGH,
                actions=[
                    InterventionAction.IMMEDIATE_SHUTDOWN,
                    InterventionAction.SCALE_RESOURCES,
                    InterventionAction.RESTART_SERVICE,
                    InterventionAction.ESCALATE_TO_HUMAN,
                ],
                priority=0,
                timeout_seconds=60,
                auto_execute=True,
            )
        )

    def get_initialized_protocol_count(self) -> int:
        """Get count of initialized protocols."""
        return self.registry.get_protocol_count()

    def reinitialize_protocols(self) -> None:
        """Clear and reinitialize all protocols."""
        self.registry.clear_protocols()
        self.initialize_default_protocols()
