#!/usr/bin/env python3
"""
Emergency Protocol Manager - Component of Emergency Response System
=================================================================

Coordinates emergency protocol strategies and execution.
"""

from typing import Dict, List, Optional, Any, Callable

from ..base_manager import BaseManager
from .logging import get_logger
from .strategies import (
    EmergencyProtocol,
    ProtocolStatus,
    ProtocolPriority,
    ResponseAction,
    EscalationProcedure,
    RecoveryProcedure,
    create_protocol_from_data,
    load_default_protocols,
)
from .executor import ProtocolExecutor


class ProtocolManager(BaseManager):
    """Coordinate emergency protocol strategies and execution."""

    def __init__(self, config_path: str = "config/protocol_manager.json"):
        super().__init__(
            manager_name="ProtocolManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )
        self.logger = get_logger(f"{__name__}.ProtocolManager")
        self.emergency_protocols: Dict[str, EmergencyProtocol] = {}
        self.protocol_handlers: Dict[str, Callable] = {}
        self.protocols_loaded = False
        self.default_protocols_configured = False

        self._load_protocol_config()
        self._setup_default_protocols()

        self.executor = ProtocolExecutor(self.emergency_protocols)
        self.logger.info("✅ Emergency Protocol Manager initialized successfully")

    def _load_protocol_config(self):
        """Load protocol manager configuration"""
        try:
            config = self.get_config()
            if "custom_protocols" in config:
                for protocol_data in config["custom_protocols"]:
                    protocol = create_protocol_from_data(protocol_data)
                    if protocol:
                        self.emergency_protocols[protocol.name] = protocol
            self.protocols_loaded = True
        except Exception as e:
            self.logger.error(f"Failed to load protocol config: {e}")

    def _setup_default_protocols(self):
        """Setup default emergency protocols"""
        try:
            defaults = load_default_protocols()
            self.emergency_protocols.update(defaults)
            self.default_protocols_configured = True
            self.logger.info("✅ Default emergency protocols configured")
        except Exception as e:
            self.logger.error(f"Failed to setup default protocols: {e}")

    def add_protocol(self, protocol: EmergencyProtocol):
        """Add a new emergency protocol"""
        self.emergency_protocols[protocol.name] = protocol
        self.logger.info(f"✅ Added emergency protocol: {protocol.name}")

    def remove_protocol(self, protocol_name: str):
        """Remove an emergency protocol"""
        if protocol_name in self.emergency_protocols:
            del self.emergency_protocols[protocol_name]
            self.logger.info(f"✅ Removed emergency protocol: {protocol_name}")

    def get_protocol(self, protocol_name: str) -> Optional[EmergencyProtocol]:
        """Get a specific emergency protocol"""
        return self.emergency_protocols.get(protocol_name)

    def list_protocols(self) -> List[str]:
        """List all available protocol names"""
        return list(self.emergency_protocols.keys())

    def evaluate_activation_conditions(
        self, protocol_name: str, system_state: Dict[str, Any]
    ) -> bool:
        """Evaluate if a protocol's activation conditions are met"""
        try:
            protocol = self.get_protocol(protocol_name)
            if not protocol:
                return False
            for condition in protocol.activation_conditions:
                if not self._evaluate_condition(condition, system_state):
                    return False
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to evaluate activation conditions for {protocol_name}: {e}"
            )
            return False

    def _evaluate_condition(self, condition: str, system_state: Dict[str, Any]) -> bool:
        """Evaluate a single activation condition"""
        try:
            if "contract completion rate" in condition:
                rate = system_state.get("contract_completion_rate", 100)
                return rate < 40
            if "agent idle time" in condition:
                idle_time = system_state.get("max_agent_idle_time", 0)
                return idle_time > 900
            if "workflow stall" in condition:
                return system_state.get("workflow_stalled", False)
            if "contract system down" in condition:
                return not system_state.get("contract_system_available", True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False

    def activate_protocol(self, protocol_name: str, source: str = "system") -> bool:
        """Activate an emergency protocol"""
        return self.executor.activate_protocol(protocol_name, source)

    def execute_protocol_actions(self, protocol_name: str) -> Dict[str, Any]:
        """Execute all actions for an active protocol"""
        return self.executor.execute_protocol_actions(protocol_name)

    def get_protocol_status(self, protocol_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific protocol"""
        return self.executor.get_protocol_status(protocol_name)

    def get_all_protocol_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all protocols"""
        return self.executor.get_all_protocol_statuses()

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get protocol execution history"""
        return self.executor.get_execution_history()

    def health_check(self) -> Dict[str, Any]:
        """Health check for the protocol manager"""
        try:
            return {
                "is_healthy": True,
                "protocols_loaded": self.protocols_loaded,
                "default_protocols_configured": self.default_protocols_configured,
                "total_protocols": len(self.emergency_protocols),
                "active_executions": len(self.executor.active_executions),
                "total_executions": len(self.executor.execution_history),
                "protocols": list(self.emergency_protocols.keys()),
            }
        except Exception as e:
            return {"is_healthy": False, "error": str(e)}


__all__ = [
    "ProtocolManager",
    "EmergencyProtocol",
    "ProtocolStatus",
    "ProtocolPriority",
    "ResponseAction",
    "EscalationProcedure",
    "RecoveryProcedure",
]
