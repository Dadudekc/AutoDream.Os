"""
Protocol Registry Handler
=========================

Manages registration and retrieval of emergency protocols.
Extracted from protocols.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models import (
    EmergencyType,
    EmergencySeverity,
    InterventionAction,
    InterventionProtocol,
    EmergencyInterventionModels,
)


class ProtocolRegistry:
    """Manages registration and retrieval of emergency protocols."""

    def __init__(self):
        """Initialize protocol registry."""
        self.protocols: Dict[str, InterventionProtocol] = {}
        self.protocol_templates: Dict[str, Dict[str, Any]] = {}

    def register_protocol(self, protocol: InterventionProtocol) -> bool:
        """Register an emergency protocol."""
        try:
            protocol_id = (
                f"{protocol.emergency_type.value}_{protocol.severity_threshold.value}"
            )
            self.protocols[protocol_id] = protocol
            return True
        except Exception as e:
            print(f"Failed to register protocol: {e}")
            return False

    def get_protocol(
        self, emergency_type: EmergencyType, severity: EmergencySeverity
    ) -> Optional[InterventionProtocol]:
        """Get protocol for specific emergency type and severity."""
        try:
            # Try exact match first
            protocol_id = f"{emergency_type.value}_{severity.value}"
            if protocol_id in self.protocols:
                return self.protocols[protocol_id]

            # Try finding compatible protocol with lower severity threshold
            compatible_protocols = [
                p
                for p in self.protocols.values()
                if (
                    p.emergency_type == emergency_type
                    and self._severity_meets_threshold(severity, p.severity_threshold)
                )
            ]

            if compatible_protocols:
                # Return highest priority protocol
                return min(compatible_protocols, key=lambda p: p.priority)

            return None

        except Exception as e:
            print(f"Failed to get protocol: {e}")
            return None

    def _severity_meets_threshold(
        self, actual: EmergencySeverity, threshold: EmergencySeverity
    ) -> bool:
        """Check if actual severity meets threshold."""
        severity_levels = {
            EmergencySeverity.LOW: 1,
            EmergencySeverity.MEDIUM: 2,
            EmergencySeverity.HIGH: 3,
            EmergencySeverity.CRITICAL: 4,
        }

        return severity_levels.get(actual, 0) >= severity_levels.get(threshold, 0)

    def list_protocols(
        self, emergency_type: Optional[EmergencyType] = None
    ) -> List[InterventionProtocol]:
        """List all protocols, optionally filtered by emergency type."""
        try:
            protocols = list(self.protocols.values())

            if emergency_type:
                protocols = [p for p in protocols if p.emergency_type == emergency_type]

            # Sort by priority
            return sorted(protocols, key=lambda p: p.priority)

        except Exception as e:
            print(f"Failed to list protocols: {e}")
            return []

    def remove_protocol(
        self, emergency_type: EmergencyType, severity: EmergencySeverity
    ) -> bool:
        """Remove a protocol."""
        try:
            protocol_id = f"{emergency_type.value}_{severity.value}"
            if protocol_id in self.protocols:
                del self.protocols[protocol_id]
                return True
            return False

        except Exception as e:
            print(f"Failed to remove protocol: {e}")
            return False

    def get_protocol_count(self) -> int:
        """Get total number of registered protocols."""
        return len(self.protocols)

    def clear_protocols(self) -> None:
        """Clear all protocols."""
        self.protocols.clear()
        self.protocol_templates.clear()

    def export_protocols(self) -> Dict[str, Any]:
        """Export all protocols for backup/transfer."""
        try:
            return {
                protocol_id: {
                    "emergency_type": protocol.emergency_type.value,
                    "severity_threshold": protocol.severity_threshold.value,
                    "actions": [action.value for action in protocol.actions],
                    "priority": protocol.priority,
                    "timeout_seconds": protocol.timeout_seconds,
                    "auto_execute": protocol.auto_execute,
                }
                for protocol_id, protocol in self.protocols.items()
            }
        except Exception as e:
            print(f"Failed to export protocols: {e}")
            return {}

    def import_protocols(self, protocol_data: Dict[str, Any]) -> bool:
        """Import protocols from backup data."""
        try:
            imported_count = 0

            for protocol_id, data in protocol_data.items():
                try:
                    protocol = EmergencyInterventionModels.create_intervention_protocol(
                        emergency_type=EmergencyType(data["emergency_type"]),
                        severity_threshold=EmergencySeverity(
                            data["severity_threshold"]
                        ),
                        actions=[
                            InterventionAction(action) for action in data["actions"]
                        ],
                        priority=data["priority"],
                        timeout_seconds=data["timeout_seconds"],
                        auto_execute=data["auto_execute"],
                    )

                    if self.register_protocol(protocol):
                        imported_count += 1

                except Exception as e:
                    print(f"Failed to import protocol {protocol_id}: {e}")
                    continue

            print(f"Successfully imported {imported_count} protocols")
            return imported_count > 0

        except Exception as e:
            print(f"Failed to import protocols: {e}")
            return False
