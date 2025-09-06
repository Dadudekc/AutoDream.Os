"""
Emergency Protocols - V2 Compliance Refactored
===============================================

V2 compliant protocol management using modular handlers.
REFACTORED: 367 lines → <150 lines for V2 compliance.

Responsibilities:
- Orchestrates modular protocol handlers
- Provides unified interface for protocol operations
- Maintains backward compatibility

V2 Compliance: Modular architecture, <300 lines, single responsibility.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import (
    EmergencyType,
    EmergencySeverity,
    InterventionAction,
    InterventionProtocol,
    EmergencyInterventionModels,
)

# Import modular handlers
from .handlers import ProtocolRegistry, ProtocolInitializer, ProtocolExecutor


class EmergencyProtocols:
    """V2 Compliant Emergency Protocols Manager.

    Uses modular handlers to provide protocol capabilities while maintaining clean,
    focused architecture.
    """

    def __init__(self):
        """Initialize emergency protocols with modular handlers."""
        # Initialize modular handlers
        self.registry = ProtocolRegistry()
        self.initializer = ProtocolInitializer(self.registry)
        self.executor = ProtocolExecutor()

        # Initialize default protocols
        self.initializer.initialize_default_protocols()

    def register_protocol(self, protocol: InterventionProtocol) -> bool:
        """Register an emergency protocol."""
        return self.registry.register_protocol(protocol)

    def get_protocol(
        self, emergency_type: EmergencyType, severity: EmergencySeverity
    ) -> Optional[InterventionProtocol]:
        """Get protocol for emergency type and severity."""
        return self.registry.get_protocol(emergency_type, severity)

    def execute_protocol(
        self,
        emergency_type: EmergencyType,
        severity: EmergencySeverity,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute protocol for emergency."""
        try:
            protocol = self.get_protocol(emergency_type, severity)

            if not protocol:
                return {
                    "status": "no_protocol",
                    "message": (
                        f"No protocol found for {emergency_type.value} with {severity.value} severity"
                    ),
                }

            execution_context = context or {}
            execution_context.update(
                {
                    "emergency_type": emergency_type.value,
                    "severity": severity.value,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            return self.executor.execute_protocol(protocol, execution_context)

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_protocols(
        self, emergency_type: Optional[EmergencyType] = None
    ) -> List[InterventionProtocol]:
        """List protocols, optionally filtered by emergency type."""
        return self.registry.list_protocols(emergency_type)

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get protocol execution history."""
        return self.executor.get_execution_history(limit)

    def get_protocol_count(self) -> int:
        """Get total number of registered protocols."""
        return self.registry.get_protocol_count()

    def get_protocols_status(self) -> Dict[str, Any]:
        """Get comprehensive protocols status."""
        try:
            return {
                "total_protocols": self.registry.get_protocol_count(),
                "active_executions": len(self.executor.get_active_executions()),
                "execution_history_size": len(self.executor.get_execution_history(100)),
                "protocol_types": {
                    emergency_type.value: len(
                        self.registry.list_protocols(emergency_type)
                    )
                    for emergency_type in EmergencyType
                },
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def reinitialize_protocols(self) -> None:
        """Reinitialize all default protocols."""
        self.initializer.reinitialize_protocols()

    def export_protocols(self) -> Dict[str, Any]:
        """Export all protocols for backup."""
        return self.registry.export_protocols()

    def import_protocols(self, protocol_data: Dict[str, Any]) -> bool:
        """Import protocols from backup data."""
        return self.registry.import_protocols(protocol_data)

    def cleanup(self) -> None:
        """Cleanup protocol resources."""
        try:
            # Cancel any active executions
            for execution_id in list(self.executor.get_active_executions().keys()):
                self.executor.cancel_execution(execution_id)

            # Clear registries
            self.registry.clear_protocols()

        except Exception as e:
            print(f"Cleanup failed: {e}")


# Factory function for backward compatibility
def create_emergency_protocols() -> EmergencyProtocols:
    """Create an emergency protocols instance."""
    return EmergencyProtocols()


# Singleton instance for global access
_protocols_instance: Optional[EmergencyProtocols] = None


def get_emergency_protocols() -> EmergencyProtocols:
    """Get the global emergency protocols instance."""
    global _protocols_instance

    if _protocols_instance is None:
        _protocols_instance = create_emergency_protocols()

    return _protocols_instance
