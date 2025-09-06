"""
Emergency Intervention Orchestrator - V2 Compliant Module
========================================================

Main orchestrator for emergency intervention operations.
Coordinates all emergency components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ..models import (
    Emergency,
    EmergencyType,
    EmergencySeverity,
    EmergencyStatus,
    InterventionProtocol,
    EmergencyResponse,
    EmergencyContext,
    EmergencyInterventionModels,
)
from ..engine import EmergencyInterventionEngine
from ..protocols import EmergencyProtocols
from .emergency_analyzer import EmergencyAnalyzer
from .emergency_logger import EmergencyLogger


class EmergencyInterventionOrchestrator:
    """Main orchestrator for emergency intervention operations.

    Coordinates emergency detection, analysis, intervention, and logging across all
    emergency components.
    """

    def __init__(self):
        """Initialize emergency intervention orchestrator."""
        self.engine = EmergencyInterventionEngine()
        self.protocols = EmergencyProtocols()
        self.analyzer = EmergencyAnalyzer()
        self.logger = EmergencyLogger()

        # Register default protocols
        self._register_default_protocols()

    def _register_default_protocols(self) -> None:
        """Register default protocols with engine."""
        for protocol in self.protocols.protocols.values():
            self.engine.register_protocol(protocol)

    def detect_emergency(
        self,
        emergency_type: EmergencyType,
        severity: EmergencySeverity,
        description: str,
        context: EmergencyContext = None,
    ) -> Emergency:
        """Detect and create emergency incident."""
        emergency = self.engine.detect_emergency(
            emergency_type=emergency_type,
            severity=severity,
            description=description,
            context=context,
        )

        # Log emergency detection
        self.logger.log_emergency_event(
            emergency.emergency_id,
            "emergency_detected",
            {
                "type": emergency_type.value,
                "severity": severity.value,
                "description": description,
            },
        )

        return emergency

    def analyze_emergency(self, emergency: Emergency) -> Dict[str, Any]:
        """Analyze emergency incident."""
        analysis = self.analyzer.analyze_emergency(emergency)

        # Log analysis
        self.logger.log_emergency_event(
            emergency.emergency_id,
            "emergency_analyzed",
            {
                "analysis_timestamp": analysis.get("analysis_timestamp"),
                "risk_level": analysis.get("risk_assessment", {}).get("risk_level"),
                "priority_score": analysis.get("priority_score"),
            },
        )

        return analysis

    def execute_intervention(self, emergency: Emergency) -> EmergencyResponse:
        """Execute intervention for emergency."""
        response = self.engine.respond_to_emergency(emergency)

        # Log intervention execution
        self.logger.log_emergency_event(
            emergency.emergency_id,
            "intervention_executed",
            {
                "success": response.resolution_time is not None,
                "escalated": response.escalated,
                "response_time": response.response_time,
            },
        )

        return response

    def handle_emergency(
        self,
        emergency_type: EmergencyType,
        severity: EmergencySeverity,
        description: str,
        context: EmergencyContext = None,
        auto_intervene: bool = True,
    ) -> Dict[str, Any]:
        """Complete emergency handling workflow."""
        # Detect emergency
        emergency = self.detect_emergency(
            emergency_type, severity, description, context
        )

        # Analyze emergency
        analysis = self.analyze_emergency(emergency)

        # Execute intervention if auto-intervene is enabled
        response = None
        if auto_intervene:
            response = self.execute_intervention(emergency)

        return {
            "emergency": emergency,
            "analysis": analysis,
            "response": response,
            "handled_at": datetime.now().isoformat(),
        }

    def register_intervention_handler(self, action: str, handler: Callable) -> None:
        """Register custom intervention handler."""
        from ..models import InterventionAction

        action_enum = InterventionAction(action)
        self.engine.register_handler(action_enum, handler)

    def get_emergency_status(self, emergency_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific emergency."""
        emergency = self.engine.active_emergencies.get(emergency_id)
        if not emergency:
            return None

        return {
            "emergency_id": emergency.emergency_id,
            "type": emergency.emergency_type.value,
            "severity": emergency.severity.value,
            "status": emergency.status.value,
            "detected_at": emergency.detected_at.isoformat(),
            "resolved_at": (
                emergency.resolved_at.isoformat() if emergency.resolved_at else None
            ),
            "description": emergency.description,
        }

    def get_active_emergencies(self) -> List[Dict[str, Any]]:
        """Get all active emergencies."""
        return [
            self.get_emergency_status(emergency.emergency_id)
            for emergency in self.engine.get_active_emergencies()
        ]

    def get_emergency_history(self, emergency_id: str) -> List[Dict[str, Any]]:
        """Get history for specific emergency."""
        return self.logger.get_emergency_history(emergency_id)

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get emergency intervention system metrics."""
        return self.engine.get_metrics()

    def get_protocol_summary(self) -> Dict[str, Any]:
        """Get protocol summary."""
        return self.protocols.get_protocol_summary()

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        metrics = self.get_system_metrics()
        active_emergencies = len(self.get_active_emergencies())

        return self.logger.calculate_system_health(active_emergencies, metrics)

    def create_custom_protocol(
        self,
        emergency_type: EmergencyType,
        severity_threshold: EmergencySeverity,
        actions: List[str],
        priority: int = 5,
        timeout_seconds: int = 300,
        auto_execute: bool = False,
    ) -> str:
        """Create custom intervention protocol."""
        from ..models import InterventionAction

        action_enums = [InterventionAction(action) for action in actions]

        protocol = self.protocols.create_custom_protocol(
            emergency_type=emergency_type,
            severity_threshold=severity_threshold,
            actions=action_enums,
            priority=priority,
            timeout_seconds=timeout_seconds,
            auto_execute=auto_execute,
        )

        # Register with engine
        self.engine.register_protocol(protocol)

        # Log protocol creation
        self.logger.log_emergency_event(
            "system",
            "protocol_created",
            {
                "protocol_id": protocol.protocol_id,
                "emergency_type": emergency_type.value,
                "severity_threshold": severity_threshold.value,
            },
        )

        return protocol.protocol_id

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "engine_status": self.engine.get_system_status(),
            "analyzer_metrics": self.analyzer.get_analysis_metrics(),
            "logger_status": self.logger.get_logger_status(),
            "protocol_count": len(self.protocols.protocols),
        }

    def shutdown(self):
        """Shutdown orchestrator and cleanup resources."""
        self.engine.shutdown()
        self.analyzer.clear_analysis_history()
        self.logger.clear_emergency_history()
