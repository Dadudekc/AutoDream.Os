"""
Base Results Manager - Phase-2 V2 Compliance Refactoring
========================================================
Base class for results management. Refactored to <200 lines.
Author: Agent-3 | Refactored: Agent-5 | License: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from ..contracts import Manager, ManagerContext, ManagerResult
from .results_processing import ResultsProcessor, ResultStatus
from .results_validation import ResultsValidator


class BaseResultsManager(Manager):
    """Base results manager with common functionality."""

    def __init__(self):
        """Initialize base results manager."""
        self.results: dict[str, dict[str, Any]] = {}
        self.result_processors: dict[str, Callable] = {}
        self.result_callbacks: dict[str, Callable] = {}
        self.archived_results: dict[str, dict[str, Any]] = {}
        self.max_results = 1000
        self.archive_after_days = 30
        self.processor = ResultsProcessor(self.result_processors, self.archived_results, self.archive_after_days)
        self.validator = ResultsValidator()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize results manager."""
        try:
            context.logger("Base Results Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize results manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute results operation."""
        try:
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
        except Exception as e:
            context.logger(f"Error executing results operation {operation}: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

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
            processed_data = self.processor.process_result_by_type(context, result_type, result_data)
            validation_passed = self.validator.validate_result(result, validation_rules)
            if validation_passed:
                result["status"] = ResultStatus.COMPLETED.value
                result["processed_data"] = processed_data
                result["completed_at"] = datetime.now().isoformat()
                if callback_key and callback_key in self.result_callbacks:
                    try:
                        self.result_callbacks[callback_key](result)
                    except Exception as e:
                        context.logger(f"Callback execution failed: {e}")
                self.processor.archive_old_results(self.results)
                return ManagerResult(
                    success=True,
                    data={"result_id": result_id, "processed_data": processed_data},
                    metrics={"results_processed": 1, "validation_passed": True, "callback_executed": callback_key is not None},
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
            context.logger(f"Error processing results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup results manager."""
        try:
            self.processor.archive_old_results(self.results)
            self.results.clear()
            self.result_processors.clear()
            self.result_callbacks.clear()
            context.logger("Results manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Error cleaning up results manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get results manager status."""
        return {
            "active_results": len(self.results),
            "archived_results": len(self.archived_results),
            "registered_processors": len(self.result_processors),
            "registered_callbacks": len(self.result_callbacks),
            "max_results": self.max_results,
            "archive_after_days": self.archive_after_days,
        }

    def _get_results(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get results with optional filtering."""
        try:
            result_id = payload.get("result_id")
            result_type = payload.get("result_type")
            status = payload.get("status")
            include_archived = payload.get("include_archived", False)
            results = dict(self.results)
            if include_archived:
                results.update(self.archived_results)
            if result_id:
                results = {k: v for k, v in results.items() if k == result_id}
            if result_type:
                results = {k: v for k, v in results.items() if v.get("type") == result_type}
            if status:
                results = {k: v for k, v in results.items() if v.get("status") == status}
            return ManagerResult(
                success=True, data={"results": results}, metrics={"results_found": len(results)}
            )
        except Exception as e:
            context.logger(f"Error getting results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _archive_results(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Archive results."""
        try:
            result_ids = payload.get("result_ids", [])
            archive_all = payload.get("archive_all", False)
            if archive_all:
                result_ids = list(self.results.keys())
            archived_count = 0
            for result_id in result_ids:
                if result_id in self.results:
                    result = self.results[result_id]
                    result["status"] = ResultStatus.ARCHIVED.value
                    result["archived_at"] = datetime.now().isoformat()
                    self.archived_results[result_id] = result
                    del self.results[result_id]
                    archived_count += 1
            return ManagerResult(
                success=True,
                data={"archived_count": archived_count},
                metrics={"results_archived": archived_count},
            )
        except Exception as e:
            context.logger(f"Error archiving results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

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
            context.logger(f"Error registering result processor: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))
