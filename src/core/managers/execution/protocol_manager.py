"""
Protocol Manager - Phase-2 V2 Compliance Refactoring
====================================================

Handles protocol-specific operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Optional, Callable
from .base_execution_manager import BaseExecutionManager, ProtocolType
from ..contracts import ManagerContext, ManagerResult


class ProtocolManager(BaseExecutionManager):
    """Manages protocol operations."""

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute protocol operation."""
        try:
            if operation == "register_protocol":
                return self.register_protocol(context, payload.get("protocol_name"), payload.get("protocol_handler"))
            elif operation == "execute_protocol":
                return self._execute_protocol(context, payload)
            elif operation == "list_protocols":
                return self._list_protocols(context, payload)
            elif operation == "enable_protocol":
                return self._enable_protocol(context, payload)
            elif operation == "disable_protocol":
                return self._disable_protocol(context, payload)
            else:
                return super().execute(context, operation, payload)
        except Exception as e:
            context.logger(f"Error executing protocol operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _execute_protocol(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Execute a protocol."""
        try:
            protocol_name = payload.get("protocol_name")
            if not protocol_name or protocol_name not in self.protocols:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Protocol name is required and must exist",
                )

            protocol = self.protocols[protocol_name]
            if not protocol.get("enabled", True):
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Protocol {protocol_name} is disabled",
                )

            # Execute protocol steps
            steps = protocol.get("steps", [])
            results = []
            
            for step in steps:
                try:
                    step_result = self._execute_protocol_step(context, step, payload)
                    results.append({
                        "step": step,
                        "success": True,
                        "result": step_result,
                    })
                except Exception as e:
                    results.append({
                        "step": step,
                        "success": False,
                        "error": str(e),
                    })
                    context.logger(f"Protocol step {step} failed: {e}")

            # Check if all steps succeeded
            all_success = all(r["success"] for r in results)
            
            return ManagerResult(
                success=all_success,
                data={
                    "protocol_name": protocol_name,
                    "steps_executed": len(steps),
                    "results": results,
                },
                metrics={
                    "protocols_executed": 1,
                    "steps_executed": len(steps),
                    "steps_succeeded": sum(1 for r in results if r["success"]),
                },
            )

        except Exception as e:
            context.logger(f"Error executing protocol {protocol_name}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _execute_protocol_step(self, context: ManagerContext, step: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single protocol step."""
        # Simulate step execution based on step name
        if step == "stop_all_tasks":
            return {"message": "All tasks stopped", "tasks_stopped": len(self.tasks)}
        elif step == "save_state":
            return {"message": "System state saved", "state_size": 1024}
        elif step == "notify_agents":
            return {"message": "Agents notified", "agents_notified": 8}
        elif step == "shutdown_system":
            return {"message": "System shutdown initiated"}
        elif step == "check_system_health":
            return {"message": "System health checked", "health_score": 95}
        elif step == "cleanup_temp_files":
            return {"message": "Temp files cleaned", "files_removed": 15}
        elif step == "update_metrics":
            return {"message": "Metrics updated", "metrics_count": 25}
        elif step == "backup_data":
            return {"message": "Data backed up", "backup_size": 2048}
        else:
            return {"message": f"Step {step} executed", "step": step}

    def _enable_protocol(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Enable a protocol."""
        try:
            protocol_name = payload.get("protocol_name")
            if not protocol_name or protocol_name not in self.protocols:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Protocol name is required and must exist",
                )

            self.protocols[protocol_name]["enabled"] = True

            return ManagerResult(
                success=True,
                data={"protocol_name": protocol_name, "enabled": True},
                metrics={"protocols_enabled": 1},
            )

        except Exception as e:
            context.logger(f"Error enabling protocol: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _disable_protocol(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Disable a protocol."""
        try:
            protocol_name = payload.get("protocol_name")
            if not protocol_name or protocol_name not in self.protocols:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Protocol name is required and must exist",
                )

            self.protocols[protocol_name]["enabled"] = False

            return ManagerResult(
                success=True,
                data={"protocol_name": protocol_name, "enabled": False},
                metrics={"protocols_disabled": 1},
            )

        except Exception as e:
            context.logger(f"Error disabling protocol: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def get_status(self) -> Dict[str, Any]:
        """Get protocol manager status."""
        base_status = super().get_status()
        base_status.update({
            "enabled_protocols": len([p for p in self.protocols.values() if p.get("enabled", True)]),
            "disabled_protocols": len([p for p in self.protocols.values() if not p.get("enabled", True)]),
            "protocol_types": list(set(p.get("type", "unknown").value if hasattr(p.get("type"), "value") else str(p.get("type", "unknown")) for p in self.protocols.values())),
        })
        return base_status
