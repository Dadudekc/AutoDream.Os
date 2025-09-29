#!/usr/bin/env python3
"""
Operations Manager - V2 Compliant
================================

Manages autonomous operations lifecycle and results.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class OperationsManager:
    """Manages autonomous operations lifecycle and results."""

    def __init__(self, core):
        """Initialize operations manager."""
        self.core = core

    async def update_operations_with_results(
        self, operations: list[dict[str, Any]], results: list[dict[str, Any]]
    ) -> None:
        """Update operations with execution results."""
        try:
            # Update operations with results
            for i, operation in enumerate(operations):
                if i < len(results):
                    result = results[i]
                    operation["last_run"] = result.get("timestamp")
                    operation["last_result"] = result.get("result", {})

            # Save updated operations
            await self._save_operations(operations)

            logger.info(f"{self.core.agent_id}: Updated {len(operations)} operations with results")

        except Exception as e:
            logger.error(f"{self.core.agent_id}: Failed to update operations with results: {e}")

    async def _save_operations(self, operations: list[dict[str, Any]]) -> None:
        """Save operations to file."""
        try:
            with open(self.core.operations_file, "w") as f:
                json.dump(operations, f, indent=2)
        except Exception as e:
            logger.error(f"{self.core.agent_id}: Failed to save operations: {e}")

    def get_operations_statistics(self) -> dict[str, Any]:
        """Get statistics about operations."""
        try:
            if not self.core.operations_file.exists():
                return {"total_operations": 0, "enabled_operations": 0, "disabled_operations": 0}

            with open(self.core.operations_file) as f:
                operations = json.load(f)

            total_operations = len(operations)
            enabled_operations = sum(1 for op in operations if op.get("enabled", True))
            disabled_operations = total_operations - enabled_operations

            return {
                "total_operations": total_operations,
                "enabled_operations": enabled_operations,
                "disabled_operations": disabled_operations,
                "operations": operations,
            }

        except Exception as e:
            logger.error(f"{self.core.agent_id}: Failed to get operations statistics: {e}")
            return {"error": str(e)}

    def enable_operation(self, operation_name: str) -> bool:
        """Enable a specific operation."""
        try:
            with open(self.core.operations_file) as f:
                operations = json.load(f)

            for operation in operations:
                if operation.get("name") == operation_name:
                    operation["enabled"] = True
                    break

            with open(self.core.operations_file, "w") as f:
                json.dump(operations, f, indent=2)

            logger.info(f"{self.core.agent_id}: Enabled operation '{operation_name}'")
            return True

        except Exception as e:
            logger.error(
                f"{self.core.agent_id}: Failed to enable operation '{operation_name}': {e}"
            )
            return False

    def disable_operation(self, operation_name: str) -> bool:
        """Disable a specific operation."""
        try:
            with open(self.core.operations_file) as f:
                operations = json.load(f)

            for operation in operations:
                if operation.get("name") == operation_name:
                    operation["enabled"] = False
                    break

            with open(self.core.operations_file, "w") as f:
                json.dump(operations, f, indent=2)

            logger.info(f"{self.core.agent_id}: Disabled operation '{operation_name}'")
            return True

        except Exception as e:
            logger.error(
                f"{self.core.agent_id}: Failed to disable operation '{operation_name}': {e}"
            )
            return False
