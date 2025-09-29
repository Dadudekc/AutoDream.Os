#!/usr/bin/env python3
"""
Operations Loader - V2 Compliant
===============================

Handles loading and management of autonomous operations.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class OperationsLoader:
    """Handles loading and management of autonomous operations."""

    def __init__(self, core):
        """Initialize operations loader."""
        self.core = core

    async def get_available_operations(self) -> list[dict[str, Any]]:
        """Get available operations for execution."""
        try:
            if not self.core.operations_file.exists():
                # Create default operations if none exist
                default_operations = await self._create_default_operations()
                await self._save_operations(default_operations)
                return default_operations

            with open(self.core.operations_file) as f:
                operations = json.load(f)

            # Filter operations that are ready to run
            available_operations = []
            for operation in operations:
                if self._is_operation_ready(operation):
                    available_operations.append(operation)

            return available_operations

        except Exception as e:
            logger.error(f"{self.core.agent_id}: Failed to get available operations: {e}")
            return []

    async def _create_default_operations(self) -> list[dict[str, Any]]:
        """Create default operations if none exist."""
        default_operations = [
            {
                "name": "Code Review",
                "type": "code_review",
                "description": "Review code quality and compliance",
                "frequency": "daily",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "Performance Analysis",
                "type": "performance_analysis",
                "description": "Analyze system performance",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "Documentation Update",
                "type": "documentation_update",
                "description": "Update project documentation",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "Test Optimization",
                "type": "test_optimization",
                "description": "Optimize test coverage and performance",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "Security Scan",
                "type": "security_scan",
                "description": "Perform security vulnerability scan",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "SSOT Validation",
                "type": "ssot_validation",
                "description": "Validate Single Source of Truth compliance",
                "frequency": "daily",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "System Integration Scan",
                "type": "system_integration_scan",
                "description": "Scan for system integration issues",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
            {
                "name": "Swarm Coordination Analysis",
                "type": "swarm_coordination_analysis",
                "description": "Analyze swarm coordination effectiveness",
                "frequency": "weekly",
                "last_run": None,
                "next_run": None,
                "enabled": True,
            },
        ]

        return default_operations

    def _is_operation_ready(self, operation: dict[str, Any]) -> bool:
        """Check if operation is ready to run."""
        if not operation.get("enabled", True):
            return False

        # For now, allow all enabled operations to run
        # In the future, this could check frequency and timing
        return True

    async def _save_operations(self, operations: list[dict[str, Any]]) -> None:
        """Save operations to file."""
        try:
            with open(self.core.operations_file, "w") as f:
                json.dump(operations, f, indent=2)
            logger.info(f"{self.core.agent_id}: Saved {len(operations)} operations")
        except Exception as e:
            logger.error(f"{self.core.agent_id}: Failed to save operations: {e}")
