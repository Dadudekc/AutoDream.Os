"""
Base Results Manager - Phase-2 V2 Compliance Refactoring
========================================================

Base class for results management with common functionality.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
import json
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
from ..contracts import Manager, ManagerContext, ManagerResult


class ResultStatus(Enum):
    """Result processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class BaseResultsManager(Manager):
    """Base results manager with common functionality."""

    def __init__(self):
        """Initialize base results manager."""
        self.results: Dict[str, Dict[str, Any]] = {}
        self.result_processors: Dict[str, Callable] = {}
        self.result_callbacks: Dict[str, Callable] = {}
        self.archived_results: Dict[str, Dict[str, Any]] = {}
        self.max_results = 1000
        self.archive_after_days = 30

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize results manager."""
        try:
            context.logger("Base Results Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize results manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
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
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            context.logger(f"Error executing results operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def process_results(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Process results with validation and callbacks."""
        try:
            result_data = payload.get("result_data", {})
            result_type = payload.get("result_type", "general")
            validation_rules = payload.get("validation_rules", [])
            callback_key = payload.get("callback_key")

            # Generate result ID
            result_id = str(uuid.uuid4())
            
            # Create result entry
            result = {
                "id": result_id,
                "type": result_type,
                "data": result_data,
                "status": ResultStatus.PENDING.value,
                "created_at": datetime.now().isoformat(),
                "validation_rules": validation_rules,
                "callback_key": callback_key,
            }

            # Store result
            self.results[result_id] = result

            # Process result
            result["status"] = ResultStatus.PROCESSING.value
            processed_data = self._process_result_by_type(
                context, result_type, result_data
            )

            # Validate result
            validation_passed = self._validate_result(
                context, result, validation_rules
            )

            if validation_passed:
                result["status"] = ResultStatus.COMPLETED.value
                result["processed_data"] = processed_data
                result["completed_at"] = datetime.now().isoformat()

                # Execute callback if provided
                if callback_key and callback_key in self.result_callbacks:
                    try:
                        self.result_callbacks[callback_key](result)
                    except Exception as e:
                        context.logger(f"Callback execution failed: {e}")

                # Archive old results
                self._archive_old_results()

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
                    metrics={
                        "results_processed": 1,
                        "validation_passed": False,
                    },
                    error="Result validation failed",
                )

        except Exception as e:
            context.logger(f"Error processing results: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup results manager."""
        try:
            # Archive all results
            self._archive_old_results()
            
            # Clear active results
            self.results.clear()
            self.result_processors.clear()
            self.result_callbacks.clear()
            
            context.logger("Results manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Error cleaning up results manager: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get results manager status."""
        return {
            "active_results": len(self.results),
            "archived_results": len(self.archived_results),
            "registered_processors": len(self.result_processors),
            "registered_callbacks": len(self.result_callbacks),
            "max_results": self.max_results,
            "archive_after_days": self.archive_after_days,
        }

    def _get_results(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get results with optional filtering."""
        try:
            result_id = payload.get("result_id")
            result_type = payload.get("result_type")
            status = payload.get("status")
            include_archived = payload.get("include_archived", False)

            results = dict(self.results)
            if include_archived:
                results.update(self.archived_results)

            # Apply filters
            if result_id:
                results = {k: v for k, v in results.items() if k == result_id}
            if result_type:
                results = {k: v for k, v in results.items() if v.get("type") == result_type}
            if status:
                results = {k: v for k, v in results.items() if v.get("status") == status}

            return ManagerResult(
                success=True,
                data={"results": results},
                metrics={"results_found": len(results)},
            )

        except Exception as e:
            context.logger(f"Error getting results: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _archive_results(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
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
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _register_result_processor(
        self, context: ManagerContext, payload: Dict[str, Any]
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
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _process_result_by_type(
        self, context: ManagerContext, result_type: str, result_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process result by type using registered processors."""
        if result_type in self.result_processors:
            try:
                return self.result_processors[result_type](result_data)
            except Exception as e:
                context.logger(f"Processor error for {result_type}: {e}")
                return {"error": str(e), "original_data": result_data}
        else:
            # Default processing
            return {"processed": True, "original_data": result_data}

    def _validate_result(
        self, context: ManagerContext, result: Dict[str, Any], rules: List[Dict[str, Any]]
    ) -> bool:
        """Validate result against rules."""
        if not rules:
            return True

        for rule in rules:
            if not self._validate_rule(rule, result.get("data", {})):
                return False

        return True

    def _validate_rule(self, rule: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Validate a single rule against data."""
        field = rule.get("field")
        rule_type = rule.get("type")
        expected_value = rule.get("expected_value")

        if field not in data:
            return False

        value = data[field]

        if rule_type == "equals":
            return value == expected_value
        elif rule_type == "not_equals":
            return value != expected_value
        elif rule_type == "greater_than":
            return value > expected_value
        elif rule_type == "less_than":
            return value < expected_value
        elif rule_type == "contains":
            return expected_value in str(value)
        elif rule_type == "not_empty":
            return bool(value)
        elif rule_type == "is_empty":
            return not bool(value)

        return True

    def _archive_old_results(self) -> None:
        """Archive results older than archive_after_days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.archive_after_days)
            to_archive = []

            for result_id, result in self.results.items():
                created_at = datetime.fromisoformat(result["created_at"])
                if created_at < cutoff_date:
                    to_archive.append(result_id)

            for result_id in to_archive:
                result = self.results[result_id]
                result["status"] = ResultStatus.ARCHIVED.value
                result["archived_at"] = datetime.now().isoformat()
                self.archived_results[result_id] = result
                del self.results[result_id]
        except Exception:
            pass  # Ignore archiving errors
