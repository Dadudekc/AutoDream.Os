"""
Manager Operations - Base Manager Operation Execution
=====================================================
Extracted from base_manager.py for V2 compliance.
Handles operation execution, validation, and result management.

Author: Agent-5 (refactored from Agent-2's base_manager.py)
License: MIT
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..shared_utilities import ErrorHandler, ResultManager, ValidationManager
    from .contracts import ManagerContext, ManagerResult
    from .manager_metrics import ManagerMetricsTracker
    from .manager_state import ManagerStateTracker


class ManagerOperationsHelper:
    """Handles operation execution with validation and error handling."""

    def __init__(
        self,
        state_tracker: ManagerStateTracker,
        metrics_tracker: ManagerMetricsTracker,
        validation_manager: ValidationManager,
        result_manager: ResultManager,
        error_handler: ErrorHandler,
    ):
        """Initialize operations helper."""
        self.state_tracker = state_tracker
        self.metrics_tracker = metrics_tracker
        self.validation_manager = validation_manager
        self.result_manager = result_manager
        self.error_handler = error_handler

    def execute_with_validation(
        self,
        context: ManagerContext,
        operation: str,
        payload: dict[str, Any],
        execute_callback: Any,
    ) -> ManagerResult:
        """
        Execute operation with validation and error handling.
        
        Args:
            context: Manager context
            operation: Operation name
            payload: Operation payload
            execute_callback: Callback function to execute the actual operation
            
        Returns:
            ManagerResult with operation results
        """
        try:
            self.metrics_tracker.record_operation_start()
            self.state_tracker.mark_operation()
            
            # Validate input
            validation_result = self.validation_manager.validate_operation(
                operation=operation,
                payload=payload,
                component_type=self.state_tracker.manager_type.value,
            )
            
            if not validation_result.is_valid:
                self.metrics_tracker.record_error()
                return self.result_manager.create_error_result(
                    error=f"Validation failed: {validation_result.errors}",
                    operation=operation,
                    component_id=self.state_tracker.manager_id,
                )
            
            # Execute operation via callback
            result = execute_callback(context, operation, payload)
            
            if result.success:
                self.metrics_tracker.record_success()
            else:
                self.metrics_tracker.record_error()
                self.state_tracker.last_error = result.error
            
            # Create standardized result
            return self.result_manager.create_result(
                data=result.data if result.success else {},
                operation=operation,
                component_id=self.state_tracker.manager_id,
                success=result.success,
                error=result.error,
                metrics=result.metrics,
            )
            
        except Exception as e:
            self.metrics_tracker.record_error()
            self.state_tracker.mark_error(str(e))
            
            # Handle error
            self.error_handler.handle_error(
                error=e,
                context={
                    "operation": operation,
                    "payload": payload,
                    "manager_id": self.state_tracker.manager_id,
                },
                component_id=self.state_tracker.manager_id,
                severity="medium",
            )
            
            return self.result_manager.create_error_result(
                error=str(e),
                operation=operation,
                component_id=self.state_tracker.manager_id,
            )
        
        finally:
            self.state_tracker.mark_ready()



