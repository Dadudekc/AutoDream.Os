"""
Core Resource Manager - Phase-2 Manager Consolidation
====================================================

Consolidates FileManager, FileLockManager, and AgentContextManager.
Handles all resource operations: files, locks, and agent contexts.
REFACTORED: Extracted CRUD operations for V2 compliance (254→<200L).

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

from __future__ import annotations

import os
from typing import Any

from .contracts import ManagerContext, ManagerResult, ResourceManager
from .resource_context_operations import ContextOperations
from .resource_crud_operations import ResourceCRUDOperations
from .resource_file_operations import FileOperations
from .resource_lock_operations import LockOperations


class CoreResourceManager(ResourceManager):
    """Core resource manager - consolidates file, lock, and context operations."""

    def __init__(self):
        """Initialize core resource manager."""
        self.file_ops = FileOperations()
        self.lock_ops = LockOperations()
        self.context_ops = ContextOperations()
        self.crud_ops = ResourceCRUDOperations(self.file_ops, self.lock_ops, self.context_ops)

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize resource manager."""
        try:
            # Ensure runtime directory exists
            os.makedirs("runtime", exist_ok=True)

            # Load existing locks
            self.lock_ops.load_locks()

            context.logger("Core Resource Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Resource Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute resource operation."""
        try:
            if operation == "create_resource":
                return self.crud_ops.create_resource(
                    context, payload.get("resource_type", ""), payload
                )
            elif operation == "get_resource":
                return self.crud_ops.get_resource(context, payload.get("resource_id", ""))
            elif operation == "update_resource":
                return self.crud_ops.update_resource(
                    context, payload.get("resource_id", ""), payload
                )
            elif operation == "delete_resource":
                return self.crud_ops.delete_resource(context, payload.get("resource_id", ""))
            elif operation == "file_operation":
                return self.file_ops.handle_operation(context, payload)
            elif operation == "lock_operation":
                return self.lock_ops.handle_operation(context, payload)
            elif operation == "context_operation":
                return self.context_ops.handle_operation(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_resource(
        self, context: ManagerContext, resource_type: str, data: dict[str, Any]
    ) -> ManagerResult:
        """Create a resource."""
        return self.crud_ops.create_resource(context, resource_type, data)

    def get_resource(self, context: ManagerContext, resource_id: str) -> ManagerResult:
        """Get a resource."""
        return self.crud_ops.get_resource(context, resource_id)

    def update_resource(
        self, context: ManagerContext, resource_id: str, updates: dict[str, Any]
    ) -> ManagerResult:
        """Update a resource."""
        return self.crud_ops.update_resource(context, resource_id, updates)

    def delete_resource(self, context: ManagerContext, resource_id: str) -> ManagerResult:
        """Delete a resource."""
        return self.crud_ops.delete_resource(context, resource_id)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup resource manager."""
        try:
            # Save locks
            self.lock_ops.save_locks()

            # Clear contexts
            self.context_ops.clear_contexts()

            # Clear locks
            self.lock_ops.clear_locks()

            context.logger("Core Resource Manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Resource Manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get resource manager status."""
        return {
            "file_operations": self.file_ops.operations_count,
            "lock_operations": self.lock_ops.operations_count,
            "context_operations": self.context_ops.operations_count,
            "active_locks": self.lock_ops.get_lock_count(),
            "agent_contexts": self.context_ops.get_context_count(),
            "context_ids": self.context_ops.get_context_ids(),
        }
