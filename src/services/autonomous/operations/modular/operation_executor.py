#!/usr/bin/env python3
"""
Operation Executor - V2 Compliant
===============================

Handles execution of individual autonomous operations.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import logging
from typing import Any

from .executors import (
    CodeReviewExecutor,
    DocumentationUpdateExecutor,
    PerformanceAnalysisExecutor,
    SecurityScanExecutor,
    SSOTValidationExecutor,
    SwarmCoordinationAnalysisExecutor,
    SystemIntegrationScanExecutor,
    TestOptimizationExecutor,
)

logger = logging.getLogger(__name__)


class OperationExecutor:
    """Handles execution of individual autonomous operations."""

    def __init__(self, core):
        """Initialize operation executor."""
        self.core = core

        # Initialize specialized executors
        self.executors = {
            "code_review": CodeReviewExecutor(self.core),
            "performance_analysis": PerformanceAnalysisExecutor(self.core),
            "documentation_update": DocumentationUpdateExecutor(self.core),
            "test_optimization": TestOptimizationExecutor(self.core),
            "security_scan": SecurityScanExecutor(self.core),
            "ssot_validation": SSOTValidationExecutor(self.core),
            "system_integration_scan": SystemIntegrationScanExecutor(self.core),
            "swarm_coordination_analysis": SwarmCoordinationAnalysisExecutor(self.core),
        }

    async def execute_operation(self, operation: dict[str, Any]) -> dict[str, Any]:
        """Execute a specific operation."""
        operation_type = operation.get("type")

        if not operation_type:
            return {"success": False, "error": "Operation type not specified"}

        if operation_type not in self.executors:
            return {"success": False, "error": f"Unknown operation type: {operation_type}"}

        try:
            executor = self.executors[operation_type]
            result = await executor.execute(operation)

            logger.info(
                f"{self.core.agent_id}: Executed operation '{operation.get('name', 'Unknown')}' of type '{operation_type}'"
            )
            return result

        except Exception as e:
            logger.error(
                f"{self.core.agent_id}: Failed to execute operation '{operation.get('name', 'Unknown')}': {e}"
            )
            return {"success": False, "error": str(e)}

    def get_executor_status(self) -> dict[str, Any]:
        """Get status of all executors."""
        status = {}

        for operation_type, executor in self.executors.items():
            try:
                status[operation_type] = executor.get_status()
            except Exception as e:
                status[operation_type] = {"error": str(e)}

        return status
