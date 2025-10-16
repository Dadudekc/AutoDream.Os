"""
Base Results Manager - Phase-2 V2 Compliance Refactoring + DUP-004
========================================================
Base class for results management. Refactored to <200 lines.
DUP-004: Now inherits from BaseManager for proper hierarchy.
Author: Agent-3 | Refactored: Agent-5 | DUP-004: Agent-2 | License: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from ..base_manager import BaseManager
from ..contracts import ManagerContext, ManagerResult
from ..manager_state import ManagerType
from .results_processing import ResultsProcessor, ResultStatus
from .results_query_helpers import ResultsQueryHelper
from .results_validation import ResultsValidator


class BaseResultsManager(BaseManager):
    """Base results manager with common functionality - inherits from BaseManager."""

    def __init__(self):
        """Initialize base results manager."""
        # Initialize BaseManager first (gets all utilities for free!)
        super().__init__(ManagerType.RESULTS, "Base Results Manager")
        
        # Results-specific state
        self.results: dict[str, dict[str, Any]] = {}
        self.result_processors: dict[str, Callable] = {}
        self.result_callbacks: dict[str, Callable] = {}
        self.archived_results: dict[str, dict[str, Any]] = {}
        self.max_results = 1000
        self.archive_after_days = 30
        
        # Results-specific components
        self.processor = ResultsProcessor(
            self.result_processors, self.archived_results, self.archive_after_days
        )
        self.validator = ResultsValidator()

    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute results-specific operations."""
        # Results-specific operations only (BaseManager handles validation/error handling)
        if operation == "process_results":
            return self.process_results(context, payload)
        elif operation == "get_results":
            return self._get_results(context, payload)
        elif operation == "archive_results":
            return self._archive_results(context, payload)
        elif operation == "register_processor":
            return self._register_result_processor(context, payload)
        else:
            return ManagerResult(
                success=False, data={}, metrics={}, error=f"Unknown operation: {operation}"
            )

    def process_results(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Process results with validation and callbacks."""
        try:
            result_data = payload.get("result_data", {})
            result_type = payload.get("result_type", "general")
            validation_rules = payload.get("validation_rules", [])
            callback_key = payload.get("callback_key")
            result_id = str(uuid.uuid4())
            result = {
                "id": result_id,
                "type": result_type,
                "data": result_data,
                "status": ResultStatus.PENDING.value,
                "created_at": datetime.now().isoformat(),
                "validation_rules": validation_rules,
                "callback_key": callback_key,
            }
            self.results[result_id] = result
            result["status"] = ResultStatus.PROCESSING.value
            processed_data = self.processor.process_result_by_type(
                context, result_type, result_data
            )
            validation_passed = self.validator.validate_result(result, validation_rules)
            if validation_passed:
                result["status"] = ResultStatus.COMPLETED.value
                result["processed_data"] = processed_data
                result["completed_at"] = datetime.now().isoformat()
                if callback_key and callback_key in self.result_callbacks:
                    try:
                        self.result_callbacks[callback_key](result)
                    except Exception as e:
                        self.logger.error(f"Callback execution failed: {e}")
                self.processor.archive_old_results(self.results)
                return ManagerResult(
                    success=True,
                    data={"result_id": result_id, "processed_data": processed_data},
                    metrics={
                        "results_processed": 1,
                        "validation_passed": True,
                        "callback_executed": callback_key is not None,
                    },
                )
            else:
                result["status"] = ResultStatus.FAILED.value
                result["failed_at"] = datetime.now().isoformat()
                result["error"] = "Validation failed"
                return ManagerResult(
                    success=False,
                    data={"result_id": result_id},
                    metrics={"results_processed": 1, "validation_passed": False},
                    error="Result validation failed",
                )
        except Exception as e:
            self.logger.error(f"Error processing results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup results manager - extends BaseManager cleanup."""
        try:
            # Results-specific cleanup
            self.processor.archive_old_results(self.results)
            self.results.clear()
            self.result_processors.clear()
            self.result_callbacks.clear()
            self.logger.info("Results manager cleaned up")
            
            # Call parent cleanup
            return super().cleanup(context)
        except Exception as e:
            self.logger.error(f"Error cleaning up results manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get results manager status - extends BaseManager status."""
        base_status = super().get_status()
        results_status = {
            "active_results": len(self.results),
            "archived_results": len(self.archived_results),
            "registered_processors": len(self.result_processors),
            "registered_callbacks": len(self.result_callbacks),
            "max_results": self.max_results,
            "archive_after_days": self.archive_after_days,
        }
        base_status.update(results_status)
        return base_status

    def _get_results(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get results with optional filtering."""
        return ResultsQueryHelper.get_results_filtered(
            self.results, self.archived_results, payload, context
        )

    def _archive_results(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Archive results."""
        return ResultsQueryHelper.archive_results_batch(
            self.results, self.archived_results, payload, context
        )

    def _register_result_processor(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Register result processor."""
        try:
            processor_type = payload.get("processor_type")
            processor_func = payload.get("processor_func")
            if not processor_type or not processor_func:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="processor_type and processor_func are required",
                )
            self.result_processors[processor_type] = processor_func
            return ManagerResult(
                success=True,
                data={"processor_type": processor_type},
                metrics={"processors_registered": len(self.result_processors)},
            )
        except Exception as e:
            self.logger.error(f"Error registering result processor: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))
