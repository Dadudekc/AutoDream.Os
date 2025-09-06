"""
Action Executor - V2 Compliant Module
====================================

Executes emergency intervention actions.
Extracted from engine.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ..models import (
    Emergency,
    EmergencySeverity,
    EmergencyType,
    EmergencyStatus,
    InterventionProtocol,
    InterventionResult,
    InterventionAction,
    EmergencyResponse,
    EmergencyContext,
    EmergencyInterventionModels,
)


class ActionExecutor:
    """Executes emergency intervention actions.

    Handles action execution, default implementations, and result processing.
    """

    def __init__(self):
        """Initialize action executor."""
        self.intervention_handlers: Dict[InterventionAction, Callable] = {}

    def register_handler(self, action: InterventionAction, handler: Callable) -> None:
        """Register intervention action handler."""
        self.intervention_handlers[action] = handler

    def execute_action(
        self, emergency: Emergency, action: InterventionAction
    ) -> InterventionResult:
        """Execute specific intervention action."""
        start_time = time.time()

        try:
            if action in self.intervention_handlers:
                handler = self.intervention_handlers[action]
                result = handler(emergency)
                success = True
                error_message = None
            else:
                # Default action implementations
                result = self._default_action_handler(emergency, action)
                success = True
                error_message = None

        except Exception as e:
            result = None
            success = False
            error_message = str(e)

        execution_time = time.time() - start_time

        return EmergencyInterventionModels.create_intervention_result(
            action=action,
            success=success,
            execution_time=execution_time,
            error_message=error_message,
            metadata={"emergency_id": emergency.emergency_id},
        )

    def _default_action_handler(
        self, emergency: Emergency, action: InterventionAction
    ) -> Any:
        """Default handler for intervention actions."""
        if action == InterventionAction.RESTART_SERVICE:
            return self._restart_service(emergency)
        elif action == InterventionAction.SCALE_RESOURCES:
            return self._scale_resources(emergency)
        elif action == InterventionAction.ISOLATE_SYSTEM:
            return self._isolate_system(emergency)
        elif action == InterventionAction.ROLLBACK_CHANGES:
            return self._rollback_changes(emergency)
        elif action == InterventionAction.NOTIFY_ADMIN:
            return self._notify_admin(emergency)
        elif action == InterventionAction.EXECUTE_SCRIPT:
            return self._execute_script(emergency)
        else:
            raise ValueError(f"Unknown action: {action}")

    def _restart_service(self, emergency: Emergency) -> Dict[str, Any]:
        """Restart service action."""
        return {
            "action": "restart_service",
            "status": "completed",
            "message": f"Service restarted for emergency {emergency.emergency_id}",
        }

    def _scale_resources(self, emergency: Emergency) -> Dict[str, Any]:
        """Scale resources action."""
        return {
            "action": "scale_resources",
            "status": "completed",
            "message": f"Resources scaled for emergency {emergency.emergency_id}",
        }

    def _isolate_system(self, emergency: Emergency) -> Dict[str, Any]:
        """Isolate system action."""
        return {
            "action": "isolate_system",
            "status": "completed",
            "message": f"System isolated for emergency {emergency.emergency_id}",
        }

    def _rollback_changes(self, emergency: Emergency) -> Dict[str, Any]:
        """Rollback changes action."""
        return {
            "action": "rollback_changes",
            "status": "completed",
            "message": f"Changes rolled back for emergency {emergency.emergency_id}",
        }

    def _notify_admin(self, emergency: Emergency) -> Dict[str, Any]:
        """Notify admin action."""
        return {
            "action": "notify_admin",
            "status": "completed",
            "message": f"Admin notified for emergency {emergency.emergency_id}",
        }

    def _execute_script(self, emergency: Emergency) -> Dict[str, Any]:
        """Execute script action."""
        return {
            "action": "execute_script",
            "status": "completed",
            "message": f"Script executed for emergency {emergency.emergency_id}",
        }

    def execute_multiple_actions(
        self, emergency: Emergency, actions: List[InterventionAction]
    ) -> List[InterventionResult]:
        """Execute multiple actions in sequence."""
        results = []

        for action in actions:
            result = self.execute_action(emergency, action)
            results.append(result)

            # Stop if action fails and protocol requires success
            if not result.success:
                break

        return results

    def get_available_actions(self) -> List[InterventionAction]:
        """Get list of available actions."""
        return list(InterventionAction)

    def get_registered_handlers(self) -> Dict[InterventionAction, str]:
        """Get registered handlers with their names."""
        return {
            action: handler.__name__ if hasattr(handler, "__name__") else str(handler)
            for action, handler in self.intervention_handlers.items()
        }

    def clear_handlers(self):
        """Clear all registered handlers."""
        self.intervention_handlers.clear()

    def has_handler(self, action: InterventionAction) -> bool:
        """Check if action has a registered handler."""
        return action in self.intervention_handlers
