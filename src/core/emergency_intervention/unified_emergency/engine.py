"""
Emergency Intervention Engine - V2 Compliant Module
==================================================

Main engine for emergency intervention operations.
Coordinates all intervention components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from collections.abc import Callable
from datetime import datetime
from typing import Any

from ...common.base_engine import BaseEngine

from ..models import (
    Emergency,
    EmergencyContext,
    EmergencyInterventionModels,
    EmergencyResponse,
    EmergencySeverity,
    EmergencyStatus,
    EmergencyType,
    InterventionAction,
    InterventionProtocol,
    InterventionResult,
)
from .action_executor import ActionExecutor
from .protocol_manager import ProtocolManager


class EmergencyInterventionEngine(BaseEngine):
    """
    Main engine for emergency intervention operations.

    Coordinates action execution, protocol management,
    and emergency response processing.
    """

    def __init__(self) -> None:
        super().__init__()
        self.protocol_manager = ProtocolManager()
        self.action_executor = ActionExecutor()
        self.active_emergencies: dict[str, Emergency] = {}
        self.metrics = EmergencyInterventionModels.create_emergency_metrics()

    def register_protocol(self, protocol: InterventionProtocol) -> None:
        """Register intervention protocol."""
        self.protocol_manager.register_protocol(protocol)

    def register_handler(self, action: InterventionAction, handler: Callable) -> None:
        """Register intervention action handler."""
        self.action_executor.register_handler(action, handler)

    def detect_emergency(
        self,
        emergency_type: EmergencyType,
        severity: EmergencySeverity,
        description: str,
        context: EmergencyContext = None,
    ) -> Emergency:
        """Detect and create emergency incident."""
        emergency = EmergencyInterventionModels.create_emergency(
            emergency_type=emergency_type,
            severity=severity,
            description=description,
            context=context or EmergencyContext(),
        )

        self.active_emergencies[emergency.emergency_id] = emergency
        self.metrics.total_emergencies += 1
        self.metrics.active_emergencies += 1

        return emergency

    def respond_to_emergency(self, emergency: Emergency) -> EmergencyResponse:
        """Respond to emergency using appropriate protocols."""
        start_time = time.time()

        # Find matching protocols
        matching_protocols = self.protocol_manager.find_matching_protocols(emergency)

        if not matching_protocols:
            return self._create_no_protocol_response(emergency)

        # Use highest priority protocol
        protocol = matching_protocols[0]

        # Execute protocol actions
        interventions = self.action_executor.execute_multiple_actions(emergency, protocol.actions)

        # Calculate response time
        response_time = time.time() - start_time

        # Update emergency status based on results
        self._update_emergency_status(emergency, interventions, protocol)

        # Create response
        response = EmergencyInterventionModels.create_emergency_response(
            emergency_id=emergency.emergency_id,
            response_time=response_time,
            interventions=interventions,
            resolution_time=(
                time.time() - start_time if emergency.status == EmergencyStatus.RESOLVED else None
            ),
            escalated=emergency.status == EmergencyStatus.ESCALATED,
        )

        # Update metrics
        self.metrics = EmergencyInterventionModels.update_emergency_metrics(
            self.metrics, emergency, response
        )

        return response

    def _create_no_protocol_response(self, emergency: Emergency) -> EmergencyResponse:
        """Create response when no matching protocol found."""
        return EmergencyInterventionModels.create_emergency_response(
            emergency_id=emergency.emergency_id,
            response_time=0.0,
            interventions=[],
            resolution_time=None,
            escalated=True,
        )

    def _update_emergency_status(
        self,
        emergency: Emergency,
        interventions: list[InterventionResult],
        protocol: InterventionProtocol,
    ) -> None:
        """Update emergency status based on intervention results."""
        successful_interventions = sum(1 for i in interventions if i.success)
        resolution_threshold = len(protocol.actions) * 0.7  # 70% success rate

        if successful_interventions >= resolution_threshold:
            emergency.status = EmergencyStatus.RESOLVED
            emergency.resolved_at = datetime.now()
            self.metrics.resolved_emergencies += 1
            self.metrics.active_emergencies -= 1
        else:
            emergency.status = EmergencyStatus.ESCALATED

    def get_active_emergencies(self) -> list[Emergency]:
        """Get list of active emergencies."""
        return list(self.active_emergencies.values())

    def get_metrics(self) -> dict[str, Any]:
        """Get emergency intervention metrics."""
        return {
            "total_emergencies": self.metrics.total_emergencies,
            "resolved_emergencies": self.metrics.resolved_emergencies,
            "active_emergencies": self.metrics.active_emergencies,
            "average_response_time": self.metrics.average_response_time,
            "average_resolution_time": self.metrics.average_resolution_time,
            "escalation_rate": self.metrics.escalation_rate,
            "last_updated": (
                self.metrics.last_updated.isoformat() if self.metrics.last_updated else None
            ),
        }

    def get_status(self) -> dict[str, Any]:
        """Extend base status with emergency-specific data."""
        status = super().get_status()
        status.update(
            {
                "active_emergencies": len(self.active_emergencies),
                "registered_protocols": self.protocol_manager.get_protocol_count(),
                "registered_handlers": len(self.action_executor.get_registered_handlers()),
                "metrics": self.get_metrics(),
                "protocol_summary": self.protocol_manager.get_protocol_summary(),
            }
        )
        return status

    def clear_emergencies(self) -> None:
        """Clear all active emergencies."""
        self.active_emergencies.clear()
        self.metrics.active_emergencies = 0

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.metrics = EmergencyInterventionModels.create_emergency_metrics()

    def clear_resources(self) -> None:  # pragma: no cover - trivial
        """Clear engine data and handlers."""
        self.clear_emergencies()
        self.reset_metrics()
        self.protocol_manager.clear_protocols()
        self.action_executor.clear_handlers()
